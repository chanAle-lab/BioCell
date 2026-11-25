"""Ingest AQA AS Biology June 2019 Paper 2 (7401/2) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795597881001_6e69c1c5.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795597880985_b1bc5ef4.pdf"
)

PAPER_ID = "2019-june-7401-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2019,
    "series": "June",
    "unit": "7401/2",
    "level": "AS",
    "date": "2019-05-24",
    "title": "7401/2 — AS Paper 2 (June 2019)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 4, "x0": 60, "y0": 155, "x1": 540, "y1": 540},
    {"filename": "fig-q1-fig2.jpg", "page": 6, "x0": 60, "y0": 86, "x1": 540, "y1": 448},
    {"filename": "fig-q2-fig3.jpg", "page": 8, "x0": 60, "y0": 488, "x1": 540, "y1": 758},
    {"filename": "fig-q4-fig4.jpg", "page": 12, "x0": 60, "y0": 240, "x1": 540, "y1": 655},
    {"filename": "fig-q5-fig5.jpg", "page": 15, "x0": 60, "y0": 106, "x1": 540, "y1": 382},
    {"filename": "fig-q5-fig6.jpg", "page": 16, "x0": 60, "y0": 240, "x1": 540, "y1": 376},
    {"filename": "fig-q5-table1.jpg", "page": 17, "x0": 60, "y0": 305, "x1": 540, "y1": 400},
    {"filename": "fig-q6-fig7.jpg", "page": 19, "x0": 60, "y0": 190, "x1": 540, "y1": 504},
    {"filename": "fig-q6-table2.jpg", "page": 20, "x0": 60, "y0": 98, "x1": 540, "y1": 270},
    {"filename": "fig-q7-fig8.jpg", "page": 21, "x0": 60, "y0": 256, "x1": 540, "y1": 515},
    {"filename": "fig-q8-fig9.jpg", "page": 24, "x0": 60, "y0": 448, "x1": 540, "y1": 528},
    {"filename": "fig-q8-fig10.jpg", "page": 25, "x0": 60, "y0": 152, "x1": 540, "y1": 562},
]

PAGE_MAP = {
    "01.1": 3, "01.2": 5, "01.3": 6,
    "02.1": 8, "02.2": 9, "02.3": 9,
    "03.1": 10, "03.2": 10, "03.3": 10,
    "04.1": 11, "04.2": 13, "04.3": 13, "04.4": 14,
    "05.1": 15, "05.2": 15, "05.3": 16, "05.4": 17, "05.5": 17,
    "06.1": 18, "06.2": 18, "06.3": 19, "06.4": 20,
    "07.1": 21, "07.2": 22, "07.3": 22, "07.4": 23,
    "08.1": 24, "08.2": 24, "08.3": 25, "08.4": 26,
    "09.1": 27, "09.2": 28,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.3.3", "marks": 4, "skills": [], "stem": "Describe the role of enzymes in the digestion of proteins in a mammal."},
    {"qnum": "01.2", "specRef": "3.3.3", "marks": 3, "skills": ["analysis"], "stem": "Conclude how protein percentage in rabbit diet affects absorption of protein digestion products using Figure 1.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.3", "specRef": "3.3.3", "marks": 3, "skills": ["analysis"], "stem": "Use Figure 2 to suggest how eating its own caecal droppings helps a rabbit's digestion and absorption of protein.", "figures": ["fig-q1-fig2.jpg"]},
    {"qnum": "02.1", "specRef": "3.3.4", "marks": 2, "skills": [], "stem": "Describe and explain the effect of increasing carbon dioxide concentration on the dissociation of oxyhaemoglobin."},
    {"qnum": "02.2", "specRef": "3.3.4", "marks": 2, "skills": ["analysis"], "stem": "Use Figure 3 to explain how the seal's myoglobin dissociation curve shows the seal is adapted for diving.", "figures": ["fig-q2-fig3.jpg"]},
    {"qnum": "02.3", "specRef": "3.3.4", "marks": 2, "skills": ["maths"], "stem": "Calculate the maximum dive time in minutes of a 190 kg seal from its oxygen carrying capacity and metabolic rate."},
    {"qnum": "03.1", "specRef": "3.1.5", "marks": 1, "skills": [], "stem": "Name the two scientists who proposed models of the chemical structure of DNA and of DNA replication."},
    {"qnum": "03.2", "specRef": "3.1.5", "marks": 1, "skills": [], "stem": "Name the enzyme used in the in-vitro DNA replication experiment."},
    {"qnum": "03.3", "specRef": "3.1.5", "marks": 3, "skills": [], "stem": "Suggest the role of single-stranded DNA fragments and DNA nucleotides in semi-conservative DNA replication."},
    {"qnum": "04.1", "specRef": "3.2.4", "marks": 2, "skills": [], "stem": "Describe and explain the role of antibodies in stimulating phagocytosis."},
    {"qnum": "04.2", "specRef": "3.2.4", "marks": 2, "skills": ["maths"], "stem": "Calculate the time for anti-meningitis antibody concentration in mouse Z (Figure 4) to halve after the 3rd injection.", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.3", "specRef": "3.2.4", "marks": 4, "skills": ["analysis"], "stem": "Conclude the effectiveness of each MenG injection on the immune response of the mice using Figure 4.", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.4", "specRef": "3.2.4", "marks": 2, "skills": ["practical"], "stem": "Suggest and explain a practical method to test whether memory B cells formed 180 days after the 3rd injection."},
    {"qnum": "05.1", "specRef": "3.3.4", "marks": 2, "skills": ["practical"], "stem": "Give two other measurements needed with Figure 5 to calculate rate of water movement in grams per hour per cm2.", "figures": ["fig-q5-fig5.jpg"]},
    {"qnum": "05.2", "specRef": "3.3.4", "marks": 1, "skills": ["practical"], "stem": "Give the reason for adding a layer of oil to the water in the beaker in Figure 5.", "figures": ["fig-q5-fig5.jpg"]},
    {"qnum": "05.3", "specRef": "3.3.4", "marks": 3, "skills": [], "stem": "Explain why coloured water moved up the celery leaf stalks (Figure 6).", "figures": ["fig-q5-fig6.jpg"]},
    {"qnum": "05.4", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Describe how the student should ensure safe handling of a sharp scalpel when cutting celery."},
    {"qnum": "05.5", "specRef": "3.3.4", "marks": 2, "skills": ["maths"], "stem": "Choose and calculate the most appropriate average (mean, median, or mode) for the celery distance data in Table 1.", "figures": ["fig-q5-table1.jpg"]},
    {"qnum": "06.1", "specRef": "RP", "marks": 3, "skills": ["practical"], "stem": "Describe and explain three ways to ensure aseptic techniques when transferring Neurospora agar cubes."},
    {"qnum": "06.2", "specRef": "3.4.3", "marks": 2, "skills": [], "stem": "Give two differences between mitosis and meiosis."},
    {"qnum": "06.3", "specRef": "3.4.3", "marks": 1, "skills": ["maths"], "stem": "Tick the box showing the number of chromatids in a Neurospora zygote at the start of meiosis given 7 chromosomes per spore.", "figures": ["fig-q6-fig7.jpg"]},
    {"qnum": "06.4", "specRef": "3.4.3", "marks": 3, "skills": ["analysis"], "stem": "Conclude what Figure 7 and Table 2 show about chromosome movement during meiosis in Neurospora.", "figures": ["fig-q6-fig7.jpg", "fig-q6-table2.jpg"]},
    {"qnum": "07.1", "specRef": "3.4.4", "marks": 2, "skills": [], "stem": "State and justify the type of selection modelled by returning only the largest or smallest fish in Figure 8.", "figures": ["fig-q7-fig8.jpg"]},
    {"qnum": "07.2", "specRef": "3.4.4", "marks": 2, "skills": ["practical"], "stem": "Explain the purpose of Tank B (random fish return) as a control in the investigation."},
    {"qnum": "07.3", "specRef": "3.4.4", "marks": 2, "skills": ["maths"], "stem": "Calculate the ratio of mean fish mass in Tank A to Tank C at 1 year and 4 years using Figure 8, and how much greater it is at 4 years.", "figures": ["fig-q7-fig8.jpg"]},
    {"qnum": "07.4", "specRef": "3.4.4", "marks": 3, "skills": ["analysis"], "stem": "Suggest how mesh size regulations that let small fish escape affect future fish populations."},
    {"qnum": "08.1", "specRef": "3.4.5", "marks": 2, "skills": [], "stem": "Give two other ways genetic diversity between species is measured besides DNA/mRNA base sequences."},
    {"qnum": "08.2", "specRef": "3.4.5", "marks": 1, "skills": ["maths"], "stem": "Calculate the percentage difference in base sequence between the two bird species in Figure 9.", "figures": ["fig-q8-fig9.jpg"]},
    {"qnum": "08.3", "specRef": "3.4.5", "marks": 1, "skills": ["analysis"], "stem": "Match each taxonomic group in Table 3 to histograms A, B, or C in Figure 10.", "figures": ["fig-q8-fig10.jpg"]},
    {"qnum": "08.4", "specRef": "3.4.5", "marks": 2, "skills": ["maths"], "stem": "Select and justify the statistical test to determine if there is a significant correlation between percentage base difference and time since divergence."},
    {"qnum": "09.1", "specRef": "3.1.8", "marks": 5, "skills": ["extended"], "stem": "Describe the roles of iron ions, sodium ions, and phosphate ions in cells."},
    {"qnum": "09.2", "specRef": "3.2.3", "marks": 5, "skills": ["extended"], "stem": "Describe how the movement of substances across cell membranes is affected by membrane structure."},
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
