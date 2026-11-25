import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599464407_3bc9f2a3.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599464482_275b58b6.pdf"

PAPER_ID = "2020-june-7402-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2020,
    "series": "June",
    "unit": "7402/2",
    "level": "A-Level",
    "date": "2020-06-11",
    "title": "AQA A-Level Biology Paper 2 (7402/2) June 2020",
    "totalMarks": 91,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 45, "y0": 98, "x1": 540, "y1": 335},
    {"filename": "fig-q3-fig2.jpg", "page": 7, "x0": 45, "y0": 64, "x1": 540, "y1": 408},
    {"filename": "fig-q7-fig4.jpg", "page": 16, "x0": 45, "y0": 64, "x1": 540, "y1": 552},
    {"filename": "fig-q10-passage.jpg", "page": 24, "x0": 45, "y0": 64, "x1": 540, "y1": 350},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 2, "specRef": "3.6.3", "summary": "Suggest and explain how the interaction between the muscles labelled in Figure 1 could cause the pupil to constrict.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.2", "page": 3, "marks": 3, "specRef": "3.6.1.2", "summary": "Explain how the fovea enables an eagle to see its prey in detail without referring to colour vision.", "figures": []},
    {"qnum": "01.3", "page": 3, "marks": 2, "specRef": "3.6.1.2", "summary": "Calculate the area of the human fovea as a percentage of the area of the retina.", "figures": []},
    {"qnum": "01.4", "page": 4, "marks": 3, "specRef": "3.6.1.2", "summary": "Explain how a high density of rod cells enables an owl to hunt its prey at night without referring to rhodopsin.", "figures": []},

    {"qnum": "02.1", "page": 5, "marks": 2, "specRef": "3.2.3", "summary": "Explain why hydrophobic steroid hormones can rapidly enter a cell by passing through its cell-surface membrane.", "figures": []},
    {"qnum": "02.2", "page": 5, "marks": 2, "specRef": "3.1.4.1", "summary": "Suggest and explain why testosterone binds to a specific androgen receptor (AR).", "figures": []},
    {"qnum": "02.3", "page": 6, "marks": 2, "specRef": "3.8.2.2", "summary": "Suggest how the androgen receptor could stimulate gene expression.", "figures": []},
    {"qnum": "02.4", "page": 6, "marks": 3, "specRef": "3.4.7", "summary": "State what can be concluded from the statistical P-value data in Table 1 on CAG repeats and prostate cancer.", "figures": []},

    {"qnum": "03.1", "page": 7, "marks": 2, "specRef": "3.5.3", "summary": "Other than the thermometer, explain how two features of the calorimeter in Figure 2 enable a valid measurement.", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "03.2", "page": 8, "marks": 2, "specRef": "3.5.3", "summary": "Calculate the heat energy released in kJ per g of biomass from the calorimeter measurements.", "figures": []},
    {"qnum": "03.3", "page": 8, "marks": 2, "specRef": "3.5.3", "summary": "Suggest two reasons why most of the light falling on producers in natural ecosystems is not used in photosynthesis.", "figures": []},
    {"qnum": "03.4", "page": 9, "marks": 2, "specRef": "3.5.1", "summary": "Name the two products of the light-dependent reaction that are required for the light-independent reaction.", "figures": []},
    {"qnum": "03.5", "page": 9, "marks": 2, "specRef": "3.7.2", "summary": "Calculate in standard form the number of Chlorella cells in the culture after 24 hours.", "figures": []},

    {"qnum": "04.1", "page": 10, "marks": 3, "specRef": "3.6.3", "summary": "Explain the banding pattern of a single sarcomere shown in Figure 3.", "figures": []},
    {"qnum": "04.2", "page": 11, "marks": 4, "specRef": "RP", "summary": "Describe how you could produce a calibration curve for creatinine using a colorimeter.", "figures": []},
    {"qnum": "04.3", "page": 12, "marks": 2, "specRef": "RP", "summary": "Describe how you would determine the concentration of creatinine in a urine sample using your calibration curve.", "figures": []},

    {"qnum": "05", "page": 13, "marks": 5, "specRef": "3.6.2.2", "summary": "Describe the sequence of events involved in transmission across a cholinergic synapse.", "figures": []},

    {"qnum": "06.1", "page": 14, "marks": 2, "specRef": "3.4.3", "summary": "Give two causes of genetic variation in organisms other than mutation.", "figures": []},
    {"qnum": "06.2", "page": 14, "marks": 1, "specRef": "3.7.1", "summary": "Name the relationship between the two alleles that code for flower colour.", "figures": []},
    {"qnum": "06.3", "page": 15, "marks": 3, "specRef": "3.7.1", "summary": "Complete the genetic diagram for a dwarf, pink-flowered plant crossed with a heterozygous tall, white-flowered plant.", "figures": []},
    {"qnum": "06.4", "page": 15, "marks": 2, "specRef": "3.7.2", "summary": "Use the Hardy-Weinberg equation to calculate the percentage of pink-flowered plants given 9% red-flowered plants.", "figures": []},

    {"qnum": "07.1", "page": 16, "marks": 1, "specRef": "3.5.4", "summary": "Calculate how many times greater the mean growth rate per day was using 37.5 g potassium nitrate than ammonium sulfate (Figure 4).", "figures": ["fig-q7-fig4.jpg"]},
    {"qnum": "07.2", "page": 17, "marks": 5, "specRef": "3.5.4", "summary": "Using all the information in Figure 4, evaluate the effect on plant growth of adding the different fertilisers to the soil.", "figures": ["fig-q7-fig4.jpg"]},
    {"qnum": "07.3", "page": 17, "marks": 2, "specRef": "3.5.3", "summary": "Suggest what the scientist should do to ensure that all water has been removed when determining dry mass.", "figures": []},

    {"qnum": "08.1", "page": 18, "marks": 2, "specRef": "3.6.4.3", "summary": "Suggest how Alport syndrome (AS) could cause proteinuria.", "figures": []},
    {"qnum": "08.2", "page": 18, "marks": 1, "specRef": "3.7.1", "summary": "Tick where a sex-linked mutation would be located in a male with Alport syndrome.", "figures": []},
    {"qnum": "08.3", "page": 19, "marks": 4, "specRef": "3.8.2.3", "summary": "Using all the information in Table 2, evaluate the use of stem cells to treat Alport syndrome in humans.", "figures": []},
    {"qnum": "08.4", "page": 20, "marks": 2, "specRef": "3.8.2.3", "summary": "Suggest how the transplanted stem cells reduce proteinuria.", "figures": []},

    {"qnum": "09.1", "page": 22, "marks": 2, "specRef": "3.8.4.1", "summary": "Describe how enzymes could be used to insert the GH gene into a plasmid.", "figures": []},
    {"qnum": "09.2", "page": 22, "marks": 2, "specRef": "3.8.4.1", "summary": "Suggest and explain how delayed insertion of the GH gene could produce offspring without the desired characteristic.", "figures": []},
    {"qnum": "09.3", "page": 23, "marks": 2, "specRef": "3.4.7", "summary": "Using Table 3, state what can be concluded about the effectiveness of the GH gene on zebrafish growth.", "figures": []},
    {"qnum": "09.4", "page": 23, "marks": 2, "specRef": "3.4.7", "summary": "Explain how two features of the investigation design helped ensure the validity of conclusions.", "figures": []},

    {"qnum": "10.1", "page": 24, "marks": 3, "specRef": "3.5.2", "summary": "Suggest and explain how black bears can hibernate for up to 7 months without food or water (lines 1-2).", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.2", "page": 25, "marks": 4, "specRef": "3.6.1.3", "summary": "Use your knowledge of nervous control of heart rate to describe how decreased heart rate and metabolic rate are linked (lines 3-5).", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.3", "page": 25, "marks": 2, "specRef": "3.5.2", "summary": "Suggest and explain how uncoupling proteins help maintain a constant body temperature during hibernation (lines 6-7).", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.4", "page": 26, "marks": 2, "specRef": "3.7.3", "summary": "Suggest and explain how climatic change has reduced the survival rate of snowshoe hares in mountain habitats (lines 11-13).", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.5", "page": 26, "marks": 4, "specRef": "3.4.4", "summary": "Explain how moulting at different times could ensure the survival of snowshoe hare populations (line 15).", "figures": ["fig-q10-passage.jpg"]},
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
        json.dump(db, f, indent=2, ensure_ascii=False)

    print(f"Ingested {len(QUESTIONS)} questions ({PAPER_META['totalMarks']} marks) for {PAPER_ID}")


if __name__ == "__main__":
    main()
