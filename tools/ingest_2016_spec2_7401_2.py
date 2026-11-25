"""Ingest AQA AS Biology Specimen Paper (Set 2) Paper 2 (7401/2) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598666428_0e40819f.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598666434_5b1c729c.pdf"
)

PAPER_ID = "2016-specimen-set2-7401-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "Specimen (Set 2)",
    "unit": "7401/2",
    "level": "AS",
    "date": "2016-01-01",
    "title": "7401/2 — AS Paper 2 (Specimen Set 2)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 60, "y0": 180, "x1": 545, "y1": 395},
    {"filename": "fig-q1-table1.jpg", "page": 3, "x0": 60, "y0": 114, "x1": 545, "y1": 230},
    {"filename": "fig-q2-fig2.jpg", "page": 4, "x0": 60, "y0": 102, "x1": 545, "y1": 405},
    {"filename": "fig-q3-fig3.jpg", "page": 6, "x0": 60, "y0": 102, "x1": 545, "y1": 325},
    {"filename": "fig-q3-table1.jpg", "page": 7, "x0": 60, "y0": 104, "x1": 545, "y1": 218},
    {"filename": "fig-q5-fig5.jpg", "page": 10, "x0": 60, "y0": 442, "x1": 545, "y1": 740},
    {"filename": "fig-q5-fig6.jpg", "page": 11, "x0": 60, "y0": 414, "x1": 545, "y1": 626},
    {"filename": "fig-q6-fig7.jpg", "page": 12, "x0": 60, "y0": 126, "x1": 545, "y1": 394},
    {"filename": "fig-q7-fig8.jpg", "page": 15, "x0": 60, "y0": 154, "x1": 545, "y1": 476},
    {"filename": "fig-q8-table4.jpg", "page": 16, "x0": 60, "y0": 140, "x1": 545, "y1": 544},
    {"filename": "fig-q9-table5.jpg", "page": 19, "x0": 60, "y0": 142, "x1": 545, "y1": 392},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 3, "01.4": 3, "01.5": 3,
    "02.1": 4, "02.2": 4, "02.3": 5,
    "03.1": 6, "03.2": 6, "03.3": 6, "03.4": 7, "03.5": 7, "03.6": 8,
    "04.1": 9, "04.2": 9,
    "05.1": 10, "05.2": 11, "05.3": 11,
    "06.1": 12, "06.2": 13,
    "07.1": 14, "07.2": 14, "07.3": 14, "07.4": 15,
    "08.1": 16, "08.2": 17, "08.3": 17,
    "09.1": 18, "09.2": 18, "09.3": 19, "09.4": 19, "09.5": 20,
    "10.1": 21, "10.2": 22,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.1.4", "marks": 1, "skills": [], "stem": "Explain why Milk B contains glucose after passing through the lactase gel bead column (Figure 1).", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.2", "specRef": "3.1.4", "marks": 1, "skills": ["practical"], "stem": "Suggest one advantage of trapping the enzyme lactase within gel beads (Figure 1).", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.3", "specRef": "3.1.4", "marks": 1, "skills": ["analysis"], "stem": "Explain the difference in Milk B glucose concentration at 50 vs 100 cm3 min^-1 flow rate in Table 1.", "figures": ["fig-q1-table1.jpg"]},
    {"qnum": "01.4", "specRef": "3.1.4", "marks": 1, "skills": ["maths"], "stem": "Calculate the volume in mm3 of a spherical gel bead with a 3.0 mm diameter."},
    {"qnum": "01.5", "specRef": "3.1.4", "marks": 2, "skills": [], "stem": "Explain how galactose inhibits the enzyme lactase."},
    {"qnum": "02.1", "specRef": "3.2.1", "marks": 1, "skills": ["maths"], "stem": "Calculate the magnification of the bacterium image using the 0.5 um scale bar in Figure 2.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.2", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Complete Table 2 comparing features of a bacterium and a virus."},
    {"qnum": "02.3", "specRef": "3.1.5", "marks": 2, "skills": [], "stem": "Give two ways in which DNA nucleotides differ from RNA nucleotides."},
    {"qnum": "03.1", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Explain why the student did not add a buffer to the lipase solution in Figure 3.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.2", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Give two variables the student would have controlled in the lipase lipid hydrolysis investigation.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.3", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Give a suitable control for the lipase lipid hydrolysis investigation.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.4", "specRef": "3.1.4", "marks": 2, "skills": ["maths"], "stem": "Draw a tangent on Figure 4 and calculate the rate of pH change at 5 minutes.", "figures": ["fig-q3-table1.jpg"]},
    {"qnum": "03.5", "specRef": "3.1.4", "marks": 2, "skills": ["analysis"], "stem": "Explain the shape of the pH curve over time in Figure 4."},
    {"qnum": "03.6", "specRef": "3.1.4", "marks": 3, "skills": ["analysis"], "stem": "Describe and explain the expected pH results when repeating the experiment with a higher lipase concentration."},
    {"qnum": "04.1", "specRef": "3.4.2", "marks": 2, "skills": [], "stem": "Explain why transcription produces pre-mRNA in eukaryotes but mRNA directly in prokaryotes."},
    {"qnum": "04.2", "specRef": "3.4.2", "marks": 2, "skills": [], "stem": "Give two differences between the structure of mRNA and the structure of tRNA."},
    {"qnum": "05.1", "specRef": "3.3.4", "marks": 4, "skills": [], "stem": "Explain four ways in which the structure of the aorta is related to its function."},
    {"qnum": "05.2", "specRef": "3.3.4", "marks": 4, "skills": ["analysis"], "stem": "Use Figure 5 to explain how the haemoglobin of more active species B allows a greater level of activity.", "figures": ["fig-q5-fig5.jpg"]},
    {"qnum": "05.3", "specRef": "3.3.4", "marks": 2, "skills": ["maths"], "stem": "Use the ECG in Figure 6 and stroke volume 0.03 cm3 to calculate cardiac output per minute for species B.", "figures": ["fig-q5-fig6.jpg"]},
    {"qnum": "06.1", "specRef": "3.2.3", "marks": 5, "skills": ["analysis"], "stem": "Use Figure 7 (with and without oxygen) to conclude the processes involved in calcium ion uptake by plant cells.", "figures": ["fig-q6-fig7.jpg"]},
    {"qnum": "06.2", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Suggest one way to ensure the solutions used for curve X in Figure 7 contained no oxygen.", "figures": ["fig-q6-fig7.jpg"]},
    {"qnum": "07.1", "specRef": "3.1.2", "marks": 1, "skills": [], "stem": "Name the monomers from which a maltose molecule is made."},
    {"qnum": "07.2", "specRef": "3.1.2", "marks": 1, "skills": [], "stem": "Name the type of chemical bond joining the two monomers in maltose."},
    {"qnum": "07.3", "specRef": "RP", "marks": 2, "skills": ["maths", "practical"], "stem": "Complete Table 3 with headings, units, and the concentration of the diluted maltose solution."},
    {"qnum": "07.4", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Explain how to use the Figure 8 calibration curve to determine maltose concentration at 0.45 absorbance.", "figures": ["fig-q7-fig8.jpg"]},
    {"qnum": "08.1", "specRef": "3.4.6", "marks": 2, "skills": ["maths"], "stem": "Complete Table 4 for species richness and total number of insects (N) in each habitat.", "figures": ["fig-q8-table4.jpg"]},
    {"qnum": "08.2", "specRef": "3.4.6", "marks": 2, "skills": ["maths"], "stem": "Calculate the index of diversity (d) of the wheat field using Table 4.", "figures": ["fig-q8-table4.jpg"]},
    {"qnum": "08.3", "specRef": "3.4.6", "marks": 3, "skills": ["analysis"], "stem": "Suggest why the index of diversity of insects was higher in the hedge than in the barley field.", "figures": ["fig-q8-table4.jpg"]},
    {"qnum": "09.1", "specRef": "3.2.2", "marks": 1, "skills": [], "stem": "Name the process by which bacterial cells divide."},
    {"qnum": "09.2", "specRef": "RP", "marks": 4, "skills": ["practical"], "stem": "Describe and explain two aseptic techniques used when transferring broth culture onto an agar plate."},
    {"qnum": "09.3", "specRef": "3.2.2", "marks": 1, "skills": ["analysis"], "stem": "Identify from Table 5 which plant oil is least effective at killing L. monocytogenes at 35 C.", "figures": ["fig-q9-table5.jpg"]},
    {"qnum": "09.4", "specRef": "3.2.2", "marks": 3, "skills": ["analysis"], "stem": "Conclude from Table 5 about the effectiveness of using plant oils with refrigeration (4 C) against L. monocytogenes.", "figures": ["fig-q9-table5.jpg"]},
    {"qnum": "09.5", "specRef": "3.2.3", "marks": 1, "skills": ["analysis"], "stem": "Suggest how low temperature (4 C) slows the rate of entry of hydrophobic plant oils across bacterial membranes."},
    {"qnum": "10.1", "specRef": "3.2.2", "marks": 5, "skills": ["extended"], "stem": "Describe the appearance and behaviour of chromosomes during mitosis."},
    {"qnum": "10.2", "specRef": "3.4.3", "marks": 5, "skills": ["extended"], "stem": "Describe and explain the processes that occur during meiosis that increase genetic variation."},
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
