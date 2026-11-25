"""Ingest AQA AS Biology Specimen Paper (Set 2) Paper 1 (7401/1) into questions.json."""

import json
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"
QP_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598666438_0438dd47.pdf"
)
MS_PDF = Path(
    r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598666473_fb059067.pdf"
)

PAPER_ID = "2016-specimen-set2-7401-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "Specimen (Set 2)",
    "unit": "7401/1",
    "level": "AS",
    "date": "2016-01-01",
    "title": "7401/1 — AS Paper 1 (Specimen Set 2)",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-table1.jpg", "page": 2, "x0": 60, "y0": 324, "x1": 545, "y1": 448},
    {"filename": "fig-q3-table3.jpg", "page": 5, "x0": 60, "y0": 76, "x1": 545, "y1": 230},
    {"filename": "fig-q4-fig1.jpg", "page": 6, "x0": 60, "y0": 438, "x1": 545, "y1": 620},
    {"filename": "fig-q5-fig2.jpg", "page": 8, "x0": 60, "y0": 65, "x1": 545, "y1": 516},
    {"filename": "fig-q7-fig3.jpg", "page": 14, "x0": 60, "y0": 462, "x1": 545, "y1": 790},
    {"filename": "fig-q8-table5.jpg", "page": 16, "x0": 60, "y0": 152, "x1": 545, "y1": 400},
]

PAGE_MAP = {
    "01.1": 2, "01.2": 2, "01.3": 2,
    "02.1": 3, "02.2": 3,
    "03.1": 4, "03.2": 4, "03.3": 5, "03.4": 5,
    "04.1": 6, "04.2": 7, "04.3": 7,
    "05.1": 8, "05.2": 8, "05.3": 9, "05.4": 9, "05.5": 9, "05.6": 10,
    "06.1": 12, "06.2": 12, "06.3": 13,
    "07.1": 14, "07.2": 14, "07.3": 15, "07.4": 15,
    "08.1": 16, "08.2": 17, "08.3": 17,
    "09.1": 18, "09.2": 19, "09.3": 19, "09.4": 19, "09.5": 20,
}

MS_QNUM_MAP: dict[str, str] = {}

QUESTIONS = [
    {"qnum": "01.1", "specRef": "3.4.2", "marks": 2, "skills": [], "stem": "Explain the meaning of degenerate and non-overlapping as applied to the genetic code."},
    {"qnum": "01.2", "specRef": "3.1.5", "marks": 2, "skills": [], "stem": "Name the bases represented by A, C, G, and U in Table 1.", "figures": ["fig-q1-table1.jpg"]},
    {"qnum": "01.3", "specRef": "3.4.2", "marks": 1, "skills": [], "stem": "Use Table 1 to give the DNA base sequence coding for serine.", "figures": ["fig-q1-table1.jpg"]},
    {"qnum": "02.1", "specRef": "3.3.2", "marks": 2, "skills": [], "stem": "Explain two ways in which the structure of fish gills is adapted for efficient gas exchange."},
    {"qnum": "02.2", "specRef": "3.3.2", "marks": 3, "skills": [], "stem": "Explain how the counter-current mechanism in fish gills ensures maximum oxygen passes into blood."},
    {"qnum": "03.1", "specRef": "3.4.5", "marks": 2, "skills": [], "stem": "Explain what phylogenetic classification starting with Apodemus indicates about European field mice."},
    {"qnum": "03.2", "specRef": "3.4.5", "marks": 2, "skills": [], "stem": "Complete Table 2 to show the taxonomic hierarchy of the long-tailed field mouse."},
    {"qnum": "03.3", "specRef": "3.4.5", "marks": 3, "skills": ["maths", "analysis"], "stem": "Use ratios and SDs in Table 3 to evaluate whether St. Kilda and long-tailed field mice are different species.", "figures": ["fig-q3-table3.jpg"]},
    {"qnum": "03.4", "specRef": "3.4.5", "marks": 2, "skills": [], "stem": "Describe how breeding experiments could determine whether the two mouse populations are the same species."},
    {"qnum": "04.1", "specRef": "3.3.3", "marks": 3, "skills": [], "stem": "Explain how cells lining the ileum absorb glucose by co-transport with sodium ions."},
    {"qnum": "04.2", "specRef": "3.1.2", "marks": 3, "skills": ["practical"], "stem": "Complete Table 4 with expected positive biochemical test results inside and outside Visking tubing (Figure 1).", "figures": ["fig-q4-fig1.jpg"]},
    {"qnum": "04.3", "specRef": "3.2.3", "marks": 3, "skills": ["analysis"], "stem": "Justify the biochemical test results in Table 4 for the Visking tubing experiment (Figure 1).", "figures": ["fig-q4-fig1.jpg"]},
    {"qnum": "05.1", "specRef": "3.2.1", "marks": 2, "skills": [], "stem": "Name the animal cell organelles labelled B and C in Figure 2.", "figures": ["fig-q5-fig2.jpg"]},
    {"qnum": "05.2", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Name two structures present in plant cells that are not present in animal cells."},
    {"qnum": "05.3", "specRef": "3.2.1", "marks": 3, "skills": ["practical"], "stem": "Explain why the cell fractionation solution was ice-cold, buffered, and of the same water potential.", "figures": ["fig-q5-fig2.jpg"]},
    {"qnum": "05.4", "specRef": "3.2.1", "marks": 2, "skills": ["practical"], "stem": "Explain why the biologist used a blender and then filtered the liver tissue mixture."},
    {"qnum": "05.5", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Name the organelle that made up most of the first pellet after low-speed centrifugation."},
    {"qnum": "05.6", "specRef": "3.2.1", "marks": 1, "skills": [], "stem": "Suggest why the second centrifuge tube was spun at a higher speed to isolate organelle C (Figure 2).", "figures": ["fig-q5-fig2.jpg"]},
    {"qnum": "06.1", "specRef": "3.1.7", "marks": 4, "skills": [], "stem": "Give and explain two properties of water that are important in the cytoplasm of cells."},
    {"qnum": "06.2", "specRef": "3.1.8", "marks": 2, "skills": [], "stem": "Other than sodium, name one inorganic ion and give one example of its biological importance in a cell."},
    {"qnum": "06.3", "specRef": "3.2.3", "marks": 3, "skills": [], "stem": "Compare and contrast the processes by which water and inorganic ions enter cells."},
    {"qnum": "07.1", "specRef": "3.2.4", "marks": 2, "skills": [], "stem": "Define what an antigen is."},
    {"qnum": "07.2", "specRef": "3.2.4", "marks": 2, "skills": [], "stem": "Define what an antibody is."},
    {"qnum": "07.3", "specRef": "3.2.4", "marks": 1, "skills": ["maths"], "stem": "Use Figure 3 to calculate the percentage increase in mean blood antibody concentration between samples 2 and 3.", "figures": ["fig-q7-fig3.jpg"]},
    {"qnum": "07.4", "specRef": "3.2.4", "marks": 4, "skills": ["analysis"], "stem": "Explain the differences between the mean antibody concentrations in blood samples 1, 2, and 3 in Figure 3.", "figures": ["fig-q7-fig3.jpg"]},
    {"qnum": "08.1", "specRef": "3.1.4", "marks": 4, "skills": ["maths", "practical"], "stem": "Process the protease rate of hydrolysis data in Table 5 and plot it on the graph paper.", "figures": ["fig-q8-table5.jpg"]},
    {"qnum": "08.2", "specRef": "3.1.4", "marks": 4, "skills": ["analysis"], "stem": "Evaluate whether Table 5 supports the conclusion that the bacterium lives at 15 C.", "figures": ["fig-q8-table5.jpg"]},
    {"qnum": "08.3", "specRef": "RP", "marks": 1, "skills": ["practical"], "stem": "Suggest two variables the biochemist controlled in the protease temperature investigation."},
    {"qnum": "09.1", "specRef": "3.3.4", "marks": 3, "skills": ["analysis"], "stem": "Explain why phloem-sap-feeding insects can take up sap without using their jaw muscles."},
    {"qnum": "09.2", "specRef": "3.1.2", "marks": 2, "skills": ["analysis"], "stem": "Suggest the advantage to a phloem-sap-feeder of polymerising sugars into insoluble polysaccharides."},
    {"qnum": "09.3", "specRef": "3.4.4", "marks": 2, "skills": ["analysis"], "stem": "Suggest how receiving only a few gut bacteria from a parent reduces bacterial genetic diversity."},
    {"qnum": "09.4", "specRef": "3.4.7", "marks": 2, "skills": ["practical"], "stem": "Other than environmental factors, give two features to control when comparing insect feeding effects on plant growth."},
    {"qnum": "09.5", "specRef": "3.4.7", "marks": 1, "skills": ["practical"], "stem": "Outline a method by which you could find the area of a plant leaf."},
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
