"""Curated diagrams, formulas, and PDF text cleanup for ISM theory guide."""
import re

# (session_id-section_id) -> enrichment
# (session_id-section_id) -> enrichment with workbook links
SECTION_ENRICH = {
    "session1-step1": {
        "diagram": None,
        "formulas": [
            (r"Mean", r"\bar{y} = \frac{1}{n}\sum_{i=1}^{n} y_i"),
            (r"Median", r"\text{middle value after sorting}"),
            (r"Mode", r"\text{most frequently occurring value}"),
        ],
        "workbook_types": [1, 2],
        "image": "distribution-shapes.png",
    },
    "session1-step2": {
        "formulas": [
            (r"Sample variance", r"s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(y_i - \bar{y})^2"),
            (r"Sample SD", r"s = \sqrt{s^2}"),
            (r"Range", r"\max - \min"),
        ],
        "workbook_types": [1],
    },
    "session1-step4": {
        "diagram": "box-plot.svg",
        "formulas": [
            (r"Five-number summary", r"\min,\ Q_1,\ \text{median},\ Q_3,\ \max"),
            (r"IQR", r"Q_3 - Q_1"),
            (r"Outlier fences", r"Q_1 - 1.5\cdot\text{IQR}\ \text{and}\ Q_3 + 1.5\cdot\text{IQR}"),
        ],
        "workbook_types": [1, 2],
    },
    "session2-building": {
        "diagram": "venn-ops.svg",
        "formulas": [
            (r"Union", r"A \cup B:\ \text{A or B (or both)}"),
            (r"Intersection", r"A \cap B:\ \text{A and B together}"),
            (r"Complement", r"A^c:\ \text{not A}"),
        ],
        "workbook_types": [3],
        "image": "bayes-theorem-visual.png",
    },
    "session2-addition": {
        "formulas": [
            (r"General addition", r"P(A \cup B) = P(A) + P(B) - P(A \cap B)"),
            (r"Mutually exclusive", r"P(A \cup B) = P(A) + P(B)\ \text{if } A \cap B = \emptyset"),
        ],
        "workbook_types": [3],
    },
    "session3-conditional": {
        "formulas": [
            (r"Conditional probability", r"P(A|B) = \frac{P(A \cap B)}{P(B)},\ P(B)>0"),
        ],
        "workbook_types": [4],
    },
    "session3-total": {
        "diagram": "bayes-tree.svg",
        "formulas": [
            (r"Total probability", r"P(B) = \sum_i P(B|A_i)P(A_i)"),
        ],
        "workbook_types": [4],
    },
    "session4-bayes": {
        "diagram": "bayes-tree.svg",
        "formulas": [
            (r"Bayes theorem", r"P(A|B) = \frac{P(B|A)P(A)}{P(B)}"),
        ],
        "workbook_types": [5],
        "image": "bayes-theorem-visual.png",
    },
    "session4-naive": {
        "diagram": "naive-bayes.svg",
        "formulas": [
            (r"Naive Bayes", r"P(C|w_1,\ldots,w_k) \propto P(C)\prod_j P(w_j|C)"),
            (r"Laplace smoothing", r"P(w|C) = \frac{\text{count}(w,C)+\alpha}{\text{count}(C)+V\alpha}"),
        ],
        "workbook_types": [6],
    },
    "session5-discrete": {
        "diagram": "pmf-cdf.svg",
        "formulas": [
            (r"PMF rules", r"f(x)=P(X=x),\ f(x)\ge 0,\ \sum_x f(x)=1"),
            (r"Uniform discrete", r"f(x)=\frac{1}{n}\ \text{for } n \text{ equally likely values}"),
        ],
        "workbook_types": [7],
        "image": "distribution-shapes.png",
    },
    "session5-expectation": {
        "formulas": [
            (r"Expectation", r"E[X] = \sum_x x\,f(x)"),
            (r"Variance", r"\text{Var}(X) = E[X^2] - (E[X])^2"),
        ],
        "workbook_types": [7],
    },
    "session6-binomial": {
        "formulas": [
            (r"Binomial PMF", r"P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}"),
            (r"Mean / variance", r"E[X]=np,\ \text{Var}(X)=np(1-p)"),
        ],
        "workbook_types": [8],
        "image": "binomial-vs-poisson.png",
    },
    "session6-poisson": {
        "formulas": [
            (r"Poisson PMF", r"P(X=k)=\frac{e^{-\lambda}\lambda^k}{k!}"),
            (r"Mean / variance", r"E[X]=\lambda,\ \text{Var}(X)=\lambda"),
        ],
        "workbook_types": [8],
        "image": "binomial-vs-poisson.png",
    },
    "session6-normal": {
        "diagram": "normal-curve.svg",
        "formulas": [
            (r"Normal PDF", r"f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}"),
        ],
        "workbook_types": [9],
        "image": "distribution-shapes.png",
    },
    "session6-zscore": {
        "formulas": [
            (r"Z-score", r"Z = \frac{X-\mu}{\sigma}"),
        ],
        "workbook_types": [9],
    },
    "session6-approx": {
        "formulas": [
            (r"Binomial to Normal", r"X\approx N(np,\ np(1-p))\ \text{when } n \text{ large}"),
            (r"Binomial to Poisson", r"\lambda=np\ \text{when } n \text{ large, } p \text{ small}"),
        ],
        "workbook_types": [8, 9],
    },
    "session7-clt": {
        "diagram": "clt-ci.svg",
        "formulas": [
            (r"CLT (informal)", r"\bar{X} \approx N\!\left(\mu,\ \frac{\sigma^2}{n}\right)\ \text{for large } n"),
        ],
        "workbook_types": [10],
        "image": "clt-visualization.png",
    },
    "session7-ci": {
        "diagram": "clt-ci.svg",
        "formulas": [
            (r"95% CI for mean", r"\bar{x} \pm t_{\alpha/2}\,\frac{s}{\sqrt{n}}"),
            (r"95% CI for proportion", r"\hat{p} \pm z_{\alpha/2}\sqrt{\frac{\hat{p}(1-\hat{p})}{n}}"),
        ],
        "workbook_types": [17],
        "image": "confidence-intervals-concept.png",
    },
    "session7-sample-size": {
        "formulas": [
            (r"Sample size (mean)", r"n = \left(\frac{z_{\alpha/2}\,\sigma}{E}\right)^2"),
        ],
        "workbook_types": [17],
    },
}

SESSION_DIAGRAM = {
    "session1": "box-plot.svg",
    "session2": "venn-ops.svg",
    "session3": "bayes-tree.svg",
    "session4": "naive-bayes.svg",
    "session5": "pmf-cdf.svg",
    "session6": "distributions.svg",
    "session7": "clt-ci.svg",
}

SESSION_HERO = {
    "session1": {
        "svg": "box-plot.svg",
        "png": "distribution-shapes.png",
        "caption": "Session 1 map: centre (mean/median), spread (SD/IQR), shape (skew), and the box plot for outliers. Practice: TYPE 1-2.",
    },
    "session2": {
        "svg": "venn-ops.svg",
        "png": "bayes-theorem-visual.png",
        "caption": "Events are sets: union, intersection, complement. Addition rule removes double-counting. Practice: TYPE 3.",
    },
    "session3": {
        "svg": "bayes-tree.svg",
        "caption": "P(A|B) shrinks the sample space to B. Tree diagrams chain conditional branches. Practice: TYPE 4.",
    },
    "session4": {
        "svg": "naive-bayes.svg",
        "png": "bayes-theorem-visual.png",
        "caption": "Bayes flips cause and effect: posterior = (likelihood x prior) / evidence. Naive Bayes scores each class. Practice: TYPE 5-6.",
    },
    "session5": {
        "svg": "pmf-cdf.svg",
        "png": "distribution-shapes.png",
        "caption": "PMF assigns probability to each value; CDF accumulates left-to-right. E[X] is the balance point. Practice: TYPE 7.",
    },
    "session6": {
        "svg": "distributions.svg",
        "png": "binomial-vs-poisson.png",
        "caption": "Pick the mould: Bernoulli (1 trial), Binomial (n trials), Poisson (rate per window), Normal (continuous). Practice: TYPE 8-9.",
    },
    "session7": {
        "svg": "clt-ci.svg",
        "png": "clt-visualization.png",
        "caption": "CLT: sample means become normal as n grows. CI = point estimate +/- margin of error. Practice: TYPE 10, 17.",
    },
}

DIAGRAM_CAPTIONS = {
    "box-plot.svg": "Box plot anatomy: whiskers to min/max (within fences), box = middle 50%, line = median, dots = outliers.",
    "venn-ops.svg": "Set operations on events A and B: union (either), intersection (both), complement (not A).",
    "bayes-tree.svg": "Probability tree: multiply along branches, add across disjoint paths.",
    "naive-bayes.svg": "Naive Bayes: multiply prior P(class) by word likelihoods; pick highest score.",
    "pmf-cdf.svg": "Left: PMF bars show P(X=k). Right: CDF steps show P(X<=k).",
    "normal-curve.svg": "Normal curve centred at mu; Z = (X-mu)/sigma standardises any normal.",
    "clt-ci.svg": "Sample mean x-bar estimates mu; 95% CI is x-bar +/- margin of error.",
    "distributions.svg": "Keyword guide: 'out of n' -> Binomial; 'per hour/rate' -> Poisson; measurements -> Normal.",
}

NOISE_RE = re.compile(
    r"(?:"
    r"number of cars in line.*?climbing in steps to 1|"
    r"Left: a PMF.*?Right: the cumulative|"
    r"PMF: probability of each value|"
    r"CDF: probability of x or less|"
    r"A B A .*?Mutually exclusive A.*?|"
    r"impossible 0\.5 fifty fiftycertain Probability lives on a scale|"
    r"x0\.\d{2}0\.\d{2}|"
    r"The four building blocks\. Union A.*?didn't\.\s*|"
    r"☞The intuition|"
    r"probabilitydistribution|"
    r"onlyever see|"
    r"¯xstrays"
    r")",
    re.I | re.S,
)

CHART_JUNK = re.compile(
    r"\b(?:x|y)\d*\.(?:\d{2}){2,}\b|"
    r"\b0\.\d{2}0\.\d{2}0\.\d{2}\b|"
    r"^\s*\d\s*$",
    re.M,
)


def clean_section_text(text: str) -> str:
    text = NOISE_RE.sub(" ", text)
    text = CHART_JUNK.sub("", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Fix common PDF math fragments
    text = text.replace("¯y", r"\(\bar{y}\)")
    text = text.replace("¯x", r"\(\bar{x}\)")
    text = text.replace("1 n n ∑", r"\(\frac{1}{n}\sum\)")
    text = text.replace("1 n", r"\(\frac{1}{n}\)")
    text = re.sub(r"(\d)\s+(\d)\s*=\s*(\d)", r"\1×\2=\3", text)  # 8 × 8 = 64
    text = re.sub(r": the idea the whole course stands on\s*", ": ", text)
    return text.strip()


def formula_strip_html(formulas) -> str:
    if not formulas:
        return ""
    items = "".join(
        f'<div class="f-item"><span class="f-label">{label}</span>'
        f'<span class="f-eq">\\[{eq}\\]</span></div>'
        for label, eq in formulas
    )
    return f'<div class="formula-strip">{items}</div>'


def render_session_hero(session_id: str, title: str) -> str:
    from svg_inline import asset_figure

    hero = SESSION_HERO.get(session_id, {})
    svg = hero.get("svg") or SESSION_DIAGRAM.get(session_id, "")
    png = hero.get("png", "")
    caption = hero.get("caption", f"Visual guide for {title}")
    return asset_figure(title, caption, svg=svg, png=png)


def render_enrichment(anchor: str) -> str:
    """Inject image + formula strip + diagram + workbook links for a section."""
    from svg_inline import asset_figure, svg_figure

    enrich = SECTION_ENRICH.get(anchor, {})
    out = ""

    if enrich.get("image"):
        png = enrich["image"]
        out += asset_figure(anchor, f"Concept visual for {anchor.replace('-', ' ')}", png=png)

    formulas = enrich.get("formulas")
    if formulas:
        out += formula_strip_html(formulas)

    diagram = enrich.get("diagram")
    if diagram:
        cap = DIAGRAM_CAPTIONS.get(diagram, "")
        out += svg_figure(diagram, anchor, caption=cap)

    types = enrich.get("workbook_types", [])
    if types:
        links = ", ".join(
            f'<a href="ISM_PYQ_Workbook.html#type{t}"><strong>TYPE {t}</strong></a>' for t in types
        )
        out += f'<div class="key-takeaway"><p>Practice questions: {links}</p></div>'

    return out
