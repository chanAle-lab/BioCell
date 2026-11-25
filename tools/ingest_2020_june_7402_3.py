import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599464584_50db2a7d.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599464573_807944e9.pdf"

PAPER_ID = "2020-june-7402-3"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2020,
    "series": "June",
    "unit": "7402/3",
    "level": "A-Level",
    "date": "2020-06-15",
    "title": "AQA A-Level Biology Paper 3 (7402/3) June 2020",
    "totalMarks": 78,
    "optionalMarks": 25,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 45, "y0": 150, "x1": 540, "y1": 455},
    {"filename": "fig-q2-table1.jpg", "page": 4, "x0": 95, "y0": 250, "x1": 540, "y1": 565},
    {"filename": "fig-q4-table2.jpg", "page": 8, "x0": 45, "y0": 64, "x1": 540, "y1": 235},
    {"filename": "fig-q6-fig3.jpg", "page": 14, "x0": 95, "y0": 270, "x1": 540, "y1": 645},
    {"filename": "fig-q6-fig4.jpg", "page": 16, "x0": 95, "y0": 64, "x1": 540, "y1": 432},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 3, "specRef": "3.4.5", "summary": "Suggest three possible limitations of the guppy mate-choice investigation (Figure 1).", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.2", "page": 3, "marks": 3, "specRef": "3.4.4", "summary": "Suggest and explain the advantage of only large-brained female guppies being attracted to bright-coloured males.", "figures": []},
    {"qnum": "01.3", "page": 3, "marks": 3, "specRef": "3.7.3", "summary": "Describe how the behaviour of female guppies could result in sympatric speciation.", "figures": []},

    {"qnum": "02.1", "page": 4, "marks": 1, "specRef": "3.7.4", "summary": "Name the type of competition between livestock and ibex.", "figures": []},
    {"qnum": "02.2", "page": 5, "marks": 3, "specRef": "3.7.4", "summary": "Using all the information in Table 1, suggest and explain three actions farmers could take to balance ibex conservation and livestock.", "figures": ["fig-q2-table1.jpg"]},

    {"qnum": "03.1", "page": 6, "marks": 2, "specRef": "3.8.1", "summary": "Suggest and explain how Ranaviruses became able to infect other species of frog.", "figures": []},
    {"qnum": "03.2", "page": 6, "marks": 1, "specRef": "3.8.4.3", "summary": "Name two techniques scientists may have used when analysing viral DNA to determine they were closely related.", "figures": []},
    {"qnum": "03.3", "page": 6, "marks": 2, "specRef": "3.8.3", "summary": "Explain how determining the genome of the viruses could allow scientists to develop a vaccine.", "figures": []},
    {"qnum": "03.4", "page": 7, "marks": 3, "specRef": "3.2.4", "summary": "Describe how the B lymphocytes of a frog would respond to vaccination against Ranavirus.", "figures": []},

    {"qnum": "04.1", "page": 8, "marks": 2, "specRef": "3.1.1", "summary": "Use suitable calculations from Table 2 to determine whether the journalist's statement about sodium RDA is true for both medicines.", "figures": ["fig-q4-table2.jpg"]},
    {"qnum": "04.2", "page": 9, "marks": 2, "specRef": "3.4.7", "summary": "Give two factors that should have been the same and one factor different for each pair of patients.", "figures": []},
    {"qnum": "04.3", "page": 9, "marks": 2, "specRef": "3.4.7", "summary": "Calculate how many of the control patients had hypertension.", "figures": []},
    {"qnum": "04.4", "page": 10, "marks": 3, "specRef": "3.2.3", "summary": "Use your knowledge of water potential to suggest how high sodium concentrations in medicines could affect blood volume.", "figures": []},

    {"qnum": "05.1", "page": 11, "marks": 2, "specRef": "3.8.2.3", "summary": "Calculate the mean number of people who died of throat cancer per month in 2016.", "figures": []},
    {"qnum": "05.2", "page": 11, "marks": 3, "specRef": "3.8.2.3", "summary": "Suggest how EGCG allows the production of mRNA from the tumour suppressor gene in daughter cells.", "figures": []},
    {"qnum": "05.3", "page": 12, "marks": 3, "specRef": "3.8.2.3", "summary": "Suggest three reasons why the reporter's conclusion that drinking green tea could cure cancer might not be valid.", "figures": []},

    {"qnum": "06.1", "page": 14, "marks": 2, "specRef": "3.3.4.1", "summary": "Describe the advantage of the Bohr effect during intense exercise.", "figures": []},
    {"qnum": "06.2", "page": 15, "marks": 2, "specRef": "3.3.2", "summary": "Use Figure 3 to determine the time when the cyclist reached VT and calculate the ratio of pO2 to pCO2.", "figures": ["fig-q6-fig3.jpg"]},
    {"qnum": "06.3", "page": 15, "marks": 2, "specRef": "3.3.2", "summary": "Suggest and explain one physiological change causing pCO2 in breathed-out air not to show a large increase during exercise.", "figures": ["fig-q6-fig3.jpg"]},
    {"qnum": "06.4", "page": 16, "marks": 1, "specRef": "3.6.3", "summary": "Tick why ATP can only be made for a limited time at more than 80% maximum muscle effort (Figure 4).", "figures": ["fig-q6-fig4.jpg"]},
    {"qnum": "06.5", "page": 17, "marks": 4, "specRef": "3.6.3", "summary": "Use Figure 4 to justify why professional athletes are not allowed to take GW1516.", "figures": ["fig-q6-fig4.jpg"]},
    {"qnum": "06.6", "page": 18, "marks": 2, "specRef": "3.3.4.1", "summary": "Suggest how overuse of EPO can increase the risk of a heart attack.", "figures": []},
    {"qnum": "06.7", "page": 18, "marks": 2, "specRef": "3.3.4.1", "summary": "Give two reasons why allowing male cyclists to use EPO until their haematocrit is 50% is not valid.", "figures": []},

    {"qnum": "07.1", "page": 19, "marks": 25, "specRef": "Essay", "summary": "Essay: The functions of enzymes and their importance in organisms.", "figures": []},
    {"qnum": "07.2", "page": 19, "marks": 25, "specRef": "Essay", "summary": "Essay: The causes and importance of variation and diversity in organisms.", "figures": []},
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
