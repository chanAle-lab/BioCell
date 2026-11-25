"""Ingest AQA AS Biology June 2016 Paper 2 (7401/2R) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795595891937_a37df9a8.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795595891815_2e9e57b5.pdf"
)

PAPER_ID = "2016-june-7401-2r"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "June",
    "unit": "7401/2R",
    "level": "AS",
    "date": "2016-06-07",
    "title": "7401/2R — AS Paper 2 (June 2016)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 3, "x0": 60, "y0": 98, "x1": 540, "y1": 405},
    {"filename": "fig-q3-fig2.jpg", "page": 6, "x0": 60, "y0": 125, "x1": 540, "y1": 240},
    {"filename": "fig-q3-fig3.jpg", "page": 7, "x0": 60, "y0": 150, "x1": 540, "y1": 345},
    {"filename": "fig-q4-fig4-5.jpg", "page": 8, "x0": 55, "y0": 150, "x1": 545, "y1": 360},
    {"filename": "fig-q5-fig6.jpg", "page": 10, "x0": 60, "y0": 175, "x1": 540, "y1": 475},
    {"filename": "fig-q6-fig7.jpg", "page": 14, "x0": 60, "y0": 200, "x1": 540, "y1": 485},
    {"filename": "fig-q8-fig8.jpg", "page": 18, "x0": 60, "y0": 175, "x1": 540, "y1": 415},
    {"filename": "fig-q9-table1.jpg", "page": 20, "x0": 60, "y0": 100, "x1": 540, "y1": 325},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 3,
    "02.1": 4, "02.2": 4, "02.3": 4, "02.4": 5, "02.5": 5,
    "03.1": 6, "03.2": 6, "03.3": 7, "03.4": 7,
    "04.1": 8, "04.2": 8, "04.3": 8, "04.4": 9, "04.5": 9,
    "05.1": 10, "05.2": 11, "05.3": 11, "05.4": 12,
    "06.1": 14, "06.2": 15, "06.3": 15, "06.4": 15,
    "07.1": 16, "07.2": 16, "07.3": 17,
    "08.1": 18, "08.2": 18, "08.3": 19, "08.4": 19,
    "09.1": 20, "09.2": 21, "09.3": 21, "09.4": 21,
    "10.1": 22, "10.2": 23,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.3.3", "marks": 1, "skills": [], "stem": "Name the other type of enzyme required alongside endopeptidases and exopeptidases for complete protein hydrolysis."},
    {"qnum": "01.2", "specRef": "3.3.3", "marks": 2, "skills": ["analysis"], "stem": "Suggest and explain why combined actions of endopeptidases and exopeptidases are more efficient."},
    {"qnum": "01.3", "specRef": "3.2.3", "marks": 3, "skills": ["analysis"], "stem": "Use Figure 1 to explain why a respiratory inhibitor stops amino acid absorption in the ileum.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "02.1", "specRef": "3.3.2", "marks": 1, "skills": ["practical"], "stem": "Suggest appropriate units to compare the distribution of stomata on leaves."},
    {"qnum": "02.2", "specRef": "3.2.1", "marks": 2, "skills": ["practical"], "stem": "Explain why it was important that leaf tissue pieces examined with an optical microscope were very thin."},
    {"qnum": "02.3", "specRef": "3.4.7", "marks": 2, "skills": ["practical"], "stem": "Give two reasons why it was important to count stomata in several parts of each piece of leaf tissue."},
    {"qnum": "02.4", "specRef": "3.3.2", "marks": 2, "skills": [], "stem": "Suggest and explain two xerophytic features of leaves other than stomatal distribution."},
    {"qnum": "02.5", "specRef": "3.3.4", "marks": 2, "skills": ["practical"], "stem": "Suggest two reasons why the rate of water uptake by a plant might not equal the rate of transpiration."},
    {"qnum": "03.1", "specRef": "3.2.3", "marks": 1, "skills": [], "stem": "Name the process by which oxygen reaches cells inside the body of a tubifex worm."},
    {"qnum": "03.2", "specRef": "3.3.1", "marks": 2, "skills": ["analysis"], "stem": "Explain how two features of the tubifex worm's body (Figure 2) allow efficient gas exchange.", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "03.3", "specRef": "3.3.4", "marks": 2, "skills": ["analysis"], "stem": "Explain how 50% haemoglobin saturation at 0.08 kPa (Figure 3) enables tubifex worms to survive sewage pollution.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.4", "specRef": "3.2.3", "marks": 2, "skills": [], "stem": "Use water potential to explain why freshwater tubifex worms cannot survive in seawater."},
    {"qnum": "04.1", "specRef": "3.4.6", "marks": 1, "skills": ["analysis"], "stem": "Read the mean species richness for dung beetles on rough grazing farms from Figure 4.", "figures": ["fig-q4-fig4-5.jpg"]},
    {"qnum": "04.2", "specRef": "3.4.6", "marks": 1, "skills": ["maths"], "stem": "State the additional measurement required alongside Figures 4 and 5 to calculate an index of diversity.", "figures": ["fig-q4-fig4-5.jpg"]},
    {"qnum": "04.3", "specRef": "3.4.7", "marks": 2, "skills": ["analysis"], "stem": "Explain what the standard deviations in Figure 5 suggest about differences in mean total dung beetle numbers.", "figures": ["fig-q4-fig4-5.jpg"]},
    {"qnum": "04.4", "specRef": "3.4.7", "marks": 1, "skills": ["practical"], "stem": "Explain the importance of placing dung beetle traps at sites chosen at random."},
    {"qnum": "04.5", "specRef": "3.4.6", "marks": 3, "skills": [], "stem": "Explain why removing hedges on intensive farms caused a decrease in bird diversity."},
    {"qnum": "05.1", "specRef": "3.1.3", "marks": 1, "skills": [], "stem": "Name the type of reaction used to break down phospholipids to release phosphate."},
    {"qnum": "05.2", "specRef": "3.1.8", "marks": 2, "skills": [], "stem": "Suggest two reasons why an increase in phosphate can be linked to growth of the plant embryo."},
    {"qnum": "05.3", "specRef": "3.1.8", "marks": 1, "skills": ["maths"], "stem": "Calculate the ratio of mean phosphate mass at 5 °C to 25 °C after 9 weeks of chilling (Figure 6).", "figures": ["fig-q5-fig6.jpg"]},
    {"qnum": "05.4", "specRef": "3.4.4", "marks": 3, "skills": ["analysis"], "stem": "Suggest how the chilling requirement of seeds enables plant species to survive seasonal changes."},
    {"qnum": "06.1", "specRef": "3.3.2", "marks": 2, "skills": ["practical"], "stem": "Suggest two precautions to ensure the mean FEV1 value of 25-year-olds was reliable."},
    {"qnum": "06.2", "specRef": "3.3.2", "marks": 2, "skills": ["analysis"], "stem": "Explain the importance of determining a mean FEV1 value of 25-year-olds in the investigation (Figure 7).", "figures": ["fig-q6-fig7.jpg"]},
    {"qnum": "06.3", "specRef": "3.3.2", "marks": 1, "skills": [], "stem": "Use knowledge of ventilation to suggest why mean FEV1 of non-smokers decreases after age 30."},
    {"qnum": "06.4", "specRef": "3.3.2", "marks": 3, "skills": ["analysis"], "stem": "Explain how a low FEV1 value in emphysema makes walking upstairs difficult."},
    {"qnum": "07.1", "specRef": "3.4.3", "marks": 4, "skills": [], "stem": "Explain how a mutation of the CCR5 gene can result in a non-functional protein receptor."},
    {"qnum": "07.2", "specRef": "3.2.4", "marks": 2, "skills": ["analysis"], "stem": "Explain why people with the CCR5 mutation show greater resistance to developing AIDS."},
    {"qnum": "07.3", "specRef": "3.4.4", "marks": 2, "skills": ["analysis"], "stem": "Suggest two reasons why the high frequency of CCR5 mutation in Europe is not due to natural selection by HIV."},
    {"qnum": "08.1", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Explain why there is a clear zone around each disinfectant paper disc in Figure 8.", "figures": ["fig-q8-fig8.jpg"]},
    {"qnum": "08.2", "specRef": "RP", "marks": 1, "skills": ["practical", "analysis"], "stem": "Use Figure 8 to explain why the student used a maximum disinfectant concentration of 40%.", "figures": ["fig-q8-fig8.jpg"]},
    {"qnum": "08.3", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Suggest two variables the student should control when using filter paper discs."},
    {"qnum": "08.4", "specRef": "RP", "marks": 2, "skills": ["maths", "practical"], "stem": "Use the areas of the clear zones in Figure 8 to determine how many times more effective D is than B.", "figures": ["fig-q8-fig8.jpg"]},
    {"qnum": "09.1", "specRef": "3.3.4", "marks": 1, "skills": ["maths"], "stem": "Use Table 1 to calculate the woman's heart rate in beats per minute.", "figures": ["fig-q9-table1.jpg"]},
    {"qnum": "09.2", "specRef": "3.3.4", "marks": 1, "skills": ["maths"], "stem": "Use Table 1 to determine the stroke volume.", "figures": ["fig-q9-table1.jpg"]},
    {"qnum": "09.3", "specRef": "3.3.4", "marks": 2, "skills": [], "stem": "Explain why higher ventricular blood pressure can cause tissue fluid to build up outside capillaries."},
    {"qnum": "09.4", "specRef": "3.3.4", "marks": 2, "skills": ["analysis"], "stem": "Suggest how widening of blood vessels caused by drugs can reduce ventricular blood pressure."},
    {"qnum": "10.1", "specRef": "3.1.2", "marks": 5, "skills": ["extended"], "stem": "Describe how the structures of starch and cellulose molecules are related to their functions."},
    {"qnum": "10.2", "specRef": "3.3.4", "marks": 5, "skills": ["extended"], "stem": "Describe the processes involved in the transport of sugars in plant stems."},
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
