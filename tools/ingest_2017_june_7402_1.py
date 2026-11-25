import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598917833_5fb12112.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598917778_867ac632.pdf"

PAPER_ID = "2017-june-7402-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2017,
    "series": "June",
    "unit": "7402/1",
    "level": "A-Level",
    "date": "2017-06-12",
    "title": "AQA A-Level Biology Paper 1 (7402/1) June 2017",
    "totalMarks": 91,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q3-table2.jpg", "page": 7, "x0": 115, "y0": 66, "x1": 540, "y1": 420},
    {"filename": "fig-q4-fig1.jpg", "page": 10, "x0": 90, "y0": 268, "x1": 530, "y1": 730},
    {"filename": "fig-q5-fig2.jpg", "page": 14, "x0": 100, "y0": 66, "x1": 525, "y1": 642},
    {"filename": "fig-q6-table3.jpg", "page": 18, "x0": 115, "y0": 66, "x1": 540, "y1": 518},
    {"filename": "fig-q9-fig4.jpg", "page": 26, "x0": 115, "y0": 66, "x1": 540, "y1": 415},
    {"filename": "fig-q9-fig5.jpg", "page": 28, "x0": 115, "y0": 66, "x1": 520, "y1": 625},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 1, "specRef": "3.2.1.1", "summary": "Give the two types of molecule from which a ribosome is made.", "figures": []},
    {"qnum": "01.2", "page": 2, "marks": 3, "specRef": "3.4.2", "summary": "Describe the role of a ribosome in the production of a polypeptide (excluding transcription).", "figures": []},
    {"qnum": "01.3", "page": 3, "marks": 1, "specRef": "3.4.2", "summary": "Complete Table 1 with the DNA base sequence from which the pre-mRNA was transcribed.", "figures": []},
    {"qnum": "01.4", "page": 3, "marks": 2, "specRef": "3.4.2", "summary": "Explain why the base sequence of eukaryotic mRNA might differ from pre-mRNA.", "figures": []},

    {"qnum": "02.1", "page": 4, "marks": 2, "specRef": "3.1.2", "summary": "Describe the structure of glycogen.", "figures": []},
    {"qnum": "02.2", "page": 4, "marks": 2, "specRef": "3.1.2", "summary": "Suggest how glycogen in cells lining the uterus acts as a source of energy for the embryo.", "figures": []},
    {"qnum": "02.3", "page": 5, "marks": 2, "specRef": "3.2.3", "summary": "Suggest and explain two ways cell-surface membranes of uterus lining cells are adapted for rapid nutrient transport.", "figures": []},
    {"qnum": "02.4", "page": 5, "marks": 2, "specRef": "3.2.2", "summary": "Calculate the mean volume of each embryo cell after 3 days in standard form.", "figures": []},

    {"qnum": "03.1", "page": 6, "marks": 3, "specRef": "3.2.3", "summary": "Suggest how the carrier protein NHE3 actively transports one sodium ion into a gut cell in exchange for one proton out.", "figures": []},
    {"qnum": "03.2", "page": 7, "marks": 4, "specRef": "3.2.3", "summary": "Use Table 2 and water potential to explain how scientists concluded Tenapanor reduced salt absorption in the gut.", "figures": []},
    {"qnum": "03.3", "page": 8, "marks": 2, "specRef": "3.3.4.1", "summary": "Explain how high salt concentration in blood plasma entering capillaries can lead to a build-up of tissue fluid.", "figures": []},

    {"qnum": "04.1", "page": 10, "marks": 2, "specRef": "3.2.2", "summary": "Describe how bacteria divide.", "figures": []},
    {"qnum": "04.2", "page": 10, "marks": 4, "specRef": "3.1.4.2", "summary": "Explain the shape of the protease activity curves at 50 °C and 60 °C in Figure 1.", "figures": ["fig-q4-fig1.jpg"]},
    {"qnum": "04.3", "page": 11, "marks": 2, "specRef": "3.3.3", "summary": "Suggest and explain one advantage to a bacterium of secreting an extracellular protease.", "figures": []},
    {"qnum": "04.4", "page": 12, "marks": 2, "specRef": "3.3.3", "summary": "Describe the action of membrane-bound dipeptidases in mammals and explain their importance.", "figures": []},

    {"qnum": "05.1", "page": 13, "marks": 1, "specRef": "3.1.6", "summary": "Tick the equation representing the reaction catalysed by ATP synthase.", "figures": []},
    {"qnum": "05.2", "page": 13, "marks": 1, "specRef": "3.1.4.2", "summary": "Suggest why the new antibiotic inhibits bacterial ATP synthase but not human ATP synthase.", "figures": []},
    {"qnum": "05.3", "page": 14, "marks": 2, "specRef": "3.4.4", "summary": "Calculate the daily antibiotic dose in mg for a 30 g mouse at 25 mg kg^-1 per day.", "figures": ["fig-q5-fig2.jpg"]},
    {"qnum": "05.4", "page": 15, "marks": 2, "specRef": "3.4.4", "summary": "Calculate the percentage difference in actual bacterial numbers in group A compared with group R using Figure 2.", "figures": ["fig-q5-fig2.jpg"]},
    {"qnum": "05.5", "page": 16, "marks": 3, "specRef": "3.4.4", "summary": "Use Figure 2 and evolution of antibiotic resistance to explain why patients should be treated with both antibiotics.", "figures": ["fig-q5-fig2.jpg"]},

    {"qnum": "06.1", "page": 18, "marks": 2, "specRef": "3.2.3", "summary": "Give three environmental variables that should be controlled when growing wheat and wild oat plants.", "figures": ["fig-q6-table3.jpg"]},
    {"qnum": "06.2", "page": 19, "marks": 4, "specRef": "3.2.3", "summary": "Evaluate the use of 2,4-D as a herbicide on a wheat crop containing wild oats using Table 3.", "figures": ["fig-q6-table3.jpg"]},
    {"qnum": "06.3", "page": 20, "marks": 2, "specRef": "3.2.3", "summary": "Suggest one reason why leaf disc flasks were kept at constant temperature and one reason why they were shaken.", "figures": []},

    {"qnum": "07.1", "page": 22, "marks": 3, "specRef": "3.2.4", "summary": "Describe how phagocytosis of a virus leads to presentation of its antigens.", "figures": []},
    {"qnum": "07.2", "page": 22, "marks": 3, "specRef": "3.2.4", "summary": "Describe how presentation of a virus antigen leads to the secretion of an antibody against it.", "figures": []},
    {"qnum": "07.3", "page": 23, "marks": 2, "specRef": "3.2.4", "summary": "Suggest how the immune response to a viral protein similar to human collagen can result in rheumatoid arthritis.", "figures": []},

    {"qnum": "08.1", "page": 24, "marks": 2, "specRef": "3.4.5", "summary": "State what classifications X and Y in Figure 3 suggest about evolutionary relationships between the three snake species.", "figures": []},
    {"qnum": "08.2", "page": 25, "marks": 1, "specRef": "3.4.5", "summary": "Complete Table 4 with the missing hierarchical taxa for the snakes.", "figures": []},
    {"qnum": "08.3", "page": 25, "marks": 1, "specRef": "3.4.5", "summary": "Give the name of the taxon about which scientists disagree in Liasis papuana vs Apodora papuana.", "figures": []},
    {"qnum": "08.4", "page": 25, "marks": 3, "specRef": "3.4.7", "summary": "State three comparisons of genetic diversity used to generate Classification Y.", "figures": []},

    {"qnum": "09.1", "page": 26, "marks": 3, "specRef": "3.3.2", "summary": "Explain three ways in which an insect's tracheal system is adapted for efficient gas exchange.", "figures": []},
    {"qnum": "09.2", "page": 27, "marks": 2, "specRef": "3.3.2", "summary": "Explain how the presence of gills adapts the predatory damselfly larva to its way of life.", "figures": []},
    {"qnum": "09.3", "page": 27, "marks": 3, "specRef": "3.3.2", "summary": "Calculate the mean surface area of one side of one gill lamella and its percentage uncertainty from Table 5.", "figures": []},
    {"qnum": "09.4", "page": 28, "marks": 2, "specRef": "3.2.1.3", "summary": "Suggest two ways the student could improve the quality of her scientific drawing of the gill in Figure 5.", "figures": ["fig-q9-fig5.jpg"]},

    {"qnum": "10.1", "page": 30, "marks": 6, "specRef": "3.2.1.3", "summary": "Contrast how an optical microscope and a transmission electron microscope work and their limitations.", "figures": []},
    {"qnum": "10.2", "page": 31, "marks": 4, "specRef": "3.4.3", "summary": "Explain the appearance of W and Z undergoing meiosis in the optical microscope image in Figure 6.", "figures": []},
    {"qnum": "10.3", "page": 32, "marks": 5, "specRef": "3.4.7", "summary": "Describe how to collect and process seed size data from city and countryside tree populations to test for a difference.", "figures": []},
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
