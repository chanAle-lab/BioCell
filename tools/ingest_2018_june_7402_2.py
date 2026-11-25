import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599387428_e87b790c.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599388497_740e6533.pdf"

PAPER_ID = "2018-june-7402-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2018,
    "series": "June",
    "unit": "7402/2",
    "level": "A-Level",
    "date": "2018-06-11",
    "title": "AQA A-Level Biology Paper 2 (7402/2) June 2018",
    "totalMarks": 91,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q3-fig3.jpg", "page": 6, "x0": 100, "y0": 66, "x1": 525, "y1": 475},
    {"filename": "fig-q4-fig5.jpg", "page": 10, "x0": 62, "y0": 66, "x1": 540, "y1": 402},
    {"filename": "fig-q4-fig6.jpg", "page": 12, "x0": 100, "y0": 66, "x1": 540, "y1": 398},
    {"filename": "fig-q5-table1.jpg", "page": 14, "x0": 110, "y0": 66, "x1": 535, "y1": 495},
    {"filename": "fig-q6-fig7-table3.jpg", "page": 18, "x0": 110, "y0": 260, "x1": 538, "y1": 698},
    {"filename": "fig-q8-fig8.jpg", "page": 22, "x0": 110, "y0": 170, "x1": 520, "y1": 655},
    {"filename": "fig-q10-passage.jpg", "page": 28, "x0": 110, "y0": 64, "x1": 535, "y1": 425},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 2, "specRef": "3.5.1", "summary": "Explain why a decrease in the light-dependent reaction due to heat stress decreases the light-independent reaction.", "figures": []},
    {"qnum": "01.2", "page": 2, "marks": 2, "specRef": "3.5.1", "summary": "Explain why a decrease in rubisco activity would limit the rate of photosynthesis.", "figures": []},
    {"qnum": "01.3", "page": 2, "marks": 1, "specRef": "3.5.1", "summary": "State precisely where rubisco is found in a cell.", "figures": []},
    {"qnum": "01.4", "page": 3, "marks": 4, "specRef": "3.5.1", "summary": "Evaluate the conclusion that heat stress reduces rubisco activity by affecting rubisco activase using Figures 1 and 2.", "figures": []},

    {"qnum": "02.1", "page": 4, "marks": 1, "specRef": "3.4.3", "summary": "Tick the statement that describes incorrectly the effect of a mutation in an exon.", "figures": []},
    {"qnum": "02.2", "page": 4, "marks": 3, "specRef": "3.8.2.3", "summary": "Describe how alterations to tumour suppressor genes can lead to the development of tumours.", "figures": []},
    {"qnum": "02.3", "page": 5, "marks": 2, "specRef": "3.2.2", "summary": "Calculate in standard form how many tumour cells are present after 4 weeks if one cell divides every 8 hours.", "figures": []},

    {"qnum": "03.1", "page": 6, "marks": 1, "specRef": "RP", "summary": "Suggest why the student left the yeast respiration apparatus in Figure 3 for one hour at constant temperature.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.2", "page": 7, "marks": 2, "specRef": "3.5.2", "summary": "Explain why the coloured liquid in Figure 3 moved to the right.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.3", "page": 7, "marks": 2, "specRef": "RP", "summary": "Calculate the volume of gas produced in cm^3 hour^-1 from the capillary tubing movement.", "figures": []},
    {"qnum": "03.4", "page": 8, "marks": 1, "specRef": "3.7.4", "summary": "Explain why a log scale is used to record yeast cell numbers in Figure 4.", "figures": []},
    {"qnum": "03.5", "page": 8, "marks": 1, "specRef": "3.7.4", "summary": "Suggest one reason why many yeast cells die during the death phase in Figure 4.", "figures": []},
    {"qnum": "03.6", "page": 9, "marks": 2, "specRef": "3.7.4", "summary": "Use X_t = X_0 e^(rt) to calculate the predicted yeast population after 10 hours.", "figures": []},

    {"qnum": "04.1", "page": 10, "marks": 3, "specRef": "RP", "summary": "Describe how to determine the mean percentage cover for beach grass on a sand dune.", "figures": ["fig-q4-fig5.jpg"]},
    {"qnum": "04.2", "page": 11, "marks": 4, "specRef": "3.7.4", "summary": "Use Figure 5 to explain why scientists concluded the sand dune results were due to succession.", "figures": ["fig-q4-fig5.jpg"]},
    {"qnum": "04.3", "page": 12, "marks": 1, "specRef": "3.7.4", "summary": "Use Figure 5 to explain the sunlight results in Figure 6.", "figures": ["fig-q4-fig5.jpg", "fig-q4-fig6.jpg"]},
    {"qnum": "04.4", "page": 12, "marks": 2, "specRef": "3.5.3", "summary": "Use Figure 6 to conclude about net primary productivity (NPP) in sand dunes older than 1000 years.", "figures": ["fig-q4-fig6.jpg"]},

    {"qnum": "05.1", "page": 14, "marks": 2, "specRef": "3.6.4.3", "summary": "Suggest and explain one reason why all volunteers were given the same food for 3 days.", "figures": ["fig-q5-table1.jpg"]},
    {"qnum": "05.2", "page": 15, "marks": 2, "specRef": "3.6.4.3", "summary": "Use Table 1 to conclude the effectiveness of furosemide and CVT in removing excess fluid.", "figures": ["fig-q5-table1.jpg"]},
    {"qnum": "05.3", "page": 15, "marks": 1, "specRef": "3.6.4.3", "summary": "Suggest how furosemide causes a decrease in blood pressure.", "figures": []},
    {"qnum": "05.4", "page": 15, "marks": 3, "specRef": "3.6.4.3", "summary": "Explain how inhibiting sodium and chloride ion reabsorption in nephrons increases urine volume.", "figures": []},
    {"qnum": "05.5", "page": 16, "marks": 1, "specRef": "3.6.4.3", "summary": "Use Table 2 to calculate how much greater blood flow into kidneys is with furosemide than placebo over 4 hours.", "figures": []},

    {"qnum": "06.1", "page": 18, "marks": 2, "specRef": "3.7.1", "summary": "Suggest two reasons why observed phenotypic ratios in genetic crosses often differ from expected ratios.", "figures": []},
    {"qnum": "06.2", "page": 18, "marks": 1, "specRef": "3.7.1", "summary": "Give the genotype of tomato offspring with dwarf plants and mottled leaves from Figure 7 and Table 3.", "figures": ["fig-q6-fig7-table3.jpg"]},
    {"qnum": "06.3", "page": 19, "marks": 3, "specRef": "3.7.1", "summary": "Use Figure 7 to explain the offspring numbers in Table 3.", "figures": ["fig-q6-fig7-table3.jpg"]},
    {"qnum": "06.4", "page": 19, "marks": 2, "specRef": "3.7.1", "summary": "Complete Table 4 for the expected phenotypic ratio if the two genes were unlinked.", "figures": []},

    {"qnum": "07.1", "page": 20, "marks": 3, "specRef": "3.6.2.2", "summary": "Describe how dopamine stimulates the production of nerve impulses in postsynaptic neurones.", "figures": []},
    {"qnum": "07.2", "page": 20, "marks": 2, "specRef": "3.6.2.2", "summary": "Explain how morphine, which has a similar structure to endorphins, provides pain relief.", "figures": []},
    {"qnum": "07.3", "page": 21, "marks": 3, "specRef": "3.6.2.2", "summary": "Explain how GABA causing chloride ions to enter postsynaptic neurones inhibits them.", "figures": []},

    {"qnum": "08.1", "page": 22, "marks": 1, "specRef": "3.4.2", "summary": "State what is meant by a genome.", "figures": []},
    {"qnum": "08.2", "page": 23, "marks": 2, "specRef": "3.2.4", "summary": "Explain why the antibody binds specifically to the transcription factor in Figure 8.", "figures": ["fig-q8-fig8.jpg"]},
    {"qnum": "08.3", "page": 23, "marks": 1, "specRef": "3.8.2.2", "summary": "Use Figure 8 to explain what 'precipitated DNA' consists of.", "figures": ["fig-q8-fig8.jpg"]},
    {"qnum": "08.4", "page": 23, "marks": 1, "specRef": "3.8.2.2", "summary": "Suggest how single-stranded cDNA could prevent transcription of the P34 gene.", "figures": []},
    {"qnum": "08.5", "page": 24, "marks": 2, "specRef": "3.8.4.1", "summary": "Describe the roles of two named types of enzymes used to insert DNA fragments into plasmids.", "figures": []},
    {"qnum": "08.6", "page": 24, "marks": 2, "specRef": "3.8.4.1", "summary": "Suggest two features of different proteins that enable separation by gel electrophoresis.", "figures": []},

    {"qnum": "09.1", "page": 26, "marks": 4, "specRef": "3.7.3", "summary": "Describe how farming cattle as a source of milk could have led to an increase in lactase persistence (LP).", "figures": []},
    {"qnum": "09.2", "page": 26, "marks": 2, "specRef": "3.7.1", "summary": "Explain why the number of people showing lactase persistence would rapidly increase once selection was established.", "figures": []},
    {"qnum": "09.3", "page": 27, "marks": 2, "specRef": "3.8.2.2", "summary": "Suggest and explain how a mutation outside the lactase gene causes lactase persistence.", "figures": []},

    {"qnum": "10.1", "page": 28, "marks": 3, "specRef": "3.6.1.2", "summary": "Explain why people with complete achromatopsia have difficulty seeing detail.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.2", "page": 29, "marks": 2, "specRef": "3.7.2", "summary": "Use the Hardy-Weinberg equation to calculate the percentage heterozygous for complete achromatopsia on Pingelap.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.3", "page": 29, "marks": 2, "specRef": "3.7.1", "summary": "Explain why sex-linked recessive red-green colour blindness affects more men than women.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.4", "page": 30, "marks": 3, "specRef": "3.6.1.2", "summary": "Explain why people with red-green colour blindness cannot distinguish between red, green and other colours.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.5", "page": 30, "marks": 2, "specRef": "3.8.2.1", "summary": "Suggest how induced pluripotent stem cells (iPS cells) could correct red-green colour blindness.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.6", "page": 31, "marks": 3, "specRef": "3.8.4.2", "summary": "Suggest and explain advantages of iPS cells over gene therapy to correct red-green colour blindness.", "figures": ["fig-q10-passage.jpg"]},
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
