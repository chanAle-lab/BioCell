import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599410894_fd2a8e08.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599411808_16153a4a.pdf"

PAPER_ID = "2019-june-7402-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2019,
    "series": "June",
    "unit": "7402/1",
    "level": "A-Level",
    "date": "2019-06-06",
    "title": "AQA A-Level Biology Paper 1 (7402/1) June 2019",
    "totalMarks": 91,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 3, "x0": 95, "y0": 64, "x1": 540, "y1": 430},
    {"filename": "fig-q1-fig2.jpg", "page": 4, "x0": 95, "y0": 64, "x1": 540, "y1": 448},
    {"filename": "fig-q2-fig3.jpg", "page": 6, "x0": 95, "y0": 255, "x1": 540, "y1": 758},
    {"filename": "fig-q3-fig4.jpg", "page": 10, "x0": 45, "y0": 64, "x1": 540, "y1": 538},
    {"filename": "fig-q4-fig5.jpg", "page": 14, "x0": 45, "y0": 64, "x1": 540, "y1": 470},
    {"filename": "fig-q5-table3.jpg", "page": 20, "x0": 95, "y0": 64, "x1": 540, "y1": 345},
    {"filename": "fig-q6-table4.jpg", "page": 22, "x0": 45, "y0": 64, "x1": 540, "y1": 305},
    {"filename": "fig-q7-fig6.jpg", "page": 26, "x0": 45, "y0": 64, "x1": 540, "y1": 378},
    {"filename": "fig-q7-fig7.jpg", "page": 27, "x0": 95, "y0": 64, "x1": 540, "y1": 375},
    {"filename": "fig-q8-fig8.jpg", "page": 28, "x0": 45, "y0": 64, "x1": 540, "y1": 460},
    {"filename": "fig-q8-fig9.jpg", "page": 30, "x0": 95, "y0": 64, "x1": 540, "y1": 350},
    {"filename": "fig-q9-table7.jpg", "page": 32, "x0": 45, "y0": 64, "x1": 540, "y1": 286},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 3, "specRef": "3.1.4.2", "summary": "Describe how a non-competitive inhibitor can reduce the rate of an enzyme-controlled reaction.", "figures": []},
    {"qnum": "01.2", "page": 3, "marks": 1, "specRef": "3.1.4.2", "summary": "Use Figure 1 to explain why the scientist concluded that pectin is a non-competitive inhibitor.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.3", "page": 4, "marks": 2, "specRef": "3.2.1.3", "summary": "Calculate the maximum length of the large lipid droplet marked X in Figure 2 and its uncertainty.", "figures": ["fig-q1-fig2.jpg"]},
    {"qnum": "01.4", "page": 5, "marks": 2, "specRef": "3.3.3", "summary": "Explain why no large lipid droplets are visible with the optical microscope in samples from suspension A.", "figures": []},

    {"qnum": "02.1", "page": 6, "marks": 3, "specRef": "3.2.1.1", "summary": "Complete Table 1 by ticking where cellulose, murein, or chitin cell wall components are present.", "figures": []},
    {"qnum": "02.2", "page": 7, "marks": 4, "specRef": "3.3.4.1", "summary": "Evaluate the student's conclusion from Figure 3 that eating an extra 10 g of fibre per day would significantly lower CVD risk.", "figures": ["fig-q2-fig3.jpg"]},
    {"qnum": "02.3", "page": 8, "marks": 2, "specRef": "3.3.4.1", "summary": "Suggest one advantage and one disadvantage of using the FFQ method compared with a 24-hour nurse interview.", "figures": []},

    {"qnum": "03.1", "page": 10, "marks": 1, "specRef": "3.4.6", "summary": "State what data students need to collect to calculate the index of diversity in each habitat (Figure 4).", "figures": ["fig-q3-fig4.jpg"]},
    {"qnum": "03.2", "page": 11, "marks": 2, "specRef": "3.4.6", "summary": "Give two ways the students would have ensured their index of diversity was representative of each habitat.", "figures": []},
    {"qnum": "03.3", "page": 11, "marks": 1, "specRef": "3.4.6", "summary": "Use Figure 4 to suggest why biodiversity decreases when farmers use larger fields.", "figures": ["fig-q3-fig4.jpg"]},
    {"qnum": "03.4", "page": 12, "marks": 2, "specRef": "3.4.6", "summary": "Suggest and explain one advantage and one disadvantage to a farmer of replanting hedges on farmland.", "figures": []},

    {"qnum": "04.1", "page": 15, "marks": 3, "specRef": "3.4.4", "summary": "Use Figure 5 to explain how human mass at birth is affected by stabilising selection.", "figures": ["fig-q4-fig5.jpg"]},
    {"qnum": "04.2", "page": 16, "marks": 3, "specRef": "3.4.2", "summary": "Write the correct biological term beside each number (1) to (6) in the passage about KIR2DS1.", "figures": []},
    {"qnum": "04.3", "page": 17, "marks": 1, "specRef": "3.4.7", "summary": "Tick the statistical test that should be used with the data in Table 2.", "figures": []},
    {"qnum": "04.4", "page": 18, "marks": 3, "specRef": "3.4.7", "summary": "Explain what can be concluded from a P value of 0.03 when testing the null hypothesis.", "figures": []},

    {"qnum": "05.1", "page": 19, "marks": 4, "specRef": "3.2.1.2", "summary": "Describe the structure of the human immunodeficiency virus (HIV).", "figures": []},
    {"qnum": "05.2", "page": 20, "marks": 1, "specRef": "3.2.4", "summary": "Tick the number of virus particles present in a 500 mm^3 blood sample from an HIV controller with median viral load (Table 3).", "figures": ["fig-q5-table3.jpg"]},
    {"qnum": "05.3", "page": 21, "marks": 3, "specRef": "3.2.4", "summary": "Use Table 3 and your knowledge of the immune response to suggest why HIV controllers do not develop AIDS symptoms.", "figures": ["fig-q5-table3.jpg"]},

    {"qnum": "06.1", "page": 22, "marks": 2, "specRef": "3.2.2", "summary": "Describe and explain the data in Table 4 on mouse heart cells undergoing mitosis and DNA replication.", "figures": ["fig-q6-table4.jpg"]},
    {"qnum": "06.2", "page": 23, "marks": 5, "specRef": "3.1.5.2", "summary": "Describe how BrdU would be incorporated into new DNA during semi-conservative replication.", "figures": []},
    {"qnum": "06.3", "page": 24, "marks": 3, "specRef": "3.2.4", "summary": "Use your knowledge of the ELISA test to suggest and explain how scientists identified cells with BrdU in their DNA.", "figures": []},

    {"qnum": "07.1", "page": 26, "marks": 1, "specRef": "3.3.1", "summary": "Suggest how Ulva lactuca is able to survive without xylem tissue (Figure 6).", "figures": ["fig-q7-fig6.jpg"]},
    {"qnum": "07.2", "page": 27, "marks": 2, "specRef": "3.4.3", "summary": "Complete each box on Figure 7 with T (mitosis) or E (meiosis) for the life cycle of Ulva lactuca.", "figures": ["fig-q7-fig7.jpg"]},
    {"qnum": "07.3", "page": 27, "marks": 2, "specRef": "3.4.5", "summary": "Suggest and explain one reason why successful reproduction between Ulva prolifera and Ulva lactuca does not happen.", "figures": []},

    {"qnum": "08.1", "page": 29, "marks": 2, "specRef": "RP", "summary": "Complete Table 5 with headings, units and volumes required to make 20 cm^3 of -1.95 MPa sodium chloride solution.", "figures": ["fig-q8-fig8.jpg"]},
    {"qnum": "08.2", "page": 29, "marks": 2, "specRef": "3.2.3", "summary": "Use Table 6 to calculate the concentration of sodium chloride solution with a water potential of -3.41 MPa.", "figures": []},
    {"qnum": "08.3", "page": 30, "marks": 2, "specRef": "3.2.3", "summary": "Use Figure 8 and Figure 9 to calculate the increase in area of a 60 cm^2 leaf with a voltage reading of -7 uV.", "figures": ["fig-q8-fig8.jpg", "fig-q8-fig9.jpg"]},
    {"qnum": "08.4", "page": 31, "marks": 2, "specRef": "3.3.2", "summary": "Suggest and explain one way leaf growth of xerophytic plants would differ from sunflowers in Figure 9.", "figures": ["fig-q8-fig9.jpg"]},
    {"qnum": "08.5", "page": 31, "marks": 2, "specRef": "3.3.2", "summary": "Use your knowledge of gas exchange in leaves to explain why plants grown in soil with very little water grow slowly.", "figures": []},

    {"qnum": "09.1", "page": 32, "marks": 3, "specRef": "3.3.4.1", "summary": "Plot haemoglobin saturation data from Table 7 and sketch full oxyhaemoglobin dissociation curves for horse and mouse.", "figures": []},
    {"qnum": "09.2", "page": 33, "marks": 2, "specRef": "3.3.1", "summary": "Use the metabolic rate equation and Table 7 to calculate how many times faster a mouse's metabolic rate is than a horse's.", "figures": ["fig-q9-table7.jpg"]},
    {"qnum": "09.3", "page": 33, "marks": 2, "specRef": "3.3.4.1", "summary": "Suggest how differences in oxyhaemoglobin dissociation curves in Table 7 allow the mouse to have a higher metabolic rate.", "figures": ["fig-q9-table7.jpg"]},
    {"qnum": "09.4", "page": 34, "marks": 3, "specRef": "3.3.1", "summary": "Use surface area to volume ratio to explain the higher metabolic rate of a mouse compared to a horse.", "figures": []},

    {"qnum": "10.1", "page": 35, "marks": 5, "specRef": "3.1.7", "summary": "Explain five properties that make water important for organisms.", "figures": []},
    {"qnum": "10.2", "page": 36, "marks": 5, "specRef": "3.1.1", "summary": "Describe the biochemical tests used to confirm the presence of lipid, non-reducing sugar and amylase in a sample.", "figures": []},
    {"qnum": "10.3", "page": 37, "marks": 5, "specRef": "3.1.1", "summary": "Describe the chemical reactions converting polymers to monomers and monomers to polymers, with two named examples.", "figures": []},
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
