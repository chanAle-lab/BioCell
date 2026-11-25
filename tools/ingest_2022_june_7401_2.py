"""Ingest AQA AS Biology June 2022 Paper 2 (7401/2) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598162526_83d71d21.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598162448_ccdebe43.pdf"
)

PAPER_ID = "2022-june-7401-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2022,
    "series": "June",
    "unit": "7401/2",
    "level": "AS",
    "date": "2022-06-01",
    "title": "7401/2 — AS Paper 2 (June 2022)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q3-fig1.jpg", "page": 6, "x0": 60, "y0": 88, "x1": 540, "y1": 356},
    {"filename": "fig-q4-fig2.jpg", "page": 10, "x0": 60, "y0": 104, "x1": 540, "y1": 196},
    {"filename": "fig-q4-fig3.jpg", "page": 11, "x0": 60, "y0": 90, "x1": 540, "y1": 436},
    {"filename": "fig-q5-table1.jpg", "page": 12, "x0": 60, "y0": 254, "x1": 540, "y1": 448},
    {"filename": "fig-q5-fig4.jpg", "page": 12, "x0": 60, "y0": 500, "x1": 540, "y1": 762},
    {"filename": "fig-q5-table2.jpg", "page": 14, "x0": 60, "y0": 250, "x1": 540, "y1": 485},
    {"filename": "fig-q6-fig5.jpg", "page": 17, "x0": 60, "y0": 102, "x1": 540, "y1": 524},
    {"filename": "fig-q6-fig6.jpg", "page": 18, "x0": 60, "y0": 164, "x1": 540, "y1": 416},
    {"filename": "fig-q6-fig7.jpg", "page": 19, "x0": 60, "y0": 74, "x1": 540, "y1": 380},
    {"filename": "fig-q7-fig8.jpg", "page": 20, "x0": 60, "y0": 98, "x1": 540, "y1": 342},
    {"filename": "fig-q7-table4.jpg", "page": 22, "x0": 60, "y0": 276, "x1": 540, "y1": 465},
    {"filename": "fig-q8-fig9.jpg", "page": 24, "x0": 60, "y0": 176, "x1": 540, "y1": 360},
    {"filename": "fig-q8-fig10.jpg", "page": 26, "x0": 60, "y0": 124, "x1": 540, "y1": 340},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 2, "01.4": 3,
    "02.1": 4, "02.2": 4, "02.3": 4, "02.4": 5, "02.5": 5,
    "03.1": 6, "03.2": 7, "03.3": 8,
    "04.1": 9, "04.2": 10, "04.3": 10, "04.4": 11,
    "05.1": 12, "05.2": 13, "05.3": 13, "05.4": 14, "05.5": 15,
    "06.1": 16, "06.2": 17, "06.3": 19,
    "07.1": 20, "07.2": 23, "07.3": 23,
    "08.1": 24, "08.2": 25, "08.3": 26,
    "09.1": 27, "09.2": 28,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.4.1", "marks": 1, "skills": [], "stem": "Define what a gene is."},
    {"qnum": "01.2", "specRef": "3.4.2", "marks": 2, "skills": [], "stem": "Describe how mRNA production in a eukaryote cell differs from mRNA production in a prokaryote cell."},
    {"qnum": "01.3", "specRef": "3.4.2", "marks": 2, "skills": ["analysis"], "stem": "Suggest how single-stranded PNA binding to DNA reduced transcription of mRNA."},
    {"qnum": "01.4", "specRef": "3.4.2", "marks": 2, "skills": [], "stem": "Describe the role of ATP in translation during protein synthesis."},
    {"qnum": "02.1", "specRef": "3.1.2", "marks": 1, "skills": [], "stem": "Name the term describing the different structures of alpha-glucose and beta-glucose."},
    {"qnum": "02.2", "specRef": "3.1.2", "marks": 1, "skills": ["practical"], "stem": "Describe how colorimeter results identify the fruit juice with higher reducing sugar content."},
    {"qnum": "02.3", "specRef": "3.1.2", "marks": 2, "skills": ["practical"], "stem": "Give two variables controlled in the Benedict's test on fruit juices."},
    {"qnum": "02.4", "specRef": "3.1.2", "marks": 2, "skills": ["maths"], "stem": "Calculate the mass of sugar in the flesh tissue of a 180 g apple with 5:1 flesh-to-core ratio and 8% sugar."},
    {"qnum": "02.5", "specRef": "3.1.2", "marks": 2, "skills": ["analysis"], "stem": "Suggest why the water potential of apple juice decreases and iodine stains less black when apples are stored."},
    {"qnum": "03.1", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Describe and explain two ways structures in Figure 1 (microvilli/mitochondria) increase ileum cell absorption rate.", "figures": ["fig-q3-fig1.jpg"]},
    {"qnum": "03.2", "specRef": "3.3.1", "marks": 2, "skills": ["maths"], "stem": "Calculate the surface area ratio of an ileum cell with 1000 microvilli to one without microvilli."},
    {"qnum": "03.3", "specRef": "3.2.4", "marks": 3, "skills": ["analysis"], "stem": "Suggest how an anti-ZO-1 monoclonal antibody helped identify ileum cells under an optical microscope."},
    {"qnum": "04.1", "specRef": "3.4.3", "marks": 4, "skills": [], "stem": "Describe how meiosis results in haploid cells (excluding sources of genetic variation)."},
    {"qnum": "04.2", "specRef": "3.4.3", "marks": 2, "skills": ["maths"], "stem": "Calculate how many of 300 meiotic cells are expected to have the identical chromosome arrangement shown in Figure 2.", "figures": ["fig-q4-fig2.jpg"]},
    {"qnum": "04.3", "specRef": "3.4.3", "marks": 1, "skills": [], "stem": "Draw a diagram to show the chromosomes in one gamete produced by meiosis from Figure 2.", "figures": ["fig-q4-fig2.jpg"]},
    {"qnum": "04.4", "specRef": "3.4.3", "marks": 1, "skills": [], "stem": "Tick the box naming process A in the fungus life cycle (Figure 3).", "figures": ["fig-q4-fig3.jpg"]},
    {"qnum": "05.1", "specRef": "3.4.5", "marks": 2, "skills": [], "stem": "Describe how organisms are grouped in a phylogenetic classification system."},
    {"qnum": "05.2", "specRef": "3.4.5", "marks": 1, "skills": [], "stem": "Use Table 1 to give the scientific name of taxon B in Figure 4.", "figures": ["fig-q5-table1.jpg", "fig-q5-fig4.jpg"]},
    {"qnum": "05.3", "specRef": "3.4.5", "marks": 1, "skills": [], "stem": "Draw an oval on Figure 4 to show the species Rhinoceros sondaicus.", "figures": ["fig-q5-fig4.jpg"]},
    {"qnum": "05.4", "specRef": "3.4.5", "marks": 4, "skills": ["analysis"], "stem": "Conclude and evaluate phylogenetic relationships between five rhinoceros species from Table 2 cyt b differences.", "figures": ["fig-q5-table2.jpg"]},
    {"qnum": "05.5", "specRef": "3.4.5", "marks": 2, "skills": ["analysis"], "stem": "Conclude which species a confiscated horn with 14% cyt b difference came from and suggest how to improve identification.", "figures": ["fig-q5-table2.jpg"]},
    {"qnum": "06.1", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Complete Table 3 with three control measures for carrying and using a scalpel during heart dissection."},
    {"qnum": "06.2", "specRef": "3.3.4", "marks": 2, "skills": ["maths"], "stem": "Use Figure 5 to calculate the total volume of blood pumped from the left ventricle in 1 minute.", "figures": ["fig-q6-fig5.jpg"]},
    {"qnum": "06.3", "specRef": "3.3.4", "marks": 4, "skills": ["analysis"], "stem": "Use Figure 6 and Figure 7 to evaluate blood pressure treatments 1 and 2 in reducing cardiovascular disease risk.", "figures": ["fig-q6-fig6.jpg", "fig-q6-fig7.jpg"]},
    {"qnum": "07.1", "specRef": "3.2.1", "marks": 3, "skills": ["practical"], "stem": "Produce a labelled tissue-plan drawing of the vertical leaf section in Figure 8 without drawing individual cells.", "figures": ["fig-q7-fig8.jpg"]},
    {"qnum": "07.2", "specRef": "3.3.4", "marks": 4, "skills": ["analysis"], "stem": "Conclude and explain from Table 4 (+/- 2 SD) how stomata density and transpiration rate affect cut flower shelf life.", "figures": ["fig-q7-table4.jpg"]},
    {"qnum": "07.3", "specRef": "3.3.4", "marks": 3, "skills": ["practical"], "stem": "Other than temperature, give and explain one environmental change to increase cut flowers' shelf life."},
    {"qnum": "08.1", "specRef": "3.4.4", "marks": 1, "skills": ["analysis"], "stem": "Suggest one type of guppy behaviour affected by brightly coloured stones in Figure 9.", "figures": ["fig-q8-fig9.jpg"]},
    {"qnum": "08.2", "specRef": "3.4.7", "marks": 2, "skills": ["practical"], "stem": "Suggest a further investigation and null hypothesis to confirm brightly coloured stones affected guppy behaviour."},
    {"qnum": "08.3", "specRef": "3.4.4", "marks": 4, "skills": ["analysis"], "stem": "Name and explain the type of selection in Figure 10 after predators were added to the guppy tank.", "figures": ["fig-q8-fig10.jpg"]},
    {"qnum": "09.1", "specRef": "3.3.2", "marks": 5, "skills": ["extended"], "stem": "Describe and explain how the insect gas exchange system provides cells with sufficient oxygen and limits water loss."},
    {"qnum": "09.2", "specRef": "3.3.2", "marks": 5, "skills": ["extended"], "stem": "Describe how humans breathe in and out."},
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
