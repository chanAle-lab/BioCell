import json
import os
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598688841_43ff4c5d.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598688691_d7dcaa14.pdf"

PAPER_ID = "2014-specimen-7401-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2014,
    "series": "Specimen",
    "unit": "7401/1",
    "level": "AS",
    "date": "2014-09-23",
    "title": "AQA AS Biology Paper 1 (7401/1) Specimen Set 1",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

# Shared figures/tables/passages:
FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 110, "y0": 438, "x1": 545, "y1": 755},
    {"filename": "fig-q2-fig2.jpg", "page": 4, "x0": 75, "y0": 68, "x1": 545, "y1": 405},
    {"filename": "fig-q3-fig3.jpg", "page": 6, "x0": 110, "y0": 70, "x1": 545, "y1": 348},
    {"filename": "fig-q4-fig4.jpg", "page": 8, "x0": 110, "y0": 80, "x1": 470, "y1": 258},
    {"filename": "fig-q4-fig5.jpg", "page": 9, "x0": 110, "y0": 82, "x1": 545, "y1": 335},
    {"filename": "fig-q5-table1.jpg", "page": 10, "x0": 110, "y0": 80, "x1": 545, "y1": 374},
    {"filename": "fig-q5-fig6.jpg", "page": 11, "x0": 45, "y0": 76, "x1": 542, "y1": 405},
    {"filename": "fig-q6-fig7.jpg", "page": 13, "x0": 105, "y0": 80, "x1": 538, "y1": 288},
    {"filename": "fig-q7-fig8.jpg", "page": 16, "x0": 115, "y0": 210, "x1": 410, "y1": 788},
    {"filename": "fig-q7-table2.jpg", "page": 18, "x0": 55, "y0": 68, "x1": 545, "y1": 325},
    {"filename": "fig-q8-table3.jpg", "page": 20, "x0": 110, "y0": 80, "x1": 535, "y1": 486},
    {"filename": "fig-q9-passage.jpg", "page": 22, "x0": 75, "y0": 68, "x1": 545, "y1": 355},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 3, "specRef": "3.2.1.3", "summary": "Describe how to use cell fractionation to isolate chloroplasts from leaf tissue.", "figures": []},
    {"qnum": "01.2", "page": 3, "marks": 2, "specRef": "3.2.1.1", "summary": "Name the parts of the chloroplast labelled A and B in Figure 1.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.3", "page": 3, "marks": 1, "specRef": "3.2.1.3", "summary": "Calculate the length of the chloroplast shown in Figure 1.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.4", "page": 3, "marks": 1, "specRef": "3.2.1.3", "summary": "Name two structures in a eukaryotic cell that cannot be identified using an optical microscope.", "figures": []},

    {"qnum": "02.1", "page": 4, "marks": 1, "specRef": "3.1.4.2", "summary": "Give one other factor the technician would have controlled in the enzyme temperature investigation.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.2", "page": 4, "marks": 2, "specRef": "3.1.4.2", "summary": "Calculate the rate of reaction at 25 °C from Figure 2.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.3", "page": 5, "marks": 5, "specRef": "3.1.4.2", "summary": "Describe and explain the differences between the 37 °C and 25 °C curves in Figure 2.", "figures": ["fig-q2-fig2.jpg"]},

    {"qnum": "03.1", "page": 6, "marks": 3, "specRef": "3.4.3", "summary": "Describe and explain the appearance of one of the chromosomes in cell X in Figure 3.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.2", "page": 7, "marks": 2, "specRef": "3.4.3", "summary": "Describe what has happened during division 1 of meiosis in Figure 3.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.3", "page": 7, "marks": 1, "specRef": "3.4.3", "summary": "Identify one event that occurred during division 2 but not during division 1.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.4", "page": 7, "marks": 2, "specRef": "3.4.3", "summary": "Name two ways in which meiosis produces genetic variation.", "figures": []},

    {"qnum": "04.1", "page": 8, "marks": 1, "specRef": "3.1.5.1", "summary": "Name part F of each DNA nucleotide shown in Figure 4.", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.2", "page": 8, "marks": 2, "specRef": "3.1.5.1", "summary": "Determine the percentages of thymine and guanine in a DNA sample containing 18% adenine.", "figures": []},
    {"qnum": "04.3", "page": 9, "marks": 1, "specRef": "3.1.5.2", "summary": "Name the enzyme shown in DNA replication in Figure 5.", "figures": ["fig-q4-fig5.jpg"]},
    {"qnum": "04.4", "page": 9, "marks": 4, "specRef": "3.1.5.2", "summary": "Use Figure 4, Figure 5 and enzyme action to explain why new DNA strands are produced in opposite directions.", "figures": ["fig-q4-fig4.jpg", "fig-q4-fig5.jpg"]},

    {"qnum": "05.1", "page": 10, "marks": 1, "specRef": "3.4.5", "summary": "Put the taxonomic letters from Table 1 into the correct hierarchical order.", "figures": ["fig-q5-table1.jpg"]},
    {"qnum": "05.2", "page": 10, "marks": 1, "specRef": "3.4.5", "summary": "Give the binomial scientific name of the otter from Table 1.", "figures": ["fig-q5-table1.jpg"]},
    {"qnum": "05.3", "page": 11, "marks": 1, "specRef": "3.4.4", "summary": "Suggest one source of DNA from otters alive before hunting started.", "figures": ["fig-q5-fig6.jpg"]},
    {"qnum": "05.4", "page": 11, "marks": 2, "specRef": "3.4.4", "summary": "Conclude the effect of hunting on genetic diversity in otters using data from Figure 6.", "figures": ["fig-q5-fig6.jpg"]},
    {"qnum": "05.5", "page": 12, "marks": 2, "specRef": "3.4.4", "summary": "Suggest two reasons other than hunting why populations might show very low genetic diversity.", "figures": []},

    {"qnum": "06.1", "page": 13, "marks": 2, "specRef": "3.3.4.1", "summary": "Use hydrostatic pressure values in Figure 7 to explain how tissue fluid is formed.", "figures": ["fig-q6-fig7.jpg"]},
    {"qnum": "06.2", "page": 13, "marks": 1, "specRef": "3.3.4.1", "summary": "Explain why hydrostatic pressure falls from the arteriole end to the venule end of the capillary.", "figures": ["fig-q6-fig7.jpg"]},
    {"qnum": "06.3", "page": 14, "marks": 3, "specRef": "3.3.4.1", "summary": "Explain how high blood pressure leads to an accumulation of tissue fluid.", "figures": []},
    {"qnum": "06.4", "page": 14, "marks": 3, "specRef": "3.3.4.1", "summary": "Explain why the water potential of blood plasma is more negative at the venule end than the arteriole end.", "figures": []},

    {"qnum": "07.1", "page": 16, "marks": 2, "specRef": "3.1.3", "summary": "Describe how to test a piece of food for the presence of lipid.", "figures": []},
    {"qnum": "07.2", "page": 17, "marks": 1, "specRef": "3.1.3", "summary": "Name the molecule from which part A of the phospholipid in Figure 8 is formed.", "figures": ["fig-q7-fig8.jpg"]},
    {"qnum": "07.3", "page": 17, "marks": 1, "specRef": "3.1.3", "summary": "Name the type of bond between part A and fatty acid X in Figure 8.", "figures": ["fig-q7-fig8.jpg"]},
    {"qnum": "07.4", "page": 17, "marks": 1, "specRef": "3.1.3", "summary": "Identify which fatty acid (X or Y) in Figure 8 is unsaturated and explain why.", "figures": ["fig-q7-fig8.jpg"]},
    {"qnum": "07.5", "page": 18, "marks": 2, "specRef": "3.2.3", "summary": "Explain how scientists calculated Percentage of lipid in plasma membrane by mass in Table 2.", "figures": ["fig-q7-table2.jpg"]},
    {"qnum": "07.6", "page": 18, "marks": 1, "specRef": "3.2.3", "summary": "Suggest one advantage of the higher percentage of cholesterol in red blood cells compared with ileum cells.", "figures": ["fig-q7-table2.jpg"]},
    {"qnum": "07.7", "page": 19, "marks": 2, "specRef": "3.2.1.2", "summary": "Explain why E. coli maintains a constant shape despite having no cholesterol in its membrane.", "figures": ["fig-q7-table2.jpg"]},

    {"qnum": "08.1", "page": 20, "marks": 1, "specRef": "RP", "summary": "Explain why the data in Table 3 are described as processed results.", "figures": ["fig-q8-table3.jpg"]},
    {"qnum": "08.2", "page": 21, "marks": 2, "specRef": "RP", "summary": "Describe how to use a 1.0 mol dm^-3 sucrose solution to produce 30 cm^3 of 0.15 mol dm^-3 sucrose solution.", "figures": []},
    {"qnum": "08.3", "page": 21, "marks": 2, "specRef": "3.2.3", "summary": "Explain the change in mass of potato tissue in the 0.40 mol dm^-3 sucrose solution.", "figures": ["fig-q8-table3.jpg"]},
    {"qnum": "08.4", "page": 21, "marks": 3, "specRef": "RP", "summary": "Describe how to use the results in Table 3 to find the water potential of the potato tissue.", "figures": ["fig-q8-table3.jpg"]},

    {"qnum": "09.1", "page": 22, "marks": 3, "specRef": "3.2.1.2", "summary": "Explain why Herpes simplex virus (HSV) infects only nerve cells.", "figures": ["fig-q9-passage.jpg"]},
    {"qnum": "09.2", "page": 23, "marks": 2, "specRef": "3.2.1.2", "summary": "Explain why HSV can be described as inactive while remaining in the body for years.", "figures": ["fig-q9-passage.jpg"]},
    {"qnum": "09.3", "page": 23, "marks": 1, "specRef": "3.2.4", "summary": "Suggest one advantage of programmed cell death in virus-infected cells.", "figures": ["fig-q9-passage.jpg"]},
    {"qnum": "09.4", "page": 23, "marks": 4, "specRef": "3.4.2", "summary": "Explain how microRNA produced from the LAT gene allows HSV to remain in the body for years.", "figures": ["fig-q9-passage.jpg"]},
]


def extract_figures():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(QP_PATH)
    for fig in FIGURES:
        page = doc[fig["page"] - 1]
        rect = fitz.Rect(fig["x0"], fig["y0"], fig["x1"], fig["y1"])
        pix = page.get_pixmap(clip=rect, matrix=fitz.Matrix(2.5, 2.5))
        out_path = IMG_DIR / fig["filename"]
        pix.save(str(out_path))
        print(f"Saved figure: {out_path}")
    doc.close()


def main():
    assert sum(q["marks"] for q in QUESTIONS) == PAPER_META["totalMarks"], "Mark sum mismatch!"
    extract_figures()
    ms_dir = IMG_DIR / "ms"
    ms_qnums = [q["qnum"] for q in QUESTIONS]
    ms_map = crop_official_markschemes(MS_PATH, ms_qnums, str(ms_dir))

    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    db["papers"] = [p for p in db["papers"] if p["id"] != PAPER_ID]
    db["questions"] = [q for q in db["questions"] if q["paper"] != PAPER_ID]
    db["papers"].append(PAPER_META)

    for q in QUESTIONS:
        qnum = q["qnum"]
        slug = qnum.replace(".", "-")
        ms_file = ms_map.get(qnum)
        if not ms_file:
            raise RuntimeError(f"Missing markscheme crop for {qnum}")
        db["questions"].append({
            "id": f"{PAPER_ID}-q{qnum}",
            "paper": PAPER_ID,
            "year": PAPER_META["year"],
            "series": PAPER_META["series"],
            "unit": PAPER_META["unit"],
            "level": PAPER_META["level"],
            "question": qnum,
            "questionNumber": qnum,
            "page": q["page"],
            "marks": q["marks"],
            "specRef": q["specRef"],
            "topics": [q["specRef"]],
            "summary": q["summary"],
            "image": f"img/{PAPER_ID}/q{slug}.jpg",
            "markscheme": f"img/{PAPER_ID}/ms/{ms_file}",
            "figures": [f"img/{PAPER_ID}/{fn}" for fn in q["figures"]],
        })

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)
    print(f"Ingested {PAPER_ID}: {len(QUESTIONS)} questions, {sum(q['marks'] for q in QUESTIONS)} marks")


if __name__ == "__main__":
    main()
