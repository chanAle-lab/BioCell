"""Ingest AQA AS Biology June 2022 Paper 1 (7401/1) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598162477_5cf89280.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598162445_1ad5f597.pdf"
)

PAPER_ID = "2022-june-7401-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2022,
    "series": "June",
    "unit": "7401/1",
    "level": "AS",
    "date": "2022-06-01",
    "title": "7401/1 — AS Paper 1 (June 2022)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 60, "y0": 124, "x1": 540, "y1": 668},
    {"filename": "fig-q1-table1.jpg", "page": 3, "x0": 60, "y0": 64, "x1": 540, "y1": 304},
    {"filename": "fig-q3-fig2.jpg", "page": 5, "x0": 60, "y0": 88, "x1": 540, "y1": 278},
    {"filename": "fig-q4-fig3.jpg", "page": 7, "x0": 60, "y0": 152, "x1": 540, "y1": 382},
    {"filename": "fig-q4-fig4.jpg", "page": 8, "x0": 60, "y0": 88, "x1": 540, "y1": 452},
    {"filename": "fig-q5-fig5.jpg", "page": 10, "x0": 60, "y0": 400, "x1": 540, "y1": 540},
    {"filename": "fig-q5-table3.jpg", "page": 11, "x0": 60, "y0": 336, "x1": 540, "y1": 462},
    {"filename": "fig-q6-fig7.jpg", "page": 13, "x0": 60, "y0": 296, "x1": 540, "y1": 478},
    {"filename": "fig-q7-fig8-table4.jpg", "page": 16, "x0": 60, "y0": 304, "x1": 540, "y1": 576},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 3,
    "02.1": 4, "02.2": 4,
    "03.1": 5, "03.2": 5, "03.3": 5, "03.4": 6, "03.5": 6, "03.6": 6,
    "04.1": 7, "04.2": 8, "04.3": 9,
    "05.1": 10, "05.2": 10, "05.3": 11, "05.4": 11, "05.5": 12,
    "06.1": 13, "06.2": 13, "06.3": 14,
    "07.1": 15, "07.2": 15, "07.3": 17,
    "08.1": 18, "08.2": 18, "08.3": 19,
    "09.1": 20, "09.2": 21, "09.3": 21, "09.4": 22, "09.5": 22,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.1.1", "marks": 4, "skills": [], "stem": "Complete Table 1 matching biological molecules A to E in Figure 1 to each statement.", "figures": ["fig-q1-fig1.jpg", "fig-q1-table1.jpg"]},
    {"qnum": "01.2", "specRef": "3.3.3", "marks": 4, "skills": [], "stem": "Describe the mechanism for the absorption of amino acids in the ileum."},
    {"qnum": "02.1", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Give the two types of molecule from which a ribosome is made."},
    {"qnum": "02.2", "specRef": "3.1.5", "marks": 4, "skills": [], "stem": "Complete Table 2 to give four structural differences between a DNA molecule and an mRNA molecule."},
    {"qnum": "03.1", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Name the bacterial structure labelled X in the scanning electron micrograph (Figure 2).", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "03.2", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Describe and explain one difference between an SEM image (Figure 2) and a TEM image of this bacterium.", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "03.3", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Explain why the resolution of an electron microscope is higher than that of an optical microscope."},
    {"qnum": "03.4", "specRef": "3.2.1", "marks": 2, "skills": ["practical"], "stem": "Describe how a student determined the actual size in micrometres of a cell structure from a microscope photograph."},
    {"qnum": "03.5", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Name two structures found in all bacteria that are not found in plant cells."},
    {"qnum": "03.6", "specRef": "3.2.4", "marks": 2, "skills": [], "stem": "Name two features of HIV particles (excluding attachment protein) that are not found in bacteria."},
    {"qnum": "04.1", "specRef": "3.3.1", "marks": 4, "skills": ["analysis"], "stem": "Use Figure 3 to conclude about oxygen uptake over the entire body of the lugworm.", "figures": ["fig-q4-fig3.jpg"]},
    {"qnum": "04.2", "specRef": "3.3.4", "marks": 3, "skills": ["maths"], "stem": "Use Figure 4 and the CdO2 equation to calculate the volume of dissolved oxygen in 0.2 cm3 of lugworm blood at 92% saturation.", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.3", "specRef": "3.3.4", "marks": 2, "skills": ["practical"], "stem": "Describe how to use a colorimeter and calibration curve to determine the pO2 in a sample of lugworm blood."},
    {"qnum": "05.1", "specRef": "3.1.4", "marks": 3, "skills": [], "stem": "Describe how monomers join to form the primary structure of a protein."},
    {"qnum": "05.2", "specRef": "3.1.4", "marks": 2, "skills": [], "stem": "Describe one similarity and one difference between the induced-fit model and lock-and-key model (Figure 5).", "figures": ["fig-q5-fig5.jpg"]},
    {"qnum": "05.3", "specRef": "3.1.4", "marks": 1, "skills": [], "stem": "State how enzymes help reactions to proceed quickly at lower temperatures."},
    {"qnum": "05.4", "specRef": "3.1.4", "marks": 2, "skills": ["maths"], "stem": "Complete Table 3 by calculating the time taken for complete hydrolysis of maltose in solution H.", "figures": ["fig-q5-table3.jpg"]},
    {"qnum": "05.5", "specRef": "3.1.4", "marks": 1, "skills": ["analysis"], "stem": "Tick the box for the independent variable changed to produce curve I in Figure 6."},
    {"qnum": "06.1", "specRef": "3.1.8", "marks": 2, "skills": [], "stem": "Explain a property of iron ions that enables them to carry out their role in red blood cells."},
    {"qnum": "06.2", "specRef": "3.2.3", "marks": 3, "skills": ["analysis"], "stem": "Use Figure 7 to explain why plasma iron ion concentration is higher in people with haemochromatosis.", "figures": ["fig-q6-fig7.jpg"]},
    {"qnum": "06.3", "specRef": "3.1.8", "marks": 2, "skills": ["maths"], "stem": "Calculate the ratio of plasma iron ion mass in a haemochromatosis patient to a healthy person."},
    {"qnum": "07.1", "specRef": "3.2.2", "marks": 2, "skills": [], "stem": "Define what a tumour is."},
    {"qnum": "07.2", "specRef": "RP", "marks": 3, "skills": ["practical"], "stem": "Describe how to determine a reliable mitotic index (MI) from tissue observed with an optical microscope."},
    {"qnum": "07.3", "specRef": "3.2.2", "marks": 4, "skills": ["analysis"], "stem": "Use Figure 8 and Table 4 to evaluate the conclusion that MI > 5 is a reliable indicator of cancer severity in dogs.", "figures": ["fig-q7-fig8-table4.jpg"]},
    {"qnum": "08.1", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Explain why E. coli cell density might be lower after 24 hours if a non-sterilised pipette was used."},
    {"qnum": "08.2", "specRef": "3.2.1", "marks": 2, "skills": ["maths"], "stem": "Calculate the number of E. coli cells per mm3 in undiluted culture 1 from dilution and haemocytometer counts."},
    {"qnum": "08.3", "specRef": "3.2.2", "marks": 3, "skills": ["maths"], "stem": "Sketch a bar chart on Figure 9 comparing E. coli cell density in cultures 1, 2 (J), and 3 (K)."},
    {"qnum": "09.1", "specRef": "3.3.4", "marks": 2, "skills": ["analysis"], "stem": "Describe and explain how blood composition in a fetal pulmonary artery differs from its mother's pulmonary artery."},
    {"qnum": "09.2", "specRef": "3.2.4", "marks": 3, "skills": ["analysis"], "stem": "Explain how a fetus is protected against pathogens infecting its mother during pregnancy via IgG transfer."},
    {"qnum": "09.3", "specRef": "3.2.4", "marks": 2, "skills": ["analysis"], "stem": "Suggest how vaccinating babies protects the UK population against measles viruses and tetanus bacteria."},
    {"qnum": "09.4", "specRef": "3.2.4", "marks": 1, "skills": ["analysis"], "stem": "Suggest why there has been a recent increase in the number of children catching measles."},
    {"qnum": "09.5", "specRef": "3.2.4", "marks": 2, "skills": ["analysis"], "stem": "Explain why giving children more than one tetanus vaccination develops good immunity."},
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
