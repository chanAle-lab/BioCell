import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599532931_dc85bca6.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599532996_44ae3cc4.pdf"

PAPER_ID = "2023-june-7402-2"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 2,  4, "3.5.1",   "Separating photosynthetic pigments by chromatography", []),
    ("01.2", 2,  2, "3.5.1",   "Explaining difference in pigments separated by solvents A and B", []),
    ("02.1", 3,  5, "3.6.2.2", "How ziconotide blocking calcium channels reduces pain", []),
    ("02.2", 3,  2, "3.6.2.2", "Why ziconotide is injected into CSF rather than taken as a pill", []),
    ("02.3", 4,  2, "3.6.2.2", "Calculating total mass of ziconotide injected over 8 days", []),
    ("02.4", 4,  2, "3.6.2.2", "Why a statistically valid pain scale was important", []),
    ("03.1", 5,  2, "3.5.4",   "Difference in phosphorus supply to soil from two stores", ["fig-q3-fig1.jpg"]),
    ("03.2", 7,  5, "3.5.4",   "Evaluating mycorrhizae for tomato production with water shortage", ["fig-q3-fig2.jpg"]),
    ("03.3", 8,  2, "3.5.4",   "Two reasons why tomato seeds were planted into sterilised soil", []),
    ("03.4", 8,  2, "3.5.4",   "Two reasons why soil contained recommended fertiliser concentration", []),
    ("04.1", 10, 1, "3.7.1",   "Naming epistasis between two genes affecting cat fur colour", ["fig-q4-stem.jpg"]),
    ("04.2", 10, 1, "3.7.1",   "Phenotype of cat with genotype XGXBff", ["fig-q4-stem.jpg"]),
    ("04.3", 10, 3, "3.7.1",   "Genetic diagram for sex-linked and epistatic cat fur cross", ["fig-q4-stem.jpg"]),
    ("04.4", 11, 2, "3.7.2",   "Hardy-Weinberg frequency of f allele in cat population", []),
    ("05.1", 12, 3, "3.6.1.2", "How orange colour is seen at 600 nm using cone photoreceptors", []),
    ("05.2", 13, 1, "3.6.1.2", "Feature associated with high sensitivity to light in retina", []),
    ("05.3", 14, 5, "3.7.3",   "Allopatric and sympatric speciation in monkeyflower species", []),
    ("06.1", 16, 3, "3.6.4.3", "Three features of PCT cells for rapid glucose reabsorption", []),
    ("06.2", 16, 1, "3.6.4.3", "Two parts of a nephron where ADH V receptors are found", []),
    ("06.3", 16, 2, "3.6.4.1", "Why V receptors only bind with ADH", []),
    ("06.4", 17, 3, "3.6.4.3", "Location of blood pressure receptors and ADH effect on BP", []),
    ("07.1", 18, 2, "3.7.4",   "Ecological terms: carrying capacity, niche, abiotic, community", []),
    ("07.2", 18, 2, "3.7.4",   "Two reasons for conserving rainforests", []),
    ("07.3", 18, 3, "3.5.3",   "Reasons for low energy transfer efficiency to tertiary consumers", []),
    ("08.1", 20, 3, "3.8.2.3", "How alteration in KRAS gene produces oncogene and tumour", []),
    ("08.2", 20, 5, "3.8.2.3", "Evaluating survival times of CRC patients with diabetes/metformin", ["fig-q8-table1.jpg"]),
    ("09.1", 22, 2, "3.8.4.1", "Removing STRs from DNA using restriction endonucleases", []),
    ("09.2", 22, 2, "3.8.4.2", "Importance of knowing flanking base sequences for PCR primers", []),
    ("09.3", 23, 2, "3.8.4.2", "Total base pairs in STR molecules after 50 PCR cycles", []),
    ("09.4", 23, 2, "3.8.4.3", "Two features of STRs enabling separation by gel electrophoresis", []),
    ("10.1", 24, 2, "3.6.3",   "Roles of ATP in skeletal muscle contraction", ["fig-q10-passage.jpg"]),
    ("10.2", 24, 1, "3.6.3",   "Calculating duration of maximum exercise without ATP resynthesis", ["fig-q10-passage.jpg"]),
    ("10.3", 25, 5, "3.6.3",   "Creatine supplements and carbohydrate loading in muscle fibres", ["fig-q10-passage.jpg"]),
    ("10.4", 26, 3, "3.5.2",   "Benefits of GLUT4 and CD36 transport proteins during exercise", ["fig-q10-passage.jpg"]),
    ("10.5", 26, 4, "3.6.1.3", "How increased muscle activity increases heart rate via CO2", ["fig-q10-passage.jpg"]),
]

FIGURES = [
    ("fig-q3-fig1.jpg",     5,  64, 275),
    ("fig-q3-fig2.jpg",     6,  64, 740),
    ("fig-q4-stem.jpg",     10, 64, 200),
    ("fig-q8-table1.jpg",   21, 64, 335),
    ("fig-q10-passage.jpg", 24, 64, 342),
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
            "year": 2023,
            "series": "June",
            "unit": "7402/2",
            "level": "A-Level",
            "title": "June 2023 Paper 2 (7402/2)",
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
            "year": 2023,
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
