import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599410888_b132ed5a.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599410887_0b61127f.pdf"

PAPER_ID = "2019-june-7402-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2019,
    "series": "June",
    "unit": "7402/2",
    "level": "A-Level",
    "date": "2019-06-13",
    "title": "AQA A-Level Biology Paper 2 (7402/2) June 2019",
    "totalMarks": 91,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q1-fig1.jpg", "page": 3, "x0": 95, "y0": 64, "x1": 540, "y1": 280},
    {"filename": "fig-q2-fig2.jpg", "page": 5, "x0": 95, "y0": 64, "x1": 540, "y1": 445},
    {"filename": "fig-q3-table1.jpg", "page": 6, "x0": 45, "y0": 64, "x1": 540, "y1": 378},
    {"filename": "fig-q4-fig3.jpg", "page": 10, "x0": 45, "y0": 64, "x1": 540, "y1": 625},
    {"filename": "fig-q6-fig4.jpg", "page": 16, "x0": 45, "y0": 64, "x1": 540, "y1": 455},
    {"filename": "fig-q7-fig5.jpg", "page": 20, "x0": 95, "y0": 64, "x1": 540, "y1": 378},
    {"filename": "fig-q8-fig6.jpg", "page": 22, "x0": 95, "y0": 225, "x1": 540, "y1": 555},
    {"filename": "fig-q8-fig7.jpg", "page": 23, "x0": 95, "y0": 185, "x1": 540, "y1": 515},
    {"filename": "fig-q10-passage.jpg", "page": 26, "x0": 45, "y0": 64, "x1": 540, "y1": 372},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 4, "specRef": "3.7.4", "summary": "Describe and explain how succession occurs in natural ecosystems.", "figures": []},
    {"qnum": "01.2", "page": 3, "marks": 1, "specRef": "3.5.3", "summary": "Use Figure 1 to calculate the percentage of sunlight energy transferred into the faeces and urine of a zebra.", "figures": ["fig-q1-fig1.jpg"]},
    {"qnum": "01.3", "page": 3, "marks": 2, "specRef": "3.5.3", "summary": "Calculate the energy stored in new tissues of the zebra using net productivity and Figure 1.", "figures": ["fig-q1-fig1.jpg"]},

    {"qnum": "02.1", "page": 4, "marks": 3, "specRef": "3.8.1", "summary": "Explain how a single base substitution causes a change in the structure of the beta polypeptide chain.", "figures": []},
    {"qnum": "02.2", "page": 4, "marks": 3, "specRef": "3.8.2.3", "summary": "Explain how HSCT is an effective long-term treatment for sickle cell disease.", "figures": []},
    {"qnum": "02.3", "page": 5, "marks": 3, "specRef": "3.8.4.1", "summary": "Use all the information provided and Figure 2 to evaluate the conclusion that gene therapy is more effective than HSCT.", "figures": ["fig-q2-fig2.jpg"]},

    {"qnum": "03.1", "page": 6, "marks": 2, "specRef": "3.6.1.1", "summary": "Explain why the student removed the shoot tip from each oat seedling.", "figures": ["fig-q3-table1.jpg"]},
    {"qnum": "03.2", "page": 7, "marks": 2, "specRef": "3.5.2", "summary": "Explain why the student added glucose solution to each Petri dish.", "figures": []},
    {"qnum": "03.3", "page": 7, "marks": 2, "specRef": "3.6.1.1", "summary": "Explain why the lids were kept on the Petri dishes.", "figures": []},
    {"qnum": "03.4", "page": 7, "marks": 3, "specRef": "3.6.1.1", "summary": "Describe and explain the results shown in Table 1 and suggest how results would differ for roots.", "figures": ["fig-q3-table1.jpg"]},
    {"qnum": "03.5", "page": 8, "marks": 1, "specRef": "RP", "summary": "Complete Table 2 with volumes of stock IAA solution and distilled water to produce 40 cm^3 of 10 ppm IAA.", "figures": []},

    {"qnum": "04.1", "page": 11, "marks": 4, "specRef": "3.6.3", "summary": "Use Figure 3 to evaluate the conclusion that a decrease in pH causes a decrease in the force of muscle contraction.", "figures": ["fig-q4-fig3.jpg"]},
    {"qnum": "04.2", "page": 12, "marks": 3, "specRef": "3.6.3", "summary": "Explain how a decrease in calcium ion concentration within muscle tissues could decrease the force of muscle contraction.", "figures": []},
    {"qnum": "04.3", "page": 12, "marks": 2, "specRef": "3.5.2", "summary": "Explain why converting pyruvate to lactate allows continued production of ATP by anaerobic respiration.", "figures": []},

    {"qnum": "05.1", "page": 14, "marks": 2, "specRef": "3.6.4.2", "summary": "Describe the role of glucagon in gluconeogenesis.", "figures": []},
    {"qnum": "05.2", "page": 14, "marks": 2, "specRef": "3.1.5.1", "summary": "Calculate the length in micrometres of the 9.531 kilobase gene for glucagon.", "figures": []},
    {"qnum": "05.3", "page": 15, "marks": 2, "specRef": "3.6.4.2", "summary": "Explain how increasing a cell's sensitivity to insulin lowers the blood glucose concentration.", "figures": []},
    {"qnum": "05.4", "page": 15, "marks": 3, "specRef": "3.6.4.2", "summary": "Explain how inhibiting adenylate cyclase may help to lower the blood glucose concentration.", "figures": []},

    {"qnum": "06.1", "page": 16, "marks": 1, "specRef": "3.7.1", "summary": "Give the full genotype of the fruit fly numbered 6 in Figure 4.", "figures": ["fig-q6-fig4.jpg"]},
    {"qnum": "06.2", "page": 16, "marks": 1, "specRef": "3.7.1", "summary": "Give one piece of evidence from Figure 4 to show that the allele for grey body colour is dominant.", "figures": ["fig-q6-fig4.jpg"]},
    {"qnum": "06.3", "page": 17, "marks": 2, "specRef": "3.7.1", "summary": "Explain one piece of evidence from Figure 4 to show that the gene for body colour is not on the X chromosome.", "figures": ["fig-q6-fig4.jpg"]},
    {"qnum": "06.4", "page": 17, "marks": 3, "specRef": "3.7.1", "summary": "Complete the genetic diagram for a heterozygous grey-bodied, white-eyed female crossed with a black-bodied, red-eyed male.", "figures": []},
    {"qnum": "06.5", "page": 18, "marks": 2, "specRef": "3.7.2", "summary": "Use the Hardy-Weinberg equation to calculate the percentage of flies heterozygous for gene G.", "figures": []},

    {"qnum": "07.1", "page": 19, "marks": 1, "specRef": "3.5.1", "summary": "Tick the chemicals needed for the light-dependent reaction of photosynthesis.", "figures": []},
    {"qnum": "07.2", "page": 19, "marks": 2, "specRef": "3.5.1", "summary": "Describe what happens during photoionisation in the light-dependent reaction.", "figures": []},
    {"qnum": "07.3", "page": 20, "marks": 1, "specRef": "RP", "summary": "Explain why the student marked the origin using a pencil rather than using ink.", "figures": ["fig-q7-fig5.jpg"]},
    {"qnum": "07.4", "page": 20, "marks": 2, "specRef": "RP", "summary": "Describe the method used to separate the pigments after the solution was applied to the origin.", "figures": ["fig-q7-fig5.jpg"]},
    {"qnum": "07.5", "page": 21, "marks": 1, "specRef": "RP", "summary": "Use Figure 5 to calculate the Rf value of pigment C given pigment A has an Rf value of 0.95.", "figures": ["fig-q7-fig5.jpg"]},
    {"qnum": "07.6", "page": 21, "marks": 1, "specRef": "3.5.1", "summary": "Suggest and explain the advantage of having different coloured pigments in leaves.", "figures": []},

    {"qnum": "08.1", "page": 22, "marks": 2, "specRef": "3.8.4.2", "summary": "State what a DNA probe is.", "figures": []},
    {"qnum": "08.2", "page": 22, "marks": 2, "specRef": "3.8.4.1", "summary": "Describe how the DNA is broken down into smaller fragments (Figure 6).", "figures": ["fig-q8-fig6.jpg"]},
    {"qnum": "08.3", "page": 23, "marks": 1, "specRef": "3.8.4.2", "summary": "Explain why the DNA on the nylon membrane is treated to form single strands.", "figures": []},
    {"qnum": "08.4", "page": 23, "marks": 2, "specRef": "3.8.4.3", "summary": "Suggest and explain how Lane 1 of Figure 7 enabled the size of the different viral fragments to be determined.", "figures": ["fig-q8-fig7.jpg"]},
    {"qnum": "08.5", "page": 24, "marks": 1, "specRef": "3.8.4.3", "summary": "Identify which volunteers had at least one of the viral DNA fragments with 250 base pairs or 535 base pairs.", "figures": ["fig-q8-fig7.jpg"]},

    {"qnum": "09.1", "page": 25, "marks": 5, "specRef": "3.7.4", "summary": "Describe how you could estimate the size of a population of sundews in a small marsh.", "figures": []},
    {"qnum": "09.2", "page": 25, "marks": 2, "specRef": "3.5.4", "summary": "Suggest and explain how digesting insects helps the sundew to grow in soil with very low concentrations of some nutrients.", "figures": []},

    {"qnum": "10.1", "page": 26, "marks": 3, "specRef": "3.6.2.1", "summary": "Explain how damage to the myelin sheath of neurones can cause muscular paralysis (lines 2-4).", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.2", "page": 27, "marks": 3, "specRef": "3.6.1.3", "summary": "Suggest and explain why Guillain-Barre syndrome sometimes causes heart rate irregularities (lines 4-5).", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.3", "page": 27, "marks": 3, "specRef": "3.8.2.2", "summary": "Suggest and explain how the single-stranded DNA drug could reduce the concentration of huntingtin protein (lines 13-14).", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.4", "page": 28, "marks": 2, "specRef": "3.8.2.2", "summary": "Suggest two reasons why the drug should not be considered a cure for Huntington's disease.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.5", "page": 28, "marks": 2, "specRef": "3.8.2.2", "summary": "Suggest two reasons why people had the drug injected into cerebrospinal fluid rather than taking a pill.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.6", "page": 28, "marks": 2, "specRef": "3.8.2.2", "summary": "Suggest and explain one way epigenetics may affect the age when symptoms of Huntington's disease start.", "figures": ["fig-q10-passage.jpg"]},
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
