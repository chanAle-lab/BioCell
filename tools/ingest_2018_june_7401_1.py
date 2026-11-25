"""Ingest AQA AS Biology June 2018 Paper 1 (7401/1) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795597620242_43544a5c.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795597621060_2733d570.pdf"
)

PAPER_ID = "2018-june-7401-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2018,
    "series": "June",
    "unit": "7401/1",
    "level": "AS",
    "date": "2018-05-24",
    "title": "7401/1 — AS Paper 1 (June 2018)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 60, "y0": 125, "x1": 540, "y1": 385},
    {"filename": "fig-q1-fig2.jpg", "page": 3, "x0": 60, "y0": 100, "x1": 540, "y1": 290},
    {"filename": "fig-q4-fig3.jpg", "page": 8, "x0": 60, "y0": 88, "x1": 540, "y1": 370},
    {"filename": "fig-q5-fig4.jpg", "page": 10, "x0": 60, "y0": 88, "x1": 540, "y1": 370},
    {"filename": "fig-q6-fig5.jpg", "page": 13, "x0": 60, "y0": 88, "x1": 540, "y1": 310},
    {"filename": "fig-q6-fig6.jpg", "page": 14, "x0": 60, "y0": 160, "x1": 540, "y1": 510},
    {"filename": "fig-q8-table1.jpg", "page": 20, "x0": 60, "y0": 215, "x1": 540, "y1": 455},
    {"filename": "fig-q9-fig7.jpg", "page": 24, "x0": 60, "y0": 125, "x1": 540, "y1": 520},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 3,
    "02.1": 4, "02.2": 4, "02.3": 5, "02.4": 5,
    "03.1": 6, "03.2": 6, "03.3": 7,
    "04.1": 8, "04.2": 8, "04.3": 9, "04.4": 9,
    "05.1": 10, "05.2": 10, "05.3": 11,
    "06.1": 13, "06.2": 13, "06.3": 15, "06.4": 15,
    "07.1": 16, "07.2": 16, "07.3": 17,
    "08.1": 19, "08.2": 19, "08.3": 20, "08.4": 21, "08.5": 21,
    "09.1": 22, "09.2": 22, "09.3": 25,
    "10.1": 27, "10.2": 28, "10.3": 28, "10.4": 29,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.3.4", "marks": 3, "skills": [], "stem": "Identify the letters representing the aorta, renal vein, and vena cava in Figure 1.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.2", "specRef": "3.3.4", "marks": 1, "skills": [], "stem": "Name the blood vessels that carry blood to the heart muscle."},
    {"qnum": "01.3", "specRef": "3.2.1", "marks": 4, "skills": ["practical"], "stem": "Produce a labelled scientific drawing of the mitochondrion in Figure 2.", "figures": ["fig-q1-fig2.jpg"]},
    {"qnum": "02.1", "specRef": "3.1.1", "marks": 1, "skills": [], "stem": "Define what a monomer is."},
    {"qnum": "02.2", "specRef": "3.1.2", "marks": 2, "skills": [], "stem": "Give one similarity and one difference between the structures of lactulose and lactose."},
    {"qnum": "02.3", "specRef": "3.2.3", "marks": 2, "skills": ["analysis"], "stem": "Use water potential to suggest why lactulose helps people suffering from constipation."},
    {"qnum": "02.4", "specRef": "3.1.8", "marks": 2, "skills": ["maths"], "stem": "Calculate the minimum percentage decrease required to bring a patient's blood H+ concentration into the normal range."},
    {"qnum": "03.1", "specRef": "3.1.5", "marks": 2, "skills": [], "stem": "Draw and label a single DNA nucleotide."},
    {"qnum": "03.2", "specRef": "3.1.5", "marks": 2, "skills": [], "stem": "Give two features of DNA and explain how each is important in semi-conservative replication."},
    {"qnum": "03.3", "specRef": "3.1.5", "marks": 1, "skills": ["maths"], "stem": "Calculate how long it takes to copy 16 500 bp mitochondrial DNA when the second strand starts after two-thirds of the first."},
    {"qnum": "04.1", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Name the prokaryotic cell structures labelled W to Z in Figure 3.", "figures": ["fig-q4-fig3.jpg"]},
    {"qnum": "04.2", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Name the main biological molecule in structures W and X of the prokaryotic cell."},
    {"qnum": "04.3", "specRef": "3.2.2", "marks": 1, "skills": [], "stem": "Name the process by which prokaryotic cells divide."},
    {"qnum": "04.4", "specRef": "3.2.2", "marks": 2, "skills": ["maths"], "stem": "Calculate the number of prokaryotic cells after 3 hours when dividing every 30 minutes."},
    {"qnum": "05.1", "specRef": "3.1.3", "marks": 2, "skills": [], "stem": "Name the molecules represented by P and Q in the triglyceride diagram (Figure 4).", "figures": ["fig-q5-fig4.jpg"]},
    {"qnum": "05.2", "specRef": "3.1.3", "marks": 1, "skills": [], "stem": "Name the type of bond between P and Q in Figure 4.", "figures": ["fig-q5-fig4.jpg"]},
    {"qnum": "05.3", "specRef": "3.1.3", "marks": 2, "skills": ["practical"], "stem": "Describe how to test a liquid sample for lipid and recognise a positive result."},
    {"qnum": "06.1", "specRef": "3.4.5", "marks": 2, "skills": [], "stem": "Explain how Figure 5 shows a hierarchical classification.", "figures": ["fig-q6-fig5.jpg"]},
    {"qnum": "06.2", "specRef": "3.4.5", "marks": 1, "skills": [], "stem": "Name the taxon to which Drosophilidae belongs.", "figures": ["fig-q6-fig5.jpg"]},
    {"qnum": "06.3", "specRef": "3.4.5", "marks": 2, "skills": ["analysis"], "stem": "Describe evidence from Figure 6 that D. erecta and D. willistoni are closely related but different species.", "figures": ["fig-q6-fig6.jpg"]},
    {"qnum": "06.4", "specRef": "3.4.5", "marks": 2, "skills": ["analysis"], "stem": "Use Figure 6 to suggest why two female D. willistoni did not attempt to mate.", "figures": ["fig-q6-fig6.jpg"]},
    {"qnum": "07.1", "specRef": "3.4.1", "marks": 1, "skills": [], "stem": "Define the proteome of a cell."},
    {"qnum": "07.2", "specRef": "3.4.2", "marks": 2, "skills": [], "stem": "Give two structural differences between mRNA and tRNA."},
    {"qnum": "07.3", "specRef": "3.4.2", "marks": 5, "skills": ["extended"], "stem": "Starting with mRNA in the cytoplasm, describe how translation produces a polypeptide."},
    {"qnum": "08.1", "specRef": "3.1.7", "marks": 2, "skills": [], "stem": "State and explain the property of water that helps buffer temperature changes."},
    {"qnum": "08.2", "specRef": "3.1.6", "marks": 1, "skills": [], "stem": "Name the two products of ATP hydrolysis."},
    {"qnum": "08.3", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Name two variables the student should have controlled in the muscle contraction ATP investigation."},
    {"qnum": "08.4", "specRef": "3.1.6", "marks": 2, "skills": ["analysis"], "stem": "Describe and explain the pattern shown in Table 1.", "figures": ["fig-q8-table1.jpg"]},
    {"qnum": "08.5", "specRef": "3.1.6", "marks": 3, "skills": ["maths"], "stem": "Calculate the energy available from ATP for muscle contraction on slide D."},
    {"qnum": "09.1", "specRef": "3.3.2", "marks": 2, "skills": [], "stem": "Describe the pathway taken by an oxygen molecule from an alveolus to the blood."},
    {"qnum": "09.2", "specRef": "3.3.2", "marks": 2, "skills": [], "stem": "Explain how one feature of an alveolus allows efficient gas exchange."},
    {"qnum": "09.3", "specRef": "3.4.7", "marks": 4, "skills": ["analysis"], "stem": "Use Figure 7 and the information provided to evaluate the politician's statement on smoking in cars.", "figures": ["fig-q9-fig7.jpg"]},
    {"qnum": "10.1", "specRef": "3.2.4", "marks": 3, "skills": ["analysis"], "stem": "Suggest how pathogenic bacteria could trigger intestinal swelling in Crohn's disease."},
    {"qnum": "10.2", "specRef": "3.4.1", "marks": 2, "skills": ["analysis"], "stem": "Suggest the meaning of 'a genetic tendency to Crohn's disease'."},
    {"qnum": "10.3", "specRef": "3.2.4", "marks": 2, "skills": ["analysis"], "stem": "Suggest why 5-ASA is only effective in controlling swelling in some people with Crohn's disease."},
    {"qnum": "10.4", "specRef": "3.1.5", "marks": 3, "skills": ["analysis"], "stem": "Suggest why 6-MP can be used to control symptoms of Crohn's disease."},
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
