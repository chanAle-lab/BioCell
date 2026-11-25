import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599550898_24987c9a.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599550913_53bd4e43.pdf"

PAPER_ID = "2016-specimen-set2-7402-2"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 2,  3, "3.6.3",   "Identifying M line, mitochondrion and myofibril in Figure 1", ["fig-q1-fig1.jpg"]),
    ("01.2", 2,  1, "3.6.3",   "Naming sarcomere between points A and B in Figure 1", ["fig-q1-fig1.jpg"]),
    ("01.3", 3,  1, "3.2.1.3", "Calculating actual distance between points A and B in um", ["fig-q1-fig1.jpg"]),
    ("01.4", 3,  2, "3.6.3",   "Role of glycogen granules in skeletal muscle", ["fig-q1-fig1.jpg"]),
    ("01.5", 3,  3, "3.6.3",   "How fall in pH reduces calcium ion stimulation of contraction", []),
    ("02.1", 4,  1, "3.6.1.1", "Why Figure 2 nerve pathway is a simple reflex arc", ["fig-q2-fig2.jpg"]),
    ("02.2", 4,  2, "3.6.1.1", "Two advantages of simple reflexes", ["fig-q2-fig2.jpg"]),
    ("02.3", 5,  2, "3.6.2.2", "How synapses ensure unidirectional impulse transmission", ["fig-q2-fig2.jpg"]),
    ("02.4", 5,  2, "3.6.2.1", "Feature of axon P causing faster impulse conduction", ["fig-q2-fig2.jpg"]),
    ("03.1", 7,  1, "3.5.1",   "Percentage decrease in sugarcane yield with Atrazine in study G", ["fig-q3-fig3.jpg"]),
    ("03.2", 7,  2, "3.5.1",   "Why no definite conclusions can be drawn from Figure 3 means", ["fig-q3-fig3.jpg"]),
    ("03.3", 7,  4, "3.5.1",   "How Atrazine blocking electron transfer reduces photosynthesis", []),
    ("03.4", 8,  1, "3.5.1",   "Why weeds treated with Atrazine give off small amounts of heat", []),
    ("04.1", 10, 1, "3.6.4.3", "Why filtrate concentration remains constant in PCT", ["fig-q4-fig4.jpg"]),
    ("04.2", 10, 3, "3.6.4.3", "Explaining filtrate concentration curve in loop of Henle", ["fig-q4-fig4.jpg"]),
    ("04.3", 11, 2, "3.6.4.3", "Evidence in Figure 4 that ADH was being secreted", ["fig-q4-fig4.jpg"]),
    ("05.1", 12, 2, "3.8.2.2", "Defining epigenetics", []),
    ("05.2", 12, 2, "3.8.2.2", "Binding features of oestrogen, methyl groups and acetyl groups", []),
    ("05.3", 13, 3, "3.8.2.3", "How increased methylation of tumour suppressor genes causes cancer", []),
    ("05.4", 13, 1, "3.8.2.3", "One difference between benign and malignant tumours", []),
    ("06.1", 14, 5, "3.7.4",   "How Table 2 stream recovery data provide evidence of succession", ["fig-q6-table2.jpg"]),
    ("06.2", 15, 2, "3.7.4",   "Comparing population growth per day of two stream species", ["fig-q6-table2.jpg"]),
    ("06.3", 15, 2, "3.7.4",   "Two features of a climax community", []),
    ("07.1", 16, 2, "3.8.4.1", "Why cDNA and gene machine work in E. coli without splicing", []),
    ("07.2", 16, 1, "3.8.4.1", "Why gene machine is faster than reverse transcriptase method", []),
    ("07.3", 17, 3, "3.8.4.1", "Inserting HGH gene copies into plasmid vectors", []),
    ("07.4", 18, 1, "3.8.4.1", "Advantage of GFP gene to identify transformed bacteria", []),
    ("07.5", 19, 2, "3.8.2.2", "Why arabinose must be included in agar for GFP expression", ["fig-q7-fig5.jpg"]),
    ("08.1", 20, 2, "3.6.1.1", "Identifying kinesis behaviour in Tenebrio molitor (Figure 6)", ["fig-q8-fig6.jpg"]),
    ("08.2", 21, 2, "3.3.2",   "How reduced movement in dry conditions reduces insect water loss", []),
    ("08.3", 21, 1, "3.6.1.1", "Identifying taxis behaviour in Figure 7", []),
    ("08.4", 22, 2, "3.6.1.1", "Whether Figure 8 supports hypothesis on antenna removal", ["fig-q8-fig6.jpg", "fig-q8-fig7.jpg"]),
    ("08.5", 23, 2, "3.6.1.1", "Evaluating student conclusion on humidity and insect movement", []),
    ("09.1", 24, 2, "3.7.1",   "Parental genotypes in monohybrid fruit fly eye shape cross", []),
    ("09.2", 24, 1, "3.7.1",   "Expected Mendelian ratio of bar-eyed to round-eyed flies", []),
    ("09.3", 24, 2, "3.7.1",   "Two reasons observed genetic ratios differ from expected", []),
    ("09.4", 24, 1, "3.7.1",   "Identifying chi-squared test for genetic ratio data", []),
    ("09.5", 25, 1, "3.7.1",   "Defining codominant alleles", []),
    ("09.6", 25, 1, "3.7.2",   "Calculating actual allele frequency without Hardy-Weinberg", []),
    ("09.7", 25, 2, "3.7.2",   "Hardy-Weinberg calculation of heterozygous fruit flies", []),
    ("10.1", 26, 2, "3.5.4",   "Two reasons poor phosphate supply causes poor plant growth", ["fig-q10-passage.jpg"]),
    ("10.2", 26, 2, "3.1.4.2", "How defensive enzymes produced by plants destroy bacteria", ["fig-q10-passage.jpg"]),
    ("10.3", 27, 3, "3.8.2.2", "How signal proteins lead to expression of defensive enzyme genes", ["fig-q10-passage.jpg"]),
    ("10.4", 27, 2, "3.5.4",   "Advantage of transmitting signals via mycorrhizal networks", ["fig-q10-passage.jpg"]),
    ("10.5", 27, 2, "3.5.4",   "Calculating rate of defensive enzyme secretion per second", ["fig-q10-passage.jpg"]),
    ("10.6", 28, 4, "3.5.4",   "Evaluating whether farmers should stop using fertilisers", ["fig-q10-passage.jpg"]),
]

FIGURES = [
    ("fig-q1-fig1.jpg",     2,  115, 515),
    ("fig-q2-fig2.jpg",     4,   75, 380),
    ("fig-q3-fig3.jpg",     6,   75, 705),
    ("fig-q4-fig4.jpg",     10,  64, 305),
    ("fig-q6-table2.jpg",   14,  75, 365),
    ("fig-q7-fig5.jpg",     18, 320, 635),
    ("fig-q8-fig6.jpg",     20,  75, 420),
    ("fig-q8-fig7.jpg",     21, 450, 695),
    ("fig-q10-passage.jpg", 26,  75, 405),
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
            "unit": "7402/2",
            "level": "A-Level",
            "title": "Specimen Set 2 Paper 2 (7402/2)",
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
