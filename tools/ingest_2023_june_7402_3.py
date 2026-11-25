import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599532760_ef0ee0be.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599532725_b9f8b12c.pdf"

PAPER_ID = "2023-june-7402-3"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 2,  3, "3.6.1.2", "How stimulation of a Pacinian corpuscle produces a generator potential", []),
    ("01.2", 3,  2, "3.6.2.1", "All-or-nothing principle in sensory neurone (Figure 1)", ["fig-q1-fig1.jpg"]),
    ("01.3", 3,  1, "3.6.2.1", "Naming the refractory period on Figure 1", ["fig-q1-fig1.jpg"]),
    ("02.1", 4,  1, "3.5.2",   "Two control variables in yeast respiration investigation", ["fig-q2-fig2.jpg"]),
    ("02.2", 5,  2, "3.5.2",   "Calculating rate of CO2 production in mm s-1 from Figure 3", ["fig-q2-fig2.jpg", "fig-q2-fig3.jpg"]),
    ("02.3", 6,  2, "3.1.2",   "Why CO2 production was slower with maltose than glucose", []),
    ("02.4", 6,  2, "3.5.2",   "Accuracy of bromothymol blue indicator method and improvement", []),
    ("02.5", 7,  2, "3.5.2",   "Completing boxes A to D for the link reaction (Figure 4)", []),
    ("03.1", 8,  1, "3.2.1.2", "Statements about the structure of prokaryotic cells", []),
    ("03.2", 9,  2, "3.2.2",   "Mean number of bacteria in undiluted bottle with novobiocin", ["fig-q3-stem.jpg", "fig-q3-table1.jpg"]),
    ("03.3", 9,  1, "3.2.2",   "Calculating bacterial generations to reach population size", []),
    ("03.4", 10, 2, "3.4.4",   "Reasons non-resistant bacteria grew in chloramphenicol culture", []),
    ("04.1", 12, 2, "3.2.1.1", "How SCFR protein is destroyed by a lysosome", ["fig-q4-fig5.jpg"]),
    ("04.2", 13, 4, "3.8.2.1", "Explaining ventricular blood pressure in Control and c-KIT- rats", ["fig-q4-stem.jpg", "fig-q4-fig6.jpg"]),
    ("04.3", 14, 2, "3.8.2.1", "Calculating percentage of new cardiomyocytes in c-KIT- group", ["fig-q4-fig6.jpg"]),
    ("04.4", 14, 2, "3.3.4.1", "Role of Connexin-43 and GATA-4 in c-KIT+ heart repair", ["fig-q4-fig6.jpg"]),
    ("05.1", 17, 1, "3.4.6",   "Identifying years matching N and sum n(n-1) from Figure 8", ["fig-q5-fig7-8.jpg"]),
    ("05.2", 17, 2, "3.4.6",   "How 1997 had highest species richness but lowest diversity index", ["fig-q5-fig7-8.jpg"]),
    ("05.3", 18, 4, "3.4.6",   "Evaluating journalist conclusion on heated water and fish diversity", ["fig-q5-fig7-8.jpg"]),
    ("06.1", 20, 2, "3.2.4",   "Two types of cell that can stimulate an immune response", []),
    ("06.2", 20, 1, "3.2.4",   "Reason why olive oil was applied to the left ear of mice", []),
    ("06.3", 21, 3, "3.2.4",   "Plotting bar chart of mean ear thickness with ±2 SD bars", ["fig-q6-table2.jpg"]),
    ("06.4", 22, 3, "3.2.4",   "Conclusions on autoimmune disease effects on cellular and humoral responses", ["fig-q6-table2.jpg"]),
    ("06.5", 23, 4, "3.2.4",   "Evaluating student conclusions on oestrogen, SLE and RA", []),
    ("06.6", 24, 2, "3.7.2",   "Whether Hardy-Weinberg principle holds for autoimmune mice", []),
    ("07.1", 25, 25, "3.7.4",  "Essay: The importance of interactions between organisms and their environment", []),
    ("07.2", 25, 25, "3.2.3",  "Essay: The importance of membranes in the functioning of cells", []),
]

FIGURES = [
    ("fig-q1-fig1.jpg",   2,  485, 760),
    ("fig-q2-fig2.jpg",   4,   64, 302),
    ("fig-q2-fig3.jpg",   5,   64, 416),
    ("fig-q3-stem.jpg",   8,  380, 670),
    ("fig-q3-table1.jpg", 9,   64, 230),
    ("fig-q4-fig5.jpg",   12,  64, 305),
    ("fig-q4-stem.jpg",   12, 450, 725),
    ("fig-q4-fig6.jpg",   13,  64, 345),
    ("fig-q5-fig7-8.jpg", 16,  64, 655),
    ("fig-q6-table2.jpg", 20, 200, 562),
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
            "year": 2023,
            "series": "June",
            "unit": "7402/3",
            "level": "A-Level",
            "title": "June 2023 Paper 3 (7402/3)",
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
            "year": 2023,
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
