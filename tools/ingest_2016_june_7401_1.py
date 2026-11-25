"""Ingest AQA AS Biology June 2016 Paper 1 (7401/1) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795595891833_d3501bca.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795595891767_5dbefe3c.pdf"
)

PAPER_ID = "2016-june-7401-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "June",
    "unit": "7401/1",
    "level": "AS",
    "date": "2016-05-26",
    "title": "7401/1 — AS Paper 1 (June 2016)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q2-fig1.jpg", "page": 5, "x0": 60, "y0": 62, "x1": 540, "y1": 240},
    {"filename": "fig-q3-fig2.jpg", "page": 6, "x0": 60, "y0": 455, "x1": 540, "y1": 645},
    {"filename": "fig-q4-fig3.jpg", "page": 8, "x0": 60, "y0": 438, "x1": 540, "y1": 745},
    {"filename": "fig-q5-table2.jpg", "page": 10, "x0": 60, "y0": 260, "x1": 540, "y1": 545},
    {"filename": "fig-q6-fig4.jpg", "page": 12, "x0": 60, "y0": 305, "x1": 540, "y1": 585},
    {"filename": "fig-q7-fig5.jpg", "page": 15, "x0": 60, "y0": 215, "x1": 540, "y1": 505},
    {"filename": "fig-q8-fig6.jpg", "page": 17, "x0": 60, "y0": 330, "x1": 540, "y1": 570},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 3,
    "02.1": 4, "02.2": 4, "02.3": 4, "02.4": 5, "02.5": 5,
    "03.1": 6, "03.2": 6, "03.3": 6, "03.4": 7, "03.5": 7,
    "04.1": 8, "04.2": 9, "04.3": 9, "04.4": 9,
    "05.1": 10, "05.2": 10, "05.3": 11,
    "06.1": 12, "06.2": 12, "06.3": 13, "06.4": 13,
    "07.1": 14, "07.2": 15, "07.3": 16, "07.4": 16,
    "08.1": 17, "08.2": 17, "08.3": 18, "08.4": 19,
    "09.1": 20, "09.2": 20, "09.3": 21, "09.4": 21, "09.5": 21,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.2.1", "marks": 2, "skills": ["analysis"], "stem": "Complete Table 1 comparing features of a bacterium and an HIV particle."},
    {"qnum": "01.2", "specRef": "3.1.5", "marks": 3, "skills": [], "stem": "Describe how the complementary strand of HIV DNA is made during semi-conservative replication."},
    {"qnum": "01.3", "specRef": "3.1.5", "marks": 3, "skills": [], "stem": "Contrast the structures of DNA and mRNA molecules to give three differences."},
    {"qnum": "02.1", "specRef": "3.1.3", "marks": 1, "skills": [], "stem": "Describe the difference between the structure of a triglyceride and a phospholipid."},
    {"qnum": "02.2", "specRef": "3.1.3", "marks": 2, "skills": ["practical"], "stem": "Describe how you would test for the presence of a lipid in a sample of food."},
    {"qnum": "02.3", "specRef": "3.1.3", "marks": 1, "skills": [], "stem": "Describe how a saturated fatty acid is different from an unsaturated fatty acid."},
    {"qnum": "02.4", "specRef": "3.1.4", "marks": 2, "skills": ["analysis"], "stem": "Suggest why the fat substitute shown in Figure 1 cannot be digested in the gut by lipase.", "figures": ["fig-q2-fig1.jpg"]},
    {"qnum": "02.5", "specRef": "3.2.3", "marks": 1, "skills": ["analysis"], "stem": "Suggest why the fat substitute cannot cross cell-surface membranes."},
    {"qnum": "03.1", "specRef": "3.1.6", "marks": 2, "skills": [], "stem": "Describe how ATP is resynthesised in cells."},
    {"qnum": "03.2", "specRef": "3.1.6", "marks": 2, "skills": [], "stem": "Give two ways in which the hydrolysis of ATP is used in cells."},
    {"qnum": "03.3", "specRef": "3.2.1", "marks": 1, "skills": ["practical"], "stem": "Give the evidence from Figure 2 that a scanning electron microscope was used.", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "03.4", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Name the part of the mitochondrion labelled X in Figure 2.", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "03.5", "specRef": "3.2.1", "marks": 2, "skills": ["maths"], "stem": "Calculate the magnification of the mitochondrion between points A and B in Figure 2.", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "04.1", "specRef": "3.2.3", "marks": 3, "skills": [], "stem": "Match examples of membrane transport to diffusion, facilitated diffusion, active transport, co-transport, or osmosis."},
    {"qnum": "04.2", "specRef": "3.1.4", "marks": 2, "skills": ["analysis"], "stem": "Using Figure 3, describe the other function of membrane protein Y besides transport.", "figures": ["fig-q4-fig3.jpg"]},
    {"qnum": "04.3", "specRef": "3.2.1", "marks": 1, "skills": ["analysis"], "stem": "Give evidence in Figure 3 that the phospholipid bilayer shown is part of the cell-surface membrane.", "figures": ["fig-q4-fig3.jpg"]},
    {"qnum": "04.4", "specRef": "3.1.2", "marks": 1, "skills": [], "stem": "Identify the type of bond that holds cellulose molecules together side by side in the cell wall."},
    {"qnum": "05.1", "specRef": "3.1.2", "marks": 2, "skills": [], "stem": "Name the two products of the hydrolysis of sucrose."},
    {"qnum": "05.2", "specRef": "3.1.4", "marks": 3, "skills": ["maths", "practical"], "stem": "Calculate the rate per minute of sucrose hydrolysis by SPS in standard form and plot a graph.", "figures": ["fig-q5-table2.jpg"]},
    {"qnum": "05.3", "specRef": "3.2.2", "marks": 3, "skills": ["analysis"], "stem": "State and explain what can be concluded about the growth of the plant cells from Table 2.", "figures": ["fig-q5-table2.jpg"]},
    {"qnum": "06.1", "specRef": "3.1.4", "marks": 2, "skills": [], "stem": "Describe the induced-fit model of enzyme action."},
    {"qnum": "06.2", "specRef": "3.1.4", "marks": 2, "skills": ["maths"], "stem": "Determine the rate of starch hydrolysis at 10 minutes from Figure 4.", "figures": ["fig-q6-fig4.jpg"]},
    {"qnum": "06.3", "specRef": "3.1.4", "marks": 2, "skills": ["analysis"], "stem": "Explain the shape of the maltose concentration curve shown in Figure 4.", "figures": ["fig-q6-fig4.jpg"]},
    {"qnum": "06.4", "specRef": "3.1.2", "marks": 3, "skills": ["practical"], "stem": "Describe how to produce and use a colorimeter calibration curve for quantitative Benedict's tests.", "figures": ["fig-q6-fig4.jpg"]},
    {"qnum": "07.1", "specRef": "3.2.4", "marks": 4, "skills": [], "stem": "Describe how giving the HPV vaccine leads to production of antibody against HPV."},
    {"qnum": "07.2", "specRef": "3.2.4", "marks": 2, "skills": ["analysis"], "stem": "Use Figure 5 to evaluate whether two or three doses of the HPV vaccine is better.", "figures": ["fig-q7-fig5.jpg"]},
    {"qnum": "07.3", "specRef": "3.4.7", "marks": 1, "skills": ["maths"], "stem": "State and justify the statistical test to compare mean antibody concentrations at 9 months."},
    {"qnum": "07.4", "specRef": "3.4.7", "marks": 2, "skills": [], "stem": "Give two ways doctors could use base sequences to compare different types of HPV."},
    {"qnum": "08.1", "specRef": "3.2.2", "marks": 1, "skills": [], "stem": "Identify the stage of mitosis when chromosomes line up on the equator of the mitotic spindle."},
    {"qnum": "08.2", "specRef": "3.2.2", "marks": 2, "skills": ["analysis"], "stem": "Suggest why a monopolar mitotic spindle (Figure 6) would prevent successful mitosis.", "figures": ["fig-q8-fig6.jpg"]},
    {"qnum": "08.3", "specRef": "3.2.2", "marks": 4, "skills": ["analysis"], "stem": "Evaluate whether Table 3 supports using 100 nmol dm-3 kinesin inhibitor in human trials."},
    {"qnum": "08.4", "specRef": "RP", "marks": 2, "skills": ["practical", "maths"], "stem": "Describe how to make 100 cm3 of 1000 nmol dm-3 kinesin inhibitor from a 10 000 nmol dm-3 stock."},
    {"qnum": "09.1", "specRef": "3.1.4", "marks": 2, "skills": ["analysis"], "stem": "Suggest how amyloid-precursor protein can be the substrate of both alpha-secretase and beta-secretase."},
    {"qnum": "09.2", "specRef": "3.1.4", "marks": 2, "skills": [], "stem": "Describe what happens in the hydrolysis reaction that produces the smaller protein from APP."},
    {"qnum": "09.3", "specRef": "3.4.3", "marks": 3, "skills": ["analysis"], "stem": "Explain how mutations decreasing alpha-secretase or increasing beta-secretase can lead to Alzheimer's disease."},
    {"qnum": "09.4", "specRef": "3.1.4", "marks": 2, "skills": ["analysis"], "stem": "Explain how a competitive inhibitor of beta-secretase could prevent Alzheimer's disease worsening."},
    {"qnum": "09.5", "specRef": "3.1.4", "marks": 1, "skills": ["analysis"], "stem": "Suggest why some patients developed serious side effects during beta-secretase inhibitor trials."},
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
