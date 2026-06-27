"""Collect ML past-paper questions by topic for index.html PYQ links."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import fitz

from ml_topics import QUESTION_TAGS, TOPIC_GROUPS, TOPICS, classify_question

BASE = Path("/Volumes/disc 2/bits pilani/ML/questions")

PAPERS = [
    ("MidSem/2023-12_Regular_ML.pdf", "Mid Sem", "Regular", "2023", "2023 Mid-Sem EC-2 Regular", "2023-midsem-regular-ml"),
    ("MidSem/2023-12_Regular_Set2_ML.pdf", "Mid Sem", "Regular", "2023", "2023 Mid-Sem EC-2 Regular (Set 2)", "2023-midsem-regular-ml-2"),
    ("MidSem/2024-12_Regular_ML.pdf", "Mid Sem", "Regular", "2024", "2024 Mid-Sem EC-2 Regular", "2024-midsem-regular-ml"),
    ("MidSem/2024-07_Makeup_ML.pdf", "Mid Sem", "Makeup", "2024", "2024 Mid-Sem EC-2 Makeup", "2024-midsem-makeup-ml"),
    ("MidSem/2025-12_Regular_QP-AnswerKey.pdf", "Mid Sem", "Regular", "2025", "Dec 2025 Mid-Sem Regular", "dec-2025-ml-midsem-regular-qp-answer-key"),
    ("MidSem/2026-01_Makeup_QP-AnswerKey.pdf", "Mid Sem", "Makeup", "2026", "Jan 2026 Mid-Sem Makeup", "jan-2026-ml-midsem-makeup-qp-answer-key"),
    ("EndSem/2026-03_Regular_QP-AnswerKey.pdf", "End Sem", "Regular", "2026", "Mar 2026 End-Sem EC-3 Regular", "mar-2026-ml-endsem-regular-qp-answer-key"),
    ("EndSem/2026-03_Makeup_QP-AnswerKey.pdf", "End Sem", "Makeup", "2026", "Mar 2026 End-Sem EC-3 Makeup", "mar-2026-ml-endsem-makeup-qp-answer-key"),
]

JUNE2026 = ("june2026", "Mid Sem", "Regular", "2026", "June 2026 EC-2 Regular", 5)

SKIP = re.compile(
    r"^(Birla Institute|Work Integrated|Second Semester|First / Second|Mid-Semester|Comprehensive|Course No|Course Title|Nature of Exam|Weightage|Duration|Date of Exam|Note to Students|Please follow|All parts|Assumptions|Please Note|No\. of Pages|No\. of Questions|\*{3,})",
    re.I,
)


def _clean(text: str) -> str:
    return "\n".join(l for l in (x.strip() for x in text.split("\n")) if l and not SKIP.match(l))


def _split_questions(text: str) -> list[tuple[str, str]]:
    text = _clean(text)
    parts = re.split(r"\n(?=Q\.?\s*\d+[\.\)]\s*(?:\[|[A-Za-z(]))", text)
    out = []
    for p in parts:
        p = p.strip()
        if len(p) < 25:
            continue
        m = re.match(r"(Q\.?\s*\d+[\.\)]?)", p, re.I)
        if not m:
            continue
        qid = re.sub(r"\s+", " ", m.group(1).strip())
        body = p[m.end() :].strip()
        for sm in ("Solution:", "Solution", "Answers:", "Answer Keys", "Ans –", "Ans -"):
            i = body.find(sm)
            if 30 < i:
                body = body[:i].strip()
                break
        out.append((qid, body))
    return out


def _qnum(qid: str) -> int:
    m = re.search(r"\d+", qid)
    return int(m.group()) if m else 0


def _short_paper(year: str, exam: str, session: str, label: str) -> str:
    if "June 2026" in label:
        return "June 2026"
    if "Set 2" in label:
        return f"{year} Reg (Set 2)"
    ec = "Mid" if exam == "Mid Sem" else "End"
    ses = "Reg" if session == "Regular" else "Makeup"
    if label.startswith("Dec ") or label.startswith("Jan ") or label.startswith("Mar "):
        return label.split(" Mid")[0].split(" End")[0] + f" {ses}"
    return f"{year} {ec} {ses}"


def _slugs_for(sid: str, qnum: int, qid: str, qtext: str) -> list[str]:
    for key in ((sid, qnum), (sid, qid), (sid, f"Q{qnum}")):
        if key in QUESTION_TAGS:
            return QUESTION_TAGS[key]
    return classify_question(sid, qnum, qtext)


def _normalize_qid(qid: str, qnum: int) -> str:
    return f"Q{qnum}"


def collect_all_questions() -> list[dict]:
    items: list[dict] = []
    sid, exam, session, year, label, n = JUNE2026
    for i in range(1, n + 1):
        qid = f"Q{i}"
        slugs = _slugs_for(sid, i, qid, "")
        items.append(
            {
                "sid": sid,
                "qid": qid,
                "qnum": i,
                "exam": exam,
                "session": session,
                "year": year,
                "label": label,
                "short": _short_paper(year, exam, session, label),
                "slugs": slugs,
                "qtext": "",
                "brief": TOPICS[slugs[0]][0] if slugs else "General",
                "href": f"ML_Past_Papers.html#{sid}-q{i}",
                "mid_only": exam == "Mid Sem",
            }
        )

    for fname, exam, session, year, label, sid in PAPERS:
        path = BASE / fname
        if not path.exists():
            continue
        text = "\n".join(p.get_text() for p in fitz.open(path))
        for qid, qtext in _split_questions(text):
            qnum = _qnum(qid)
            slugs = _slugs_for(sid, qnum, qid, qtext)
            items.append(
                {
                    "sid": sid,
                    "qid": _normalize_qid(qid, qnum),
                    "qnum": qnum,
                    "exam": exam,
                    "session": session,
                    "year": year,
                    "label": label,
                    "short": _short_paper(year, exam, session, label),
                    "slugs": slugs,
                    "qtext": qtext,
                    "brief": TOPICS[slugs[0]][0] if slugs else "General",
                    "href": f"ML_Past_Papers.html#{sid}-q{qnum}",
                    "mid_only": exam == "Mid Sem",
                }
            )
    return items


def group_by_topic_card(mid_sem_only: bool = False) -> dict[str, list[dict]]:
    """Return {t1..t6: [question dicts]} — a question may appear in multiple groups."""
    by_group: dict[str, list[dict]] = defaultdict(list)
    seen_in_group: dict[str, set[tuple[str, int]]] = defaultdict(set)

    for row in collect_all_questions():
        if mid_sem_only and not row["mid_only"]:
            continue
        groups_for_q: set[str] = set()
        for slug in row["slugs"]:
            if slug in TOPICS:
                groups_for_q.add(TOPICS[slug][1])
        if not groups_for_q:
            continue
        for grp in groups_for_q:
            key = (row["sid"], row["qnum"])
            if key in seen_in_group[grp]:
                continue
            seen_in_group[grp].add(key)
            by_group[grp].append(row)

    for grp in by_group:
        by_group[grp].sort(
            key=lambda r: (r["year"], r["session"] != "Regular", r["qnum"]),
            reverse=True,
        )
    return dict(by_group)


def render_pyq_list(grp_id: str, mid_sem_only: bool = True) -> str:
    catalog = group_by_topic_card(mid_sem_only=mid_sem_only)
    rows = catalog.get(grp_id, [])
    if not rows:
        return '<p class="pyq-empty">No tagged PYQs yet — check <a href="ML_Past_Papers.html">Past Papers</a>.</p>'
    lis = []
    for r in rows:
        label = r["brief"]
        for slug in r["slugs"]:
            if slug in TOPICS and TOPICS[slug][1] == grp_id:
                label = TOPICS[slug][0]
                break
        q = r["qid"]
        lis.append(
            f'<li><span class="pyq-meta">{r["short"]}</span>'
            f'<a href="{r["href"]}">{q}</a>'
            f'<span class="pyq-label">— {label}</span></li>'
        )
    return f'<ul class="pyq-list">{"".join(lis)}</ul>'
