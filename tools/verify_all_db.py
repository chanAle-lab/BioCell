"""Verify integrity of coolBio/questions.json and all referenced image/markscheme files."""

import json
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
QUESTIONS_FILE = REPO_DIR / "questions.json"


def verify() -> bool:
    db = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    papers = {p["id"]: p for p in db.get("papers", [])}
    questions = db.get("questions", [])
    print(f"Total papers in database: {len(papers)}")
    print(f"Total questions in database: {len(questions)}")

    missing_images = []
    missing_ms = []
    invalid_ms_key = []
    missing_figures = []
    paper_marks = {}
    paper_counts = {}

    for q in questions:
        pid = q.get("paper", "unknown")
        paper_counts[pid] = paper_counts.get(pid, 0) + 1
        paper_marks[pid] = paper_marks.get(pid, 0) + int(q.get("marks", 0))

        img_rel = q.get("image")
        if not img_rel:
            missing_images.append((q["id"], "No image field"))
        else:
            img_abs = REPO_DIR / img_rel.replace("/", "\\")
            if not img_abs.exists() or img_abs.stat().st_size == 0:
                missing_images.append((q["id"], img_rel))

        ms_rel = q.get("markscheme")
        if isinstance(ms_rel, dict):
            ms_rel = ms_rel.get("image")
        elif isinstance(ms_rel, list):
            ms_rel = ms_rel[0] if ms_rel else None
        if not ms_rel:
            invalid_ms_key.append(q["id"])
        else:
            ms_abs = REPO_DIR / ms_rel.replace("/", "\\")
            if not ms_abs.exists() or ms_abs.stat().st_size == 0:
                missing_ms.append((q["id"], ms_rel))

        for fig_rel in q.get("figures", []):
            fig_abs = REPO_DIR / fig_rel.replace("/", "\\")
            if not fig_abs.exists() or fig_abs.stat().st_size == 0:
                missing_figures.append((q["id"], fig_rel))

    marks_mismatch = []
    print("\n--- Summary per Paper ---")
    for pid in sorted(papers.keys()):
        expected = papers[pid].get("totalMarks")
        optional = papers[pid].get("optionalMarks", 0)
        actual = paper_marks.get(pid, 0)
        cnt = paper_counts.get(pid, 0)
        status = "OK" if (expected is None or actual == expected + optional) else f"MISMATCH (expected {expected + optional})"
        print(f"  {pid}: {cnt} questions, {actual}m [{status}]")
        if expected is not None and actual != expected + optional:
            marks_mismatch.append((pid, actual, expected + optional))

    print("\n--- Integrity Results ---")
    print(f"Missing or empty question images: {len(missing_images)}")
    for item in missing_images[:10]:
        print("  ", item)

    print(f"Missing markscheme key in q: {len(invalid_ms_key)}")
    for item in invalid_ms_key[:10]:
        print("  ", item)

    print(f"Missing or empty markscheme images: {len(missing_ms)}")
    for item in missing_ms[:10]:
        print("  ", item)

    print(f"Missing or empty figure images: {len(missing_figures)}")
    for item in missing_figures[:10]:
        print("  ", item)

    print(f"Paper totalMarks mismatches: {len(marks_mismatch)}")
    for item in marks_mismatch[:10]:
        print("  ", item)

    ok = not (missing_images or invalid_ms_key or missing_ms or missing_figures or marks_mismatch)
    if ok:
        print("\nALL INTEGRITY CHECKS PASSED PERFECTLY!")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if verify() else 1)
