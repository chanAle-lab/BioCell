import json
import os
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598688862_9bca5ce0.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598688728_7af835d2.pdf"

PAPER_ID = "2014-specimen-7401-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2014,
    "series": "Specimen",
    "unit": "7401/2",
    "level": "AS",
    "date": "2014-09-23",
    "title": "AQA AS Biology Paper 2 (7401/2) Specimen Set 1",
    "totalMarks": 75,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q2-fig2.jpg", "page": 4, "x0": 75, "y0": 68, "x1": 545, "y1": 465},
    {"filename": "fig-q3-fig3.jpg", "page": 6, "x0": 110, "y0": 72, "x1": 485, "y1": 325},
    {"filename": "fig-q3-table1.jpg", "page": 7, "x0": 110, "y0": 78, "x1": 480, "y1": 215},
    {"filename": "fig-q4-fig4.jpg", "page": 8, "x0": 110, "y0": 375, "x1": 538, "y1": 775},
    {"filename": "fig-q5-fig5.jpg", "page": 12, "x0": 110, "y0": 78, "x1": 540, "y1": 628},
    {"filename": "fig-q6-table2.jpg", "page": 14, "x0": 110, "y0": 78, "x1": 480, "y1": 298},
    {"filename": "fig-q7-fig6.jpg", "page": 16, "x0": 55, "y0": 76, "x1": 545, "y1": 608},
    {"filename": "fig-q8-fig7.jpg", "page": 20, "x0": 60, "y0": 76, "x1": 538, "y1": 616},
    {"filename": "fig-q9-fig9.jpg", "page": 24, "x0": 110, "y0": 68, "x1": 545, "y1": 390},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 2, "specRef": "RP", "summary": "Explain why a student preparing an onion root tip squash pushes down hard on the cover slip but not sideways.", "figures": []},
    {"qnum": "01.2", "page": 2, "marks": 2, "specRef": "3.2.2", "summary": "State whether the cell in Figure 1 is in anaphase of mitosis and give two reasons.", "figures": []},
    {"qnum": "01.3", "page": 3, "marks": 2, "specRef": "3.2.2", "summary": "Calculate how many minutes onion root tip cells spend in anaphase given 6 of 200 cells and a 16-hour cycle.", "figures": []},

    {"qnum": "02.1", "page": 4, "marks": 1, "specRef": "3.2.3", "summary": "Calculate the rate of uptake of sodium ions by the tissue in flask G during the first 20 minutes.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.2", "page": 5, "marks": 4, "specRef": "3.2.3", "summary": "Explain how the information and Figure 2 support the conclusion that cells in flask G took up sodium ions by active transport.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.3", "page": 5, "marks": 2, "specRef": "3.2.3", "summary": "Explain why the curve for flask F in Figure 2 levelled off after 20 minutes.", "figures": ["fig-q2-fig2.jpg"]},

    {"qnum": "03.1", "page": 6, "marks": 1, "specRef": "3.4.2", "summary": "Name the process of protein synthesis shown in Figure 3.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.2", "page": 6, "marks": 1, "specRef": "3.4.2", "summary": "Identify molecule Q shown in Figure 3.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.3", "page": 6, "marks": 2, "specRef": "3.4.2", "summary": "Give the complementary DNA base sequence and missing anticodon for the first codon AUG in Figure 3.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.4", "page": 7, "marks": 1, "specRef": "3.1.4.1", "summary": "Describe how two amino acids such as aspartic acid and proline differ from one another.", "figures": ["fig-q3-table1.jpg"]},
    {"qnum": "03.5", "page": 7, "marks": 3, "specRef": "3.4.3", "summary": "Explain why deletion of the sixth base (G) in Figure 3 changes the protein whereas substitution does not.", "figures": ["fig-q3-fig3.jpg", "fig-q3-table1.jpg"]},

    {"qnum": "04.1", "page": 8, "marks": 4, "specRef": "3.3.2", "summary": "Describe and explain the mechanism that causes forced expiration.", "figures": []},
    {"qnum": "04.2", "page": 9, "marks": 1, "specRef": "3.3.2", "summary": "Calculate the percentage decrease in FEV for group B compared with group A using Figure 4.", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.3", "page": 9, "marks": 4, "specRef": "3.3.2", "summary": "Explain how an asthma attack caused the drop in mean FEV shown for group B in Figure 4.", "figures": ["fig-q4-fig4.jpg"]},

    {"qnum": "05.1", "page": 11, "marks": 2, "specRef": "3.3.3", "summary": "Suggest two non-ethical reasons why scientists used kittens as model organisms for milk digestion.", "figures": []},
    {"qnum": "05.2", "page": 11, "marks": 2, "specRef": "3.3.3", "summary": "Explain why monitoring the pH of the mixture could show whether cat's milk contained bile-activated lipase.", "figures": []},
    {"qnum": "05.3", "page": 13, "marks": 3, "specRef": "3.3.3", "summary": "Conclude from Figure 5 the importance of bile-activated lipase in breast milk.", "figures": ["fig-q5-fig5.jpg"]},

    {"qnum": "06.1", "page": 14, "marks": 1, "specRef": "3.4.6", "summary": "Give the species richness of the heathland plant sample in Table 2.", "figures": ["fig-q6-table2.jpg"]},
    {"qnum": "06.2", "page": 14, "marks": 2, "specRef": "3.4.6", "summary": "Calculate the index of diversity of the heathland plant sample in Table 2.", "figures": ["fig-q6-table2.jpg"]},
    {"qnum": "06.3", "page": 15, "marks": 2, "specRef": "3.4.6", "summary": "Suggest how the student would obtain data to give a more precise index of diversity for the habitat.", "figures": []},

    {"qnum": "07.1", "page": 17, "marks": 1, "specRef": "3.4.4", "summary": "Explain whether Figure 6 allows you to conclude the Bt-resistant insect pest in 2002-2005 was the same species.", "figures": ["fig-q7-fig6.jpg"]},
    {"qnum": "07.2", "page": 17, "marks": 4, "specRef": "3.4.4", "summary": "Evaluate the farmer's claim that Bt crops caused a mutation that spread to other insect species.", "figures": ["fig-q7-fig6.jpg"]},
    {"qnum": "07.3", "page": 18, "marks": 3, "specRef": "3.4.4", "summary": "Explain why there was a time lag between introducing Bt crops and the appearance of the first resistant species.", "figures": ["fig-q7-fig6.jpg"]},

    {"qnum": "08.1", "page": 21, "marks": 2, "specRef": "3.2.4", "summary": "Explain why monoclonal antibody A attaches only to the protein found in species of Plasmodium.", "figures": ["fig-q8-fig7.jpg"]},
    {"qnum": "08.2", "page": 21, "marks": 2, "specRef": "3.2.4", "summary": "Explain why antibody B is important if the malaria test shows a person is not infected.", "figures": ["fig-q8-fig7.jpg"]},
    {"qnum": "08.3", "page": 22, "marks": 4, "specRef": "3.2.4", "summary": "State what can be concluded from the malaria test strip result in Figure 8 and explain how.", "figures": ["fig-q8-fig7.jpg"]},

    {"qnum": "09.1", "page": 23, "marks": 3, "specRef": "3.3.4.2", "summary": "Describe how a high hydrostatic pressure is produced in the leaves for translocation.", "figures": []},
    {"qnum": "09.2", "page": 24, "marks": 2, "specRef": "3.3.4.2", "summary": "Explain why it was important to keep the rate of photosynthesis constant during the PCMBS translocation experiment.", "figures": ["fig-q9-fig9.jpg"]},
    {"qnum": "09.3", "page": 25, "marks": 2, "specRef": "3.3.4.2", "summary": "Explain how Figure 9 supports the conclusion that some translocation occurs in the spaces in cell walls.", "figures": ["fig-q9-fig9.jpg"]},

    {"qnum": "10.1", "page": 26, "marks": 5, "specRef": "3.2.4", "summary": "Describe how giving a vaccine leads to the production of antibodies against a pathogen.", "figures": []},
    {"qnum": "10.2", "page": 27, "marks": 5, "specRef": "3.2.4", "summary": "Describe the differences between active and passive immunity.", "figures": []},
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
