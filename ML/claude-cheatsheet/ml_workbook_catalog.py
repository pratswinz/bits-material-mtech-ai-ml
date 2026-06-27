"""Map ML workbook TYPE numbers to past-paper questions from ML/questions/."""
from __future__ import annotations

import re
from collections import defaultdict

from ml_pyq_catalog import collect_all_questions
from ml_topics import TOPICS

# slug lists per workbook TYPE (mid-sem focus)
TYPE_SLUGS: dict[int, list[str]] = {
    1: ["lp", "rl", "uns"],
    2: ["pre"],
    3: ["gd"],
    4: ["met", "acc", "prec", "rec", "f1"],
    5: ["of", "uf", "bv"],
    6: ["reg"],
    7: ["dt", "ent", "ig"],
    8: ["lr", "ce"],
    9: ["scale"],
    10: ["rob"],
    11: ["ne"],
}

# Prefer this slug for brief label when a question matches multiple TYPE slugs
TYPE_BRIEF_SLUG: dict[int, str] = {
    1: "lp",
    2: "pre",
    3: "gd",
    4: "met",
    5: "bv",
    6: "reg",
    7: "dt",
    8: "lr",
    9: "scale",
    10: "rob",
    11: "ne",
}

SCALING_RE = re.compile(r"min-max|z-score|normaliz|feature scaling|scaling", re.I)
NORMAL_EQ_RE = re.compile(r"normal equation|closed form|x\^tx|\(x\^tx\)|dimensions of", re.I)
ROBUST_RE = re.compile(r"robust|random forest|noise.*dataset|outlier.*model|affected by", re.I)


def types_for_row(slugs: list[str], qtext: str = "") -> set[int]:
    found: set[int] = set()
    blob = (qtext or "").lower()
    for type_num, type_slugs in TYPE_SLUGS.items():
        if any(s in slugs for s in type_slugs):
            found.add(type_num)
    if SCALING_RE.search(blob):
        found.add(9)
    if NORMAL_EQ_RE.search(blob):
        found.add(11)
    if ROBUST_RE.search(blob):
        found.add(10)
    return found


def _brief_for_type(row: dict, type_num: int) -> str:
    prefer = TYPE_BRIEF_SLUG.get(type_num)
    slugs = row["slugs"]
    if prefer and prefer in slugs:
        return TOPICS[prefer][0]
    for slug in TYPE_SLUGS.get(type_num, []):
        if slug in slugs:
            return TOPICS[slug][0]
    return row["brief"]


def collect_by_type(mid_sem_only: bool = True) -> dict[int, list[dict]]:
    by_type: dict[int, list[dict]] = defaultdict(list)
    seen: dict[int, set[tuple[str, int]]] = defaultdict(set)

    for row in collect_all_questions():
        if mid_sem_only and not row["mid_only"]:
            continue
        qtext = row.get("qtext") or ""
        for type_num in types_for_row(row["slugs"], qtext):
            key = (row["sid"], row["qnum"])
            if key in seen[type_num]:
                continue
            seen[type_num].add(key)
            entry = dict(row)
            entry["brief"] = _brief_for_type(row, type_num)
            by_type[type_num].append(entry)

    for type_num in by_type:
        by_type[type_num].sort(
            key=lambda r: (r["year"], r["session"] != "Regular", r["qnum"]),
            reverse=True,
        )
    return dict(by_type)
