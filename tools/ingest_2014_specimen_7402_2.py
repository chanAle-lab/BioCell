import json, os, re
import fitz

QP_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599564166_062d8f08.pdf"
MS_PDF = r"C:\Users\Alexander\.gemini\antigravity\brain\612a35cc-d762-46fb-84f6-b44e37b7645b\.user_uploaded\media_1795599564103_f10af63a.pdf"

PAPER_ID = "2014-specimen-7402-2"
OUT_IMG_DIR = os.path.join("img", PAPER_ID)
OUT_MS_DIR = os.path.join(OUT_IMG_DIR, "ms")
os.makedirs(OUT_MS_DIR, exist_ok=True)

QUESTIONS = [
    ("01.1", 2,  3, "3.5.2", "Explaining experimental setup steps in respirometer investigation", ["fig-q1-fig1.jpg"]),
    ("01.2", 3,  2, "3.5.2", "Why chosen temperature was 20 °C for pea seed respiration", ["fig-q1-fig1.jpg"]),
    ("01.3", 4,  3, "3.5.2", "Why coloured liquid moved towards tube B in respirometer", ["fig-q1-fig1.jpg", "fig-q1-table1.jpg"]),
    ("01.4", 5,  2, "3.5.2", "Calculating oxygen consumption rate per gram of pea seeds", ["fig-q1-table1.jpg"]),
    ("02.1", 7,  5, "3.6.3", "Roles of calcium ions and ATP in myofibril contraction", []),
    ("02.2", 7,  2, "3.5.2", "Why ATP is an immediate energy source in biological processes", []),
    ("03.1", 8,  1, "3.7.1", "Meaning of linked genes in fruit flies", []),
    ("03.2", 9,  4, "3.7.1", "Explaining fruit fly offspring phenotypes using gene linkage and crossing over", ["fig-q3-fig2-fig3.jpg"]),
    ("03.3", 9,  1, "3.7.1", "Expected offspring ratio if body colour and wing length genes were not linked", ["fig-q3-fig2-fig3.jpg"]),
    ("03.4", 9,  2, "3.7.1", "Identifying chi-squared test and why it is appropriate", ["fig-q3-fig2-fig3.jpg"]),
    ("04.1", 10, 2, "3.6.2", "Explaining resting potential across neurone membrane", ["fig-q4-fig4-table2.jpg"]),
    ("04.2", 11, 3, "3.6.1", "How pressure on Pacinian corpuscle changes potential at Q", ["fig-q4-fig4-table2.jpg"]),
    ("04.3", 11, 2, "3.6.2", "Why heavy pressure is needed to record potential at R and S", ["fig-q4-fig4-table2.jpg"]),
    ("04.4", 11, 2, "3.6.2", "Effect of myelin sheath damage on potential recorded at S", ["fig-q4-fig4-table2.jpg"]),
    ("05.1", 13, 2, "3.8.4", "Why plasmids were injected into silkworm eggs rather than adult cells", ["fig-q5-fig5.jpg"]),
    ("05.2", 13, 2, "3.8.4", "Explaining use of marker gene for green fluorescent protein", ["fig-q5-fig5.jpg"]),
    ("05.3", 13, 1, "3.8.4", "Naming DNA sequence required for RNA polymerase binding", ["fig-q5-fig5.jpg"]),
    ("05.4", 13, 2, "3.8.4", "Why transgenic silkworms were engineered to secrete protein into cocoons", ["fig-q5-fig5.jpg"]),
    ("06.1", 14, 2, "3.7.2", "Using Hardy-Weinberg equation to calculate heterozygous mosquito frequency", ["fig-q6-fig6.jpg"]),
    ("06.2", 15, 4, "3.7.3", "Explaining change in KDR minus allele frequency from 2003 to 2012", ["fig-q6-fig6.jpg"]),
    ("06.3", 15, 2, "3.6.2", "How DDT causes continuous firing of action potentials", []),
    ("06.4", 15, 2, "3.7.3", "How KDR minus allele confers resistance to DDT", []),
    ("07.1", 16, 1, "3.6.4", "Part of brain containing osmoreceptors", []),
    ("07.2", 16, 2, "3.6.4", "Effect of sweating without drinking on ADH secretion", []),
    ("07.3", 16, 4, "3.6.4", "How ADH reduces water loss in the kidneys", []),
    ("07.4", 17, 1, "3.6.4", "Calculating glomerular filtration rate from creatinine excretion", []),
    ("07.5", 17, 1, "3.6.4", "Two reasons GFR measurement assumes creatinine is not reabsorbed or secreted", []),
    ("08.1", 18, 2, "3.5.1", "Why rate of oxygen production was measured in chloroplast investigation", ["fig-q8-fig7.jpg"]),
    ("08.2", 19, 4, "3.5.1", "Calculating extra oxygen produced by normal plants vs mutant plants", ["fig-q8-fig7.jpg"]),
    ("08.3", 19, 2, "3.5.1", "Explaining difference in oxygen production between normal and mutant chloroplasts", ["fig-q8-fig7.jpg"]),
    ("09.1", 20, 3, "3.8.2", "How methylation of tumour suppressor genes leads to cancer", []),
    ("09.2", 21, 3, "3.8.2", "Describing suitable scatter graph for fat intake and breast cancer deaths", ["fig-q9-table3.jpg"]),
    ("09.3", 21, 2, "3.8.2", "Evaluating whether Table 3 proves fat in diet causes breast cancer", ["fig-q9-table3.jpg"]),
    ("10.1", 22, 3, "3.5.2", "Why mitochondrial disease causes muscle weakness", ["fig-q10-passage.jpg"]),
    ("10.2", 23, 4, "3.7.1", "Comparing chances of passing mitochondrial disease for Couple A and Couple B", ["fig-q10-passage.jpg"]),
    ("10.3", 24, 3, "3.8.1", "How mitochondrial tRNA gene mutation prevents polypeptide production", ["fig-q10-passage.jpg"]),
    ("10.4", 24, 3, "3.5.2", "Why blood lactate concentration increases after exercise in MD patients", ["fig-q10-passage.jpg"]),
    ("10.5", 25, 2, "3.8.4", "Two reasons PCR is used before testing embryonic DNA", ["fig-q10-passage.jpg"]),
]

FIGURES = [
    ("fig-q1-fig1.jpg",        2,  125, 505),
    ("fig-q1-table1.jpg",      4,   75, 460),
    ("fig-q3-fig2-fig3.jpg",   8,  205, 770),
    ("fig-q4-fig4-table2.jpg", 10, 155, 615),
    ("fig-q5-fig5.jpg",        12,  75, 430),
    ("fig-q6-fig6.jpg",        14,  65, 485),
    ("fig-q8-fig7.jpg",        18,  75, 505),
    ("fig-q9-table3.jpg",      20, 360, 770),
    ("fig-q10-passage.jpg",    22,  75, 458),
]


def crop_figures():
    doc = fitz.open(QP_PDF)
    for fname, page_num, y0, y1 in FIGURES:
        page = doc[page_num - 1]
        rect = fitz.Rect(35, y0, page.rect.width - 35, y1)
        pix = page.get_pixmap(clip=rect, dpi=180)
        out = os.path.join(OUT_IMG_DIR, fname)
        pix.save(out)
        print(f"Saved figure {out}")


def crop_mark_schemes():
    doc = fitz.open(MS_PDF)
    markers = []
    for pno in range(len(doc)):
        if pno < 4:
            continue
        blocks = doc[pno].get_text("blocks")
        for b in blocks:
            txt = " ".join(b[4].split())
            m = re.match(r"^(0[1-9]\.[1-9]|10\.[1-9])\b", txt)
            if m:
                qcode = m.group(1)
                if not any(x[0] == qcode for x in markers):
                    markers.append((qcode, pno, b[1]))
    markers.sort(key=lambda x: (x[1], x[2]))
    print(f"Found {len(markers)} MS markers")
    for idx, (qcode, pno, y_start) in enumerate(markers):
        if idx + 1 < len(markers):
            next_pno, next_y = markers[idx + 1][1], markers[idx + 1][2]
        else:
            next_pno, next_y = pno, 760
        q_num, sub_num = qcode.split(".")
        out_name = f"q{int(q_num):02d}-{int(sub_num)}.png"
        out_path = os.path.join(OUT_MS_DIR, out_name)

        if next_pno == pno:
            y0 = max(60, y_start - 8)
            y1 = min(770, next_y - 4)
            rect = fitz.Rect(35, y0, doc[pno].rect.width - 35, y1)
            pix = doc[pno].get_pixmap(clip=rect, dpi=180)
            pix.save(out_path)
        else:
            imgs = []
            for p in range(pno, next_pno + 1):
                page = doc[p]
                y0 = max(60, y_start - 8) if p == pno else 65
                y1 = min(770, next_y - 4) if p == next_pno else 765
                if y1 - y0 < 15:
                    continue
                rect = fitz.Rect(35, y0, page.rect.width - 35, y1)
                imgs.append(page.get_pixmap(clip=rect, dpi=180))
            if len(imgs) == 1:
                imgs[0].save(out_path)
            else:
                from PIL import Image
                import io
                pil_imgs = [Image.open(io.BytesIO(im.tobytes("png"))) for im in imgs]
                w = max(im.width for im in pil_imgs)
                h = sum(im.height for im in pil_imgs)
                merged = Image.new("RGB", (w, h), (255, 255, 255))
                cy = 0
                for im in pil_imgs:
                    merged.paste(im, (0, cy))
                    cy += im.height
                merged.save(out_path)
        print(f"Saved MS {out_path}")


def update_questions_json():
    with open("questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data["papers"] = [p for p in data["papers"] if p["id"] != PAPER_ID]
    data["questions"] = [q for q in data["questions"] if q["paper"] != PAPER_ID]

    data["papers"].append({
        "id": PAPER_ID,
        "year": 2014,
        "series": "Specimen",
        "unit": "7402/2",
        "level": "A-Level",
        "title": "2014 Specimen A-Level Paper 2 (7402/2)",
        "totalMarks": 91
    })

    for qcode, page, marks, spec_ref, summary, figs in QUESTIONS:
        q_num, sub_num = qcode.split(".")
        data["questions"].append({
            "id": f"{PAPER_ID}-q{qcode}",
            "paper": PAPER_ID,
            "year": 2014,
            "series": "Specimen",
            "unit": "7402/2",
            "level": "A-Level",
            "question": qcode,
            "questionNumber": qcode,
            "page": page,
            "marks": marks,
            "specRef": spec_ref,
            "topics": [spec_ref],
            "summary": summary,
            "image": f"img/{PAPER_ID}/q{int(q_num):02d}-{int(sub_num)}.jpg",
            "markscheme": f"img/{PAPER_ID}/ms/q{int(q_num):02d}-{int(sub_num)}.png",
            "figures": [f"img/{PAPER_ID}/{fg}" for fg in figs]
        })

    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated questions.json with {len(QUESTIONS)} questions for {PAPER_ID}")


if __name__ == "__main__":
    crop_figures()
    crop_mark_schemes()
    update_questions_json()
