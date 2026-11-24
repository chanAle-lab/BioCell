"""Crop per-question .jpg images and figure/stem crops from AQA Biology Question Paper PDFs."""

import re
from pathlib import Path
from typing import Optional

import pymupdf as fitz


# Matches AQA question markers like "0 1 . 1", "0 1", "0 2 . 3" at the left margin
_MARKER_RE = re.compile(r"^0?\s*(\d{1,2})(?:\s*\.\s*(\d{1,2}))?$")


def find_question_markers(page: fitz.Page) -> list[dict]:
    """Detect AQA question markers near the left margin (x < 95pt) on a QP page."""
    words = page.get_text("words")
    lines: dict[int, list[tuple]] = {}
    for w in words:
        x0, y0, x1, y1, txt = w[:5]
        if x0 < 105 and 40 < y0 < page.rect.height - 45:
            bucket = round(y0 / 4.0)
            lines.setdefault(bucket, []).append(w)

    markers: list[dict] = []
    for bucket in sorted(lines.keys()):
        row = sorted(lines[bucket], key=lambda w: w[0])
        joined = " ".join(w[4] for w in row).strip()
        m = _MARKER_RE.match(joined)
        if not m:
            continue
        q_main = int(m.group(1))
        q_sub = m.group(2)
        qnum = f"{q_main:02d}.{q_sub}" if q_sub is not None else f"{q_main:02d}"
        y0 = min(w[1] for w in row)
        y1 = max(w[3] for w in row)
        markers.append({"qnum": qnum, "y0": y0, "y1": y1})
    return markers


def crop_qp_questions(
    qp_pdf: Path,
    out_dir: Path,
    page_map: Optional[dict[str, int]] = None,
    dpi_scale: float = 2.5,
) -> dict[str, str]:
    """Crop each detected question from qp_pdf into out_dir/q<slug>.jpg.

    Returns a mapping {qnum: filename}.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(qp_pdf))

    all_markers: list[dict] = []
    for p_idx in range(len(doc)):
        page = doc[p_idx]
        for mk in find_question_markers(page):
            mk["page_idx"] = p_idx
            all_markers.append(mk)

    saved: dict[str, str] = {}
    for idx, mk in enumerate(all_markers):
        qnum = mk["qnum"]
        if page_map and qnum in page_map and (mk["page_idx"] + 1) != page_map[qnum]:
            continue
        page = doc[mk["page_idx"]]
        y_top = max(42.0, mk["y0"] - 8.0)

        # Bottom boundary: next marker on same page, or page footer
        y_bot = page.rect.height - 42.0
        for nxt in all_markers[idx + 1 :]:
            if nxt["page_idx"] == mk["page_idx"]:
                y_bot = min(y_bot, max(y_top + 30.0, nxt["y0"] - 8.0))
                break

        rect = fitz.Rect(32.0, y_top, page.rect.width - 32.0, y_bot)
        pix = page.get_pixmap(clip=rect, matrix=fitz.Matrix(dpi_scale, dpi_scale))
        slug = qnum.replace(".", "-")
        fname = f"q{slug}.jpg"
        pix.save(str(out_dir / fname))
        saved[qnum] = fname

    doc.close()
    return saved
