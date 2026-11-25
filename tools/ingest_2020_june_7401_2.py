"""Ingest AQA AS Biology June 2020 Paper 2 (7401/2) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598112984_dd3502cb.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598112974_9dd396df.pdf"
)

PAPER_ID = "2020-june-7401-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2020,
    "series": "June",
    "unit": "7401/2",
    "level": "AS",
    "date": "2020-05-22",
    "title": "7401/2 — AS Paper 2 (June 2020)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q3-fig1.jpg", "page": 6, "x0": 60, "y0": 324, "x1": 540, "y1": 572},
    {"filename": "fig-q4-fig3.jpg", "page": 11, "x0": 60, "y0": 92, "x1": 540, "y1": 398},
    {"filename": "fig-q6-fig4.jpg", "page": 16, "x0": 60, "y0": 140, "x1": 540, "y1": 698},
    {"filename": "fig-q7-fig5.jpg", "page": 20, "x0": 60, "y0": 110, "x1": 540, "y1": 408},
    {"filename": "fig-q8-fig6.jpg", "page": 24, "x0": 60, "y0": 128, "x1": 540, "y1": 554},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 2, "01.4": 3,
    "02.1": 4, "02.2": 4, "02.3": 4, "02.4": 5,
    "03.1": 6, "03.2": 7, "03.3": 8, "03.4": 8,
    "04.1": 9, "04.2": 9, "04.3": 10, "04.4": 11,
    "05.1": 14, "05.2": 14, "05.3": 15, "05.4": 15,
    "06.1": 17, "06.2": 17, "06.3": 17, "06.4": 18, "06.5": 18,
    "07.1": 19, "07.2": 20,
    "08.1": 22, "08.2": 23, "08.3": 24, "08.4": 25,
    "09.1": 26, "09.2": 27,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.4.7", "marks": 2, "skills": ["practical"], "stem": "Give two ways to ensure snail shell height samples provide a reliable measure of variation in each population."},
    {"qnum": "01.2", "specRef": "3.4.7", "marks": 1, "skills": ["maths"], "stem": "Give two other statistical values besides median, mode, and range that could be calculated from shell height measurements."},
    {"qnum": "01.3", "specRef": "3.4.5", "marks": 1, "skills": [], "stem": "Name the taxon in the hierarchy of classification represented by Littorina and littorea."},
    {"qnum": "01.4", "specRef": "3.4.7", "marks": 2, "skills": ["maths"], "stem": "Give a suitable null hypothesis and name the statistical test to test for a significant difference in shell height."},
    {"qnum": "02.1", "specRef": "3.1.5", "marks": 2, "skills": [], "stem": "Describe how a phosphodiester bond is formed between two nucleotides within a DNA molecule."},
    {"qnum": "02.2", "specRef": "3.1.5", "marks": 2, "skills": ["maths"], "stem": "Calculate the maximum number of amino acids coded by a gene with 168 guanine bases using G = 4(A + T) - C."},
    {"qnum": "02.3", "specRef": "3.4.1", "marks": 1, "skills": [], "stem": "Name the protein associated with DNA in a chromosome."},
    {"qnum": "02.4", "specRef": "3.1.5", "marks": 2, "skills": [], "stem": "Describe how the separation of DNA strands occurs during semi-conservative replication."},
    {"qnum": "03.1", "specRef": "3.3.4", "marks": 2, "skills": [], "stem": "Explain how an arteriole can reduce the blood flow into capillaries."},
    {"qnum": "03.2", "specRef": "3.3.4", "marks": 4, "skills": ["analysis"], "stem": "Conclude heart muscle activity and blood movement from the appearance of heart valves in Figure 1.", "figures": ["fig-q3-fig1.jpg"]},
    {"qnum": "03.3", "specRef": "3.3.4", "marks": 1, "skills": [], "stem": "Tick the box next to the blood vessel carrying blood at the lowest blood pressure."},
    {"qnum": "03.4", "specRef": "3.3.4", "marks": 2, "skills": ["maths"], "stem": "Calculate the athlete's heart rate after exercise to 2 significant figures using Table 1."},
    {"qnum": "04.1", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Give one way to ensure the first three beetroot cylinders were kept at 25 C throughout the experiment."},
    {"qnum": "04.2", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Give two variables the student did not control in the beetroot pigment permeability procedure."},
    {"qnum": "04.3", "specRef": "RP", "marks": 2, "skills": ["maths", "practical"], "stem": "Find the uncertainty of reading 10 cm3 with the Figure 2 measuring cylinder and suggest how to reduce it."},
    {"qnum": "04.4", "specRef": "3.2.3", "marks": 4, "skills": ["analysis"], "stem": "Conclude and explain the damage caused to beetroot cells by water, ethanol, HCl, and temperature in Figure 3.", "figures": ["fig-q4-fig3.jpg"]},
    {"qnum": "05.1", "specRef": "RP", "marks": 2, "skills": ["practical"], "stem": "Draw a results table with completed column headings for the amylase starch hydrolysis investigation."},
    {"qnum": "05.2", "specRef": "3.1.4", "marks": 1, "skills": ["analysis"], "stem": "Describe the expected results for time to hydrolyse starch as starch concentration increases."},
    {"qnum": "05.3", "specRef": "3.1.4", "marks": 3, "skills": [], "stem": "Explain how a competitive inhibitor decreases the rate of an enzyme-controlled reaction."},
    {"qnum": "05.4", "specRef": "3.3.3", "marks": 3, "skills": ["analysis"], "stem": "Suggest how eating stale bread containing retrograded starch (a competitive inhibitor of amylase) reduces weight gain."},
    {"qnum": "06.1", "specRef": "3.4.4", "marks": 2, "skills": ["maths"], "stem": "Use Figure 4 and its linear equation to calculate the median mass of trout after 195 days' feeding.", "figures": ["fig-q6-fig4.jpg"]},
    {"qnum": "06.2", "specRef": "3.2.2", "marks": 2, "skills": [], "stem": "Complete Table 2 showing chromosome numbers and DNA mass in trout nuclei at prophase, telophase, and in an egg cell."},
    {"qnum": "06.3", "specRef": "3.4.3", "marks": 1, "skills": [], "stem": "Give one reason why trout eggs produced by meiosis are genetically different."},
    {"qnum": "06.4", "specRef": "3.4.3", "marks": 1, "skills": ["maths"], "stem": "Give the number of chromosomes in body cells of offspring from a diploid egg cell and normal male trout."},
    {"qnum": "06.5", "specRef": "3.4.3", "marks": 2, "skills": ["analysis"], "stem": "Suggest and explain why triploid offspring produced from farmed trout are sterile."},
    {"qnum": "07.1", "specRef": "3.2.4", "marks": 3, "skills": [], "stem": "Explain how HIV affects the production of antibodies when AIDS develops in a person."},
    {"qnum": "07.2", "specRef": "3.2.4", "marks": 5, "skills": ["analysis"], "stem": "Use Figure 5 to evaluate the effectiveness of the drug in treating AIDS.", "figures": ["fig-q7-fig5.jpg"]},
    {"qnum": "08.1", "specRef": "3.3.4", "marks": 2, "skills": ["maths"], "stem": "Calculate the percentage error of the mean phloem pressure from the nine readings in Table 3."},
    {"qnum": "08.2", "specRef": "3.3.4", "marks": 3, "skills": [], "stem": "Use the mass flow hypothesis to explain how pressure is generated inside a phloem tube."},
    {"qnum": "08.3", "specRef": "3.3.4", "marks": 1, "skills": ["analysis"], "stem": "Describe the relationship between phloem pressure and rate of water movement in xylem in Figure 6.", "figures": ["fig-q8-fig6.jpg"]},
    {"qnum": "08.4", "specRef": "3.3.4", "marks": 3, "skills": ["analysis"], "stem": "Use Figure 6, transpiration, and mass flow to explain why phloem pressure falls during the hottest part of the day.", "figures": ["fig-q8-fig6.jpg"]},
    {"qnum": "09.1", "specRef": "3.3.3", "marks": 5, "skills": ["extended"], "stem": "Describe the processes involved in the absorption and transport of digested lipid molecules from the ileum into lymph vessels."},
    {"qnum": "09.2", "specRef": "3.1.4", "marks": 5, "skills": ["extended"], "stem": "Describe how the structure of a protein depends on the amino acids it contains."},
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
