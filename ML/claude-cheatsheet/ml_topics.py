"""ML mid-sem important topics + question tagging for past papers."""
import html as H
import re

# Display groups for index.html (6 cards)
TOPIC_GROUPS = [
    ("t1", "Learning paradigms", [
        "Supervised learning",
        "Unsupervised learning",
        "Reinforcement learning",
        "Mitchell definition (E, T, P)",
    ]),
    ("t2", "Logistic regression & optimization", [
        "Logistic regression",
        "Gradient descent",
        "Cross entropy loss",
        "Sigmoid / log-odds",
    ]),
    ("t3", "Model fit & regularization", [
        "Overfitting",
        "Underfitting",
        "Regularization (Ridge / Lasso)",
        "Bias–variance tradeoff",
    ]),
    ("t4", "Data & preprocessing", [
        "Data preprocessing",
        "Data quality issues",
        "Feature scaling (min-max, z-score)",
        "Dataset splitting (train / val / test)",
        "Normal equation (matrix dimensions)",
    ]),
    ("t5", "Evaluation metrics", [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 score",
        "Confusion matrix",
    ]),
    ("t6", "Decision trees", [
        "Decision trees (ID3 / CART)",
        "Entropy",
        "Information gain",
    ]),
]

# slug -> (label, css group t1..t6)
TOPICS = {
    "lp": ("Learning paradigms", "t1"),
    "sup": ("Supervised", "t1"),
    "uns": ("Unsupervised", "t1"),
    "rl": ("Reinforcement learning", "t1"),
    "lr": ("Logistic regression", "t2"),
    "gd": ("Gradient descent", "t2"),
    "ce": ("Cross entropy loss", "t2"),
    "of": ("Overfitting", "t3"),
    "uf": ("Underfitting", "t3"),
    "reg": ("Regularization", "t3"),
    "bv": ("Bias–variance tradeoff", "t3"),
    "pre": ("Data preprocessing", "t4"),
    "split": ("Dataset splitting", "t4"),
    "scale": ("Feature scaling", "t4"),
    "ne": ("Normal equation", "t4"),
    "rob": ("Model robustness", "t4"),
    "met": ("Evaluation metrics", "t5"),
    "acc": ("Accuracy", "t5"),
    "prec": ("Precision", "t5"),
    "rec": ("Recall", "t5"),
    "f1": ("F1", "t5"),
    "dt": ("Decision trees", "t6"),
    "ent": ("Entropy", "t6"),
    "ig": ("Information gain", "t6"),
}

# (paper_slug, question_key) -> list of topic slugs
QUESTION_TAGS = {
    # June 2026 (image paper)
    ("june2026", "Q1"): ["gd"],
    ("june2026", "Q2"): ["dt", "ent", "ig"],
    ("june2026", "Q3"): ["scale", "lr", "gd"],
    ("june2026", "Q4"): ["met", "acc", "prec", "rec", "f1"],
    ("june2026", "Q5"): ["bv", "of", "uf"],
    # 2023 Regular
    ("2023-midsem-regular-ml", 1): ["lp", "sup", "rl"],
    ("2023-midsem-regular-ml", 2): ["pre"],
    ("2023-midsem-regular-ml", 3): ["lr", "gd", "ce"],
    ("2023-midsem-regular-ml", 4): ["met", "acc", "prec", "rec", "f1"],
    ("2023-midsem-regular-ml", 5): ["dt", "ent", "ig"],
    ("2023-midsem-regular-ml", 6): ["ne", "gd"],
    # 2023 Regular Set 2
    ("2023-midsem-regular-ml-2", 1): ["pre", "sup", "uns"],
    ("2023-midsem-regular-ml-2", 2): ["reg", "bv"],
    ("2023-midsem-regular-ml-2", 3): ["lr", "gd", "ce"],
    ("2023-midsem-regular-ml-2", 4): ["met", "acc", "prec", "rec", "f1"],
    ("2023-midsem-regular-ml-2", 5): ["dt", "ent", "ig"],
    # 2024 Regular
    ("2024-midsem-regular-ml", 1): ["of", "reg"],
    ("2024-midsem-regular-ml", 2): ["pre", "split"],
    ("2024-midsem-regular-ml", 3): ["reg", "gd", "lr"],
    ("2024-midsem-regular-ml", 4): ["lr", "ce"],
    # 2024 Makeup
    ("2024-midsem-makeup-ml", 1): ["lp"],
    ("2024-midsem-makeup-ml", 2): ["pre"],
    ("2024-midsem-makeup-ml", 3): ["gd", "reg"],
    ("2024-midsem-makeup-ml", 4): ["met", "bv", "prec", "rec"],
    ("2024-midsem-makeup-ml", 5): ["lr"],
    ("2024-midsem-makeup-ml", 6): ["dt", "ent", "ig"],
    # Dec 2025
    ("dec-2025-ml-midsem-regular-qp-answer-key", 1): ["lr", "sup"],
    ("dec-2025-ml-midsem-regular-qp-answer-key", 2): ["bv", "of", "uf"],
    ("dec-2025-ml-midsem-regular-qp-answer-key", 3): ["dt", "ent", "ig"],
    ("dec-2025-ml-midsem-regular-qp-answer-key", 4): ["met", "acc", "prec", "rec", "f1"],
    ("dec-2025-ml-midsem-regular-qp-answer-key", 5): ["gd", "reg"],
    # Jan 2026 Makeup
    ("jan-2026-ml-midsem-makeup-qp-answer-key", 1): ["of", "uf", "bv"],
    ("jan-2026-ml-midsem-makeup-qp-answer-key", 2): ["lr", "split"],
    ("jan-2026-ml-midsem-makeup-qp-answer-key", 3): ["lr", "gd", "ce"],
    ("jan-2026-ml-midsem-makeup-qp-answer-key", 4): ["met", "acc", "prec", "rec", "f1"],
    ("jan-2026-ml-midsem-makeup-qp-answer-key", 5): ["lr"],
    ("jan-2026-ml-midsem-makeup-qp-answer-key", 6): ["pre", "dt"],
    # Mar 2026 End Regular
    ("mar-2026-ml-endsem-regular-qp-answer-key", 1): ["reg", "gd"],
    ("mar-2026-ml-endsem-regular-qp-answer-key", 2): ["lr", "sup"],
    ("mar-2026-ml-endsem-regular-qp-answer-key", 4): ["lr", "ce"],
    ("mar-2026-ml-endsem-regular-qp-answer-key", 6): ["uns"],
    ("mar-2026-ml-endsem-regular-qp-answer-key", 7): ["bv", "reg"],
    # Mar 2026 End Makeup
    ("mar-2026-ml-endsem-makeup-qp-answer-key", 1): ["reg"],
    ("mar-2026-ml-endsem-makeup-qp-answer-key", 4): ["lr", "sup"],
    ("mar-2026-ml-endsem-makeup-qp-answer-key", 6): ["gd", "lr"],
    ("mar-2026-ml-endsem-makeup-qp-answer-key", 7): ["sup"],
    ("mar-2026-ml-endsem-makeup-qp-answer-key", 8): ["dt", "of"],
}

TOPIC_BADGE_CSS = """
.b.topic{font-size:.62rem;letter-spacing:.02em;font-weight:700;padding:3px 8px;border-radius:99px;text-transform:none}
.b.t1{background:#ecfdf5;color:#059669}.b.t2{background:#eff6ff;color:#2563eb}
.b.t3{background:#fffbeb;color:#d97706}.b.t4{background:#f5f3ff;color:#7c3aed}
.b.t5{background:#fdf2f8;color:#db2777}.b.t6{background:#ecfeff;color:#0891b2}
"""


def _qnum(qkey):
    if isinstance(qkey, int):
        return qkey
    m = re.search(r"\d+", str(qkey))
    return int(m.group()) if m else qkey


def classify_question(sid: str, qkey, qtext: str = "") -> list:
    """Heuristic fallback when no manual tag exists."""
    key = (sid, _qnum(qkey))
    if key in QUESTION_TAGS:
        return QUESTION_TAGS[key]
    key2 = (sid, qkey)
    if key2 in QUESTION_TAGS:
        return QUESTION_TAGS[key2]

    t = (qtext or "").lower()
    tags = []

    def add(*slugs):
        for s in slugs:
            if s not in tags:
                tags.append(s)

    if re.search(r"tom mitchell|experience e|task t|performance measure", t):
        add("lp")
    if re.search(r"supervised|classification|regression model|labeled", t):
        add("sup")
    if re.search(r"unsupervised|cluster|k-means|gmm", t):
        add("uns")
    if re.search(r"reinforcement|reward|agent|policy", t):
        add("rl")
    if re.search(r"logistic|sigmoid|log-odds|log loss", t):
        add("lr")
    if re.search(r"cross.?entropy|log loss|bce", t):
        add("ce")
    if re.search(r"gradient descent|∂j/∂|partial derivative|learning rate", t):
        add("gd")
    if re.search(r"overfit|high variance|validation.*train.*gap", t):
        add("of")
    if re.search(r"underfit|high bias|train.*validation.*both high", t):
        add("uf")
    if re.search(r"ridge|lasso|regulariz|lambda|l1|l2", t):
        add("reg")
    if re.search(r"bias.?variance|train rmse|validation rmse", t):
        add("bv")
    if re.search(r"preprocess|data quality|missing value|feature scaling|min-max|z-score|normaliz", t):
        add("pre")
    if re.search(r"train.*test|validation set|split|80.*20|hold.?out", t):
        add("split")
    if re.search(r"confusion matrix|precision|recall|f1|f-measure|false positive", t):
        add("met")
    if "accuracy" in t:
        add("acc")
    if "precision" in t:
        add("prec")
    if "recall" in t:
        add("rec")
    if re.search(r"\bf1\b|f-measure|f1 score", t):
        add("f1")
    if re.search(r"decision tree|id3|cart|split.*attribute", t):
        add("dt")
    if "entropy" in t or re.search(r"h\(s\)|-\s*sum.*log", t):
        add("ent")
    if re.search(r"information gain|\big\b", t):
        add("ig")

    return tags


def render_question_tags(sid: str, qkey, qtext: str = "") -> str:
    slugs = QUESTION_TAGS.get((sid, qkey)) or QUESTION_TAGS.get((sid, _qnum(qkey)))
    if not slugs:
        slugs = classify_question(sid, qkey, qtext)
    parts = []
    seen = set()
    for slug in slugs:
        if slug in seen or slug not in TOPICS:
            continue
        seen.add(slug)
        label, grp = TOPICS[slug]
        parts.append(
            f'<span class="b topic {grp}" title="{H.escape(label)}">{H.escape(label)}</span>'
        )
    return "".join(parts)
