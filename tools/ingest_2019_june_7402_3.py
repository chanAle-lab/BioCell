import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599410931_94f0e10c.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599410895_57d69acc.pdf"

PAPER_ID = "2019-june-7402-3"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2019,
    "series": "June",
    "unit": "7402/3",
    "level": "A-Level",
    "date": "2019-06-17",
    "title": "AQA A-Level Biology Paper 3 (7402/3) June 2019",
    "totalMarks": 78,
    "optionalMarks": 25,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q3-fig2.jpg", "page": 6, "x0": 45, "y0": 64, "x1": 540, "y1": 398},
    {"filename": "fig-q3-fig3.jpg", "page": 8, "x0": 95, "y0": 64, "x1": 540, "y1": 525},
    {"filename": "fig-q4-fig4-5.jpg", "page": 12, "x0": 95, "y0": 340, "x1": 540, "y1": 638},
    {"filename": "fig-q4-fig6.jpg", "page": 14, "x0": 95, "y0": 64, "x1": 540, "y1": 385},
    {"filename": "fig-q5-table1.jpg", "page": 16, "x0": 45, "y0": 64, "x1": 540, "y1": 332},
    {"filename": "fig-q6-fig7.jpg", "page": 18, "x0": 45, "y0": 64, "x1": 540, "y1": 548},
    {"filename": "fig-q6-fig8-9.jpg", "page": 20, "x0": 95, "y0": 72, "x1": 540, "y1": 545},
    {"filename": "fig-q6-fig10.jpg", "page": 22, "x0": 80, "y0": 64, "x1": 540, "y1": 448},
    {"filename": "fig-q6-table3.jpg", "page": 24, "x0": 95, "y0": 64, "x1": 540, "y1": 468},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 3, "specRef": "3.6.4.3", "summary": "Describe how ultrafiltration occurs in a glomerulus.", "figures": []},
    {"qnum": "01.2", "page": 2, "marks": 1, "specRef": "3.6.4.3", "summary": "Tick the correct ways in which glucose and water are reabsorbed by the proximal convoluted tubule.", "figures": []},
    {"qnum": "01.3", "page": 3, "marks": 1, "specRef": "3.6.4.3", "summary": "Calculate the mean length of the loop of Henle in an organism producing urine of concentration 16.56 arbitrary units.", "figures": []},
    {"qnum": "01.4", "page": 4, "marks": 3, "specRef": "3.6.4.3", "summary": "Explain the pattern shown by the results in Figure 1 relating kidney medulla thickness to urine concentration.", "figures": []},

    {"qnum": "02.1", "page": 5, "marks": 2, "specRef": "3.5.4", "summary": "Describe the role of saprobionts in the nitrogen cycle.", "figures": []},
    {"qnum": "02.2", "page": 5, "marks": 3, "specRef": "RP", "summary": "Describe how you would obtain a quantitative measurement of the cloudiness of river water samples.", "figures": []},

    {"qnum": "03.1", "page": 6, "marks": 1, "specRef": "3.3.4.1", "summary": "Name valve A and chamber B in Figure 2.", "figures": []},
    {"qnum": "03.2", "page": 6, "marks": 1, "specRef": "RP", "summary": "Give two safety precautions that should be followed when dissecting a heart.", "figures": []},
    {"qnum": "03.3", "page": 7, "marks": 2, "specRef": "3.3.4.1", "summary": "Explain how valve A in Figure 2 maintains a unidirectional flow of blood.", "figures": ["fig-q3-fig2.jpg"]},
    {"qnum": "03.4", "page": 9, "marks": 2, "specRef": "3.6.1.3", "summary": "Suggest how caffeine could account for the results of Group I in Figure 3 at 60 minutes.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.5", "page": 9, "marks": 1, "specRef": "3.3.4.1", "summary": "Calculate the mean volume of blood leaving the heart at each beat 15 minutes after taking the drink.", "figures": []},
    {"qnum": "03.6", "page": 10, "marks": 2, "specRef": "3.6.1.3", "summary": "Suggest one drink to be given to an additional group and give a reason.", "figures": ["fig-q3-fig3.jpg"]},

    {"qnum": "04.1", "page": 12, "marks": 1, "specRef": "3.8.1", "summary": "Name the type of gene mutation most likely to have occurred at nucleotide position 16 519.", "figures": []},
    {"qnum": "04.2", "page": 13, "marks": 3, "specRef": "3.4.7", "summary": "Evaluate the student's conclusion from Figure 4 and Figure 5 that training has a positive effect on VO2max and CS activity.", "figures": ["fig-q4-fig4-5.jpg"]},
    {"qnum": "04.3", "page": 13, "marks": 2, "specRef": "3.4.2", "summary": "Suggest two reasons why the mutation at nucleotide position 16 519 could lead to the differences in Figure 5.", "figures": ["fig-q4-fig4-5.jpg"]},
    {"qnum": "04.4", "page": 15, "marks": 3, "specRef": "3.5.2", "summary": "Evaluate the conclusion that having thymine at nucleotide 16 519 in Group T causes an increase in ability to exercise for longer.", "figures": ["fig-q4-fig4-5.jpg", "fig-q4-fig6.jpg"]},

    {"qnum": "05.1", "page": 16, "marks": 1, "specRef": "3.4.7", "summary": "State a null hypothesis the marine biologists tested in this investigation (Table 1).", "figures": ["fig-q5-table1.jpg"]},
    {"qnum": "05.2", "page": 16, "marks": 1, "specRef": "3.6.1.1", "summary": "Suggest two factors that should be kept constant in the choice chambers so COTS display normal behaviour.", "figures": []},
    {"qnum": "05.3", "page": 17, "marks": 3, "specRef": "3.4.7", "summary": "Evaluate the journalist's suggestion from Table 1 that either type of light could cause COTS to move away from coral reefs.", "figures": ["fig-q5-table1.jpg"]},
    {"qnum": "05.4", "page": 17, "marks": 2, "specRef": "3.6.1.1", "summary": "Calculate the shortest time one COTS would take to move up a coral reef from 66 m to 18 m under water (Table 2).", "figures": []},

    {"qnum": "06.1", "page": 18, "marks": 1, "specRef": "3.8.2.3", "summary": "Use Figure 7 to calculate the percentage of maximum growth this type of tumour reaches before it can be detected.", "figures": []},
    {"qnum": "06.2", "page": 19, "marks": 1, "specRef": "3.8.2.3", "summary": "Calculate the age of a tumour of 3.98 x 10^11 cells using Figure 7.", "figures": ["fig-q6-fig7.jpg"]},
    {"qnum": "06.3", "page": 21, "marks": 3, "specRef": "3.1.4.2", "summary": "Use Figure 8 and Figure 9 to suggest how Trexall slows cell division.", "figures": ["fig-q6-fig8-9.jpg"]},
    {"qnum": "06.4", "page": 22, "marks": 2, "specRef": "3.8.2.3", "summary": "Suggest why the scientists recorded both percentage change and tumour volume (Figure 10).", "figures": ["fig-q6-fig10.jpg"]},
    {"qnum": "06.5", "page": 23, "marks": 2, "specRef": "3.8.2.3", "summary": "Use Figure 10 to calculate the volume of the patient's tumour before treatment with 15 mg of Trexall per week.", "figures": ["fig-q6-fig10.jpg"]},
    {"qnum": "06.6", "page": 23, "marks": 2, "specRef": "3.4.7", "summary": "Explain whether it would be better to use 30 mg or 20 mg of Trexall per week to reduce tumour size.", "figures": ["fig-q6-fig10.jpg"]},
    {"qnum": "06.7", "page": 24, "marks": 1, "specRef": "3.4.7", "summary": "Apart from age and general health, give two important factors when choosing patients for this investigation.", "figures": []},
    {"qnum": "06.8", "page": 25, "marks": 3, "specRef": "3.4.7", "summary": "Evaluate the student's conclusion from Table 3 that Trexall was effective in reducing pain in arthritis patients.", "figures": ["fig-q6-table3.jpg"]},

    {"qnum": "07.1", "page": 26, "marks": 25, "specRef": "Essay", "summary": "Essay: The importance of DNA as an information-carrying molecule and its use in gene technologies.", "figures": []},
    {"qnum": "07.2", "page": 26, "marks": 25, "specRef": "Essay", "summary": "Essay: The importance of bonds and bonding in organisms.", "figures": []},
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
    expected_total = PAPER_META["totalMarks"] + PAPER_META.get("optionalMarks", 0)
    assert sum(q["marks"] for q in QUESTIONS) == expected_total, "Mark sum mismatch!"
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

    print(f"Ingested {len(QUESTIONS)} questions ({PAPER_META['totalMarks']} marks + {PAPER_META['optionalMarks']} optional) for {PAPER_ID}")


if __name__ == "__main__":
    main()
