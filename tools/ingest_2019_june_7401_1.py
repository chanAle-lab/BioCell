"""Ingest AQA AS Biology June 2019 Paper 1 (7401/1) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795597880988_f0c92384.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795597880986_00f8398c.pdf"
)

PAPER_ID = "2019-june-7401-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2019,
    "series": "June",
    "unit": "7401/1",
    "level": "AS",
    "date": "2019-05-21",
    "title": "7401/1 — AS Paper 1 (June 2019)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 3, "x0": 60, "y0": 82, "x1": 540, "y1": 360},
    {"filename": "fig-q3-fig2.jpg", "page": 5, "x0": 60, "y0": 90, "x1": 540, "y1": 195},
    {"filename": "fig-q3-table1.jpg", "page": 6, "x0": 60, "y0": 250, "x1": 540, "y1": 440},
    {"filename": "fig-q4-tables2-3.jpg", "page": 8, "x0": 60, "y0": 130, "x1": 540, "y1": 460},
    {"filename": "fig-q5-fig3.jpg", "page": 10, "x0": 60, "y0": 335, "x1": 540, "y1": 576},
    {"filename": "fig-q6-fig4.jpg", "page": 13, "x0": 60, "y0": 86, "x1": 540, "y1": 308},
    {"filename": "fig-q6-fig5.jpg", "page": 14, "x0": 60, "y0": 210, "x1": 540, "y1": 530},
    {"filename": "fig-q6-table4.jpg", "page": 14, "x0": 60, "y0": 538, "x1": 540, "y1": 715},
    {"filename": "fig-q7-table5.jpg", "page": 18, "x0": 60, "y0": 288, "x1": 540, "y1": 505},
    {"filename": "fig-q8-fig6.jpg", "page": 21, "x0": 60, "y0": 178, "x1": 540, "y1": 376},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 3, "01.4": 3,
    "02.1": 4, "02.2": 4, "02.3": 4,
    "03.1": 5, "03.2": 5, "03.3": 6, "03.4": 7, "03.5": 7,
    "04.1": 8, "04.2": 9, "04.3": 9, "04.4": 9, "04.5": 9,
    "05.1": 10, "05.2": 10, "05.3": 11, "05.4": 11, "05.5": 11, "05.6": 12,
    "06.1": 13, "06.2": 13, "06.3": 15, "06.4": 15,
    "07.1": 16, "07.2": 18, "07.3": 19, "07.4": 19, "07.5": 19,
    "08.1": 20, "08.2": 20, "08.3": 21,
    "09.1": 22, "09.2": 22, "09.3": 23, "09.4": 24,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.4.1", "marks": 3, "skills": [], "stem": "Give three ways in which chloroplast DNA is different from nuclear DNA."},
    {"qnum": "01.2", "specRef": "3.1.5", "marks": 1, "skills": [], "stem": "Give one structural difference between a thymine DNA nucleotide and a uracil RNA nucleotide."},
    {"qnum": "01.3", "specRef": "3.4.2", "marks": 1, "skills": [], "stem": "Name the structures labelled W and X in the tRNA molecule (Figure 1).", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.4", "specRef": "3.4.2", "marks": 2, "skills": [], "stem": "Give two reasons why not all mutations in a gene nucleotide sequence alter polypeptide structure."},
    {"qnum": "02.1", "specRef": "3.2.4", "marks": 1, "skills": [], "stem": "Define what a monoclonal antibody is."},
    {"qnum": "02.2", "specRef": "3.2.4", "marks": 1, "skills": [], "stem": "Give one example of using monoclonal antibodies in a medical treatment."},
    {"qnum": "02.3", "specRef": "3.2.4", "marks": 4, "skills": [], "stem": "Describe the role of antibodies in producing a positive result in an ELISA test."},
    {"qnum": "03.1", "specRef": "3.1.2", "marks": 1, "skills": [], "stem": "Draw boxes on Figure 2 around the chemical groups in two alpha-glucose molecules used to form a glycosidic bond.", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "03.2", "specRef": "3.1.2", "marks": 2, "skills": ["practical"], "stem": "Suggest a method, other than a colorimeter, to compare the mass of precipitate formed in a Benedict's test."},
    {"qnum": "03.3", "specRef": "3.1.2", "marks": 2, "skills": ["analysis"], "stem": "Explain the Benedict's test results before and after maltase treatment for beakers A and B in Table 1.", "figures": ["fig-q3-table1.jpg"]},
    {"qnum": "03.4", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Give one reason why using a colorimeter improves the repeatability of the student's results."},
    {"qnum": "03.5", "specRef": "3.1.2", "marks": 2, "skills": ["maths"], "stem": "Calculate the percentage error for the volume measurements used to obtain a 20 cm3 Benedict's test mixture."},
    {"qnum": "04.1", "specRef": "3.4.6", "marks": 1, "skills": ["maths"], "stem": "Complete Table 3 by calculating the index of diversity (d) at Site 1 using Table 2.", "figures": ["fig-q4-tables2-3.jpg"]},
    {"qnum": "04.2", "specRef": "3.4.6", "marks": 2, "skills": [], "stem": "Explain why it is more useful to calculate an index of diversity than to record species richness."},
    {"qnum": "04.3", "specRef": "3.4.7", "marks": 1, "skills": ["practical"], "stem": "Suggest how the scientist measured the rate of water flow in the river."},
    {"qnum": "04.4", "specRef": "3.4.6", "marks": 2, "skills": ["analysis"], "stem": "Use Table 2 and Table 3 to suggest and explain why Slate Drake mayfly numbers differed between Site 1 and Site 2.", "figures": ["fig-q4-tables2-3.jpg"]},
    {"qnum": "04.5", "specRef": "3.4.7", "marks": 1, "skills": ["practical"], "stem": "Give one way the sampling procedure for collecting mayflies could be standardised."},
    {"qnum": "05.1", "specRef": "3.2.1", "marks": 1, "skills": ["maths"], "stem": "Tick the box showing the correct order of magnitude from 50 nm to 5 x 10^-2 mm."},
    {"qnum": "05.2", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Identify structures D and E in the chloroplast electron micrograph (Figure 3).", "figures": ["fig-q5-fig3.jpg"]},
    {"qnum": "05.3", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Explain why the detail shown in Figure 3 would not be seen using an optical microscope.", "figures": ["fig-q5-fig3.jpg"]},
    {"qnum": "05.4", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Name an organelle found in both a chloroplast and a prokaryotic cell."},
    {"qnum": "05.5", "specRef": "3.2.1", "marks": 2, "skills": ["maths"], "stem": "Calculate the volume of cytoplasm in a plant cell given total cell volume and organelle volume percentage."},
    {"qnum": "05.6", "specRef": "3.2.1", "marks": 3, "skills": ["practical"], "stem": "State and explain two properties of the solution used when separating cell components by fractionation."},
    {"qnum": "06.1", "specRef": "3.3.2", "marks": 1, "skills": [], "stem": "Identify structures F and G in the scanning electron micrograph of a fish gill (Figure 4).", "figures": ["fig-q6-fig4.jpg"]},
    {"qnum": "06.2", "specRef": "3.3.2", "marks": 3, "skills": [], "stem": "Describe and explain the advantage of the counter-current principle in gas exchange across a fish gill."},
    {"qnum": "06.3", "specRef": "3.3.2", "marks": 2, "skills": ["analysis"], "stem": "Use Figure 5 and Table 4 to describe the relationship between dissolved oxygen concentration, depth, and Anoplopoma fimbria distribution.", "figures": ["fig-q6-fig5.jpg", "fig-q6-table4.jpg"]},
    {"qnum": "06.4", "specRef": "3.3.2", "marks": 2, "skills": ["analysis"], "stem": "Use Figure 5 and Table 4 to conclude how the gas exchange surfaces of these three fish species are adapted.", "figures": ["fig-q6-fig5.jpg", "fig-q6-table4.jpg"]},
    {"qnum": "07.1", "specRef": "3.1.4", "marks": 3, "skills": [], "stem": "Explain how the active site of an enzyme causes a high rate of reaction."},
    {"qnum": "07.2", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Give one other factor the student would have controlled in the catalase hydrogen peroxide investigation.", "figures": ["fig-q7-table5.jpg"]},
    {"qnum": "07.3", "specRef": "RP", "marks": 2, "skills": ["maths"], "stem": "Complete Table 5 by calculating the relative rate of reaction in arbitrary units.", "figures": ["fig-q7-table5.jpg"]},
    {"qnum": "07.4", "specRef": "3.1.4", "marks": 3, "skills": ["maths", "practical"], "stem": "Plot a suitable graph of the processed rate of reaction data from Table 5.", "figures": ["fig-q7-table5.jpg"]},
    {"qnum": "07.5", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Suggest a change to the procedure so 10 cm3 of oxygen is produced in less than 6 seconds at 2.0 mol dm^-3 H2O2."},
    {"qnum": "08.1", "specRef": "3.1.4", "marks": 2, "skills": ["practical"], "stem": "Describe a biochemical test to confirm the presence of protein in a solution."},
    {"qnum": "08.2", "specRef": "3.1.4", "marks": 3, "skills": [], "stem": "Describe the similarities and differences between two dipeptides containing different amino acids."},
    {"qnum": "08.3", "specRef": "3.1.4", "marks": 3, "skills": ["analysis"], "stem": "Explain what the positions of the spots in the electrophoresis diagram (Figure 6) show about the three amino acids.", "figures": ["fig-q8-fig6.jpg"]},
    {"qnum": "09.1", "specRef": "3.2.2", "marks": 2, "skills": ["analysis"], "stem": "Suggest why preventing spindle fibre formation by ABZ stopped the cell cycle."},
    {"qnum": "09.2", "specRef": "3.2.2", "marks": 1, "skills": ["analysis"], "stem": "Suggest and explain why ABZ could be used to treat cancer even though it affects some healthy cells."},
    {"qnum": "09.3", "specRef": "3.2.2", "marks": 4, "skills": ["analysis"], "stem": "Conclude the effect of ABZ on tumour cells using Cyclin B concentrations and DNA mass changes."},
    {"qnum": "09.4", "specRef": "3.2.2", "marks": 3, "skills": ["analysis"], "stem": "Evaluate the scientists' suggestion that ABZ could be used to successfully treat stomach cancer."},
]


def extract_figures() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(QP_PDF))
    for fig in FIGURES:
        page = doc[fig["page"] - 1]
        rect = fitz.Rect(fig["x0"], fig["y0"], fig["x1"], fig["y1"])
        pix = page.get_pixmap(clip=rect, matrix=fitz.Matrix(2.5, 2.5))
        out_path = IMG_DIR / fig["filename"]
        pix.save(str(out_path))
        print(f"Saved figure: {out_path}")
    doc.close()


def main() -> None:
    extract_figures()
    ms_labels = [MS_QNUM_MAP.get(q["qnum"], q["qnum"]) for q in QUESTIONS]
    ms_map = crop_official_markschemes(MS_PDF, ms_labels, IMG_DIR / "ms")

    data = json.loads(DB_PATH.read_text(encoding="utf-8"))
    data["papers"] = [p for p in data["papers"] if p["id"] != PAPER_ID]
    data["questions"] = [q for q in data["questions"] if q.get("paper") != PAPER_ID]
    data["papers"].append(PAPER_META)

    total_marks = 0
    for q in QUESTIONS:
        qnum = q["qnum"]
        slug = qnum.replace(".", "-")
        ms_key = MS_QNUM_MAP.get(qnum, qnum)
        data["questions"].append(
            {
                "id": f"{PAPER_ID}-q{qnum}",
                "paper": PAPER_ID,
                "year": PAPER_META["year"],
                "series": PAPER_META["series"],
                "unit": PAPER_META["unit"],
                "level": PAPER_META["level"],
                "question": qnum,
                "questionNumber": qnum,
                "page": PAGE_MAP[qnum],
                "marks": q["marks"],
                "topics": [q["specRef"]],
                "skills": q.get("skills", []),
                "summary": q["stem"],
                "specRef": q["specRef"],
                "image": f"img/{PAPER_ID}/q{slug}.jpg",
                "markscheme": f"img/{PAPER_ID}/ms/{ms_map[ms_key]}",
                "figures": [f"img/{PAPER_ID}/{f}" for f in q.get("figures", [])],
            }
        )
        total_marks += q["marks"]

    DB_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Ingested {PAPER_ID}: {len(QUESTIONS)} questions, {total_marks} marks")


if __name__ == "__main__":
    main()
