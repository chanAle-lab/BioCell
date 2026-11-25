import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599490055_ad0424f6.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599490045_66a5599f.pdf"

PAPER_ID = "2021-june-7402-1"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 2,  3, "3.1.4.2", "Induced-fit model of enzyme action and catalysis", []),
    ("01.2", 2,  1, "3.1.6",   "ATP synthase reaction: identifying ADP as substrate", []),
    ("01.3", 3,  2, "3.1.4.2", "ATP synthase investigation: control procedure at 2 minutes", []),
    ("01.4", 3,  2, "3.1.4.2", "Explaining ATP concentration change with increasing Pi", ["fig-q1-fig1.jpg"]),
    ("02.1", 4,  2, "3.3.1",   "Advantage of specialised oxygen uptake system in larger animals", []),
    ("02.2", 5,  2, "3.3.2",   "Environmental adaptations for oxygen uptake models A vs B", ["fig-q2-fig2.jpg"]),
    ("02.3", 6,  2, "3.3.2",   "Justifying greater efficiency of fish gas exchange from Figure 3", []),
    ("02.4", 6,  2, "3.3.2",   "Counter-current principle for efficient gas exchange", []),
    ("02.5", 7,  3, "3.3.2",   "Calculating lung volume per unit body mass: bat vs shrew", []),
    ("03.1", 9,  3, "3.4.2",   "Translation: adding an amino acid to a polypeptide at a ribosome", []),
    ("03.2", 10, 2, "3.1.4.1", "Amino acid replacement in crystallin protein and cataracts", ["fig-q3-table2.jpg"]),
    ("03.3", 11, 2, "3.4.3",   "Single base substitution mutation: mRNA codon and tRNA anticodon", ["fig-q3-table2.jpg"]),
    ("04.1", 13, 2, "3.3.4.1", "Improving scientific drawing quality of blood vessel dissection", ["fig-q4-fig4.jpg", "fig-q4-fig5.jpg"]),
    ("04.2", 13, 2, "3.3.4.1", "Identifying blood vessels X and Y in dissection photograph", ["fig-q4-fig4.jpg"]),
    ("04.3", 13, 2, "3.3.4.1", "Safe handling and washing of sharp dissection instruments", []),
    ("05.1", 14, 4, "3.2.1.3", "Isolating chloroplasts from leaves by cell fractionation", []),
    ("05.2", 15, 2, "3.2.1.1", "Chloroplast feature for protein synthesis vs prokaryotic cells", []),
    ("05.3", 15, 1, "3.1.4.1", "Ratio of protein to chlorophyll in iron-deficient plants", ["fig-q5-table4.jpg"]),
    ("05.4", 16, 3, "3.2.1.1", "Explaining reduced growth rate in iron-deficient chloroplasts", []),
    ("06.1", 18, 2, "3.2.2",   "Rate of centromere movement during phase E of mitosis", []),
    ("06.2", 19, 5, "3.2.2",   "Phases of mitosis C, D, E: spindle fibres and chromosomes", ["fig-q6-fig7.jpg"]),
    ("07.1", 20, 3, "3.2.4",   "Phagocytosis-like entry of antibody-drug conjugate into tumour cell", []),
    ("07.2", 21, 2, "3.2.4",   "Explaining side effects of ADC treatment on healthy cells", []),
    ("07.3", 23, 2, "3.2.4",   "Calculating volume of monoclonal antibody solution injected", ["fig-q7-fig9.jpg"]),
    ("07.4", 23, 1, "3.2.4",   "Explaining why Group G and H lines end at day 26", ["fig-q7-fig9.jpg"]),
    ("07.5", 23, 2, "3.2.4",   "Further stages before ADC can be used to treat humans", ["fig-q7-fig9.jpg"]),
    ("08.1", 24, 3, "3.1.3",   "Structure and synthesis of a triglyceride molecule", []),
    ("08.2", 25, 1, "3.1.3",   "Identifying unsaturated fatty acid diagram K for palmitoleic acid", []),
    ("08.3", 26, 1, "3.4.4",   "Using a data logger for root length and why seeds were washed", ["fig-q8-table6.jpg"]),
    ("08.4", 27, 4, "3.4.4",   "Adaptation of warm and cool plant populations to environment", ["fig-q8-table6.jpg"]),
    ("08.5", 27, 1, "3.4.5",   "Evidence that both populations belong to the same species", []),
    ("09.1", 29, 2, "3.1.5.1", "Elements found in ATP, DNA, RNA, and phospholipids", []),
    ("09.2", 31, 2, "3.2.2",   "Calculating bacterial generation time from Figure 11", ["fig-q9-fig11.jpg"]),
    ("09.3", 33, 3, "3.1.5.2", "Evaluating DNA replication models P, Q, R from 15N/14N results", ["fig-q9-fig12.jpg", "fig-q9-fig13.jpg"]),
    ("10.1", 34, 5, "3.1.5.1", "Comparing and contrasting DNA and RNA structure", []),
    ("10.2", 35, 5, "3.2.3",   "Transport of substances across cell-surface membranes", []),
    ("10.3", 37, 5, "3.2.1.1", "Comparing animal cell and prokaryotic cell micrographs", ["fig-q10-fig14.jpg"]),
]

FIGURES = [
    ("fig-q1-fig1.jpg",   3,  140, 368),
    ("fig-q2-fig2.jpg",   5,   64, 340),
    ("fig-q3-table2.jpg", 10,  64, 445),
    ("fig-q4-fig4.jpg",   12,  64, 345),
    ("fig-q4-fig5.jpg",   12, 350, 620),
    ("fig-q5-table4.jpg", 15, 172, 295),
    ("fig-q6-fig7.jpg",   18, 102, 336),
    ("fig-q7-fig9.jpg",   22,  64, 580),
    ("fig-q8-table6.jpg", 26,  64, 515),
    ("fig-q9-fig11.jpg",  30,  64, 620),
    ("fig-q9-fig12.jpg",  32,  64, 545),
    ("fig-q9-fig13.jpg",  33,  64, 368),
    ("fig-q10-fig14.jpg", 36,  64, 405),
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
            "unit": "7402/1",
            "level": "A-Level",
            "title": "June 2021 Paper 1 (7402/1)",
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
            "unit": "7402/1",
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
