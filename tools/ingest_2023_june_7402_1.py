import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599532740_0f454c65.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599532835_cfb620fb.pdf"

PAPER_ID = "2023-june-7402-1"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 2,  2, "3.2.1.2", "Three structural features found in all virus particles", []),
    ("01.2", 2,  2, "3.2.1.2", "Why viruses are described as acellular and non-living", []),
    ("01.3", 2,  1, "3.2.1.2", "Why antibiotics are not effective against viruses", []),
    ("02.1", 3,  3, "3.1.2",   "Comparing structure of chitin to cellulose using Figure 1", []),
    ("02.2", 4,  2, "3.3.2",   "Adaptation of gas exchange surface in insect tracheal system", []),
    ("02.3", 4,  3, "3.3.4.2", "Importance of xylem being kept open as a continuous tube", []),
    ("03.1", 6,  1, "3.2.1.1", "Eukaryotic structure in Plasmodium vivax (Figure 2)", []),
    ("03.2", 6,  2, "3.2.1.1", "Two functions of the Golgi apparatus in a eukaryotic cell", []),
    ("03.3", 7,  1, "3.4.5",   "Order of human migration out of Africa from Figure 3", ["fig-q3-fig3.jpg"]),
    ("03.4", 8,  1, "3.4.4",   "Calculating worldwide malaria cases caused by P. vivax", []),
    ("03.5", 8,  4, "3.4.4",   "Natural selection for P. vivax resistance in Africa", []),
    ("04.1", 9,  3, "3.3.3",   "Reduced absorption of digestion products and water in ileum", []),
    ("04.2", 11, 3, "3.2.4",   "Passive immunity with anti-toxin antibody in C. difficile", ["fig-q4-fig4.jpg"]),
    ("04.3", 11, 3, "3.3.3",   "How oral anti-toxin antibody would be digested", []),
    ("05.1", 12, 3, "3.4.4",   "Aseptic techniques for spreading bacterial cultures on agar", []),
    ("05.2", 13, 2, "3.4.4",   "Calculating minimum depth of agar well for 50 mm3 oil", []),
    ("05.3", 15, 2, "3.4.4",   "Positive and negative controls in antimicrobial agar test", ["fig-q5-fig5-table1.jpg"]),
    ("05.4", 15, 1, "3.4.4",   "Completing median and mean clear zone diameters in Table 1", ["fig-q5-fig5-table1.jpg"]),
    ("05.5", 15, 2, "3.4.4",   "Using standard deviations to evaluate difference in means", ["fig-q5-fig5-table1.jpg"]),
    ("06.1", 16, 2, "3.4.2",   "Defining genome and proteome", []),
    ("06.2", 16, 3, "3.4.5",   "Accuracy and limitations of early bacterial classification", []),
    ("06.3", 17, 1, "3.4.5",   "Why several bacterial species have been renamed recently", []),
    ("06.4", 17, 2, "3.2.1.3", "Calculating magnification of bacterial cell image", []),
    ("07.1", 18, 3, "3.3.4.1", "Effect of carbon monoxide on oxygen loading and unloading", []),
    ("07.2", 19, 3, "3.3.4.1", "Evaluating WHO carbon monoxide exposure recommendations", []),
    ("08.1", 20, 2, "3.2.2",   "Identifying cancer cells treated with MiTMAB inhibiting cytokinesis", []),
    ("08.2", 21, 3, "3.1.4.2", "How non-competitive inhibitor MiTMAB inactivates dynamin", []),
    ("08.3", 23, 3, "3.2.2",   "Explaining effect of MiTMAB concentration on cancer cell growth", ["fig-q8-fig9.jpg"]),
    ("08.4", 23, 2, "3.2.2",   "Calculating increase in mass of MiTMAB added to cells", ["fig-q8-fig9.jpg"]),
    ("09.1", 25, 2, "3.2.4",   "How dengue fever ELISA test produces a positive line at T", ["fig-q9-fig10-11.jpg"]),
    ("09.2", 25, 1, "3.2.4",   "Why a line at C shows the ELISA test has worked", ["fig-q9-fig10-11.jpg"]),
    ("09.3", 26, 2, "3.2.4",   "Why fused hybridoma cells allow continuous antibody production", ["fig-q9-fig12.jpg"]),
    ("09.4", 26, 1, "3.2.4",   "Evaluating ethics of monoclonal antibody production in Figure 12", ["fig-q9-fig12.jpg"]),
    ("09.5", 29, 3, "3.2.4",   "Discussing recommendation for worldwide use of new ELISA test", ["fig-q9-table3.jpg"]),
    ("09.6", 29, 2, "3.3.4.1", "Effect of blood protein loss on tissue fluid return", []),
    ("10.1", 30, 5, "3.1.4.1", "How a quaternary protein is formed from its monomers", []),
    ("10.2", 31, 6, "3.1.5.1", "Structure of DNA and structure of a chromosome", []),
    ("10.3", 32, 4, "3.4.3",   "Processes other than mutation increasing genetic variation", []),
]

FIGURES = [
    ("fig-q3-fig3.jpg",        7,  64, 445),
    ("fig-q4-fig4.jpg",        10, 64, 715),
    ("fig-q5-fig5-table1.jpg", 14, 64, 690),
    ("fig-q8-fig9.jpg",        22, 64, 630),
    ("fig-q9-fig10-11.jpg",    24, 64, 660),
    ("fig-q9-fig12.jpg",       26, 64, 426),
    ("fig-q9-table3.jpg",      28, 64, 470),
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
            "unit": "7402/1",
            "level": "A-Level",
            "title": "June 2023 Paper 1 (7402/1)",
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
