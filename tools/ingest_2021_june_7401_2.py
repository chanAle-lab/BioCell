"""Ingest AQA AS Biology June 2021 Paper 2 (7401/2) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598140607_3ab4e22c.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598140367_69f8eab9.pdf"
)

PAPER_ID = "2021-june-7401-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2021,
    "series": "June",
    "unit": "7401/2",
    "level": "AS",
    "date": "2021-06-01",
    "title": "7401/2 — AS Paper 2 (June 2021)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 60, "y0": 228, "x1": 540, "y1": 334},
    {"filename": "fig-q1-fig2.jpg", "page": 3, "x0": 60, "y0": 88, "x1": 540, "y1": 328},
    {"filename": "fig-q2-fig3.jpg", "page": 5, "x0": 60, "y0": 208, "x1": 540, "y1": 514},
    {"filename": "fig-q3-fig4.jpg", "page": 8, "x0": 60, "y0": 360, "x1": 540, "y1": 636},
    {"filename": "fig-q3-fig5.jpg", "page": 9, "x0": 60, "y0": 124, "x1": 540, "y1": 218},
    {"filename": "fig-q4-fig6.jpg", "page": 12, "x0": 60, "y0": 216, "x1": 540, "y1": 462},
    {"filename": "fig-q5-fig7.jpg", "page": 14, "x0": 60, "y0": 196, "x1": 540, "y1": 424},
    {"filename": "fig-q5-table1.jpg", "page": 16, "x0": 60, "y0": 126, "x1": 540, "y1": 220},
    {"filename": "fig-q6-table2.jpg", "page": 19, "x0": 60, "y0": 86, "x1": 540, "y1": 190},
    {"filename": "fig-q7-fig8.jpg", "page": 20, "x0": 60, "y0": 476, "x1": 540, "y1": 734},
    {"filename": "fig-q8-fig9.jpg", "page": 22, "x0": 60, "y0": 100, "x1": 540, "y1": 250},
    {"filename": "fig-q8-fig10.jpg", "page": 24, "x0": 60, "y0": 196, "x1": 540, "y1": 500},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 2, "01.4": 3,
    "02.1": 4, "02.2": 5, "02.3": 6,
    "03.1": 8, "03.2": 8, "03.3": 8, "03.4": 9, "03.5": 9,
    "04.1": 10, "04.2": 10, "04.3": 12, "04.4": 13,
    "05.1": 14, "05.2": 15, "05.3": 15, "05.4": 16, "05.5": 16,
    "06.1": 18, "06.2": 18, "06.3": 19, "06.4": 19,
    "07.1": 20, "07.2": 21, "07.3": 21,
    "08.1": 22, "08.2": 22, "08.3": 25, "08.4": 25,
    "09.1": 26, "09.2": 27,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.1.3", "marks": 1, "skills": [], "stem": "Name the COOH group in a fatty acid (RCOOH)."},
    {"qnum": "01.2", "specRef": "3.1.3", "marks": 2, "skills": [], "stem": "Name and explain the type of fatty acid R group shown in Figure 1.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.3", "specRef": "3.1.3", "marks": 2, "skills": ["practical"], "stem": "Describe how to test for the presence of a lipid in a liquid sample of food."},
    {"qnum": "01.4", "specRef": "3.2.3", "marks": 3, "skills": [], "stem": "Give one similarity and two differences between the 1935 membrane model (Figure 2) and the fluid-mosaic model.", "figures": ["fig-q1-fig2.jpg"]},
    {"qnum": "02.1", "specRef": "3.3.2", "marks": 2, "skills": [], "stem": "Describe and explain one feature of the alveolar epithelium adapting it for gas exchange (excluding surface area and moisture)."},
    {"qnum": "02.2", "specRef": "3.3.2", "marks": 2, "skills": ["maths"], "stem": "Use Figure 3 to determine the FEV1:FVC ratio of a man with emphysema and compare it with healthy lungs.", "figures": ["fig-q2-fig3.jpg"]},
    {"qnum": "02.3", "specRef": "3.3.2", "marks": 3, "skills": ["analysis"], "stem": "Suggest and explain how a reduced tidal volume affects carbon dioxide exchange between blood and alveoli."},
    {"qnum": "03.1", "specRef": "3.4.5", "marks": 1, "skills": [], "stem": "Name the taxonomy method of identifying an organism by its genus and species name."},
    {"qnum": "03.2", "specRef": "3.4.3", "marks": 1, "skills": [], "stem": "Define the term mutagenic agent."},
    {"qnum": "03.3", "specRef": "3.4.3", "marks": 1, "skills": ["maths"], "stem": "Complete Figure 4 with the chromosome numbers in Spartina diploid cells and gametes.", "figures": ["fig-q3-fig4.jpg"]},
    {"qnum": "03.4", "specRef": "3.4.3", "marks": 3, "skills": [], "stem": "Name and explain the mutation that doubled chromosomes from S. townsendii to S. anglica (Figure 5).", "figures": ["fig-q3-fig5.jpg"]},
    {"qnum": "03.5", "specRef": "3.4.3", "marks": 2, "skills": [], "stem": "Apart from mutation, crossing over, and independent segregation, explain one other way genetic variation increases."},
    {"qnum": "04.1", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Give two structures found in all prokaryotic cells and in all eukaryotic cells."},
    {"qnum": "04.2", "specRef": "3.2.2", "marks": 2, "skills": ["analysis"], "stem": "Suggest one explanation for faster plasmid replication in cells grown in high amino acid concentration."},
    {"qnum": "04.3", "specRef": "3.2.1", "marks": 2, "skills": ["analysis"], "stem": "Conclude and explain a structural difference between plasmids and circular DNA from Figure 6.", "figures": ["fig-q4-fig6.jpg"]},
    {"qnum": "04.4", "specRef": "3.2.2", "marks": 2, "skills": ["analysis"], "stem": "Conclude from Figure 6 the effect of antibiotic X on plasmid and circular DNA replication.", "figures": ["fig-q4-fig6.jpg"]},
    {"qnum": "05.1", "specRef": "3.1.4", "marks": 2, "skills": [], "stem": "Explain the appearance of the clear starch-agar area surrounding well D containing amylase (Figure 7).", "figures": ["fig-q5-fig7.jpg"]},
    {"qnum": "05.2", "specRef": "3.1.4", "marks": 2, "skills": ["analysis"], "stem": "Conclude about amylase activity from the agar around wells E (boiled) and F (water) in Figure 7.", "figures": ["fig-q5-fig7.jpg"]},
    {"qnum": "05.3", "specRef": "3.1.2", "marks": 2, "skills": ["practical"], "stem": "Describe a different biochemical test on the clear agar around well D to confirm amylase acted on starch."},
    {"qnum": "05.4", "specRef": "3.1.4", "marks": 2, "skills": ["maths"], "stem": "Use Table 1 dilution volumes to predict the clear area diameter (to nearest whole mm) around diluted amylase.", "figures": ["fig-q5-table1.jpg"]},
    {"qnum": "05.5", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Explain why the predicted diameter measured with a ruler should be given to the nearest whole number."},
    {"qnum": "06.1", "specRef": "3.1.4", "marks": 3, "skills": [], "stem": "Suggest why the ADF allele enzyme catalyses alcohol breakdown faster than the ADS allele enzyme."},
    {"qnum": "06.2", "specRef": "3.4.7", "marks": 1, "skills": ["practical"], "stem": "Suggest why the scientist took his sample of fruit flies from the population at random."},
    {"qnum": "06.3", "specRef": "3.4.4", "marks": 4, "skills": ["analysis"], "stem": "Suggest and explain why the frequency of the ADF allele changed from 0.20 to 0.74 over 45 generations (Table 2).", "figures": ["fig-q6-table2.jpg"]},
    {"qnum": "06.4", "specRef": "3.4.4", "marks": 1, "skills": [], "stem": "Tick the box identifying the type of selection investigated in the 45 generations of fruit flies."},
    {"qnum": "07.1", "specRef": "3.1.6", "marks": 4, "skills": [], "stem": "Describe how an ATP molecule is formed from its component molecules."},
    {"qnum": "07.2", "specRef": "3.2.3", "marks": 1, "skills": ["maths"], "stem": "Use Figure 8 to calculate the percentage decrease in amino acid absorption by H cells in 30 mmol dm^-3 cyanide.", "figures": ["fig-q7-fig8.jpg"]},
    {"qnum": "07.3", "specRef": "3.2.3", "marks": 3, "skills": ["analysis"], "stem": "Conclude from Figure 8 how amino acid uptake occurs in E. coli G and H cells.", "figures": ["fig-q7-fig8.jpg"]},
    {"qnum": "08.1", "specRef": "3.1.4", "marks": 1, "skills": ["analysis"], "stem": "Use Figure 9 to identify all products formed when the GOx and HRP reaction sequence is completed.", "figures": ["fig-q8-fig9.jpg"]},
    {"qnum": "08.2", "specRef": "3.1.4", "marks": 3, "skills": ["maths"], "stem": "Calculate the volume of a GOx molecule with units from DNA cage dimensions and enzyme volume proportions."},
    {"qnum": "08.3", "specRef": "3.1.4", "marks": 3, "skills": ["analysis"], "stem": "Conclude from Figure 10 (error bars +/- 2 SD) the effect of trapping GOx and HRP inside DNA cages.", "figures": ["fig-q8-fig10.jpg"]},
    {"qnum": "08.4", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Suggest a suitable control for the GOx/HRP DNA cage investigation."},
    {"qnum": "09.1", "specRef": "3.1.7", "marks": 5, "skills": ["extended"], "stem": "Explain five properties that make water important for organisms."},
    {"qnum": "09.2", "specRef": "3.1.5", "marks": 5, "skills": ["extended"], "stem": "Describe the process of semi-conservative replication of DNA."},
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
