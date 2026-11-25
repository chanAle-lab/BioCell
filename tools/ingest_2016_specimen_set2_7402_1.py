import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599550998_98216f1a.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599551542_3a787725.pdf"

PAPER_ID = "2016-specimen-set2-7402-1"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 2,  2, "3.1.2",   "Identifying beta-glucose and adenosine triphosphate in Figure 1", ["fig-q1-fig1.jpg"]),
    ("01.2", 2,  2, "3.1.3",   "Identifying molecule C as a saturated fatty acid", ["fig-q1-fig1.jpg"]),
    ("01.3", 3,  2, "3.1.4.1", "Drawing dipeptide formed from two glycine molecules", ["fig-q1-fig1.jpg"]),
    ("01.4", 3,  1, "3.1.1",   "Naming water formed during peptide bond condensation", []),
    ("02.1", 4,  1, "3.2.1.3", "Why cell-surface membrane is visible with TEM but not optical microscope", ["fig-q2-fig2.jpg"]),
    ("02.2", 4,  1, "3.2.1.1", "Why no organelles are visible in red blood cell cytoplasm", ["fig-q2-fig2.jpg"]),
    ("02.3", 5,  3, "3.2.3",   "Explaining appearance of cell-surface membrane as two dark lines", ["fig-q2-fig2.jpg"]),
    ("02.4", 5,  3, "3.2.3",   "Describing movement of substances by facilitated diffusion", []),
    ("03.1", 6,  1, "3.4.5",   "Naming the phylum taxon represented by Zygomycota", ["fig-q3-fig3.jpg"]),
    ("03.2", 6,  1, "3.4.3",   "Identifying where meiosis occurs in Rhizopus life cycle", ["fig-q3-fig4.jpg"]),
    ("03.3", 7,  2, "3.4.3",   "Advantages of asexual and sexual reproduction in Rhizopus", ["fig-q3-fig4.jpg"]),
    ("03.4", 7,  1, "3.4.4",   "Advantage of vertical hypha supporting sporangium", []),
    ("03.5", 8,  3, "3.2.1.3", "Calculating mean volume of Rhizopus spores from Figure 5", ["fig-q3-fig5.jpg"]),
    ("04.1", 10, 2, "3.1.4.2", "Explaining enzyme-substrate curve A without inhibitor", ["fig-q4-fig6.jpg"]),
    ("04.2", 11, 4, "3.1.4.2", "Comparing Vmax with competitive vs non-competitive inhibitor", ["fig-q4-fig6.jpg"]),
    ("04.3", 11, 1, "3.1.4.2", "Using Michaelis constant Km to identify type of inhibition", ["fig-q4-fig6.jpg"]),
    ("05.1", 13, 2, "3.4.6",   "Two reasons grassy strips increase animal biodiversity", []),
    ("05.2", 13, 2, "3.4.6",   "Determining 40 minutes as appropriate soil sorting time", []),
    ("05.3", 14, 1, "3.4.6",   "Why index of diversity cannot be calculated from Table 1", []),
    ("05.4", 15, 4, "3.4.6",   "Evaluating journalist conclusion on grassy strips and diversity", ["fig-q5-table1.jpg"]),
    ("06.1", 16, 1, "3.4.2",   "Range in number of copies of AMY1 gene from Figure 7", ["fig-q6-fig7.jpg"]),
    ("06.2", 16, 2, "3.4.2",   "Estimating standard deviation of AMY1 gene copies from Figure 7", ["fig-q6-fig7.jpg"]),
    ("06.3", 17, 3, "3.4.2",   "Interpreting correlation coefficient R=0.50, P<0.0001", []),
    ("06.4", 17, 3, "3.3.3",   "Why AMY1 gene copies unlikely to affect starch digestion", []),
    ("07.1", 18, 2, "3.1.5.1", "How organic bases stabilise the structure of DNA", []),
    ("07.2", 18, 1, "3.4.2",   "Advantage of showing genetic code as mRNA base sequences", []),
    ("07.3", 19, 1, "3.4.2",   "Naming a group of three mRNA bases coding for an amino acid", []),
    ("07.4", 19, 2, "3.4.2",   "Using Table 2 to explain why genetic code is degenerate", ["fig-q7-table2.jpg"]),
    ("07.5", 19, 2, "3.4.2",   "Role of mRNA stop triplets UGA, UAG and UAA", ["fig-q7-table2.jpg"]),
    ("07.6", 20, 2, "3.4.2",   "Completing DNA template and amino acid sequence in Table 3", ["fig-q7-table2.jpg"]),
    ("08.1", 22, 1, "3.1.4.1", "Explaining meaning of quaternary protein structure", []),
    ("08.2", 22, 1, "3.3.4.1", "Formula for percentage saturation of haemoglobin with oxygen", []),
    ("08.3", 23, 2, "3.3.4.1", "Evidence from Figure 8 for cooperative oxygen binding", ["fig-q8-fig8.jpg"]),
    ("08.4", 23, 1, "3.3.4.1", "Advantage of haemoglobin affinity change for oxygen", ["fig-q8-fig8.jpg"]),
    ("08.5", 24, 3, "3.3.4.1", "Calculating volume of oxygen released to tissues per minute", ["fig-q8-fig8.jpg"]),
    ("09.1", 26, 2, "3.3.4.2", "Explaining nutrient-poor sand and 48 hours dark in translocation study", ["fig-q9-table4.jpg"]),
    ("09.2", 27, 2, "3.3.4.2", "Two reasons for drying plant samples in oven at 100 °C", ["fig-q9-table4.jpg"]),
    ("09.3", 27, 4, "3.3.4.2", "Evaluating whether Table 4 supports sucrose-borate hypothesis", ["fig-q9-table4.jpg"]),
    ("09.4", 27, 2, "3.3.4.2", "Adapting method to identify tissue carrying labelled sucrose", []),
    ("10.1", 28, 6, "3.2.4",   "How vaccination leads to protection against bacterial meningitis", []),
    ("10.2", 29, 4, "3.4.4",   "How Neisseria meningitidis becomes resistant to antibiotics", []),
    ("10.3", 30, 5, "3.2.1.2", "Contrasting structure of a bacterial cell and a human cell", []),
]

FIGURES = [
    ("fig-q1-fig1.jpg",   2,  125, 465),
    ("fig-q2-fig2.jpg",   4,   75, 320),
    ("fig-q3-fig3.jpg",   6,   75, 215),
    ("fig-q3-fig4.jpg",   6,  290, 645),
    ("fig-q3-fig5.jpg",   7,  310, 590),
    ("fig-q4-fig6.jpg",   10,  75, 565),
    ("fig-q5-table1.jpg", 14,  75, 395),
    ("fig-q6-fig7.jpg",   16,  75, 505),
    ("fig-q7-table2.jpg", 18, 320, 720),
    ("fig-q8-fig8.jpg",   22, 330, 725),
    ("fig-q9-table4.jpg", 26,  75, 555),
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
            "year": 2016,
            "series": "Specimen Set 2",
            "unit": "7402/1",
            "level": "A-Level",
            "title": "Specimen Set 2 Paper 1 (7402/1)",
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
            "year": 2016,
            "series": "Specimen Set 2",
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
