import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599564148_cbf9c801.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599564225_3cecd64d.pdf"

PAPER_ID = "2014-specimen-7402-3"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 2,  2, "3.7.4",   "Using random coordinates for release-recapture insect sampling", []),
    ("01.2", 2,  2, "3.7.4",   "Assumptions of mark-release-recapture population estimates", []),
    ("01.3", 2,  2, "3.7.4",   "Why UV fluorescent powder was suitable for marking insects", []),
    ("01.4", 3,  2, "3.7.4",   "Calculating insect population size 1 day after release", ["fig-q1-table1.jpg"]),
    ("01.5", 3,  2, "3.7.4",   "Why population estimate on day 5 is not valid", ["fig-q1-table1.jpg"]),
    ("02.1", 4,  4, "3.2.1.3", "Making a temporary mount of plant tissue for optical microscopy", []),
    ("02.2", 5,  2, "3.2.1.1", "Identifying and giving function of organelles W and Z", ["fig-q2-fig1.jpg"]),
    ("02.3", 5,  2, "3.2.1.3", "Why a transmission electron microscope was used for Figure 1", ["fig-q2-fig1.jpg"]),
    ("02.4", 5,  1, "3.2.1.3", "Calculating magnification of plant cell electron micrograph", ["fig-q2-fig1.jpg"]),
    ("03.1", 6,  2, "3.3.3",   "Naming reducing sugar produced by amylase and enzyme digesting it", ["fig-q3-method.jpg"]),
    ("03.2", 6,  1, "3.3.3",   "Naming enzyme that digests maltose", ["fig-q3-method.jpg"]),
    ("03.3", 6,  1, "3.3.3",   "Why acid was added after chewing cooked wheat", ["fig-q3-method.jpg"]),
    ("03.4", 7,  2, "3.3.3",   "Control experiment to show starch digestion is due to salivary amylase", ["fig-q3-method.jpg"]),
    ("03.5", 7,  3, "3.3.3",   "Explaining higher reducing sugar concentration in chewed vs chopped wheat", []),
    ("04.1", 8,  2, "3.8.2",   "Finding median survival time from patient data", ["fig-q4-table2.jpg"]),
    ("04.2", 9,  1, "3.8.2",   "Why a placebo control group is unethical in cancer drug trials", ["fig-q4-table2.jpg"]),
    ("04.3", 9,  4, "3.8.2",   "Evaluating whether ipilimumab improves metastatic melanoma treatment", ["fig-q4-table2.jpg"]),
    ("04.4", 10, 3, "3.2.4",   "How T-cells destroy melanoma cells with faulty receptor proteins", []),
    ("05.1", 11, 2, "3.5.4",   "Why seeds and soil were sterilised before planting", ["fig-q5-method.jpg"]),
    ("05.2", 11, 1, "3.5.4",   "Why soil had low nitrate and ammonium concentration", ["fig-q5-method.jpg"]),
    ("05.3", 11, 2, "3.5.4",   "Why plants were grown in the same greenhouse for 6 weeks", ["fig-q5-method.jpg"]),
    ("05.4", 12, 2, "3.5.3",   "Ensuring all water was removed during oven drying", []),
    ("05.5", 13, 4, "3.5.4",   "Conclusions about effect of fungus and fertilisers on plant growth", ["fig-q5-table3.jpg"]),
    ("05.6", 14, 2, "3.5.3",   "Why dry mass was measured instead of fresh mass", ["fig-q5-table3.jpg"]),
    ("05.7", 14, 2, "3.5.4",   "Explaining root-to-shoot dry mass ratios with nitrate fertiliser and fungus", ["fig-q5-table3.jpg"]),
    ("06.1", 15, 25, "3.9",    "Essay: The importance of movement in living organisms", []),
    ("06.2", 15, 25, "3.9",    "Essay: The importance of receptors in living organisms", []),
]

FIGURES = [
    ("fig-q1-table1.jpg", 3,   65, 295),
    ("fig-q2-fig1.jpg",   4,  425, 730),
    ("fig-q3-method.jpg", 6,   75, 295),
    ("fig-q4-table2.jpg", 8,   75, 540),
    ("fig-q5-method.jpg", 11,  75, 192),
    ("fig-q5-table3.jpg", 12, 295, 700),
]


def crop_figures():
    doc = fitz.open(QP_PDF)
    for fname, page_num, y0, y1 in FIGURES:
        page = doc[page_num - 1]
        rect = fitz.Rect(35, y0, page.rect.width - 35, y1)
        pix = page.get_pixmap(clip=rect, dpi=180)
        out = os.path.join(OUT_IMG_DIR, fname)
        pix.save(out)
        print(f"Saved figure {out}")


def crop_mark_schemes():
    doc = fitz.open(MS_PDF)
    markers = []
    for pno in range(len(doc)):
        if pno < 4:
            continue
        blocks = doc[pno].get_text("blocks")
        for b in blocks:
            txt = " ".join(b[4].split())
            m = re.match(r"^(0[1-5]\.[1-9])\b", txt) or re.match(r"^Question\s+(06\.[12]):", txt)
            if m:
                qcode = m.group(1)
                if not any(x[0] == qcode for x in markers):
                    markers.append((qcode, pno, b[1]))
    markers.sort(key=lambda x: (x[1], x[2]))
    print(f"Found {len(markers)} MS markers")
    for idx, (qcode, pno, y_start) in enumerate(markers):
        if qcode.startswith("06."):
            next_pno, next_y = pno, 760
        elif idx + 1 < len(markers):
            next_pno, next_y = markers[idx + 1][1], markers[idx + 1][2]
        else:
            next_pno, next_y = pno, 760
        q_num, sub_num = qcode.split(".")
        out_name = f"q{int(q_num):02d}-{int(sub_num)}.png"
        out_path = os.path.join(OUT_MS_DIR, out_name)

        if next_pno == pno:
            y0 = max(60, y_start - 8)
            y1 = min(770, next_y - 4)
            rect = fitz.Rect(35, y0, doc[pno].rect.width - 35, y1)
            pix = doc[pno].get_pixmap(clip=rect, dpi=180)
            pix.save(out_path)
        else:
            imgs = []
            for p in range(pno, next_pno + 1):
                page = doc[p]
                y0 = max(60, y_start - 8) if p == pno else 65
                y1 = min(770, next_y - 4) if p == next_pno else 765
                if y1 - y0 < 15:
                    continue
                rect = fitz.Rect(35, y0, page.rect.width - 35, y1)
                imgs.append(page.get_pixmap(clip=rect, dpi=180))
            if len(imgs) == 1:
                imgs[0].save(out_path)
            else:
                from PIL import Image
                import io
                pil_imgs = [Image.open(io.BytesIO(im.tobytes("png"))) for im in imgs]
                w = max(im.width for im in pil_imgs)
                h = sum(im.height for im in pil_imgs)
                merged = Image.new("RGB", (w, h), (255, 255, 255))
                cy = 0
                for im in pil_imgs:
                    merged.paste(im, (0, cy))
                    cy += im.height
                merged.save(out_path)
        print(f"Saved MS {out_path}")


def update_questions_json():
    with open("questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data["papers"] = [p for p in data["papers"] if p["id"] != PAPER_ID]
    data["questions"] = [q for q in data["questions"] if q["paper"] != PAPER_ID]

    data["papers"].append({
        "id": PAPER_ID,
        "year": 2014,
        "series": "Specimen",
        "unit": "7402/3",
        "level": "A-Level",
        "title": "2014 Specimen A-Level Paper 3 (7402/3)",
        "totalMarks": 78,
        "optionalMarks": 25
    })

    for qcode, page, marks, spec_ref, summary, figs in QUESTIONS:
        q_num, sub_num = qcode.split(".")
        data["questions"].append({
            "id": f"{PAPER_ID}-q{qcode}",
            "paper": PAPER_ID,
            "year": 2014,
            "series": "Specimen",
            "unit": "7402/3",
            "level": "A-Level",
            "question": qcode,
            "questionNumber": qcode,
            "page": page,
            "marks": marks,
            "specRef": spec_ref,
            "topics": [spec_ref],
            "summary": summary,
            "image": f"img/{PAPER_ID}/q{int(q_num):02d}-{int(sub_num)}.jpg",
            "markscheme": f"img/{PAPER_ID}/ms/q{int(q_num):02d}-{int(sub_num)}.png",
            "figures": [f"img/{PAPER_ID}/{fg}" for fg in figs]
        })

    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated questions.json with {len(QUESTIONS)} questions for {PAPER_ID}")


if __name__ == "__main__":
    crop_figures()
    crop_mark_schemes()
    update_questions_json()
