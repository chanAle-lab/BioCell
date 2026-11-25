"""Ingest AQA AS Biology June 2017 Paper 2 (7401/2) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795595930411_ee6b458f.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795595930688_71b693e2.pdf"
)

PAPER_ID = "2017-june-7401-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2017,
    "series": "June",
    "unit": "7401/2",
    "level": "AS",
    "date": "2017-06-06",
    "title": "7401/2 — AS Paper 2 (June 2017)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 3, "x0": 55, "y0": 98, "x1": 540, "y1": 412},
    {"filename": "fig-q2-fig2.jpg", "page": 5, "x0": 60, "y0": 88, "x1": 540, "y1": 455},
    {"filename": "fig-q3-fig3.jpg", "page": 6, "x0": 60, "y0": 155, "x1": 540, "y1": 470},
    {"filename": "fig-q4-fig4.jpg", "page": 10, "x0": 60, "y0": 128, "x1": 540, "y1": 395},
    {"filename": "fig-q5-fig5.jpg", "page": 14, "x0": 60, "y0": 102, "x1": 540, "y1": 330},
    {"filename": "fig-q5-table1.jpg", "page": 15, "x0": 60, "y0": 180, "x1": 540, "y1": 370},
    {"filename": "fig-q6-fig6.jpg", "page": 17, "x0": 60, "y0": 188, "x1": 540, "y1": 415},
    {"filename": "fig-q7-fig7.jpg", "page": 20, "x0": 60, "y0": 180, "x1": 540, "y1": 420},
    {"filename": "fig-q8-fig8.jpg", "page": 22, "x0": 60, "y0": 140, "x1": 540, "y1": 505},
    {"filename": "fig-q8-fig9.jpg", "page": 24, "x0": 60, "y0": 155, "x1": 540, "y1": 420},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 2, "01.4": 3, "01.5": 3,
    "02.1": 4, "02.2": 4, "02.3": 5, "02.4": 5,
    "03.1": 6, "03.2": 7, "03.3": 8,
    "04.1": 10, "04.2": 11, "04.3": 11, "04.4": 12, "04.5": 12,
    "05.1": 14, "05.2": 14, "05.3": 15,
    "06.1": 16, "06.2": 17, "06.3": 18, "06.4": 18,
    "07.1": 19, "07.2": 20, "07.3": 21,
    "08.1": 22, "08.2": 23, "08.3": 23, "08.4": 24,
    "09.1": 25, "09.2": 26,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.1.2", "marks": 2, "skills": [], "stem": "Describe two differences between the structure of a cellulose molecule and a glycogen molecule."},
    {"qnum": "01.2", "specRef": "3.1.2", "marks": 2, "skills": [], "stem": "Describe and explain two features of starch that make it a good storage molecule."},
    {"qnum": "01.3", "specRef": "3.1.2", "marks": 1, "skills": ["practical"], "stem": "Identify the biochemical test used to show the presence of starch."},
    {"qnum": "01.4", "specRef": "3.2.1", "marks": 2, "skills": ["maths"], "stem": "Calculate the actual diameter of the starch grain between points A and B in Figure 1.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.5", "specRef": "3.2.1", "marks": 2, "skills": ["practical"], "stem": "Identify the type of microscope used for Figure 1 and give one piece of evidence.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "02.1", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Explain why it was important to control the volume of water in each beetroot tube."},
    {"qnum": "02.2", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Describe a method to monitor the temperature of the water in each tube."},
    {"qnum": "02.3", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Draw a suitable curve on Figure 2.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.4", "specRef": "3.2.3", "marks": 2, "skills": ["analysis"], "stem": "Suggest how increasing temperature caused release of red pigment from beetroot cells.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "03.1", "specRef": "3.4.7", "marks": 3, "skills": ["analysis"], "stem": "Describe what Figure 3 shows about AMY1 gene copy number in high- and low-starch populations.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.2", "specRef": "3.4.2", "marks": 3, "skills": [], "stem": "Use knowledge of protein synthesis and enzyme action to explain the advantage of multiple AMY1 copies."},
    {"qnum": "03.3", "specRef": "3.4.4", "marks": 3, "skills": [], "stem": "Suggest how multiple copies of the AMY1 gene evolved through natural selection."},
    {"qnum": "04.1", "specRef": "3.4.7", "marks": 1, "skills": ["maths"], "stem": "Calculate the difference between males and females in the fall in mean plasma protein (Figure 4).", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.2", "specRef": "3.4.7", "marks": 2, "skills": ["maths"], "stem": "Use Figure 4 to calculate the rate of change of mean plasma protein in males between ages 60 and 95.", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.3", "specRef": "3.4.7", "marks": 2, "skills": ["analysis"], "stem": "Conclude from Figure 4 the effect of ageing on mean plasma protein in males and females.", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.4", "specRef": "RP", "marks": 3, "skills": ["practical"], "stem": "Describe how to produce and use a colorimeter calibration curve to find plasma protein concentration."},
    {"qnum": "04.5", "specRef": "3.2.4", "marks": 1, "skills": ["analysis"], "stem": "Suggest how lower plasma protein concentration in older people links to infectious disease."},
    {"qnum": "05.1", "specRef": "3.3.4", "marks": 2, "skills": [], "stem": "Explain how changes in haemoglobin shape result in the sigmoid oxyhaemoglobin dissociation curve."},
    {"qnum": "05.2", "specRef": "3.3.4", "marks": 2, "skills": ["analysis"], "stem": "Use Figure 5 to explain why replacing HbF with HbA by 6 months is an advantage for the baby.", "figures": ["fig-q5-fig5.jpg"]},
    {"qnum": "05.3", "specRef": "3.3.4", "marks": 3, "skills": ["analysis"], "stem": "Suggest how Figure 5 and Table 1 support hydroxyurea increasing blood oxygen in sickle cell disease.", "figures": ["fig-q5-fig5.jpg", "fig-q5-table1.jpg"]},
    {"qnum": "06.1", "specRef": "3.2.1", "marks": 3, "skills": ["practical"], "stem": "Describe how to use an eyepiece graticule to determine the mean diameter of stomata."},
    {"qnum": "06.2", "specRef": "3.3.2", "marks": 2, "skills": ["maths"], "stem": "Calculate the ratio of mean stomatal diameter of leaves treated with PS3 to ABA (Figure 6).", "figures": ["fig-q6-fig6.jpg"]},
    {"qnum": "06.3", "specRef": "3.3.2", "marks": 2, "skills": [], "stem": "Explain why producing ABA helps plant species survive in dry conditions."},
    {"qnum": "06.4", "specRef": "3.3.2", "marks": 1, "skills": ["analysis"], "stem": "Suggest how treatment with Lam13 might protect plants against powdery mildew infection."},
    {"qnum": "07.1", "specRef": "3.2.4", "marks": 4, "skills": [], "stem": "Explain why anti-AQP4 antibody only damages nerve cells in the spinal cord."},
    {"qnum": "07.2", "specRef": "3.4.7", "marks": 3, "skills": ["analysis"], "stem": "Use Figure 7 to suggest why anti-AQP4 concentration might not reliably predict damaged vertebrae.", "figures": ["fig-q7-fig7.jpg"]},
    {"qnum": "07.3", "specRef": "3.2.4", "marks": 2, "skills": ["analysis"], "stem": "Suggest how a monoclonal antibody with the same variable region prevents anti-AQP4 nerve damage."},
    {"qnum": "08.1", "specRef": "3.4.3", "marks": 1, "skills": ["analysis"], "stem": "State the effect of Patau syndrome on the chromosomes shown in Figure 8.", "figures": ["fig-q8-fig8.jpg"]},
    {"qnum": "08.2", "specRef": "3.4.3", "marks": 2, "skills": [], "stem": "Describe how the change in chromosome number in Patau syndrome was produced."},
    {"qnum": "08.3", "specRef": "3.2.2", "marks": 2, "skills": [], "stem": "Explain why all the cells of the body will have the Patau syndrome mutation."},
    {"qnum": "08.4", "specRef": "3.3.4", "marks": 3, "skills": ["analysis"], "stem": "Suggest how blood flow between aorta and pulmonary artery (Figure 9) could cause infant death.", "figures": ["fig-q8-fig9.jpg"]},
    {"qnum": "09.1", "specRef": "3.3.4", "marks": 5, "skills": ["extended"], "stem": "Describe the cohesion-tension theory of water transport in the xylem."},
    {"qnum": "09.2", "specRef": "3.4.2", "marks": 5, "skills": ["extended"], "stem": "Describe how mRNA is produced in a plant cell."},
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
