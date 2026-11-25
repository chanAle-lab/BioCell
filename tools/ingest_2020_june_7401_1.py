"""Ingest AQA AS Biology June 2020 Paper 1 (7401/1) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598113005_33b1bd58.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598113150_b654690f.pdf"
)

PAPER_ID = "2020-june-7401-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2020,
    "series": "June",
    "unit": "7401/1",
    "level": "AS",
    "date": "2020-05-19",
    "title": "7401/1 — AS Paper 1 (June 2020)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 60, "y0": 124, "x1": 540, "y1": 388},
    {"filename": "fig-q3-fig2.jpg", "page": 6, "x0": 60, "y0": 88, "x1": 540, "y1": 262},
    {"filename": "fig-q4-fig3.jpg", "page": 8, "x0": 60, "y0": 86, "x1": 540, "y1": 396},
    {"filename": "fig-q6-table3.jpg", "page": 14, "x0": 60, "y0": 84, "x1": 540, "y1": 182},
    {"filename": "fig-q7-fig7.jpg", "page": 16, "x0": 60, "y0": 116, "x1": 540, "y1": 472},
    {"filename": "fig-q8-table4.jpg", "page": 18, "x0": 60, "y0": 138, "x1": 540, "y1": 420},
    {"filename": "fig-q8-fig9.jpg", "page": 20, "x0": 60, "y0": 108, "x1": 540, "y1": 512},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 3, "01.3": 3,
    "02.1": 4, "02.2": 4, "02.3": 4,
    "03.1": 5, "03.2": 5, "03.3": 6, "03.4": 6,
    "04.1": 7, "04.2": 8, "04.3": 8, "04.4": 8, "04.5": 9,
    "05.1": 10, "05.2": 11, "05.3": 11, "05.4": 12,
    "06.1": 13, "06.2": 13, "06.3": 14, "06.4": 14,
    "07.1": 15, "07.2": 16, "07.3": 17, "07.4": 17,
    "08.1": 19, "08.2": 19, "08.3": 20,
    "09.1": 22, "09.2": 22, "09.3": 23, "09.4": 23,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.1.1", "marks": 4, "skills": [], "stem": "Complete Table 1 matching biological molecules A, B, C, or D in Figure 1 to each statement.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.2", "specRef": "3.1.2", "marks": 1, "skills": ["maths"], "stem": "Give the number of carbon, hydrogen, and oxygen atoms in a molecule of the trisaccharide raffinose."},
    {"qnum": "01.3", "specRef": "3.1.2", "marks": 3, "skills": ["practical"], "stem": "Describe a biochemical test to show that raffinose solution contains a non-reducing sugar."},
    {"qnum": "02.1", "specRef": "3.2.3", "marks": 2, "skills": [], "stem": "Explain the arrangement of phospholipids in a cell-surface membrane."},
    {"qnum": "02.2", "specRef": "3.1.3", "marks": 2, "skills": [], "stem": "Describe how an ester bond is formed in a phospholipid molecule."},
    {"qnum": "02.3", "specRef": "3.1.7", "marks": 2, "skills": [], "stem": "State and explain the property of water that helps prevent temperature increase in a cell."},
    {"qnum": "03.1", "specRef": "3.2.4", "marks": 3, "skills": [], "stem": "Describe how a phagocyte destroys a pathogen present in the blood."},
    {"qnum": "03.2", "specRef": "3.2.4", "marks": 2, "skills": [], "stem": "Give two types of cell, other than pathogens, that can stimulate an immune response."},
    {"qnum": "03.3", "specRef": "3.2.4", "marks": 1, "skills": [], "stem": "Label Figure 2 with an X to show where an antigen-antibody complex forms.", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "03.4", "specRef": "3.1.4", "marks": 1, "skills": [], "stem": "State the role of the disulfide bridge in forming the quaternary structure of an antibody.", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "04.1", "specRef": "3.2.1", "marks": 4, "skills": [], "stem": "Outline the role of organelles in the production, transport, and release of proteins from eukaryotic cells."},
    {"qnum": "04.2", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Suggest why a nucleus is not visible in the plant cell TEM (Figure 3).", "figures": ["fig-q4-fig3.jpg"]},
    {"qnum": "04.3", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Name the organelles labelled S and T in Figure 3.", "figures": ["fig-q4-fig3.jpg"]},
    {"qnum": "04.4", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Give one advantage of viewing a biological specimen using a TEM compared with an SEM."},
    {"qnum": "04.5", "specRef": "3.2.1", "marks": 2, "skills": ["maths"], "stem": "Calculate the number of cells in the upper surface of the leaf in standard form using Figure 4."},
    {"qnum": "05.1", "specRef": "3.3.2", "marks": 3, "skills": [], "stem": "Describe and explain the mechanism that causes lungs to fill with air."},
    {"qnum": "05.2", "specRef": "3.3.2", "marks": 1, "skills": [], "stem": "Identify the air-filled tube K and blood vessel L in a section of lung tissue."},
    {"qnum": "05.3", "specRef": "3.2.1", "marks": 2, "skills": ["practical"], "stem": "Suggest why haematoxylin solution rather than iodine solution was used to stain lung tissue."},
    {"qnum": "05.4", "specRef": "3.3.2", "marks": 3, "skills": ["analysis"], "stem": "Evaluate the student's conclusion from Table 2 P-values that all three risk factors are linked with asthma."},
    {"qnum": "06.1", "specRef": "3.4.2", "marks": 3, "skills": [], "stem": "Describe how mRNA is produced from an exposed template strand of DNA."},
    {"qnum": "06.2", "specRef": "3.4.1", "marks": 1, "skills": [], "stem": "Define the term exon."},
    {"qnum": "06.3", "specRef": "3.4.2", "marks": 1, "skills": [], "stem": "Use Table 3 and the DNA template sequence in Figure 6 to give the four-amino-acid sequence.", "figures": ["fig-q6-table3.jpg"]},
    {"qnum": "06.4", "specRef": "3.4.3", "marks": 2, "skills": ["analysis"], "stem": "Explain whether Table 3 and Figure 6 support the conclusion that the mutation involved adding one nucleotide.", "figures": ["fig-q6-table3.jpg"]},
    {"qnum": "07.1", "specRef": "3.2.2", "marks": 3, "skills": [], "stem": "Describe binary fission in bacteria."},
    {"qnum": "07.2", "specRef": "3.2.1", "marks": 1, "skills": ["maths"], "stem": "Tick the box equal to 680 femtograms (fg) in grams."},
    {"qnum": "07.3", "specRef": "3.2.2", "marks": 2, "skills": ["maths"], "stem": "Use Figure 7 and a 90 fg mass increase over 5 minutes to determine the B. subtilis cell mass after binary fission.", "figures": ["fig-q7-fig7.jpg"]},
    {"qnum": "07.4", "specRef": "3.2.2", "marks": 4, "skills": ["analysis"], "stem": "Suggest and explain how two environmental variables could be changed to increase bacterial cell growth rate."},
    {"qnum": "08.1", "specRef": "3.4.4", "marks": 4, "skills": ["maths"], "stem": "Draw a suitable histogram on Figure 8 to show the distribution of baby birth mass from Table 4.", "figures": ["fig-q8-table4.jpg"]},
    {"qnum": "08.2", "specRef": "3.4.4", "marks": 2, "skills": ["maths"], "stem": "Use Table 4 to calculate the number of babies born with low birth mass (< 2.5 kg).", "figures": ["fig-q8-table4.jpg"]},
    {"qnum": "08.3", "specRef": "3.4.4", "marks": 3, "skills": ["analysis"], "stem": "State three conclusions from Figure 9 on birth mass, smoking during pregnancy, and infant survival.", "figures": ["fig-q8-fig9.jpg"]},
    {"qnum": "09.1", "specRef": "3.4.1", "marks": 2, "skills": ["analysis"], "stem": "Explain how the proteome of a genetically modified tobacco plant cell differs from an unmodified control."},
    {"qnum": "09.2", "specRef": "3.2.3", "marks": 2, "skills": ["analysis"], "stem": "Explain how increased transcription of the PIP1b aquaporin gene affects membrane permeability to water."},
    {"qnum": "09.3", "specRef": "3.3.2", "marks": 4, "skills": ["analysis"], "stem": "Suggest and explain one advantage and one disadvantage of increased stomatal density on tobacco leaf growth."},
    {"qnum": "09.4", "specRef": "3.2.3", "marks": 2, "skills": ["maths"], "stem": "Calculate how much greater the K+ to water movement ratio is across a vacuole membrane than a cell-surface membrane."},
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
