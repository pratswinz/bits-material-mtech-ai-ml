"""Scan ISM MidSem folder and group questions by workbook TYPE."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import fitz

from build_past_papers import QUESTION_TAGS, classify_question, split_questions

BASE = Path("/Volumes/disc 2/bits pilani/ISM/previous question papers")

# Canonical mid-sem PDFs (prefer answer keys / compact sets; skip duplicate QP-only)
MIDSEM_PAPERS = [
    ("MidSem/2024-07_Regular_Answers.pdf", "Regular", "2024", "Jul 2024 Mid-Sem EC-2 Regular (Answers)"),
    ("MidSem/2024-07_Makeup_Answers.pdf", "Makeup", "2024", "Jul 2024 Mid-Sem EC-2 Makeup (Answers)"),
    ("MidSem/2025-01_Regular_S2-24.pdf", "Regular", "2025", "Jan 2025 Mid-Sem EC-2 Regular"),
    ("MidSem/2025-06_Makeup_S2-24.pdf", "Makeup", "2025", "Jun 2025 Mid-Sem EC-2 Makeup"),
    ("MidSem/2025-12_Regular_QP-AnswerKey.pdf", "Regular", "2025", "Dec 2025 Mid-Sem EC-2 Regular (Key)"),
    ("MidSem/2026-01_Makeup_QP-AnswerKey.pdf", "Makeup", "2026", "Jan 2026 Mid-Sem EC-2 Makeup (Key)"),
]

JUNE2026 = [
    ("Q1", [(1, 2, "Five-number summary"), (3, 4, "Total probability")]),
    ("Q2", [(2, 3, "Inclusion–exclusion (3 sets)")]),
    ("Q3", [(6, 8, "Binomial")]),
    ("Q4", [(5, 10, "Continuous PDF / E[X]")]),
    ("Q5", [(4, 6, "Naïve Bayes — purchase table")]),
    ("Q6", [(4, 5, "Bayes — fraud flag"), (6, 9, "Normal — delivery time")]),
]

JUL2024_REGULAR = [
    ("Q1", [(1, 1, "Summary table — three inferences")]),
    ("Q2", [(2, None, "Independence validation")]),
    ("Q3", [(3, 4, "Conditional probability")]),
    ("Q4", [(4, 5, "Bayes — captain selection")]),
    ("Q5", [(5, 10, "Continuous PDF on [0,2]")]),
    ("Q6", [(5, 10, "Joint distribution (independent)")]),
    ("Q7", [(6, 8, "Binomial — normal approx")]),
    ("Q8", [(6, 9, "Sampling distribution of mean")]),
]

JUL2024_MAKEUP = [
    ("Q1", [(2, 4, "Independent events")]),
    ("Q2", [(6, 8, "Binomial from μ, σ")]),
    ("Q3", [(4, 6, "Naïve Bayes — employment")]),
    ("Q4", [(5, 7, "Discrete PMF find k")]),
    ("Q5", [(5, 10, "Joint PDF")]),
    ("Q6", [(6, 9, "Normal — employee salaries")]),
    ("Q7", [(6, 8, "Sampling vs binomial")]),
]


def _slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def _add(catalog: dict, type_id: int, paper: str, href: str, qid: str, label: str, year: str, session: str):
    key = (paper, qid, label)
    for row in catalog[type_id]:
        if (row[0], row[2], row[3]) == key:
            return
    catalog[type_id].append((paper, href, qid, label, year, session))


def collect_midsem_by_type() -> dict[int, list[tuple]]:
    """Return {type_num: [(paper_label, past_papers_href, qid, sub_label, year, session), ...]}."""
    catalog: dict[int, list] = defaultdict(list)

    for fname, session, year, label in MIDSEM_PAPERS:
        path = BASE / fname
        if not path.exists():
            continue
        sid = _slug(label)
        href = f"ISM_Past_Papers.html#{sid}"
        if sid == "jul-2024-mid-sem-ec-2-regular-answers":
            for qid, tags in JUL2024_REGULAR:
                for _topic, typ, sub in tags:
                    if typ and 1 <= typ <= 11:
                        _add(catalog, typ, label, href, qid, sub, year, session)
            continue
        if sid == "jul-2024-mid-sem-ec-2-makeup-answers":
            for qid, tags in JUL2024_MAKEUP:
                for _topic, typ, sub in tags:
                    if typ and 1 <= typ <= 11:
                        _add(catalog, typ, label, href, qid, sub, year, session)
            continue
        text = "\n".join(p.get_text() for p in fitz.open(path))
        for qnum, qid, qtext, _ in split_questions(text):
            tags = QUESTION_TAGS.get((sid, qnum)) or classify_question(sid, qnum, qtext)
            for _topic, typ, sub in tags:
                if typ and 1 <= typ <= 11:
                    _add(catalog, typ, label, href, qid, sub, year, session)

    june_href = "ISM_Past_Papers.html#june2026"
    for qid, tags in JUNE2026:
        for _topic, typ, sub in tags:
            if typ and 1 <= typ <= 11:
                _add(catalog, typ, "June 2026 Mid Regular", june_href, qid, sub, "2026", "Regular")

    for typ in catalog:
        catalog[typ].sort(key=lambda x: (x[4], x[5], x[0], x[2]))
    return dict(catalog)
