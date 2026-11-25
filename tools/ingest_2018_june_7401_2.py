"""Ingest AQA AS Biology June 2018 Paper 2 (7401/2) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795597620145_9e2b44f7.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795597621014_f1abfd5b.pdf"
)

PAPER_ID = "2018-june-7401-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2018,
    "series": "June",
    "unit": "7401/2",
    "level": "AS",
    "date": "2018-06-04",
    "title": "7401/2 — AS Paper 2 (June 2018)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q3-table2.jpg", "page": 7, "x0": 60, "y0": 100, "x1": 540, "y1": 280},
    {"filename": "fig-q4-fig1.jpg", "page": 10, "x0": 60, "y0": 125, "x1": 540, "y1": 450},
    {"filename": "fig-q5-fig2.jpg", "page": 14, "x0": 60, "y0": 98, "x1": 540, "y1": 430},
    {"filename": "fig-q5-fig3.jpg", "page": 16, "x0": 60, "y0": 150, "x1": 540, "y1": 345},
    {"filename": "fig-q6-fig4-t3.jpg", "page": 18, "x0": 55, "y0": 165, "x1": 545, "y1": 775},
    {"filename": "fig-q7-table4.jpg", "page": 22, "x0": 60, "y0": 178, "x1": 540, "y1": 335},
    {"filename": "fig-q8-table5.jpg", "page": 26, "x0": 60, "y0": 140, "x1": 540, "y1": 295},
]

PAGE_MAP = {
    "01.1": 3, "01.2": 3,
    "02.1": 4, "02.2": 4, "02.3": 5,
    "03.1": 6, "03.2": 6, "03.3": 7, "03.4": 7, "03.5": 8, "03.6": 8,
    "04.1": 9, "04.2": 11, "04.3": 11,
    "05.1": 13, "05.2": 14, "05.3": 15, "05.4": 15, "05.5": 16,
    "06.1": 19, "06.2": 19, "06.3": 20,
    "07.1": 21, "07.2": 21, "07.3": 22, "07.4": 23, "07.5": 23,
    "08.1": 24, "08.2": 25, "08.3": 25, "08.4": 26, "08.5": 27,
    "09.1": 28, "09.2": 29,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.2.1", "marks": 3, "skills": [], "stem": "Complete Table 1 matching plant cell structures to their descriptions."},
    {"qnum": "01.2", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Explain the role of many mitochondria and Golgi vesicles in breast milk production and secretion."},
    {"qnum": "02.1", "specRef": "3.1.4", "marks": 2, "skills": [], "stem": "Describe how a peptide bond is formed between two amino acids to form a dipeptide."},
    {"qnum": "02.2", "specRef": "3.1.4", "marks": 2, "skills": [], "stem": "Describe how the secondary structure of a polypeptide is produced."},
    {"qnum": "02.3", "specRef": "3.1.4", "marks": 2, "skills": [], "stem": "Explain why two proteins with the same number and type of amino acids can have different tertiary structures."},
    {"qnum": "03.1", "specRef": "3.3.1", "marks": 1, "skills": [], "stem": "Describe the relationship between organism size and surface area to volume ratio."},
    {"qnum": "03.2", "specRef": "3.3.1", "marks": 2, "skills": ["maths"], "stem": "Calculate the mean diameter of a spherical frog egg with surface area 9.73 mm2."},
    {"qnum": "03.3", "specRef": "3.3.1", "marks": 1, "skills": ["analysis"], "stem": "Suggest why the scientist used µmol g-1 h-1 for the rate of oxygen uptake."},
    {"qnum": "03.4", "specRef": "3.3.1", "marks": 1, "skills": ["practical"], "stem": "Suggest one practical advantage of measuring mass rather than volume of frog eggs, tadpoles, and adults."},
    {"qnum": "03.5", "specRef": "3.3.1", "marks": 1, "skills": [], "stem": "Explain why oxygen uptake is a measure of metabolic rate."},
    {"qnum": "03.6", "specRef": "3.4.7", "marks": 3, "skills": ["analysis"], "stem": "Use Table 2 to explain why a conclusion cannot be made about development stage and metabolic rate.", "figures": ["fig-q3-table2.jpg"]},
    {"qnum": "04.1", "specRef": "3.2.3", "marks": 2, "skills": [], "stem": "Give two similarities in the movement of substances by diffusion and osmosis."},
    {"qnum": "04.2", "specRef": "3.2.3", "marks": 3, "skills": ["analysis"], "stem": "Explain the shape of the monosaccharide uptake curve in Figure 1 between A–B and C–D.", "figures": ["fig-q4-fig1.jpg"]},
    {"qnum": "04.3", "specRef": "3.2.3", "marks": 2, "skills": ["analysis"], "stem": "Suggest how Figure 1 provides evidence that monoglycerides are lipid-soluble.", "figures": ["fig-q4-fig1.jpg"]},
    {"qnum": "05.1", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Explain why only the first 5 mm of onion root tip is used and why the cover slip is pressed firmly."},
    {"qnum": "05.2", "specRef": "RP", "marks": 2, "skills": ["maths", "practical"], "stem": "Use Figure 2 to calculate anaphase duration and percentage difference from the scientists' mean.", "figures": ["fig-q5-fig2.jpg"]},
    {"qnum": "05.3", "specRef": "3.2.2", "marks": 1, "skills": [], "stem": "Identify the name given to division of the cytoplasm during the cell cycle."},
    {"qnum": "05.4", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Describe and explain what the student should do when counting cells to ensure an accurate mitotic index."},
    {"qnum": "05.5", "specRef": "3.2.2", "marks": 3, "skills": ["analysis"], "stem": "Use Figure 3 to suggest how the chemical stops the growth of roots.", "figures": ["fig-q5-fig3.jpg"]},
    {"qnum": "06.1", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Explain how the measurement from control treatment D is used by the scientist."},
    {"qnum": "06.2", "specRef": "3.3.4", "marks": 3, "skills": ["analysis"], "stem": "Conclude from treatments D and E in Figure 4 and Table 3 about root growth.", "figures": ["fig-q6-fig4-t3.jpg"]},
    {"qnum": "06.3", "specRef": "3.3.4", "marks": 4, "skills": ["analysis"], "stem": "Evaluate whether Figure 4 and Table 3 support the mass flow hypothesis for phloem transport.", "figures": ["fig-q6-fig4-t3.jpg"]},
    {"qnum": "07.1", "specRef": "3.3.3", "marks": 2, "skills": [], "stem": "Define digestion."},
    {"qnum": "07.2", "specRef": "3.1.4", "marks": 2, "skills": [], "stem": "Suggest why endocellulases and exocellulases act at different places on cellulose molecules."},
    {"qnum": "07.3", "specRef": "3.1.4", "marks": 2, "skills": ["maths"], "stem": "Use Table 4 to calculate the rate of cellulose digestion in g min-1 in standard form when both enzymes are present.", "figures": ["fig-q7-table4.jpg"]},
    {"qnum": "07.4", "specRef": "3.3.3", "marks": 2, "skills": ["analysis"], "stem": "Suggest why the rate of cellulose digestion is greatest when both endocellulase and exocellulase are present."},
    {"qnum": "07.5", "specRef": "3.1.4", "marks": 1, "skills": ["maths"], "stem": "Write the equation for calculating percentage loss in mass of cellulose."},
    {"qnum": "08.1", "specRef": "RP", "marks": 3, "skills": ["practical"], "stem": "Describe how to make a 1 in 10 dilution and use it to make a 1 in 1000 dilution of a bacterial culture."},
    {"qnum": "08.2", "specRef": "RP", "marks": 2, "skills": ["maths", "practical"], "stem": "Calculate the number of cells in 1 cm3 of undiluted culture from 15 cells in 0.004 mm3 of a 1 in 1000 dilution."},
    {"qnum": "08.3", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Suggest why the student decided not to use the 1 in 10 dilution to count cells."},
    {"qnum": "08.4", "specRef": "3.4.4", "marks": 2, "skills": ["analysis"], "stem": "Use Table 5 to suggest and explain why tetracycline-resistant bacteria are more common than streptomycin-resistant bacteria.", "figures": ["fig-q8-table5.jpg"]},
    {"qnum": "08.5", "specRef": "3.4.4", "marks": 1, "skills": ["analysis"], "stem": "Suggest why the percentage of tetracycline-resistant bacteria remained constant after stopping tetracycline."},
    {"qnum": "09.1", "specRef": "3.4.1", "marks": 5, "skills": ["extended"], "stem": "Compare and contrast the DNA in eukaryotic cells with the DNA in prokaryotic cells."},
    {"qnum": "09.2", "specRef": "3.4.5", "marks": 5, "skills": ["extended"], "stem": "Explain how differences in haemoglobin primary structure provide evidence of phylogenetic relationships."},
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
