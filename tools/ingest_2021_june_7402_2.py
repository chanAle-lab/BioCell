import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599490127_c511cb5a.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599490047_1d9fe2da.pdf"

PAPER_ID = "2021-june-7402-2"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 2,  4, "3.5.2", "Describing the process of glycolysis", []),
    ("01.2", 2,  2, "3.5.2", "Explaining why malonate decreases oxygen uptake in a respiring cell", []),
    ("02.1", 3,  3, "3.6.2.1", "Maintaining a resting potential across an axon membrane", []),
    ("02.2", 3,  3, "3.6.2.1", "Faster impulse transmission along myelinated vs non-myelinated axon", []),
    ("02.3", 4,  3, "3.6.2.1", "Effect of respiratory inhibitor on neurone resting potential", []),
    ("03.1", 5,  3, "3.6.1.1", "Explaining plant shoot growth curvature using IAA", ["fig-q3-fig1.jpg"]),
    ("03.2", 7,  5, "3.6.1.1", "Comparing IAA concentration in two plant species using bioassay", ["fig-q3-fig2-3.jpg"]),
    ("03.3", 9,  2, "3.6.1.1", "Conclusions about IAA from directional light experiments", ["fig-q3-fig4-table1.jpg"]),
    ("04.1", 10, 2, "3.7.1", "Sex-linked eye colour cross in fruit flies: offspring phenotypes", []),
    ("04.2", 10, 1, "3.7.1", "Genotype of red-eyed female fruit fly offspring", []),
    ("04.3", 11, 3, "3.7.1", "Explaining dihybrid cross results with autosomal linkage", ["fig-q4-table2.jpg"]),
    ("04.4", 12, 3, "3.7.2", "Calculating number of female fruit flies in fifth generation", []),
    ("05.1", 13, 2, "3.6.4.2", "Amino acid sequence change preventing insulin binding to receptor", []),
    ("05.2", 14, 3, "3.6.4.2", "Explaining how decreased PI3K activity causes type II diabetes", ["fig-q5-fig5.jpg"]),
    ("05.3", 15, 3, "3.6.4.3", "Explaining glucose in urine of person with untreated diabetes", []),
    ("06.1", 16, 3, "3.8.2.3", "How malignant tumour cells are destroyed by donor T cells", []),
    ("06.2", 16, 3, "3.8.2.2", "How increased methylation of tumour suppressor genes causes cancer", []),
    ("06.3", 17, 2, "3.8.2.3", "Reasons control patients were treated with conventional drugs", ["fig-q6-fig6.jpg"]),
    ("06.4", 17, 2, "3.8.2.3", "Difference in number of patients alive at 25 months: AZA vs control", ["fig-q6-fig6.jpg"]),
    ("07.1", 18, 2, "3.2.1.2", "Calculating how many times larger a liver cell is than HBV", ["fig-q7-fig7.jpg"]),
    ("07.2", 19, 1, "3.8.4.1", "Method of transferring RNAi molecules into cells", ["fig-q7-fig8.jpg"]),
    ("07.3", 20, 5, "3.8.2.2", "Evaluating shRNA vs lhRNA for treating hepatitis B in humans", ["fig-q7-fig8.jpg"]),
    ("08.1", 21, 4, "3.8.4.2", "Describing and explaining how PCR amplifies a DNA fragment", []),
    ("08.2", 21, 2, "3.8.4.2", "Explaining the shape of the PCR DNA amplification curve", ["fig-q8-fig9.jpg"]),
    ("09.1", 22, 3, "3.7.4", "Explaining how succession increases fish variety on coral reefs", []),
    ("09.2", 22, 2, "3.7.4", "Using concrete blocks at constant depth in coral reef investigation", []),
    ("09.3", 23, 5, "3.7.4", "Evaluating effect of parrotfish and surgeonfish on algal growth", ["fig-q9-table3.jpg"]),
    ("10.1", 24, 4, "3.7.3", "Speciation of fish in Lake Malawi from a common ancestor", ["fig-q10-passage.jpg"]),
    ("10.2", 25, 2, "3.5.4", "Calculating mean loss of forest cover in Malawi per week", ["fig-q10-passage.jpg"]),
    ("10.3", 25, 4, "3.5.4", "How soil nutrient loss and lake nutrients reduce fish populations", ["fig-q10-passage.jpg"]),
    ("10.4", 26, 4, "3.7.4", "Estimating fish population size using mark-release-recapture", ["fig-q10-passage.jpg"]),
    ("10.5", 26, 1, "3.7.4", "Why mark-release-recapture can be unreliable in very large lakes", ["fig-q10-passage.jpg"]),
]

FIGURES = [
    ("fig-q3-fig1.jpg",        5,   64, 275),
    ("fig-q3-fig2-3.jpg",      6,   64, 575),
    ("fig-q3-fig4-table1.jpg", 8,   64, 680),
    ("fig-q4-table2.jpg",      11,  64, 315),
    ("fig-q5-fig5.jpg",        14,  64, 332),
    ("fig-q6-fig6.jpg",        17,  64, 380),
    ("fig-q7-fig7.jpg",        18,  64, 458),
    ("fig-q7-fig8.jpg",        19,  64, 515),
    ("fig-q8-fig9.jpg",        21, 365, 585),
    ("fig-q9-table3.jpg",      23,  64, 462),
    ("fig-q10-passage.jpg",    24,  64, 370),
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
        if pno < 3:
            continue
        blocks = doc[pno].get_text("blocks")
        for b in blocks:
            txt = " ".join(b[4].split())
            m = re.match(r"^(0[1-9]\.[1-9]|10\.[1-9])\b", txt)
            if m:
                qcode = m.group(1)
                if not any(x[0] == qcode for x in markers):
                    markers.append((qcode, pno, b[1]))
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
            "unit": "7402/2",
            "level": "A-Level",
            "title": "June 2021 Paper 2 (7402/2)",
            "totalMarks": 91
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
            "unit": "7402/2",
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
