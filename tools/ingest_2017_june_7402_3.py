import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598917902_0893e518.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598917679_6fe1004c.pdf"

PAPER_ID = "2017-june-7402-3"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2017,
    "series": "June",
    "unit": "7402/3",
    "level": "A-Level",
    "date": "2017-06-26",
    "title": "AQA A-Level Biology Paper 3 (7402/3) June 2017",
    "totalMarks": 78,
    "optionalMarks": 25,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q2-fig2.jpg", "page": 6, "x0": 115, "y0": 66, "x1": 530, "y1": 388},
    {"filename": "fig-q2-fig3.jpg", "page": 8, "x0": 75, "y0": 66, "x1": 535, "y1": 588},
    {"filename": "fig-q3-fig4.jpg", "page": 10, "x0": 50, "y0": 274, "x1": 535, "y1": 698},
    {"filename": "fig-q6-fig5.jpg", "page": 18, "x0": 115, "y0": 66, "x1": 535, "y1": 298},
    {"filename": "fig-q6-fig7.jpg", "page": 22, "x0": 60, "y0": 66, "x1": 535, "y1": 520},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 3, "marks": 3, "specRef": "3.6.2.2", "summary": "Describe how a nerve impulse arriving at a synapse causes neurotransmitter release from vesicles.", "figures": []},
    {"qnum": "01.2", "page": 4, "marks": 2, "specRef": "3.6.3", "summary": "Suggest how the myosin molecule moves a mitochondrion towards the presynaptic membrane in Figure 1.", "figures": []},
    {"qnum": "01.3", "page": 5, "marks": 2, "specRef": "3.6.2.2", "summary": "Suggest and explain one advantage of mitochondria moving towards the presynaptic membrane.", "figures": []},

    {"qnum": "02.1", "page": 6, "marks": 1, "specRef": "3.2.1.2", "summary": "Tick the correct statement about the structures of a bacteriophage and a bacterium in Figure 2.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.2", "page": 7, "marks": 2, "specRef": "3.2.1.3", "summary": "Use the scales in Figure 2 to calculate how many times longer the bacterium is than the bacteriophage.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.3", "page": 8, "marks": 1, "specRef": "3.2.1.2", "summary": "State the scientists' null hypothesis for the bacteriophage lung infection investigation in Figure 3.", "figures": ["fig-q2-fig3.jpg"]},
    {"qnum": "02.4", "page": 9, "marks": 2, "specRef": "RP", "summary": "Use Figure 3 to explain why serial dilutions were necessary for some bacterial samples but not others.", "figures": ["fig-q2-fig3.jpg"]},
    {"qnum": "02.5", "page": 9, "marks": 3, "specRef": "3.2.1.2", "summary": "Conclude from Figure 3 the effectiveness of the bacteriophage in treating lung infections in mice.", "figures": ["fig-q2-fig3.jpg"]},

    {"qnum": "03.1", "page": 10, "marks": 2, "specRef": "3.5.4", "summary": "Give two examples of nitrogen-containing biological molecules removed when a crop is harvested.", "figures": []},
    {"qnum": "03.2", "page": 10, "marks": 2, "specRef": "3.5.4", "summary": "Use Figure 4 to calculate the difference in mass of grain produced per hectare in 1970 compared with 2005.", "figures": ["fig-q3-fig4.jpg"]},
    {"qnum": "03.3", "page": 11, "marks": 2, "specRef": "3.5.4", "summary": "Use Figure 4 to evaluate the use of artificial fertilisers on grain-producing crops in India.", "figures": ["fig-q3-fig4.jpg"]},

    {"qnum": "04.1", "page": 12, "marks": 2, "specRef": "3.4.6", "summary": "Calculate the index of diversity for the Scottish island grassland site using Table 1.", "figures": []},
    {"qnum": "04.2", "page": 13, "marks": 3, "specRef": "RP", "summary": "Outline a method ecologists could have used to determine plant species richness at one site.", "figures": []},
    {"qnum": "04.3", "page": 14, "marks": 3, "specRef": "3.4.6", "summary": "State whether Table 2 shows significant changes in grassland communities on Islay, Colonsay and Harris.", "figures": []},

    {"qnum": "05.1", "page": 16, "marks": 2, "specRef": "3.1.5.2", "summary": "Name two enzymes involved in the semi-conservative replication of DNA.", "figures": []},
    {"qnum": "05.2", "page": 16, "marks": 2, "specRef": "3.1.4.2", "summary": "Suggest why phosphorylation by ATR enables DNA-repair enzymes to bind to their substrates.", "figures": []},
    {"qnum": "05.3", "page": 17, "marks": 1, "specRef": "3.1.4.2", "summary": "Use energy changes to suggest why ATR-activated reactions only occur if substrates are phosphorylated.", "figures": []},
    {"qnum": "05.4", "page": 17, "marks": 3, "specRef": "3.8.2.3", "summary": "Predict the possible effects of a mutation producing a non-functional form of ATM.", "figures": []},

    {"qnum": "06.1", "page": 18, "marks": 2, "specRef": "RP", "summary": "Calculate the rate of water uptake in mm^3 hour^-1 from the potometer experiment in Figure 5.", "figures": ["fig-q6-fig5.jpg"]},
    {"qnum": "06.2", "page": 19, "marks": 3, "specRef": "RP", "summary": "Outline a method to determine the rate of water loss per mm^2 of leaf surface area.", "figures": ["fig-q6-fig5.jpg"]},
    {"qnum": "06.3", "page": 19, "marks": 1, "specRef": "3.3.4.2", "summary": "Suggest one reason why water movement in a cut shoot in a potometer may differ from a whole plant.", "figures": []},
    {"qnum": "06.4", "page": 20, "marks": 2, "specRef": "3.2.3", "summary": "Use Figure 6 to suggest two reasons why water and carbon dioxide molecules can both pass through PIP1.", "figures": []},
    {"qnum": "06.5", "page": 21, "marks": 3, "specRef": "3.8.2.2", "summary": "Conclude the effect of foreign DNA producing single-stranded RNA on PIP1 expression in transgenic poplars.", "figures": []},
    {"qnum": "06.6", "page": 21, "marks": 1, "specRef": "3.8.2.2", "summary": "Suggest why transgenic poplars still produced some PIP1.", "figures": []},
    {"qnum": "06.7", "page": 22, "marks": 3, "specRef": "3.2.3", "summary": "Use Figure 7 to evaluate the importance of PIP1 in moving carbon dioxide and water through poplar leaves.", "figures": ["fig-q6-fig7.jpg"]},

    {"qnum": "07.1", "page": 24, "marks": 25, "specRef": "Essay", "summary": "Essay: The importance of nitrogen-containing substances in biological systems.", "figures": []},
    {"qnum": "07.2", "page": 24, "marks": 25, "specRef": "Essay", "summary": "Essay: The importance of diffusion in organisms.", "figures": []},
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
