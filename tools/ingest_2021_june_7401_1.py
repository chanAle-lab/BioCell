"""Ingest AQA AS Biology June 2021 Paper 1 (7401/1) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598140467_34efd9c8.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598140311_ad86f039.pdf"
)

PAPER_ID = "2021-june-7401-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2021,
    "series": "June",
    "unit": "7401/1",
    "level": "AS",
    "date": "2021-06-01",
    "title": "7401/1 — AS Paper 1 (June 2021)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 60, "y0": 124, "x1": 540, "y1": 340},
    {"filename": "fig-q2-fig2.jpg", "page": 4, "x0": 60, "y0": 90, "x1": 540, "y1": 286},
    {"filename": "fig-q3-fig3.jpg", "page": 6, "x0": 60, "y0": 108, "x1": 540, "y1": 268},
    {"filename": "fig-q4-fig4.jpg", "page": 8, "x0": 60, "y0": 120, "x1": 540, "y1": 340},
    {"filename": "fig-q5-fig5.jpg", "page": 10, "x0": 60, "y0": 476, "x1": 540, "y1": 604},
    {"filename": "fig-q5-table1.jpg", "page": 11, "x0": 60, "y0": 152, "x1": 540, "y1": 348},
    {"filename": "fig-q6-fig6.jpg", "page": 13, "x0": 60, "y0": 102, "x1": 540, "y1": 284},
    {"filename": "fig-q7-fig7.jpg", "page": 16, "x0": 60, "y0": 286, "x1": 540, "y1": 715},
    {"filename": "fig-q8-table2.jpg", "page": 20, "x0": 60, "y0": 230, "x1": 540, "y1": 366},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 3, "01.4": 3,
    "02.1": 4, "02.2": 4,
    "03.1": 6, "03.2": 6, "03.3": 7, "03.4": 7,
    "04.1": 8, "04.2": 9, "04.3": 9, "04.4": 9,
    "05.1": 10, "05.2": 10, "05.3": 10, "05.4": 11,
    "06.1": 12, "06.2": 13, "06.3": 14,
    "07.1": 17, "07.2": 17, "07.3": 18,
    "08.1": 20, "08.2": 21, "08.3": 21, "08.4": 22,
    "09.1": 24, "09.2": 24, "09.3": 25, "09.4": 25, "09.5": 25,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.1.5", "marks": 2, "skills": [], "stem": "Name the bonds between complementary base pairs and between adjacent nucleotides in DNA (Figure 1).", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.2", "specRef": "3.1.5", "marks": 2, "skills": ["maths"], "stem": "Use Figure 1 to calculate the length in nm of a gene containing 4.38 x 10^3 base pairs.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.3", "specRef": "3.4.2", "marks": 2, "skills": [], "stem": "Describe two differences between the structure of a tRNA molecule and an mRNA molecule."},
    {"qnum": "01.4", "specRef": "3.4.2", "marks": 2, "skills": [], "stem": "Describe and explain a difference between the structure of mRNA used in translation and pre-mRNA."},
    {"qnum": "02.1", "specRef": "3.2.4", "marks": 2, "skills": [], "stem": "Name structures A and B on the HIV virus diagram (Figure 2).", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.2", "specRef": "3.2.4", "marks": 4, "skills": [], "stem": "Describe how HIV is replicated."},
    {"qnum": "03.1", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Explain why it is not possible to determine the identity of structures X on Uronema marinum using an optical microscope (Figure 3).", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.2", "specRef": "3.2.1", "marks": 3, "skills": [], "stem": "Describe the role of one named organelle in digesting bacteria ingested by U. marinum."},
    {"qnum": "03.3", "specRef": "3.2.1", "marks": 2, "skills": ["maths"], "stem": "Calculate the actual length of the cell between Y and Z in Figure 3 at x900 magnification to 2 significant figures.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.4", "specRef": "3.3.1", "marks": 2, "skills": ["analysis"], "stem": "Use surface area to volume ratios to suggest why mitochondria are near the cell-surface membrane in large U. marinum cells."},
    {"qnum": "04.1", "specRef": "3.2.2", "marks": 2, "skills": ["analysis"], "stem": "Describe and explain the arrangement of genetic material during prophase in Figure 4.", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.2", "specRef": "3.2.2", "marks": 1, "skills": [], "stem": "Tick the diagram representing metaphase chromosomes in an insect cell with diploid number 4."},
    {"qnum": "04.3", "specRef": "3.4.1", "marks": 1, "skills": [], "stem": "Name the fixed position occupied by a gene on a DNA molecule."},
    {"qnum": "04.4", "specRef": "3.4.1", "marks": 3, "skills": [], "stem": "Describe how a gene codes for the production of a polypeptide (excluding transcription and translation)."},
    {"qnum": "05.1", "specRef": "3.1.2", "marks": 4, "skills": [], "stem": "Describe how the structure of glycogen is related to its function."},
    {"qnum": "05.2", "specRef": "3.3.3", "marks": 1, "skills": [], "stem": "Name the type of peptidase that hydrolyses the internal peptide bond G in Figure 5.", "figures": ["fig-q5-fig5.jpg"]},
    {"qnum": "05.3", "specRef": "3.1.4", "marks": 1, "skills": [], "stem": "Give the number of different R groups in the polypeptide shown in Figure 5.", "figures": ["fig-q5-fig5.jpg"]},
    {"qnum": "05.4", "specRef": "3.1.4", "marks": 2, "skills": ["maths"], "stem": "Use Table 1 to calculate the number of polypeptides 6 and 20 amino acids in length from a 101-amino-acid polypeptide.", "figures": ["fig-q5-table1.jpg"]},
    {"qnum": "06.1", "specRef": "3.3.4", "marks": 3, "skills": [], "stem": "Give the pathway a red blood cell takes from a kidney to the lungs."},
    {"qnum": "06.2", "specRef": "3.3.4", "marks": 2, "skills": ["analysis"], "stem": "Identify and explain the type of blood vessel labelled M in Figure 6.", "figures": ["fig-q6-fig6.jpg"]},
    {"qnum": "06.3", "specRef": "3.3.4", "marks": 4, "skills": [], "stem": "Explain how water from tissue fluid is returned to the circulatory system."},
    {"qnum": "07.1", "specRef": "3.4.6", "marks": 2, "skills": ["maths"], "stem": "Use Figure 7 to calculate the index of diversity (d) for insects captured in plot 1 to 2 significant figures.", "figures": ["fig-q7-fig7.jpg"]},
    {"qnum": "07.2", "specRef": "3.4.6", "marks": 1, "skills": ["analysis"], "stem": "Use Figure 7 to explain why the conclusion that mowing increased species richness is incorrect.", "figures": ["fig-q7-fig7.jpg"]},
    {"qnum": "07.3", "specRef": "3.4.7", "marks": 4, "skills": ["practical"], "stem": "Suggest how to use plot 1 data and meadow dimensions to estimate the total number of beetles in the meadow.", "figures": ["fig-q7-fig7.jpg"]},
    {"qnum": "08.1", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Suggest one improvement to the design of Table 2 and one improvement to data presentation.", "figures": ["fig-q8-table2.jpg"]},
    {"qnum": "08.2", "specRef": "3.2.3", "marks": 2, "skills": ["practical"], "stem": "Suggest and explain an advantage of carrying out the egg osmosis investigation at 30 C rather than 20 C."},
    {"qnum": "08.3", "specRef": "3.2.3", "marks": 3, "skills": ["analysis"], "stem": "Evaluate the conclusion from Table 2 that water potential inside the egg is higher than that of vinegar.", "figures": ["fig-q8-table2.jpg"]},
    {"qnum": "08.4", "specRef": "RP", "marks": 4, "skills": ["practical"], "stem": "Advise how to use final-to-initial mass ratios across a sugar dilution series to determine egg water potential."},
    {"qnum": "09.1", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Identify two organelles in kidney cells that enable the production of the glycoprotein EPO."},
    {"qnum": "09.2", "specRef": "3.3.4", "marks": 2, "skills": ["analysis"], "stem": "Explain the biological advantage to athletes of injecting synthetic EPO."},
    {"qnum": "09.3", "specRef": "3.2.4", "marks": 3, "skills": [], "stem": "Describe how mice injected with human EPO produce anti-human EPO antibody."},
    {"qnum": "09.4", "specRef": "3.2.4", "marks": 3, "skills": [], "stem": "Describe the roles of anti-human EPO antibody and enzyme-linked anti-mouse antibody in an ELISA test."},
    {"qnum": "09.5", "specRef": "3.2.4", "marks": 1, "skills": ["analysis"], "stem": "Use the passage to suggest why some people object to using monoclonal antibodies in testing programmes."},
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
