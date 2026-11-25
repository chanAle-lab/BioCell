import json
import fitz
from pathlib import Path
from crop_official_markscheme import crop_official_markschemes

ROOT = Path(r"C:\Users\Alexander\.gemini\antigravity\scratch\coolBio")
DB_PATH = ROOT / "questions.json"
QP_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598917776_16d62256.pdf"
MS_PATH = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795598917723_cc881ff1.pdf"

PAPER_ID = "2017-june-7402-2"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2017,
    "series": "June",
    "unit": "7402/2",
    "level": "A-Level",
    "date": "2017-06-20",
    "title": "AQA A-Level Biology Paper 2 (7402/2) June 2017",
    "totalMarks": 91,
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-q2-fig2.jpg", "page": 6, "x0": 75, "y0": 212, "x1": 540, "y1": 608},
    {"filename": "fig-q4-table1.jpg", "page": 12, "x0": 115, "y0": 66, "x1": 540, "y1": 452},
    {"filename": "fig-q5-fig5.jpg", "page": 16, "x0": 75, "y0": 330, "x1": 540, "y1": 768},
    {"filename": "fig-q6-fig6.jpg", "page": 20, "x0": 80, "y0": 66, "x1": 540, "y1": 565},
    {"filename": "fig-q7-fig7.jpg", "page": 22, "x0": 115, "y0": 255, "x1": 540, "y1": 555},
    {"filename": "fig-q8-fig8.jpg", "page": 24, "x0": 115, "y0": 66, "x1": 540, "y1": 545},
    {"filename": "fig-q10-passage.jpg", "page": 29, "x0": 115, "y0": 62, "x1": 540, "y1": 415},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 4, "specRef": "3.6.2.1", "summary": "Describe the role of receptors and of the nervous system in increasing heart rate during exercise.", "figures": []},
    {"qnum": "01.2", "page": 3, "marks": 3, "specRef": "3.5.2", "summary": "Using Figure 1, explain the benefit of activation of AMPK during exercise.", "figures": []},

    {"qnum": "02.1", "page": 5, "marks": 2, "specRef": "3.7.4", "summary": "Explain how using the Sterile Insect Technique (SIT) could reduce transmission of dengue.", "figures": []},
    {"qnum": "02.2", "page": 5, "marks": 3, "specRef": "3.7.4", "summary": "Describe how the mark-release-recapture method could be used to determine the population of A. aegypti.", "figures": []},
    {"qnum": "02.3", "page": 6, "marks": 1, "specRef": "3.7.4", "summary": "Suggest one reason why releasing radiation-sterilised A. aegypti has not been very successful.", "figures": []},
    {"qnum": "02.4", "page": 6, "marks": 1, "specRef": "3.7.4", "summary": "Suggest why scientists released more transgenic males every week in Figure 2.", "figures": ["fig-q2-fig2.jpg"]},
    {"qnum": "02.5", "page": 7, "marks": 2, "specRef": "3.7.4", "summary": "Describe how the results in Figure 2 support the conclusion that transgenic males reduced A. aegypti numbers.", "figures": ["fig-q2-fig2.jpg"]},

    {"qnum": "03.1", "page": 8, "marks": 1, "specRef": "3.6.3", "summary": "Suggest one reason for the difference in succinic acid dehydrogenase staining between control and trained mice in Figure 3.", "figures": []},
    {"qnum": "03.2", "page": 9, "marks": 3, "specRef": "3.6.3", "summary": "Explain why trained mice were able to carry out prolonged exercise for longer than control mice.", "figures": []},
    {"qnum": "03.3", "page": 9, "marks": 2, "specRef": "3.6.3", "summary": "Calculate the mean diameter in micrometres of muscle fibres from a circular field of view of 1.25 mm^2.", "figures": []},
    {"qnum": "03.4", "page": 10, "marks": 2, "specRef": "3.6.3", "summary": "Describe two differences between the muscle fibre diameter distributions of young and adult mice in Figure 4.", "figures": []},

    {"qnum": "04.1", "page": 12, "marks": 2, "specRef": "3.5.1", "summary": "Explain why it was important that the suspension solution had the same water potential as the chloroplasts.", "figures": ["fig-q4-table1.jpg"]},
    {"qnum": "04.2", "page": 13, "marks": 2, "specRef": "3.5.1", "summary": "Explain why the student set up Tube 1 (without chloroplasts in light).", "figures": ["fig-q4-table1.jpg"]},
    {"qnum": "04.3", "page": 13, "marks": 2, "specRef": "3.5.1", "summary": "Explain the decolourisation of DCPIP in Tube 3.", "figures": ["fig-q4-table1.jpg"]},
    {"qnum": "04.4", "page": 13, "marks": 1, "specRef": "3.5.1", "summary": "Explain the advantage of using IC50 when evaluating weed-killers.", "figures": []},
    {"qnum": "04.5", "page": 14, "marks": 2, "specRef": "3.5.1", "summary": "Explain how chemicals that inhibit DCPIP decolourisation could slow the growth of weeds.", "figures": []},

    {"qnum": "05.1", "page": 16, "marks": 1, "specRef": "3.5.4", "summary": "Suggest one way in which increased uptake of phosphate could increase plant growth.", "figures": []},
    {"qnum": "05.2", "page": 16, "marks": 1, "specRef": "3.5.4", "summary": "Suggest one way in which arbuscular mycorrhiza fungi (AMF) benefit from associating with plants.", "figures": []},
    {"qnum": "05.3", "page": 16, "marks": 2, "specRef": "3.5.3", "summary": "Explain why an increase in shoot biomass can be taken as a measurement of net primary productivity.", "figures": ["fig-q5-fig5.jpg"]},
    {"qnum": "05.4", "page": 17, "marks": 4, "specRef": "3.5.3", "summary": "Use Figure 5 to evaluate the effect on plant productivity of adding AMF species and phosphate to soil.", "figures": ["fig-q5-fig5.jpg"]},
    {"qnum": "05.5", "page": 18, "marks": 2, "specRef": "3.5.3", "summary": "Determine the rate of shoot biomass production in g day^-1 for the normal phosphate control plot using Figure 5.", "figures": ["fig-q5-fig5.jpg"]},

    {"qnum": "06.1", "page": 19, "marks": 2, "specRef": "3.6.4.2", "summary": "Give two reasons why pancreas transplants are not used to treat type II diabetes.", "figures": []},
    {"qnum": "06.2", "page": 19, "marks": 1, "specRef": "3.6.4.2", "summary": "Tick the statement which describes incorrectly the action of insulin.", "figures": []},
    {"qnum": "06.3", "page": 20, "marks": 2, "specRef": "3.8.2.2", "summary": "Suggest how transcription factors can reprogramme skin cells to form iPS cells.", "figures": ["fig-q6-fig6.jpg"]},
    {"qnum": "06.4", "page": 21, "marks": 4, "specRef": "3.8.2.1", "summary": "Use Figure 6 and the information provided to evaluate the use of iPS cells to treat type I diabetes in humans.", "figures": ["fig-q6-fig6.jpg"]},

    {"qnum": "07.1", "page": 22, "marks": 2, "specRef": "3.7.1", "summary": "State what is meant by the term phenotype.", "figures": []},
    {"qnum": "07.2", "page": 22, "marks": 1, "specRef": "3.7.1", "summary": "Name the type of gene interaction shown in Figure 7.", "figures": ["fig-q7-fig7.jpg"]},
    {"qnum": "07.3", "page": 22, "marks": 1, "specRef": "3.7.1", "summary": "Give the expected fruit colours for genotypes AAbb and aaBB from Figure 7.", "figures": ["fig-q7-fig7.jpg"]},
    {"qnum": "07.4", "page": 23, "marks": 3, "specRef": "3.7.1", "summary": "Complete the genetic diagram for the cross aabb x AaBb showing genotypes, phenotypes and phenotypic ratio.", "figures": ["fig-q7-fig7.jpg"]},
    {"qnum": "07.5", "page": 23, "marks": 2, "specRef": "3.7.2", "summary": "Use the Hardy-Weinberg equation to calculate the percentage of plants heterozygous for gene B.", "figures": []},

    {"qnum": "08.1", "page": 24, "marks": 1, "specRef": "3.8.4.1", "summary": "Explain the role of reverse transcriptase in RT-PCR.", "figures": ["fig-q8-fig8.jpg"]},
    {"qnum": "08.2", "page": 25, "marks": 1, "specRef": "3.8.4.1", "summary": "Explain the role of DNA polymerase in RT-PCR.", "figures": ["fig-q8-fig8.jpg"]},
    {"qnum": "08.3", "page": 25, "marks": 2, "specRef": "3.8.4.1", "summary": "Explain why any DNA in the sample is hydrolysed by enzymes before RT-PCR.", "figures": ["fig-q8-fig8.jpg"]},
    {"qnum": "08.4", "page": 26, "marks": 2, "specRef": "3.8.4.1", "summary": "Calculate the ratio of RNA content in sample A to sample B using 1/C from Figure 9.", "figures": []},
    {"qnum": "08.5", "page": 27, "marks": 1, "specRef": "3.8.4.1", "summary": "Suggest one reason why DNA replication stops in PCR.", "figures": []},
    {"qnum": "08.6", "page": 27, "marks": 2, "specRef": "3.8.4.1", "summary": "Explain why scientists produced a variety of primers to detect different RNA respiratory viruses.", "figures": []},

    {"qnum": "09.1", "page": 28, "marks": 1, "specRef": "3.7.2", "summary": "Define a gene pool.", "figures": []},
    {"qnum": "09.2", "page": 28, "marks": 5, "specRef": "3.7.3", "summary": "Suggest how two species of palm tree on Lord Howe Island arose by sympatric speciation.", "figures": []},

    {"qnum": "10.1", "page": 29, "marks": 2, "specRef": "3.7.2", "summary": "Calculate the annual percentage increase in Alzheimer's disease cases in America for 2014.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.2", "page": 30, "marks": 3, "specRef": "3.6.2.2", "summary": "Explain how donepezil could improve communication between nerve cells.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.3", "page": 30, "marks": 2, "specRef": "3.7.2", "summary": "Suggest and explain two reasons why there is a high frequency of the E280A mutation in Yaramul.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.4", "page": 30, "marks": 2, "specRef": "3.7.3", "summary": "Explain why natural selection has not reduced the frequency of the E280A mutation.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.5", "page": 31, "marks": 2, "specRef": "3.8.2.2", "summary": "Suggest and explain one reason why the age at which the E280A mutation is expressed varies.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.6", "page": 31, "marks": 2, "specRef": "3.7.1", "summary": "Suggest explanations for why 102 individuals had a sample size of 204 and 75 mutations but 74 potential AD cases.", "figures": ["fig-q10-passage.jpg"]},
    {"qnum": "10.7", "page": 31, "marks": 2, "specRef": "3.8.4.3", "summary": "Suggest why a DNA probe for the mutated triplet was not suitable for detecting the E280A mutation.", "figures": ["fig-q10-passage.jpg"]},
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
