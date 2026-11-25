import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599387904_a0a25523.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599388430_cb4ef149.pdf"

PAPER_ID = "2018-june-7402-3"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2018,
    "series": "June",
    "unit": "7402/3",
    "level": "A-Level",
    "date": "2018-06-18",
    "title": "AQA A-Level Biology Paper 3 (7402/3) June 2018",
    "totalMarks": 78,
    "optionalMarks": 25,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 2, "x0": 100, "y0": 100, "x1": 530, "y1": 590},
    {"filename": "fig-q2-fig2.jpg", "page": 6, "x0": 45, "y0": 64, "x1": 538, "y1": 555},
    {"filename": "fig-q2-table1.jpg", "page": 8, "x0": 80, "y0": 64, "x1": 535, "y1": 382},
    {"filename": "fig-q3-fig3.jpg", "page": 10, "x0": 110, "y0": 64, "x1": 535, "y1": 735},
    {"filename": "fig-q4-fig4.jpg", "page": 16, "x0": 65, "y0": 64, "x1": 535, "y1": 510},
    {"filename": "fig-q6-fig6.jpg", "page": 22, "x0": 45, "y0": 64, "x1": 538, "y1": 635},
    {"filename": "fig-q6-fig7.jpg", "page": 26, "x0": 70, "y0": 64, "x1": 535, "y1": 642},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 3, "marks": 2, "specRef": "3.6.4.1", "summary": "Use Figure 1 to explain why osteocalcin secretion by osteoblasts is controlled by positive feedback.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.2", "page": 3, "marks": 2, "specRef": "3.1.4.1", "summary": "Suggest how acidic pH created by osteoclasts changes inactive osteocalcin into the active form.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.3", "page": 4, "marks": 2, "specRef": "3.6.4.2", "summary": "Explain how binding of insulin leads to an increase in the rate of respiration in osteoblasts.", "figures": []},

    {"qnum": "02.1", "page": 6, "marks": 1, "specRef": "3.4.7", "summary": "Name the statistical test for a relationship between CD20 amount and % B cells destroyed in Figure 2, and give a reason.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.2", "page": 7, "marks": 3, "specRef": "3.2.4", "summary": "Conclude from Figure 2 the effectiveness of Rituximab in treating patients with CLL.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.3", "page": 8, "marks": 2, "specRef": "3.2.4", "summary": "Use Table 1 to calculate in standard form the difference in B cells per dm^3 between patients with and without NOTCH1 mutation.", "figures": ["fig-q2-table1.jpg"]},
    {"qnum": "02.4", "page": 9, "marks": 3, "specRef": "3.8.2.2", "summary": "Suggest how the NOTCH1 mutation led to the difference in percentage of B cells destroyed by Rituximab.", "figures": ["fig-q2-table1.jpg"]},

    {"qnum": "03.1", "page": 11, "marks": 1, "specRef": "3.4.3", "summary": "Complete Figure 3 with A or a in the boxes for meiotic division.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.2", "page": 11, "marks": 1, "specRef": "3.4.3", "summary": "Tick the process that produced the allele combination on the chromosome in the first polar body in Figure 3.", "figures": ["fig-q3-fig3.jpg"]},
    {"qnum": "03.3", "page": 11, "marks": 2, "specRef": "3.2.1.1", "summary": "Calculate the number of mitochondria in the spherical polar body given diameters and mitochondrial density.", "figures": []},
    {"qnum": "03.4", "page": 12, "marks": 2, "specRef": "3.8.4.2", "summary": "Suggest how replacing a donated egg's nucleus with a polar body prevents inheritance of mitochondrial diseases.", "figures": []},
    {"qnum": "03.5", "page": 13, "marks": 2, "specRef": "3.1.6", "summary": "Suggest and explain why faulty mitochondria prevent or slow down many enzyme-catalysed reactions.", "figures": []},

    {"qnum": "04.1", "page": 15, "marks": 2, "specRef": "3.3.4.1", "summary": "Explain why binding of one oxygen molecule to haemoglobin makes it easier for a second oxygen to bind.", "figures": []},
    {"qnum": "04.2", "page": 17, "marks": 2, "specRef": "3.2.1.3", "summary": "Calculate in standard form the number of red blood cells per mm^3 in the original blood sample using Figure 4.", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.3", "page": 17, "marks": 2, "specRef": "3.2.1.3", "summary": "Suggest two reasons for the haemocytometer rule of counting top/left lines and excluding right/bottom lines.", "figures": ["fig-q4-fig4.jpg"]},
    {"qnum": "04.4", "page": 18, "marks": 1, "specRef": "3.2.1.3", "summary": "Suggest why the doctor only diluted the blood sample by 20 times when counting white blood cells.", "figures": []},
    {"qnum": "04.5", "page": 18, "marks": 1, "specRef": "3.2.1.3", "summary": "Explain how a nuclear stain allowed the doctor to count white blood cells amongst red blood cells.", "figures": []},

    {"qnum": "05.1", "page": 20, "marks": 2, "specRef": "3.2.3", "summary": "Suggest how a detergent that dissolves lipids releases CENP-W from cells and organelles.", "figures": []},
    {"qnum": "05.2", "page": 20, "marks": 2, "specRef": "3.2.1.3", "summary": "Explain how ultracentrifugation separates CENP-W from other molecules.", "figures": []},
    {"qnum": "05.3", "page": 21, "marks": 3, "specRef": "3.8.2.2", "summary": "Suggest how siRNA against the CENP-W gene produced the electrophoresis results in Figure 5.", "figures": []},

    {"qnum": "06.1", "page": 23, "marks": 2, "specRef": "3.5.4", "summary": "Suggest why scientists used units of ug g^-1 for ammonia concentration in soil.", "figures": ["fig-q6-fig6.jpg"]},
    {"qnum": "06.2", "page": 23, "marks": 2, "specRef": "3.5.4", "summary": "Calculate the difference in rate of ammonia breakdown per day between day 0 and day 2 in soil A and soil B.", "figures": ["fig-q6-fig6.jpg"]},
    {"qnum": "06.3", "page": 24, "marks": 3, "specRef": "3.5.4", "summary": "Give evidence from Figure 6 supporting the conclusion that soils A and B had different bacterial communities.", "figures": ["fig-q6-fig6.jpg"]},
    {"qnum": "06.4", "page": 27, "marks": 2, "specRef": "3.8.2.2", "summary": "Use a calculation from Figure 7 to show which species' amoA mRNA copies were more affected by pH 4.9 to 7.5.", "figures": ["fig-q6-fig7.jpg"]},
    {"qnum": "06.5", "page": 28, "marks": 4, "specRef": "3.8.2.2", "summary": "Explain why this method estimated amoA gene expression but not bacterial population growth.", "figures": ["fig-q6-fig7.jpg"]},
    {"qnum": "06.6", "page": 29, "marks": 2, "specRef": "RP", "summary": "Suggest a suitable method to sterilise glass bottles and explain why sterilisation was necessary.", "figures": []},

    {"qnum": "07.1", "page": 30, "marks": 25, "specRef": "Essay", "summary": "Essay: The importance of the control of movement in cells and organisms.", "figures": []},
    {"qnum": "07.2", "page": 30, "marks": 25, "specRef": "Essay", "summary": "Essay: The importance of interactions between cells and between organisms.", "figures": []},
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
        json.dump(db, f, indent=2)
    print(f"Ingested {PAPER_ID}: {len(QUESTIONS)} questions, {sum(q['marks'] for q in QUESTIONS)} marks")


if __name__ == "__main__":
    main()
