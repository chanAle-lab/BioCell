import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599464478_051b8849.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599464467_d560aaed.pdf"

PAPER_ID = "2020-june-7402-1"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2020,
    "series": "June",
    "unit": "7402/1",
    "level": "A-Level",
    "date": "2020-06-04",
    "title": "AQA A-Level Biology Paper 1 (7402/1) June 2020",
    "totalMarks": 91,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 45, "y0": 98, "x1": 540, "y1": 316},
    {"filename": "fig-q1-fig2.jpg", "page": 4, "x0": 95, "y0": 64, "x1": 540, "y1": 445},
    {"filename": "fig-q2-table1.jpg", "page": 6, "x0": 45, "y0": 64, "x1": 540, "y1": 330},
    {"filename": "fig-q3-fig3.jpg", "page": 8, "x0": 45, "y0": 64, "x1": 540, "y1": 468},
    {"filename": "fig-q4-fig4.jpg", "page": 11, "x0": 95, "y0": 64, "x1": 540, "y1": 420},
    {"filename": "fig-q5-fig5.jpg", "page": 14, "x0": 95, "y0": 300, "x1": 540, "y1": 765},
    {"filename": "fig-q6-fig6.jpg", "page": 17, "x0": 95, "y0": 64, "x1": 540, "y1": 385},
    {"filename": "fig-q8-table3.jpg", "page": 22, "x0": 95, "y0": 64, "x1": 540, "y1": 258},
    {"filename": "fig-q8-fig8.jpg", "page": 22, "x0": 95, "y0": 325, "x1": 540, "y1": 645},
    {"filename": "fig-q9-fig9.jpg", "page": 25, "x0": 45, "y0": 64, "x1": 540, "y1": 320},
    {"filename": "fig-q9-fig10.jpg", "page": 26, "x0": 95, "y0": 64, "x1": 540, "y1": 570},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 2, "specRef": "3.2.3", "summary": "Explain the function of the membrane-bound ATP hydrolase linked to carrier protein X (Figure 1).", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.2", "page": 2, "marks": 2, "specRef": "3.2.3", "summary": "Explain how the movement of Na+ out of the cell allows the absorption of glucose into the cell lining the ileum.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.3", "page": 3, "marks": 2, "specRef": "3.3.3", "summary": "Describe and explain two features you would expect to find in a cell specialised for absorption.", "figures": []},
    {"qnum": "01.4", "page": 4, "marks": 2, "specRef": "3.2.3", "summary": "Draw phospholipids on Figure 2 to show how the SGLT1 carrier protein fits into the cell-surface membrane.", "figures": ["fig-q1-fig2.jpg"]},
    {"qnum": "01.5", "page": 5, "marks": 2, "specRef": "3.1.4.1", "summary": "Describe how amino acids join to form a polypeptide so there is always NH2 at one end and COOH at the other (Figure 2).", "figures": ["fig-q1-fig2.jpg"]},

    {"qnum": "02.1", "page": 6, "marks": 3, "specRef": "3.3.3", "summary": "Use your knowledge of lipid digestion to explain the differences in the results for samples A and B in Table 1.", "figures": ["fig-q2-table1.jpg"]},
    {"qnum": "02.2", "page": 7, "marks": 2, "specRef": "3.1.4.2", "summary": "Explain why the scientist immediately heated the collected samples to 70 degrees C for 10 minutes.", "figures": []},
    {"qnum": "02.3", "page": 7, "marks": 3, "specRef": "3.3.3", "summary": "Describe the role of micelles in the absorption of fats into the cells lining the ileum.", "figures": []},

    {"qnum": "03.1", "page": 8, "marks": 2, "specRef": "3.3.4.1", "summary": "Use evidence from Figure 3 to explain why the rate of blood flow has not yet started to increase in the aorta at P.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.2", "page": 9, "marks": 2, "specRef": "3.3.4.1", "summary": "Explain how the small increase in pressure and rate of blood flow in the aorta at Q (Figure 3) happens and its importance.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.3", "page": 9, "marks": 2, "specRef": "3.3.4.1", "summary": "Describe one similarity and one difference between right ventricle pressure and left ventricle pressure in Figure 3.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.4", "page": 9, "marks": 1, "specRef": "3.3.4.1", "summary": "Use information from Figure 3 to calculate the heart rate of this dog.", "figures": ["fig-q3-fig3.jpg"]},

    {"qnum": "04.1", "page": 10, "marks": 1, "specRef": "RP", "summary": "Tick the most appropriate volumes to make up 100 cm^3 of extraction solvent E in a 70:30:1 ratio.", "figures": []},
    {"qnum": "04.2", "page": 10, "marks": 2, "specRef": "RP", "summary": "Name two other variables the student should have kept constant during the blueberry anthocyanin extraction.", "figures": []},
    {"qnum": "04.3", "page": 11, "marks": 4, "specRef": "3.2.3", "summary": "Use your knowledge of membrane structure to explain the absorbance results in Figure 4.", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.4", "page": 12, "marks": 3, "specRef": "RP", "summary": "Describe a method to prepare colour standards and use them to determine total anthocyanin extracted without a colorimeter.", "figures": []},

    {"qnum": "05.1", "page": 14, "marks": 2, "specRef": "3.1.5.2", "summary": "Describe the role of DNA polymerase in the semi-conservative replication of DNA.", "figures": []},
    {"qnum": "05.2", "page": 15, "marks": 2, "specRef": "3.2.2", "summary": "Use Figure 5 to calculate the percentage decrease in time for 25% of cells with cyclin D vs without cyclin D to undergo DNA replication.", "figures": ["fig-q5-fig5.jpg"]},
    {"qnum": "05.3", "page": 15, "marks": 2, "specRef": "3.1.6", "summary": "Describe how an enzyme can be phosphorylated.", "figures": []},
    {"qnum": "05.4", "page": 15, "marks": 2, "specRef": "3.2.2", "summary": "Use Figure 5 to suggest why higher than normal concentrations of cyclin D could result in a tumour.", "figures": ["fig-q5-fig5.jpg"]},

    {"qnum": "06.1", "page": 16, "marks": 3, "specRef": "3.3.2", "summary": "Explain why death of alveolar epithelium cells reduces gas exchange in human lungs.", "figures": []},
    {"qnum": "06.2", "page": 17, "marks": 2, "specRef": "3.3.2", "summary": "Use suitable calculations from Figure 6 to justify whether the relationship between particulate matter and dead cells is linear.", "figures": ["fig-q6-fig6.jpg"]},

    {"qnum": "07.1", "page": 18, "marks": 2, "specRef": "3.1.2", "summary": "Give the chemical formula for alpha-gal and describe how it is formed from two galactose molecules.", "figures": []},
    {"qnum": "07.2", "page": 18, "marks": 3, "specRef": "3.2.4", "summary": "Draw a labelled diagram of an antibody and identify the specific alpha-gal binding site.", "figures": []},
    {"qnum": "07.3", "page": 19, "marks": 2, "specRef": "3.2.4", "summary": "Suggest how one antibody can be specific to tick protein and to alpha-gal.", "figures": []},
    {"qnum": "07.4", "page": 20, "marks": 3, "specRef": "3.2.4", "summary": "Consider whether Figure 7 supports the hypothesis that an earlier immune response to tick protein causes the allergic reaction.", "figures": []},

    {"qnum": "08.1", "page": 21, "marks": 3, "specRef": "3.4.1", "summary": "Complete Table 2 to show three differences between DNA in the nucleus of a plant cell and DNA in a prokaryotic cell.", "figures": []},
    {"qnum": "08.2", "page": 21, "marks": 2, "specRef": "3.4.1", "summary": "Define non-coding base sequences and describe where non-coding multiple repeats are positioned in the genome.", "figures": []},
    {"qnum": "08.3", "page": 22, "marks": 1, "specRef": "3.4.5", "summary": "Use the information in Table 3 to complete the phylogenetic tree shown in Figure 8.", "figures": ["fig-q8-table3.jpg", "fig-q8-fig8.jpg"]},
    {"qnum": "08.4", "page": 23, "marks": 2, "specRef": "3.4.5", "summary": "Use Table 3 to evaluate how a 66% similarity within five individuals of species T affects the validity of the phylogenetic tree.", "figures": ["fig-q8-table3.jpg"]},

    {"qnum": "09.1", "page": 25, "marks": 2, "specRef": "3.3.2", "summary": "Calculate the mean stomatal density per mm^2 in the three fields of view in Figure 9.", "figures": ["fig-q9-fig9.jpg"]},
    {"qnum": "09.2", "page": 26, "marks": 2, "specRef": "3.4.7", "summary": "Give a null hypothesis for the stomatal density investigation and name an appropriate statistical test (Figure 10).", "figures": ["fig-q9-fig10.jpg"]},
    {"qnum": "09.3", "page": 27, "marks": 2, "specRef": "3.3.2", "summary": "Use Figure 10 to calculate the mean rate of change in stomatal density from 1910 to 2000 per 10-year period.", "figures": ["fig-q9-fig10.jpg"]},
    {"qnum": "09.4", "page": 27, "marks": 4, "specRef": "3.3.2", "summary": "Evaluate the journalist's suggestion from Figure 10 that future increases in atmospheric CO2 could result in less transpiration.", "figures": ["fig-q9-fig10.jpg"]},

    {"qnum": "10.1", "page": 28, "marks": 5, "specRef": "3.4.2", "summary": "Describe how mRNA is formed by transcription in eukaryotes.", "figures": []},
    {"qnum": "10.2", "page": 29, "marks": 6, "specRef": "3.4.2", "summary": "Describe how a polypeptide is formed by translation of mRNA.", "figures": []},
    {"qnum": "10.3", "page": 30, "marks": 4, "specRef": "3.4.3", "summary": "Define gene mutation and explain how a gene mutation can have no effect or a positive effect on an individual.", "figures": []},
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
