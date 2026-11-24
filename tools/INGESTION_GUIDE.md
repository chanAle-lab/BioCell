# Past Paper Ingestion Guide (`coolBio`)

Follow this pipeline whenever ingesting official AQA Biology (`7401` / `7402`) Question Paper (QP), Mark Scheme (MS), and Insert/Resource PDFs into `questions.json` and `img/<paper-id>/`.

## 1. Core Principles
- **Never generate synthetic/AI-written markschemes.** Always crop the official Mark Scheme PDF per question into `.png` files under `img/<paper-id>/ms/`.
- **Keep raw PDFs out of the repo** (only commit cropped images + `questions.json` + ingestion scripts) so the static site loads fast on GitHub Pages.
- **One ingestion script per paper** (`tools/ingest_<year>_<series>_<unit>.py`) plus `tools/recrop_all_questions.py`, `tools/crop_official_markscheme.py`, `tools/verify_all_db.py`, and `tools/add_cache_busting.py`.

## 2. Target `questions.json` Schema
- `papers[]`: `id` (`<year>-<series>-<unit>`), `year`, `series`, `unit`, `level`, `date` (`YYYY-MM-DD`), `title`, `totalMarks`, `pdf`: `null`, `ms`: `null`.
- `questions[]`: `id` (`<paper-id>-q<qnum>`), `paper`, `year`, `series`, `unit`, `level`, `question`, `questionNumber`, `page` (1-indexed QP page where the question number marker appears), `marks` (must sum to `paper.totalMarks`), `specRef`, `topics` (`[specRef]`), `summary`, `image` (`img/<paper-id>/q<slug>.jpg`), `markscheme` (`img/<paper-id>/ms/<cropped-file>.png`), `figures` (`["img/<paper-id>/fig-*.jpg"]`), and optional `crop_exclude_y`.

## 3. Step-by-Step Workflow
1. **Audit QP & MS PDFs:** Verify page 1 metadata, record every `qnum`, `page`, `marks`, `specRef`, confirm sum equals `totalMarks`, and note any QP vs MS numbering mismatches in `MS_QNUM_MAP`.
2. **Extract Shared Figures (`FIGURES`):** Render shared graphs/tables/diagrams at `2.5x` scale (`fitz.Matrix(2.5, 2.5)`) with generous `y0`/`y1` padding and link them in `figures`.
3. **Crop Official Mark Schemes:** Use `crop_official_markschemes(...)` from `tools/crop_official_markscheme.py` (handles front-matter skipping, multi-page stitching, canonical key matching, and Section B MCQs).
4. **Crop Questions:** Register `<paper-id>: <qp_pdf_path>` in `PDF_MAP` in `tools/recrop_all_questions.py` and run it.
5. **Verify & Cache-Bust:** Run `py tools/verify_all_db.py`, visually spot-check `q*.jpg`, `fig-*.jpg`, and `ms/q*.png`, then run `py tools/add_cache_busting.py` to bump `?v=...` in `index.html`.
