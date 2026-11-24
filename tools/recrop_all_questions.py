"""
coolBio - Precision Question Recropping Tool
============================================
Re-crops all past paper question images from the original Question Paper PDFs
with exact bounding boxes, supporting split two-digit AQA markers (0 1 . 1),
subpart markers, and optional crop_exclude_y bands.
"""

import io
import json
import os
import re
from collections import defaultdict

import pymupdf as fitz
from PIL import Image

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTIONS_FILE = os.path.join(REPO_DIR, "questions.json")

# Register ingested papers here: '<paper-id>': r'<path-to-qp.pdf>'
PDF_MAP: dict[str, str] = {}


def extract_lines(page: fitz.Page) -> list[tuple]:
    blocks = page.get_text("dict")["blocks"]
    lines = []
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                txt = "".join(s["text"] for s in l["spans"]).strip()
                bbox = l["bbox"]
                if txt and 60 <= bbox[1] <= 814:
                    lines.append((bbox, txt))
    lines.sort(key=lambda x: (x[0][1], x[0][0]))
    return lines


def main() -> None:
    print("Loading questions.json...")
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    docs = {p: fitz.open(path) for p, path in PDF_MAP.items() if os.path.exists(path)}
    if not docs:
        print("No PDFs registered in PDF_MAP (or paths do not exist). Nothing to recrop.")
        return

    pages = defaultdict(list)
    for q in db["questions"]:
        if q["paper"] in docs:
            pages[(q["paper"], q["page"])].append(q)

    total_target = sum(len(ql) for ql in pages.values())
    print(f"Processing {total_target} questions across {len(pages)} pages in {len(docs)} papers...")

    success_count = 0
    total_count = 0

    for (paper, p_num), q_list in sorted(pages.items()):
        doc = docs[paper]
        page = doc[p_num - 1]
        lines = extract_lines(page)

        main_q_top = None
        for bbox, txt in lines:
            if bbox[0] < 70 and re.match(r"^\d+$", txt.strip()):
                main_q_top = (int(txt.strip()), bbox[1])
                break

        subpart_letter_locs = []
        for bbox, txt in lines:
            if bbox[0] < 120:
                m_sub = re.match(r"^\(([a-h])\)", txt.strip())
                if m_sub:
                    subpart_letter_locs.append((m_sub.group(1), bbox[1]))

        curr_y = 60.0
        located = []
        for q_idx, q in enumerate(q_list):
            total_count += 1
            q_label = q["question"]
            m_dot = re.match(r"^(\d{2})\.(\d+)$", q_label)
            m_mcq = re.match(r"^(\d{2})$", q_label)
            m = re.match(r"^(\d+)?(?:\(([a-z\d]+)\))?(?:\(([a-z\d]+)\))?", q_label)
            if m_dot:
                main_q, sub1, sub2 = str(int(m_dot.group(1))), None, None
            else:
                main_q, sub1, sub2 = m.groups() if m else (None, None, None)

            max_search_y = 800.0
            if sub1:
                for s_char, s_y in subpart_letter_locs:
                    if s_char > sub1 and s_y >= curr_y - 5:
                        max_search_y = min(max_search_y, s_y)
                        break

            parent_sub_y0 = None
            if sub2 and (q_idx == 0 or not q_list[q_idx - 1]["question"].startswith(f"{main_q}({sub1})")):
                for bbox, txt in lines:
                    if curr_y - 5 <= bbox[1] < max_search_y and bbox[0] < 120:
                        words = txt.split()
                        if words and (
                            words[0] == f"({sub1})"
                            or (
                                (txt.startswith(f"{main_q} ({sub1})") or txt.startswith(f"{main_q}({sub1})"))
                                and not re.match(rf"^{re.escape(main_q)}\s*\({re.escape(sub1)}\)\s*\(", txt)
                            )
                        ):
                            parent_sub_y0 = bbox[1]
                            break

            candidates = []
            if sub2:
                if main_q and sub1:
                    candidates.extend([f"{main_q} ({sub1}) ({sub2})", f"{main_q}({sub1})({sub2})", f"{main_q} ({sub1})({sub2})"])
                candidates.append(f"({sub2})")
                if sub1:
                    candidates.extend([f"({sub1})({sub2})", f"({sub1}) ({sub2})"])
            elif sub1:
                candidates.append(f"({sub1})")
                if main_q:
                    candidates.extend([f"{main_q} ({sub1})", f"{main_q}({sub1})"])
            elif m_dot:
                d1, d2 = m_dot.group(1), m_dot.group(2)
                candidates.extend([f"{d1[0]} {d1[1]} . {d2}", f"{d1}.{d2}", f"{int(d1)}.{d2}"])
            elif m_mcq:
                d1 = m_mcq.group(1)
                candidates.extend([f"{d1[0]} {d1[1]}", d1, str(int(d1))])
            elif main_q:
                candidates.append(main_q)

            found_y0 = None
            search_start = parent_sub_y0 if parent_sub_y0 is not None else curr_y
            for bbox, txt in lines:
                if search_start - 5 <= bbox[1] < max_search_y:
                    for cand in candidates:
                        if bbox[0] < 140:
                            words = txt.split()
                            if (words and (words[0] == cand or txt.startswith(cand))) or txt == cand:
                                found_y0 = bbox[1]
                                break
                    if found_y0 is not None:
                        break

            # Fallback for split two-digit question boxes in 2017+ AQA papers
            if found_y0 is None and (m_dot or m_mcq):
                d1 = m_dot.group(1) if m_dot else m_mcq.group(1)
                right_target = f"{d1[1]} . {m_dot.group(2)}" if m_dot else d1[1]
                for bbox, txt in lines:
                    if search_start - 5 <= bbox[1] < max_search_y and 60 <= bbox[0] < 95 and txt.strip() == right_target:
                        if any(b2[0] < 65 and abs(b2[1] - bbox[1]) < 4 and t2.strip() == d1[0] for b2, t2 in lines):
                            found_y0 = bbox[1]
                            break

            if found_y0 is None and q_idx == 0 and lines:
                found_y0 = lines[0][0][1]

            actual_y0 = parent_sub_y0 if parent_sub_y0 is not None else found_y0
            located.append((q, found_y0, actual_y0))
            if found_y0 is not None:
                curr_y = found_y0 + 10.0

        for i, (q, ly0, start_y0) in enumerate(located):
            if ly0 is None:
                print(f"ERROR: Could not locate label for {q['id']} ({q['question']}) on page {p_num}")
                continue

            if q.get("crop_y0") is not None:
                y0 = float(q["crop_y0"])
            elif i == 0:
                m = re.match(r"^(\d+)", q["question"])
                q_num = int(m.group(1)) if m else None
                if main_q_top and q_num and main_q_top[0] == q_num and main_q_top[1] < start_y0:
                    y0 = max(68.0, main_q_top[1] - 8.0)
                else:
                    y0 = max(68.0, start_y0 - 8.0)
            else:
                y0 = max(68.0, start_y0 - 8.0)

            if i + 1 < len(located) and located[i + 1][2] is not None:
                y1 = located[i + 1][2] - 6.0
            else:
                after_lines = [
                    l for l in lines
                    if l[0][1] >= ly0 and l[0][3] < 785.0
                    and "Turn over" not in l[1]
                    and "APW/" not in l[1]
                    and "Section B" not in l[1]
                    and "Answer these questions" not in l[1]
                    and not re.match(r"^\d+$", l[1].strip())
                ]
                if after_lines:
                    y1 = min(775.0, max(l[0][3] for l in after_lines) + 18.0)
                else:
                    y1 = min(775.0, ly0 + 120.0)

            exclude_y = sorted(q.get("crop_exclude_y") or [])
            if not exclude_y:
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), clip=fitz.Rect(35, y0, 545, y1))
                im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            else:
                strips, cur = [], y0
                for ey0, ey1 in exclude_y:
                    if ey0 > cur + 2:
                        strips.append((cur, min(ey0, y1)))
                    cur = max(cur, ey1)
                if cur < y1 - 2:
                    strips.append((cur, y1))
                parts = [
                    Image.open(io.BytesIO(page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), clip=fitz.Rect(35, sy0, 545, sy1)).tobytes("png"))).convert("RGB")
                    for sy0, sy1 in strips if sy1 > sy0 + 2
                ]
                if parts:
                    im = Image.new("RGB", (parts[0].width, sum(p_im.height for p_im in parts)), (255, 255, 255))
                    yy = 0
                    for p_im in parts:
                        im.paste(p_im, (0, yy))
                        yy += p_im.height
                else:
                    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), clip=fitz.Rect(35, y0, 545, y1))
                    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")

            img_abs = os.path.join(REPO_DIR, q["image"].replace("/", os.sep))
            os.makedirs(os.path.dirname(img_abs), exist_ok=True)
            im.save(img_abs, format="JPEG", quality=92)
            success_count += 1

    print(f"\nSuccessfully cropped {success_count} / {total_count} questions!")
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print("Updated questions.json successfully!")


if __name__ == "__main__":
    main()
