import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599387423_9180a146.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599388779_07943ccd.pdf"

PAPER_ID = "2018-june-7402-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2018,
    "series": "June",
    "unit": "7402/1",
    "level": "A-Level",
    "date": "2018-06-07",
    "title": "AQA A-Level Biology Paper 1 (7402/1) June 2018",
    "totalMarks": 91,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1-2.jpg", "page": 2, "x0": 85, "y0": 100, "x1": 535, "y1": 360},
    {"filename": "fig-q2-fig3.jpg", "page": 6, "x0": 95, "y0": 66, "x1": 540, "y1": 540},
    {"filename": "fig-q3-fig4.jpg", "page": 10, "x0": 75, "y0": 66, "x1": 540, "y1": 435},
    {"filename": "fig-q4-fig5.jpg", "page": 16, "x0": 95, "y0": 64, "x1": 525, "y1": 620},
    {"filename": "fig-q5-table1.jpg", "page": 20, "x0": 75, "y0": 348, "x1": 535, "y1": 728},
    {"filename": "fig-q5-table2.jpg", "page": 22, "x0": 100, "y0": 64, "x1": 520, "y1": 290},
    {"filename": "fig-q6-fig6.jpg", "page": 24, "x0": 110, "y0": 54, "x1": 540, "y1": 580},
    {"filename": "fig-q6-table3.jpg", "page": 26, "x0": 95, "y0": 64, "x1": 540, "y1": 515},
    {"filename": "fig-q7-fig8.jpg", "page": 29, "x0": 110, "y0": 64, "x1": 440, "y1": 520},
    {"filename": "fig-q8-fig9-table4.jpg", "page": 32, "x0": 65, "y0": 64, "x1": 538, "y1": 688},
    {"filename": "fig-q8-fig10.jpg", "page": 34, "x0": 85, "y0": 64, "x1": 540, "y1": 525},
    {"filename": "fig-q9-table5.jpg", "page": 38, "x0": 80, "y0": 64, "x1": 530, "y1": 485},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 2, "specRef": "3.2.2", "summary": "Give two pieces of evidence from Figure 1 that the human cell was undergoing mitosis.", "figures": []},
    {"qnum": "01.2", "page": 3, "marks": 1, "specRef": "3.2.2", "summary": "Tick the box giving the stage of mitosis shown in Figure 1.", "figures": ["fig-q1-fig1-2.jpg"]},
    {"qnum": "01.3", "page": 3, "marks": 2, "specRef": "3.2.3", "summary": "Suggest how placing the cells in a higher water potential solution moved chromosomes apart.", "figures": []},
    {"qnum": "01.4", "page": 4, "marks": 1, "specRef": "3.4.1", "summary": "Suggest one way chromosome structure differs along its length causing a striped staining appearance.", "figures": []},
    {"qnum": "01.5", "page": 4, "marks": 1, "specRef": "3.4.1", "summary": "Define a homologous pair of chromosomes (as arranged in Figure 2).", "figures": ["fig-q1-fig1-2.jpg"]},
    {"qnum": "01.6", "page": 4, "marks": 2, "specRef": "3.4.1", "summary": "Give two ways the arrangement of prokaryotic DNA differs from human DNA in Figure 1.", "figures": ["fig-q1-fig1-2.jpg"]},

    {"qnum": "02.1", "page": 7, "marks": 3, "specRef": "RP", "summary": "Describe the method used to obtain the potato cube osmosis results in Figure 3 and variables controlled.", "figures": ["fig-q2-fig3.jpg"]},
    {"qnum": "02.2", "page": 8, "marks": 3, "specRef": "3.3.1", "summary": "Calculate whether the rate of osmosis per mm^2 per minute differs between large cube A and small cubes B in Figure 3.", "figures": ["fig-q2-fig3.jpg"]},

    {"qnum": "03.1", "page": 10, "marks": 1, "specRef": "3.4.6", "summary": "State what is meant by species richness.", "figures": []},
    {"qnum": "03.2", "page": 11, "marks": 4, "specRef": "3.4.6", "summary": "Evaluate whether Figure 4 supports conclusions about natural and town habitats for bees.", "figures": ["fig-q3-fig4.jpg"]},
    {"qnum": "03.3", "page": 12, "marks": 2, "specRef": "3.4.6", "summary": "Suggest one ethical consideration and one identification consideration when collecting bees.", "figures": []},
    {"qnum": "03.4", "page": 13, "marks": 2, "specRef": "3.4.6", "summary": "Suggest and explain two ways to improve data collection in the bee biodiversity investigation.", "figures": []},
    {"qnum": "03.5", "page": 14, "marks": 2, "specRef": "3.4.5", "summary": "Explain what the binomial names of three bee species suggest about their evolutionary relationships.", "figures": []},

    {"qnum": "04.1", "page": 15, "marks": 2, "specRef": "3.1.4.2", "summary": "Explain how formation of an enzyme-substrate complex increases the rate of reaction.", "figures": []},
    {"qnum": "04.2", "page": 15, "marks": 2, "specRef": "3.1.4.2", "summary": "Calculate in standard form how many times faster amino acid removal is with the enzyme present.", "figures": []},
    {"qnum": "04.3", "page": 17, "marks": 2, "specRef": "3.1.4.2", "summary": "Calculate the rate without lyxose at 2.5 mmol dm^-3 ATP as a percentage of the maximum rate with lyxose in Figure 5.", "figures": ["fig-q4-fig5.jpg"]},
    {"qnum": "04.4", "page": 18, "marks": 3, "specRef": "3.1.4.2", "summary": "Suggest a reason for the difference in enzyme activity with and without lyxose in Figure 5.", "figures": ["fig-q4-fig5.jpg"]},

    {"qnum": "05.1", "page": 20, "marks": 1, "specRef": "3.1.4.1", "summary": "Draw the general structure of an amino acid.", "figures": []},
    {"qnum": "05.2", "page": 21, "marks": 2, "specRef": "3.4.2", "summary": "Explain what is meant by a degenerate genetic code using an example from Table 1.", "figures": ["fig-q5-table1.jpg"]},
    {"qnum": "05.3", "page": 22, "marks": 1, "specRef": "3.4.2", "summary": "Give the minimum number of bases in the gene coding for a 465-amino-acid polypeptide.", "figures": []},
    {"qnum": "05.4", "page": 23, "marks": 1, "specRef": "3.4.3", "summary": "Use Table 1 to tick the single base substitution in DNA changing Val to Ala at position 203.", "figures": ["fig-q5-table1.jpg"]},
    {"qnum": "05.5", "page": 23, "marks": 3, "specRef": "3.1.4.2", "summary": "Suggest why changing Glu to Lys at amino acid 300 had no effect whereas at 279 it reduced enzyme rate.", "figures": ["fig-q5-table1.jpg", "fig-q5-table2.jpg"]},

    {"qnum": "06.1", "page": 25, "marks": 2, "specRef": "3.4.3", "summary": "Complete Figure 7 to show chromosomes resulting from normal meiosis of the diploid cell in Figure 6.", "figures": ["fig-q6-fig6.jpg"]},
    {"qnum": "06.2", "page": 26, "marks": 2, "specRef": "3.4.3", "summary": "Complete Table 3 with expected numbers of plants producing and not producing 2n gametes after 1 cycle.", "figures": []},
    {"qnum": "06.3", "page": 27, "marks": 2, "specRef": "3.4.3", "summary": "Interpret the chi-squared result (350 vs critical value 3.841 at P=0.05) for the red clover breeding cycles.", "figures": ["fig-q6-table3.jpg"]},
    {"qnum": "06.4", "page": 27, "marks": 3, "specRef": "3.4.4", "summary": "Use directional selection to explain the results in Table 3.", "figures": ["fig-q6-table3.jpg"]},

    {"qnum": "07.1", "page": 28, "marks": 2, "specRef": "3.2.4", "summary": "Explain how antivenom works and why passive immunity is essential rather than active immunity.", "figures": []},
    {"qnum": "07.2", "page": 29, "marks": 2, "specRef": "3.2.4", "summary": "Suggest why a mixture of venoms from several snakes of the same species is used in Figure 8.", "figures": []},
    {"qnum": "07.3", "page": 30, "marks": 2, "specRef": "3.2.4", "summary": "Use a calculation to suggest whether horses (350 kg) or rabbits (2 kg) are better for antivenom production.", "figures": []},
    {"qnum": "07.4", "page": 30, "marks": 1, "specRef": "3.2.4", "summary": "Suggest one reason why animals are under ongoing veterinary observation during antivenom production in Figure 8.", "figures": ["fig-q7-fig8.jpg"]},
    {"qnum": "07.5", "page": 31, "marks": 3, "specRef": "3.2.4", "summary": "Use the humoral immune response to explain the two-dose venom vaccination programme.", "figures": []},

    {"qnum": "08.1", "page": 33, "marks": 2, "specRef": "3.3.4.2", "summary": "Explain how Figure 9 supports the conclusion that heat treatment damaged the phloem.", "figures": ["fig-q8-fig9-table4.jpg"]},
    {"qnum": "08.2", "page": 33, "marks": 2, "specRef": "3.3.4.2", "summary": "Explain how Table 4 supports the conclusion that heat treatment did not affect the xylem.", "figures": ["fig-q8-fig9-table4.jpg"]},
    {"qnum": "08.3", "page": 34, "marks": 4, "specRef": "3.3.4.2", "summary": "Conclude from Figure 10 how Fe3+ ions move in barley plants.", "figures": ["fig-q8-fig10.jpg"]},

    {"qnum": "09.1", "page": 37, "marks": 3, "specRef": "3.1.5.2", "summary": "Describe the role of two named enzymes in semi-conservative DNA replication.", "figures": []},
    {"qnum": "09.2", "page": 38, "marks": 3, "specRef": "3.1.5.2", "summary": "Suggest explanations for the DNA replication results with cyclin A treatments in Table 5.", "figures": ["fig-q9-table5.jpg"]},

    {"qnum": "10.1", "page": 40, "marks": 6, "specRef": "3.3.2", "summary": "Describe the gross structure of the human gas exchange system and how we breathe in and out.", "figures": []},
    {"qnum": "10.2", "page": 41, "marks": 5, "specRef": "3.1.3", "summary": "Compare and contrast the structure and properties of triglycerides and phospholipids.", "figures": []},
    {"qnum": "10.3", "page": 42, "marks": 4, "specRef": "3.1.2", "summary": "Describe how lactose is formed and where in the cell it is attached to a polypeptide to form a glycoprotein.", "figures": []},
]


def extract_figures():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(QP_PATH)
    for fig in FIGURES:
        page = doc[fig["page"] - 1]
        rect = fitz.Rect(fig["x0"], fig["y0"], fig["x1"], fig["y1"])
        pix = page.get_pixmap(clip=rect, matrix=fitz.Matrix(2.5, 2.5))
        out_path = IMG_DIR / fig["filename"]
        pix.save(str(out_path))
        print(f"Saved figure: {out_path}")
    doc.close()


def main():
    assert sum(q["marks"] for q in QUESTIONS) == PAPER_META["totalMarks"], "Mark sum mismatch!"
    extract_figures()
    ms_dir = IMG_DIR / "ms"
    ms_qnums = [q["qnum"] for q in QUESTIONS]
    ms_map = crop_official_markschemes(MS_PATH, ms_qnums, str(ms_dir))

    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    db["papers"] = [p for p in db["papers"] if p["id"] != PAPER_ID]
    db["questions"] = [q for q in db["questions"] if q["paper"] != PAPER_ID]
    db["papers"].append(PAPER_META)

    for q in QUESTIONS:
        qnum = q["qnum"]
        slug = qnum.replace(".", "-")
        ms_file = ms_map.get(qnum)
        if not ms_file:
            raise RuntimeError(f"Missing markscheme crop for {qnum}")
        db["questions"].append({
            "id": f"{PAPER_ID}-q{qnum}",
            "paper": PAPER_ID,
            "year": PAPER_META["year"],
            "series": PAPER_META["series"],
            "unit": PAPER_META["unit"],
            "level": PAPER_META["level"],
            "question": qnum,
            "questionNumber": qnum,
            "page": q["page"],
            "marks": q["marks"],
            "specRef": q["specRef"],
            "topics": [q["specRef"]],
            "summary": q["summary"],
            "image": f"img/{PAPER_ID}/q{slug}.jpg",
            "markscheme": f"img/{PAPER_ID}/ms/{ms_file}",
            "figures": [f"img/{PAPER_ID}/{fn}" for fn in q["figures"]],
        })

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)
    print(f"Ingested {PAPER_ID}: {len(QUESTIONS)} questions, {sum(q['marks'] for q in QUESTIONS)} marks")


if __name__ == "__main__":
    main()
