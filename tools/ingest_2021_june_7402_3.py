import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599490040_bfe9c112.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599490039_4a5844f6.pdf"

PAPER_ID = "2021-june-7402-3"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 2,  2, "3.7.2", "Hardy-Weinberg estimate of brown-black squirrels", ["fig-q1-table1.jpg"]),
    ("01.2", 3,  1, "3.7.2", "Calculating actual allele frequency without Hardy-Weinberg", ["fig-q1-table1.jpg"]),
    ("01.3", 3,  1, "3.7.2", "Why actual frequency differs from Hardy-Weinberg estimate", []),
    ("01.4", 4,  2, "3.4.3", "Percentage reduction in protein size from 24 bp deletion", []),
    ("01.5", 5,  3, "3.4.3", "Explaining black fur in CB CB squirrels using Figure 1", ["fig-q1-fig1.jpg"]),
    ("02.1", 6,  4, "3.2.4", "Replication of HIV inside helper T cells", []),
    ("02.2", 7,  5, "3.2.4", "Evaluating CCR5 gene editing vs ART for HIV-1 treatment", []),
    ("03.1", 8,  2, "3.6.1.1", "Taxis behaviour in adult pine beetles and its advantage", ["fig-q3-fig2.jpg"]),
    ("03.2", 11, 3, "3.6.1.1", "Evaluating student conclusions on pine beetle movement", ["fig-q3-fig3.jpg"]),
    ("04.1", 12, 2, "3.5.3", "Why freshwater marshes have high carbon use efficiency (CUE)", []),
    ("04.2", 12, 2, "3.5.3", "How decomposition of dead plants returns carbon to atmosphere", []),
    ("04.3", 13, 2, "3.5.3", "Calculating plant growth rate R from biomass measurements", []),
    ("04.4", 13, 2, "3.5.3", "Estimating dry biomass from fresh plant samples", []),
    ("05.1", 14, 2, "3.3.3", "How endopeptidases and exopeptidases increase protein digestion", []),
    ("05.2", 14, 2, "3.1.4.1", "Body proteins linked to reduced muscle power and immunity", []),
    ("05.3", 15, 3, "3.3.3", "Comparing casein vs whey protein for muscle recovery in older men", ["fig-q5-table2.jpg", "fig-q5-fig4.jpg"]),
    ("06.1", 16, 4, "3.3.4.2", "Role of SUT1 co-transporter in loading sucrose into phloem", []),
    ("06.2", 17, 4, "3.8.2.2", "How antisense SUT1 mRNA reduces SUT1 protein production", []),
    ("06.3", 18, 1, "3.3.4.2", "Ratio of 14C remaining in type B to type A leaves at 16 hours", []),
    ("06.4", 19, 2, "3.3.4.2", "Why 14C remaining in type B leaves does not reach zero", ["fig-q6-fig5.jpg"]),
    ("06.5", 21, 4, "3.5.1", "Explaining decreased dry mass in type A tobacco plants", ["fig-q6-table3.jpg"]),
    ("07.1", 22, 25, "3.1.4.2", "Essay: The importance of complementary shapes of molecules in organisms", []),
    ("07.2", 22, 25, "3.1.8", "Essay: The importance of ions in metabolic processes", []),
]

FIGURES = [
    ("fig-q1-table1.jpg", 2,  150, 380),
    ("fig-q1-fig1.jpg",   4,  350, 768),
    ("fig-q3-fig2.jpg",   8,   64, 455),
    ("fig-q3-fig3.jpg",   10,  64, 522),
    ("fig-q5-table2.jpg", 14, 430, 710),
    ("fig-q5-fig4.jpg",   15,  64, 305),
    ("fig-q6-fig5.jpg",   18, 160, 468),
    ("fig-q6-table3.jpg", 20,  64, 350),
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
            m = re.match(r"^(0[1-9]\.[1-9])\b", txt)
            if m:
                qcode = m.group(1)
                if not any(x[0] == qcode for x in markers):
                    y_pos = 110.0 if qcode in ("07.1", "07.2") else b[1]
                    markers.append((qcode, pno, y_pos))
    markers.sort(key=lambda x: (x[1], x[2]))
    print(f"Found {len(markers)} MS markers")
    for idx, (qcode, pno, y_start) in enumerate(markers):
        if idx + 1 < len(markers):
            _, next_pno, next_y = markers[idx + 1]
        else:
            next_pno, next_y = len(doc) - 1, 760
        imgs = []
        for p in range(pno, next_pno + 1):
            page = doc[p]
            top = max(85, y_start - 8) if p == pno else 85
            bot = min(775, next_y - 6) if p == next_pno else 775
            if bot - top < 25:
                continue
            pix = page.get_pixmap(clip=fitz.Rect(30, top, page.rect.width - 30, bot), dpi=180)
            imgs.append(pix)
        from PIL import Image
        import io
        pil_imgs = [Image.open(io.BytesIO(px.tobytes("png"))) for px in imgs]
        if not pil_imgs:
            continue
        w = max(im.width for im in pil_imgs)
        h = sum(im.height for im in pil_imgs)
        merged = Image.new("RGB", (w, h), (255, 255, 255))
        y_off = 0
        for im in pil_imgs:
            merged.paste(im, (0, y_off))
            y_off += im.height
        q_num = int(qcode.split(".")[0])
        sub_num = int(qcode.split(".")[1])
        out_name = f"q{q_num:02d}-{sub_num}.png"
        merged.save(os.path.join(OUT_MS_DIR, out_name))
        print(f"Saved MS {out_name}")


def update_questions_json():
    with open("questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if not any(p["id"] == PAPER_ID for p in data["papers"]):
        data["papers"].append({
            "id": PAPER_ID,
            "year": 2021,
            "series": "June",
            "unit": "7402/3",
            "level": "A-Level",
            "title": "June 2021 Paper 3 (7402/3)",
            "totalMarks": 78,
            "optionalMarks": 25
        })

    data["questions"] = [q for q in data["questions"] if q.get("paper") != PAPER_ID]

    for qcode, page, marks, spec_ref, summary, figs in QUESTIONS:
        q_num = int(qcode.split(".")[0])
        sub_num = int(qcode.split(".")[1])
        q_id = f"{PAPER_ID}-q{qcode}"
        data["questions"].append({
            "id": q_id,
            "paper": PAPER_ID,
            "year": 2021,
            "series": "June",
            "unit": "7402/3",
            "level": "A-Level",
            "question": qcode,
            "questionNumber": qcode,
            "page": page,
            "marks": marks,
            "specRef": spec_ref,
            "topics": [spec_ref],
            "summary": summary,
            "image": f"img/{PAPER_ID}/q{q_num:02d}-{sub_num}.jpg",
            "markscheme": f"img/{PAPER_ID}/ms/q{q_num:02d}-{sub_num}.png",
            "figures": [f"img/{PAPER_ID}/{fg}" for fg in figs]
        })

    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated questions.json with {len(QUESTIONS)} questions for {PAPER_ID}")


if __name__ == "__main__":
    crop_figures()
    crop_mark_schemes()
    update_questions_json()
