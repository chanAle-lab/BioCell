import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599564207_7be1c002.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599564164_d578ddc7.pdf"

PAPER_ID = "2014-specimen-7402-1"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 2,  1, "3.1.4.2", "Factors controlled in amylase starch hydrolysis experiment", ["fig-q1-fig1.jpg"]),
    ("01.2", 2,  2, "3.1.4.2", "Using tangents to calculate ratio of initial reaction rates", ["fig-q1-fig1.jpg"]),
    ("01.3", 3,  2, "3.1.4.2", "Explaining initial rate and curve levelling at 60 °C", ["fig-q1-fig1.jpg"]),
    ("01.4", 3,  4, "3.1.4.2", "Determining time for enzyme denaturation at 60 °C", ["fig-q1-fig1.jpg"]),
    ("02.1", 4,  4, "3.3.2",   "Pathway of air from trachea to alveoli and breathing out", []),
    ("02.2", 5,  1, "3.3.2",   "Percentage of maximum air volume breathed out by Group A in 1 s", ["fig-q2-fig2.jpg"]),
    ("02.3", 5,  3, "3.3.2",   "Identifying group with lung fibrosis from FEV and vital capacity", ["fig-q2-fig2.jpg"]),
    ("03.1", 6,  1, "3.4.6",   "Difference between species richness and index of diversity", []),
    ("03.2", 6,  1, "3.4.6",   "Why canopy butterfly traps were not set at the same height", ["fig-q3-table1.jpg"]),
    ("03.3", 7,  3, "3.4.6",   "Calculating ratio of canopy to understorey index of diversity", ["fig-q3-table1.jpg"]),
    ("03.4", 7,  3, "3.4.6",   "Interpreting statistical test results on butterfly species distribution", ["fig-q3-table1.jpg"]),
    ("04.1", 8,  2, "3.1.2",   "Structural differences between starch and cellulose molecules", ["fig-q4-fig3.jpg"]),
    ("04.2", 8,  2, "3.1.2",   "How starch structure relates to its function in plant cells", ["fig-q4-fig3.jpg"]),
    ("04.3", 9,  3, "3.1.2",   "How cellulose structure adapts it for plant cell walls", ["fig-q4-fig3.jpg"]),
    ("05.1", 10, 3, "3.2.3",   "Contrasting facilitated diffusion and active transport", []),
    ("05.2", 11, 2, "3.2.3",   "Calculating ratio of mean chloride ion uptake rates", ["fig-q5-fig4.jpg"]),
    ("05.3", 11, 4, "3.2.3",   "Explaining chloride ion uptake with and without respiratory inhibitor", ["fig-q5-fig4.jpg"]),
    ("06.1", 12, 2, "3.4.5",   "Completing taxonomic classification table for bluethroat", ["fig-q6-table2.jpg"]),
    ("06.2", 13, 1, "3.4.4",   "Meaning of genetic diversity in wild vs zoo bird populations", ["fig-q6-table3.jpg"]),
    ("06.3", 13, 2, "3.4.4",   "Comparing genetic diversity of wild and zoo-bred birds", ["fig-q6-table3.jpg"]),
    ("07.1", 14, 2, "3.2.4",   "Why HIV antibody ELISA test cannot diagnose AIDS", ["fig-q7-fig5.jpg"]),
    ("07.2", 15, 2, "3.2.4",   "Why ELISA solution remains yellow if not infected with HIV", ["fig-q7-fig5.jpg"]),
    ("07.3", 15, 2, "3.2.4",   "Why baby of HIV-positive mother may test positive without HIV", ["fig-q7-fig5.jpg"]),
    ("07.4", 15, 2, "3.2.4",   "Two purposes of the control well in the ELISA test", ["fig-q7-fig5.jpg"]),
    ("08.1", 16, 1, "3.1.5.1", "Drawing a box around a single nucleotide on DNA diagram", ["fig-q8-fig6.jpg"]),
    ("08.2", 16, 2, "3.1.5.1", "Completing DNA base percentage table for both strands", ["fig-q8-table4.jpg"]),
    ("08.3", 17, 4, "3.1.5.2", "Role of DNA polymerase and 5' to 3' replication in Figure 6", ["fig-q8-fig6.jpg"]),
    ("09.1", 18, 4, "3.3.4.2", "Mass flow hypothesis for translocation in plants", []),
    ("09.2", 19, 1, "3.3.4.2", "Process using 14C-labelled compounds between leaf and trunk", ["fig-q9-fig7.jpg"]),
    ("09.3", 19, 2, "3.3.4.2", "Calculating rate of movement of 14C label down tree trunk", ["fig-q9-fig7.jpg"]),
    ("09.4", 19, 1, "3.3.4.2", "Other measurement needed to calculate translocation rate", ["fig-q9-fig7.jpg"]),
    ("10.1", 20, 1, "3.2.2",   "Ordering stages of mitosis from onion root tip images", ["fig-q10-fig8.jpg"]),
    ("10.2", 20, 2, "3.2.2",   "Explaining steps of preparing an onion root tip squash", []),
    ("10.3", 21, 3, "3.4.3",   "Explaining chromosome behaviour and DNA changes in meiosis", ["fig-q10-fig9.jpg"]),
    ("10.4", 21, 1, "3.4.3",   "Effect of fertilisation on DNA amount per cell", ["fig-q10-fig9.jpg"]),
    ("11.1", 22, 6, "3.4.2",   "Role of mRNA and tRNA during translation", []),
    ("11.2", 23, 5, "3.1.4.1", "Describing primary, secondary, tertiary, and quaternary protein structure", []),
    ("11.3", 24, 4, "3.3.3",   "Describing digestion of proteins by endopeptidases, exopeptidases, and dipeptidases", []),
]

FIGURES = [
    ("fig-q1-fig1.jpg",   2,  175, 435),
    ("fig-q2-fig2.jpg",   4,  375, 790),
    ("fig-q3-table1.jpg", 6,  340, 665),
    ("fig-q4-fig3.jpg",   8,   78, 295),
    ("fig-q5-fig4.jpg",   10, 480, 740),
    ("fig-q6-table2.jpg", 12,  78, 380),
    ("fig-q6-table3.jpg", 12, 520, 760),
    ("fig-q7-fig5.jpg",   14,  78, 585),
    ("fig-q8-fig6.jpg",   16,  78, 410),
    ("fig-q8-table4.jpg", 16, 495, 670),
    ("fig-q9-fig7.jpg",   18, 375, 780),
    ("fig-q10-fig8.jpg",  20,  78, 370),
    ("fig-q10-fig9.jpg",  21,  78, 382),
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
            m = re.match(r"^(0[1-9]\.[1-9]|1[01]\.[1-9])\b", txt)
            if m:
                qcode = m.group(1)
                if not any(x[0] == qcode for x in markers):
                    markers.append((qcode, pno, b[1]))
    markers.sort(key=lambda x: (x[1], x[2]))
    print(f"Found {len(markers)} MS markers")
    for idx, (qcode, pno, y_start) in enumerate(markers):
        if idx + 1 < len(markers):
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
        "unit": "7402/1",
        "level": "A-Level",
        "title": "2014 Specimen A-Level Paper 1 (7402/1)",
        "totalMarks": 91
    })

    for qcode, page, marks, spec_ref, summary, figs in QUESTIONS:
        q_num, sub_num = qcode.split(".")
        data["questions"].append({
            "id": f"{PAPER_ID}-q{qcode}",
            "paper": PAPER_ID,
            "year": 2014,
            "series": "Specimen",
            "unit": "7402/1",
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
