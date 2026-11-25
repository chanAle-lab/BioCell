"""Ingest AQA AS Biology June 2017 Paper 1 (7401/1) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795595930340_683151dc.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795595931570_112f0bf5.pdf"
)

PAPER_ID = "2017-june-7401-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2017,
    "series": "June",
    "unit": "7401/1",
    "level": "AS",
    "date": "2017-05-25",
    "title": "7401/1 — AS Paper 1 (June 2017)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 60, "y0": 134, "x1": 540, "y1": 415},
    {"filename": "fig-q2-table1.jpg", "page": 5, "x0": 60, "y0": 105, "x1": 540, "y1": 365},
    {"filename": "fig-q3-fig2.jpg", "page": 8, "x0": 60, "y0": 98, "x1": 540, "y1": 545},
    {"filename": "fig-q4-fig3.jpg", "page": 10, "x0": 60, "y0": 118, "x1": 540, "y1": 300},
    {"filename": "fig-q5-fig4.jpg", "page": 12, "x0": 60, "y0": 302, "x1": 540, "y1": 465},
    {"filename": "fig-q6-fig5.jpg", "page": 14, "x0": 60, "y0": 115, "x1": 540, "y1": 495},
    {"filename": "fig-q6-fig6.jpg", "page": 15, "x0": 60, "y0": 350, "x1": 540, "y1": 620},
    {"filename": "fig-q7-fig7-8.jpg", "page": 19, "x0": 55, "y0": 280, "x1": 545, "y1": 505},
    {"filename": "fig-q8-table4.jpg", "page": 20, "x0": 60, "y0": 418, "x1": 540, "y1": 715},
    {"filename": "fig-q9-fig9.jpg", "page": 24, "x0": 60, "y0": 318, "x1": 540, "y1": 625},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 3, "01.4": 3,
    "02.1": 4, "02.2": 5, "02.3": 6,
    "03.1": 8, "03.2": 9, "03.3": 9,
    "04.1": 10, "04.2": 10, "04.3": 11, "04.4": 11,
    "05.1": 12, "05.2": 12, "05.3": 12, "05.4": 13,
    "06.1": 14, "06.2": 15, "06.3": 15, "06.4": 16,
    "07.1": 18, "07.2": 18, "07.3": 19, "07.4": 19,
    "08.1": 20, "08.2": 21, "08.3": 21, "08.4": 22,
    "09.1": 24, "09.2": 24, "09.3": 25,
    "10.1": 26, "10.2": 27, "10.3": 28,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.1.5", "marks": 1, "skills": ["analysis"], "stem": "Count how many nucleotides are shown in Figure 1.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.2", "specRef": "3.1.5", "marks": 1, "skills": [], "stem": "Name the type of bond labelled X in Figure 1.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.3", "specRef": "3.1.5", "marks": 2, "skills": [], "stem": "Describe the function of DNA helicase and DNA polymerase in DNA replication."},
    {"qnum": "01.4", "specRef": "3.1.6", "marks": 2, "skills": [], "stem": "Contrast the structures of ATP and a DNA nucleotide to give two differences."},
    {"qnum": "02.1", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Explain the purpose of boiling the agar and transferring the same volume of bacterial culture."},
    {"qnum": "02.2", "specRef": "RP", "marks": 2, "skills": ["maths", "practical"], "stem": "Calculate the number of bacteria in 1 cm3 of undiluted liquid culture using Table 1.", "figures": ["fig-q2-table1.jpg"]},
    {"qnum": "02.3", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Describe how to obtain a more accurate estimate of the minimum inhibitory concentration of propan-2-ol."},
    {"qnum": "03.1", "specRef": "3.3.3", "marks": 1, "skills": [], "stem": "Identify the process by which fatty acids and glycerol enter the intestinal epithelial cell (Figure 2).", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "03.2", "specRef": "3.3.3", "marks": 3, "skills": [], "stem": "Explain the advantages of lipid droplet and micelle formation."},
    {"qnum": "03.3", "specRef": "3.2.1", "marks": 4, "skills": ["analysis"], "stem": "Name structure Q in Figure 2 and suggest how it is involved in lipid absorption.", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "04.1", "specRef": "3.3.4", "marks": 2, "skills": ["analysis"], "stem": "Use Figure 3 to complete Table 2 showing when the semi-lunar and atrioventricular valves open and close.", "figures": ["fig-q4-fig3.jpg"]},
    {"qnum": "04.2", "specRef": "3.3.4", "marks": 2, "skills": ["maths"], "stem": "Use Figure 3 to calculate the volume of blood pumped per minute by the left ventricle.", "figures": ["fig-q4-fig3.jpg"]},
    {"qnum": "04.3", "specRef": "3.3.4", "marks": 2, "skills": [], "stem": "Explain the role of the heart in the formation of tissue fluid."},
    {"qnum": "04.4", "specRef": "3.3.4", "marks": 1, "skills": ["analysis"], "stem": "Suggest how a blockage in the lymphatic system could cause lymphoedema."},
    {"qnum": "05.1", "specRef": "3.1.4", "marks": 1, "skills": ["practical"], "stem": "Name the biochemical test used to identify amino acids/proteins in white wine."},
    {"qnum": "05.2", "specRef": "3.1.4", "marks": 1, "skills": [], "stem": "Draw a box around the constant part of the amino acid isoleucine in Figure 4.", "figures": ["fig-q5-fig4.jpg"]},
    {"qnum": "05.3", "specRef": "3.1.3", "marks": 1, "skills": [], "stem": "Name the chemical element found in all amino acids that is not found in triglycerides."},
    {"qnum": "05.4", "specRef": "3.4.7", "marks": 3, "skills": ["maths", "analysis"], "stem": "Name and justify the statistical test used and explain what P = 0.04 indicates."},
    {"qnum": "06.1", "specRef": "3.4.3", "marks": 1, "skills": ["analysis"], "stem": "Identify which letter in Figure 5 shows where meiosis occurs in the moss life cycle.", "figures": ["fig-q6-fig5.jpg"]},
    {"qnum": "06.2", "specRef": "3.4.3", "marks": 2, "skills": [], "stem": "Explain how the chromosome number is halved during meiosis."},
    {"qnum": "06.3", "specRef": "3.4.3", "marks": 1, "skills": ["analysis"], "stem": "Determine the haploid number of chromosomes for the moss species from Figure 6.", "figures": ["fig-q6-fig6.jpg"]},
    {"qnum": "06.4", "specRef": "3.4.3", "marks": 4, "skills": [], "stem": "Describe the process of crossing over and explain how it increases genetic diversity."},
    {"qnum": "07.1", "specRef": "3.2.1", "marks": 3, "skills": ["practical"], "stem": "Describe how to use cell fractionation techniques to obtain a sample of chloroplasts from leaf tissue."},
    {"qnum": "07.2", "specRef": "3.2.1", "marks": 3, "skills": [], "stem": "Complete Table 3 comparing features of a mitochondrion and a chloroplast."},
    {"qnum": "07.3", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Give the function of a mitochondrion."},
    {"qnum": "07.4", "specRef": "3.2.1", "marks": 2, "skills": ["analysis"], "stem": "Explain what Figures 7 and 8 suggest about the effect of an exercise programme on mitochondria.", "figures": ["fig-q7-fig7-8.jpg"]},
    {"qnum": "08.1", "specRef": "3.1.7", "marks": 3, "skills": [], "stem": "Give three properties of water that are important in biology."},
    {"qnum": "08.2", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Name the method used to produce sucrose solutions of different concentrations from a stock."},
    {"qnum": "08.3", "specRef": "RP", "marks": 3, "skills": ["maths", "practical"], "stem": "Calculate the ratio of final to initial mass of potato chips (Table 4) and plot a graph.", "figures": ["fig-q8-table4.jpg"]},
    {"qnum": "08.4", "specRef": "3.2.3", "marks": 2, "skills": ["analysis"], "stem": "Explain the result for the potato chip in 0.8 mol dm-3 sucrose solution."},
    {"qnum": "09.1", "specRef": "3.4.5", "marks": 2, "skills": [], "stem": "Define the terms species and species richness."},
    {"qnum": "09.2", "specRef": "3.4.6", "marks": 1, "skills": ["maths"], "stem": "Determine the modal value of species richness from Figure 9.", "figures": ["fig-q9-fig9.jpg"]},
    {"qnum": "09.3", "specRef": "3.4.6", "marks": 3, "skills": ["analysis"], "stem": "Give reasons why 68% of fish coming from sample A does not show sample A has the greatest index of diversity.", "figures": ["fig-q9-fig9.jpg"]},
    {"qnum": "10.1", "specRef": "3.2.4", "marks": 4, "skills": ["analysis"], "stem": "Suggest and explain why AZT does not destroy HIV but stops or slows the development of AIDS."},
    {"qnum": "10.2", "specRef": "3.4.4", "marks": 4, "skills": ["analysis"], "stem": "Suggest and explain two advantages of using HAART combination therapy."},
    {"qnum": "10.3", "specRef": "3.2.1", "marks": 2, "skills": ["analysis"], "stem": "Suggest why high doses of AZT lead to muscle wastage."},
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
