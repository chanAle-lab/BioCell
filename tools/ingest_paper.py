"""coolBio Streamlined Past Paper Ingestion Tool (AQA Biology 7401 / 7402).

Ingests an AQA Biology Question Paper + Mark Scheme PDF pair:
1. Crops per-question .jpg images from the Question Paper.
2. Crops official per-question .png markscheme images from the Mark Scheme PDF.
3. Maps AQA Biology specification topics (3.1.1–3.8.4 & RP) and skills.
4. Updates questions.json idempotently for the given paper ID.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_official_markscheme import crop_official_markschemes
from crop_qp_questions import crop_qp_questions

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions.json"

# Canonical mapping overrides when MS labels differ from QP (e.g. "06" -> "6" or "06.1")
MS_QNUM_MAP: dict[str, str] = {}

TOPIC_KEYWORDS = [
    ("3.1.1", ["monomer", "polymer", "condensation", "hydrolysis"]),
    ("3.1.2", ["monosaccharide", "disaccharide", "polysaccharide", "starch", "glycogen", "cellulose", "glycosidic", "benedict", "iodine"]),
    ("3.1.3", ["triglyceride", "phospholipid", "fatty acid", "ester bond", "emulsion test"]),
    ("3.1.4", ["amino acid", "peptide bond", "tertiary structure", "quaternary", "biuret", "enzyme", "active site", "induced fit", "inhibitor"]),
    ("3.1.5", ["nucleotide", "phosphodiester", "dna helicase", "dna polymerase", "semi-conservative", "meselson"]),
    ("3.1.6", ["atp hydrolase", "atp synthase", "adenosine triphosphate"]),
    ("3.1.7", ["specific heat capacity", "latent heat of vaporisation", "cohesion", "metabolite"]),
    ("3.1.8", ["inorganic ion", "fe2+", "haem group", "phosphate ion"]),
    ("3.2.1", ["eukaryote", "prokaryote", "mitochondri", "chloroplast", "golgi", "lysosome", "ribosome", "magnification", "resolution", "cell fractionation", "ultracentrifugation"]),
    ("3.2.2", ["mitosis", "interphase", "prophase", "metaphase", "anaphase", "telophase", "mitotic index", "binary fission", "tumour"]),
    ("3.2.3", ["phospholipid bilayer", "fluid-mosaic", "facilitated diffusion", "osmosis", "water potential", "active transport", "co-transport"]),
    ("3.2.4", ["phagocyt", "lysozyme", "t lymphocyte", "b lymphocyte", "plasma cell", "antibody", "monoclonal", "vaccine", "herd immunity", "hiv", "elisa"]),
    ("3.3.1", ["surface area to volume", "sa:v"]),
    ("3.3.2", ["spiracle", "tracheole", "gill lamellae", "countercurrent", "stomata", "xerophyte", "alveoli", "diaphragm", "intercostal"]),
    ("3.3.3", ["amylase", "disaccharidase", "endopeptidase", "exopeptidase", "micelle", "lipase", "bile salt"]),
    ("3.3.4", ["haemoglobin", "bohr", "dissociation curve", "cardiac cycle", "arteriole", "tissue fluid", "xylem", "cohesion-tension", "phloem", "mass flow"]),
    ("3.4.1", ["histone", "intron", "exon", "degenerate", "non-overlapping", "triplet"]),
    ("3.4.2", ["transcription", "splicing", "pre-mrna", "translation", "trna", "anticodon", "codon"]),
    ("3.4.3", ["meiosis", "crossing over", "chiasma", "independent segregation", "non-disjunction"]),
    ("3.4.4", ["natural selection", "directional selection", "stabilising selection", "antibiotic resistance"]),
    ("3.4.5", ["courtship", "phylogenetic", "taxonomy", "binomial"]),
    ("3.4.6", ["index of diversity", "species richness", "monoculture", "hedgerow"]),
    ("3.4.7", ["random sampling", "standard deviation", "amino acid sequence"]),
    ("3.5.1", ["photosynthesis", "thylakoid", "stroma", "calvin cycle", "rubisco", "photolysis", "dcpip"]),
    ("3.5.2", ["glycolysis", "pyruvate", "link reaction", "krebs cycle", "oxidative phosphorylation", "cristae", "lactate", "anaerobic"]),
    ("3.5.3", ["gross primary", "net primary", "npp", "gpp", "trophic"]),
    ("3.5.4", ["nitrogen fixation", "nitrification", "denitrification", "saprobiont", "mycorrhizae", "eutrophication"]),
    ("3.6.1", ["taxis", "kinesis", "iaa", "phototropism", "pacinian", "rhodopsin", "iodopsin", "medulla", "chemoreceptor"]),
    ("3.6.2", ["resting potential", "action potential", "depolarisation", "repolarisation", "refractory", "saltatory", "synapse", "acetylcholine"]),
    ("3.6.3", ["sarcomere", "actin", "myosin", "troponin", "tropomyosin", "phosphocreatine"]),
    ("3.6.4", ["insulin", "glucagon", "glycogenolysis", "gluconeogenesis", "nephron", "loop of henle", "adh", "aquaporin", "osmoreceptor"]),
    ("3.7.1", ["monohybrid", "dihybrid", "codominance", "sex-linked", "epistasis", "chi-squared"]),
    ("3.7.2", ["hardy-weinberg", "allele frequency", "gene pool"]),
    ("3.7.3", ["allopatric", "sympatric", "speciation", "genetic drift"]),
    ("3.7.4", ["carrying capacity", "quadrat", "mark-release-recapture", "succession", "climax community", "pioneer species"]),
    ("3.8.1", ["substitution", "frameshift", "nonsense", "missense"]),
    ("3.8.2", ["totipotent", "pluripotent", "ips", "transcription factor", "oestrogen", "epigenetic", "methylation", "acetylation", "sirna", "oncogene", "tumour suppressor"]),
    ("3.8.3", ["genome project", "proteome"]),
    ("3.8.4", ["reverse transcriptase", "restriction endonuclease", "plasmid", "pcr", "taq polymerase", "dna probe", "vntr", "genetic fingerprinting"]),
    ("RP", ["required practical", "colorimeter", "potometer", "aseptic", "choice chamber", "belt transect"]),
]


def map_topics(text: str) -> list[str]:
    low = text.lower()
    matched = []
    for code, kws in TOPIC_KEYWORDS:
        if any(kw in low for kw in kws):
            matched.append(code)
    return matched[:3] if matched else ["3.1.1"]


def infer_skills(text: str) -> list[str]:
    low = text.lower()
    skills = []
    if any(k in low for k in ["calculate", "percentage", "ratio", "mean", "standard deviation", "chi-squared", "rate"]):
        skills.append("maths")
    if any(k in low for k in ["method", "control", "variable", "colorimeter", "microscope", "quadrat", "transect"]):
        skills.append("practical")
    if any(k in low for k in ["explain", "suggest", "evaluate", "conclude", "compare", "describe"]):
        skills.append("analysis")
    if any(k in low for k in ["essay", "write an essay"]):
        skills.append("extended")
    return skills


def ingest(
    qp_pdf: Path,
    ms_pdf: Path,
    paper_id: str,
    unit: str,
    level: str,
    year: int,
    series: str,
    total_marks: int,
    title: str | None = None,
) -> None:
    img_dir = ROOT / "img" / paper_id
    qp_crops = crop_qp_questions(qp_pdf, img_dir)
    if not qp_crops:
        raise RuntimeError(f"No question markers detected in {qp_pdf}")

    qnums = list(qp_crops.keys())
    ms_labels = [MS_QNUM_MAP.get(q, q) for q in qnums]
    ms_map = crop_official_markschemes(ms_pdf, ms_labels, img_dir / "ms")

    qp_doc = fitz.open(str(qp_pdf))
    full_text = "\n".join(p.get_text() for p in qp_doc)
    qp_doc.close()

    paper_meta = {
        "id": paper_id,
        "year": year,
        "series": series,
        "unit": unit,
        "level": level,
        "date": f"{year}-06-15" if series.lower() == "june" else f"{year}-01-15",
        "title": title or f"{unit} — {level} ({series} {year})",
        "totalMarks": total_marks,
        "pdf": None,
        "ms": None,
    }

    db = json.loads(DB_PATH.read_text(encoding="utf-8"))
    db["papers"] = [p for p in db["papers"] if p["id"] != paper_id]
    db["questions"] = [q for q in db["questions"] if q.get("paper") != paper_id]
    db["papers"].append(paper_meta)

    for qnum in qnums:
        ms_key = MS_QNUM_MAP.get(qnum, qnum)
        ms_file = ms_map.get(ms_key)
        if not ms_file:
            print(f"Warning: No markscheme crop matched for {qnum} (key={ms_key})")
            continue
        topics = map_topics(full_text)
        db["questions"].append(
            {
                "id": f"{paper_id}-q{qnum}",
                "paper": paper_id,
                "year": year,
                "series": series,
                "unit": unit,
                "level": level,
                "question": qnum,
                "questionNumber": qnum,
                "page": 1,
                "marks": 1,
                "topics": [topics[0]],
                "skills": infer_skills(full_text),
                "summary": f"{unit} Question {qnum}",
                "specRef": topics[0],
                "image": f"img/{paper_id}/{qp_crops[qnum]}",
                "markscheme": f"img/{paper_id}/ms/{ms_file}",
                "figures": [],
            }
        )

    DB_PATH.write_text(json.dumps(db, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Ingested {paper_id}: {len(qnums)} questions.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest AQA Biology 7401/7402 QP + MS PDFs into coolBio.")
    parser.add_argument("--qp", required=True, type=Path, help="Path to Question Paper PDF")
    parser.add_argument("--ms", required=True, type=Path, help="Path to Mark Scheme PDF")
    parser.add_argument("--paper-id", required=True, help="Paper ID (e.g. 2023-june-7402-1)")
    parser.add_argument("--unit", required=True, help="Unit code (e.g. 7402/1)")
    parser.add_argument("--level", default="A-level", choices=["AS", "A-level"], help="Qualification level")
    parser.add_argument("--year", required=True, type=int, help="Exam year")
    parser.add_argument("--series", default="June", help="Exam series (e.g. June)")
    parser.add_argument("--total-marks", required=True, type=int, help="Official paper total marks")
    parser.add_argument("--title", default=None, help="Optional paper display title")
    args = parser.parse_args()
    ingest(args.qp, args.ms, args.paper_id, args.unit, args.level, args.year, args.series, args.total_marks, args.title)


if __name__ == "__main__":
    main()
