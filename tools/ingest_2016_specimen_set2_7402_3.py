import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599550909_04dc3dc3.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599550998_feab589b.pdf"

PAPER_ID = "2016-specimen-set2-7402-3"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 3,  3, "3.3.1",   "Calculating CO2 release per gram and plotting against temperature", ["fig-q1-table1.jpg"]),
    ("01.2", 4,  1, "3.3.2",   "Change in rate per hour of spiracle opening between 10 °C and 20 °C", []),
    ("01.3", 5,  1, "3.3.2",   "Determining total CO2 secreted at 30 °C from Figure 1", ["fig-q1-fig1.jpg"]),
    ("01.4", 5,  3, "3.5.2",   "Explaining effect of temperature on rate of CO2 release in insects", ["fig-q1-fig1.jpg"]),
    ("02.1", 6,  1, "3.4.3",   "Defining a substitution mutation", []),
    ("02.2", 7,  2, "3.8.4.3", "How gel electrophoresis separates synaptic proteins", ["fig-q2-fig2.jpg"]),
    ("02.3", 7,  3, "3.2.4",   "Why each labelled antibody binds specifically to one protein", ["fig-q2-fig2.jpg"]),
    ("02.4", 7,  2, "3.6.2.2", "Effect of NL3 mutation on synaptic proteins in Figure 2", ["fig-q2-fig2.jpg"]),
    ("02.5", 8,  2, "3.6.2.2", "How NL3 mutation may affect mouse memory", ["fig-q2-fig2.jpg"]),
    ("03.1", 9,  2, "3.5.3",   "Calculating percentage of water in freshly cut wood sample", ["fig-q3-table2.jpg"]),
    ("03.2", 9,  2, "3.5.3",   "Determining whether oven drying removed all water from wood", []),
    ("03.3", 10, 2, "3.5.3",   "Relationship between trunk diameter and tree biomass (Figure 3)", []),
    ("03.4", 11, 4, "3.5.4",   "Estimating total carbon mass in a tree plantation", ["fig-q3-table2.jpg", "fig-q3-fig3.jpg"]),
    ("04.1", 13, 3, "3.4.6",   "Conclusions on human activities and plant biodiversity (Figure 4)", ["fig-q4-fig4.jpg"]),
    ("04.2", 13, 2, "3.7.4",   "Explaining effect size when non-native species are introduced", ["fig-q4-fig4.jpg"]),
    ("04.3", 14, 3, "3.7.4",   "Investigating effect of non-native plant invasion over many years", []),
    ("04.4", 14, 2, "3.4.6",   "Writing equation and calculating effect size for species richness", []),
    ("05.1", 15, 1, "3.8.2.1", "Why embryonic pluripotent stem cells may repair heart damage", []),
    ("05.2", 15, 2, "3.8.2.3", "How putting ESCs into heart might cause tumour/harm", []),
    ("05.3", 16, 2, "3.3.4.1", "Two ways Group A acts as a control in heart transplant study", []),
    ("05.4", 17, 3, "3.3.4.1", "Conclusions on cardiomyocyte stimulation of new blood vessels", ["fig-q5-fig5.jpg"]),
    ("05.5", 17, 3, "3.3.4.1", "How new blood vessels increase rate of heart tissue repair", []),
    ("05.6", 18, 4, "3.2.1.3", "Microscope method to find mean number of capillaries per mm2", []),
    ("06.1", 19, 25, "3.1.5.1", "Essay: Importance of nucleotides, derived molecules and nucleic acids", []),
    ("06.2", 19, 25, "3.1.7",   "Essay: Ways water and regulation of water content are important", []),
]

FIGURES = [
    ("fig-q1-table1.jpg", 3,  145, 390),
    ("fig-q1-fig1.jpg",   4,  180, 770),
    ("fig-q2-fig2.jpg",   6,   75, 505),
    ("fig-q3-table2.jpg", 9,   75, 360),
    ("fig-q3-fig3.jpg",   10,  80, 480),
    ("fig-q4-fig4.jpg",   12,  75, 665),
    ("fig-q5-fig5.jpg",   16,  75, 595),
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
            m = re.match(r"^[)\s]*(0[1-9]\.[1-9])\b", txt)
            m2 = re.match(r"^Question\s+(06\.[12]):", txt)
            qcode = m.group(1) if m else (m2.group(1) if m2 else None)
            if qcode and not any(x[0] == qcode for x in markers):
                markers.append((qcode, pno, b[1]))
    markers.sort(key=lambda x: (x[1], x[2]))
    print(f"Found {len(markers)} MS markers")
    for idx, (qcode, pno, y_start) in enumerate(markers):
        if qcode == "06.1":
            next_pno, next_y = pno, 730
        elif qcode == "06.2":
            next_pno, next_y = pno, 730
        elif idx + 1 < len(markers):
            _, next_pno, next_y = markers[idx + 1]
            if next_pno > pno + 1:
                next_pno, next_y = pno, 760
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
            "unit": "7402/3",
            "level": "A-Level",
            "title": "Specimen Set 2 Paper 3 (7402/3)",
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
            "year": 2016,
            "series": "Specimen Set 2",
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
