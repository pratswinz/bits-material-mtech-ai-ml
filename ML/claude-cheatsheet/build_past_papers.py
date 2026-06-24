#!/usr/bin/env python3
"""Rebuild ML_Past_Papers.html from Sem 1 PDFs with formulas + diagram assets."""
import fitz
import html as H
import re
from pathlib import Path

from svg_inline import SVG_WRAP_CSS, reset_uid, svg_div, svg_figure
from solution_format import SOL_CSS, format_solution, prepare_solution_raw
from table_format import (
    TABLE_CSS,
    format_content,
    format_stem,
    enrich_jan2026_q6_solution,
    enrich_mar2026_endsem_q6_solution,
    enrich_knn_gower_solution,
    enrich_gbm_solution,
    enrich_lwlr_solution,
)
from math_format import format_math_in_html

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ML_Past_Papers.html"
BASE = Path("/Volumes/disc 2/bits pilani/Sem 1/ML/Question papers")

PAPERS = [
    ("2023 MidSem Regular ML.pdf", "Mid Sem", "Regular", "2023", "2023 Mid-Sem EC-2 Regular"),
    ("2023 MidSem Regular ML 2.pdf", "Mid Sem", "Regular", "2023", "2023 Mid-Sem EC-2 Regular (Set 2)"),
    ("2024 MidSem Regular ML.pdf", "Mid Sem", "Regular", "2024", "2024 Mid-Sem EC-2 Regular"),
    ("2024 MidSem Makeup ML.pdf", "Mid Sem", "Makeup", "2024", "2024 Mid-Sem EC-2 Makeup"),
    ("Dec 2025 ML Midsem Regular QP & answer key.pdf", "Mid Sem", "Regular", "2025", "Dec 2025 Mid-Sem Regular"),
    ("Jan 2026 ML Midsem Makeup QP & answer key.pdf", "Mid Sem", "Makeup", "2026", "Jan 2026 Mid-Sem Makeup"),
    ("Mar 2026 ML endsem regular QP & answer key.pdf", "End Sem", "Regular", "2026", "Mar 2026 End-Sem EC-3 Regular"),
    ("Mar 2026 ML endsem makeup QP & answer key.pdf", "End Sem", "Makeup", "2026", "Mar 2026 End-Sem EC-3 Makeup"),
]

# (keyword list, formula html, diagram filename or None)
# Order matters for generic keys; enrich() checks PRIORITY first.
PRIORITY_ENRICHMENTS = [
    (["k-means algorithm", "centroid-based clustering", "gaussian mixture model", "gmm with two"],
     r"<h5>K-Means &amp; GMM</h5>Assign to nearest centroid → update mean · GMM: soft responsibilities \(\gamma_{ik}\) · hard vs soft assignment",
     None),
    (["dataset a", "dataset b", "noisy / irrelevant", "outliers introduced", "model l1:", "model t:"],
     r"<h5>Bias–Variance</h5>Train≈Test high→bias · Train low, Test high→variance · \(R^2=1-SS_{res}/SS_{tot}\)",
     "bias-variance.svg"),
    (["log-odds", "guarantees", "cgpa", "logistic regression parameters", "θ₂"],
     r"<h5>Logistic</h5>\(\sigma(z)=1/(1+e^{-z})\) · BCE: \(-[y\log\hat p+(1-y)\log(1-\hat p)]\)",
     "logistic-sigmoid.svg"),
]

ENRICHMENTS = [
    (["entropy", "information gain", "decision tree", "id3", "ig("],
     r"<h5>Entropy &amp; IG</h5>\(H(S)=-\sum p_k\log_2 p_k\) · \(IG=H(S)-\sum_v\frac{|S_v|}{|S|}H(S_v)\)",
     "entropy-ig-tree.svg"),
    (["confusion matrix", "precision", "recall", "f1", "f-measure", "tp=", "false negative"],
     r"<h5>Metrics</h5>Acc=\(\frac{TP+TN}{N}\) · Prec=\(\frac{TP}{TP+FP}\) · Rec=\(\frac{TP}{TP+FN}\) · F1=\(\frac{2PR}{P+R}\)",
     "confusion-matrix.svg"),
    (["gradient descent", "∂j/∂", "ridge", "lasso", "regularization", "θ₀", "theta"],
     r"<h5>GD + Regularization</h5>\(\theta_j\leftarrow\theta_j-\alpha\frac{\partial J}{\partial\theta_j}\) · Ridge adds \((\lambda/m)\theta_j\)",
     "gd-flow.svg"),
    (["logistic", "sigmoid", "cross-entropy", "log loss", "playoff"],
     r"<h5>Logistic</h5>\(\sigma(z)=1/(1+e^{-z})\) · BCE: \(-[y\log\hat p+(1-y)\log(1-\hat p)]\)",
     "logistic-sigmoid.svg"),
    (["min-max", "z-score", "normaliz", "feature scaling", "scaling"],
     r"<h5>Scaling</h5>\(x'=\frac{x-x_{min}}{x_{max}-x_{min}}\) · \(x'=\frac{x-\mu}{\sigma}\)",
     "min-max-scaling.svg"),
    (["high bias", "high variance", "overfit", "underfit", "bias–variance", "train≈test", "rmse", "r²", "r2"],
     r"<h5>Bias–Variance</h5>Train≈Test high→bias · Train low, Test high→variance · \(R^2=1-SS_{res}/SS_{tot}\)",
     "bias-variance.svg"),
    (["tom mitchell", "experience e", "task t", "performance measure"],
     r"<h5>Mitchell</h5>Learn from <strong>E</strong> (data) for <strong>T</strong> (task), improve <strong>P</strong> (metric)",
     "mitchell-etp.svg"),
    (["lasso", "ridge", "l1", "l2", "λ"],
     r"<h5>Ridge vs Lasso</h5>L2 shrinks · L1 can zero weights",
     "ridge-lasso.svg"),
]

SKIP = re.compile(
    r'^(Birla Institute|Work Integrated|Work-Integrated|Second Semester|First / Second|Mid-Semester|Comprehensive|Course No|Course Title|Nature of Exam|Weightage|Duration|Date of Exam|Note to Students|Please follow|All parts|Assumptions|Please Note|No\. of Pages|No\. of Questions|\*{3,})',
    re.I,
)

JUNE2026_BLOCKS = [
    ("Q1", "Electricity bill regression [5M]",
     "../questions/june mid sem regular 2026/WhatsApp Image 2026-06-21 at 11.43.21.jpeg",
     r"""<div class="formula"><h5>Model</h5>\(\hat y = 120 + 7.5x_1 + 45x_2 - 4x_3 + 18x_4\)</div>
{gd}
<p>(a) Interpret coefs · (b) kWh→Wh: \(w_1' = 7.5/1000 = 0.0075\) · (c) \(\partial J/\partial\theta_3=-12 \Rightarrow \theta_3\leftarrow\theta_3+12\alpha\)</p>""".format(gd=svg_figure("gd-flow.svg", "GD"))),
    ("Q2", "Decision tree — entropy [2M+]",
     "../questions/june mid sem regular 2026/WhatsApp Image 2026-06-21 at 11.43.22.jpeg",
     r"""<div class="formula"><h5>Entropy</h5>\(H=-0.6\log_2 0.6-0.4\log_2 0.4\approx 0.971\)</div>
{ig}
<p>Split Existing Loan=No → IG ≈ 0.610</p>""".format(ig=svg_figure("entropy-ig-tree.svg", "IG"))),
    ("Q3", "Logistic + min-max [4M+]",
     "../questions/june mid sem regular 2026/WhatsApp Image 2026-06-21 at 11.43.23.jpeg",
     r"""<div class="formula"><h5>Min-max</h5>\(x'=(x-590)/120\) → S1=0.25, S2=0.75, S3=0, S4=1.0 · 650→0.50</div>
<figure class="diagram">{scale}{sig}</figure>""".format(
         scale=svg_div("min-max-scaling.svg", "scale"),
         sig=svg_div("logistic-sigmoid.svg", "sigmoid", "margin-top:.5rem"),
     )),
    ("Q4", "Fraud confusion matrix [2.5M]",
     "../questions/june mid sem regular 2026/WhatsApp Image 2026-06-21 at 11.43.24.jpeg",
     r"""{cm}
<div class="formula"><h5>Model A</h5>Acc=98.55% · Prec=33.3% · Rec=45% · F1=38.3%</div>""".format(cm=svg_figure("confusion-matrix.svg", "CM"))),
    ("Q5", "Bias-variance spam [1M+]",
     "../questions/june mid sem regular 2026/WhatsApp Image 2026-06-21 at 11.43.21 (1).jpeg",
     r"""{bv}
<p>A: 61%/60% high bias · B: 99%/67% high variance</p>""".format(bv=svg_figure("bias-variance.svg", "BV"))),
]


def esc(s):
    if not s:
        return ""
    return format_stem(H.escape(s).replace("\n", "<br>"))


def esc_sol(s):
    if not s:
        return ""
    s = prepare_solution_raw(s)
    html = format_content(H.escape(s).replace("\n", "<br>"))
    html = enrich_jan2026_q6_solution(html)
    html = enrich_mar2026_endsem_q6_solution(html)
    html = enrich_knn_gower_solution(html)
    html = format_solution(html)
    html = enrich_gbm_solution(html)
    html = enrich_lwlr_solution(html)
    return format_math_in_html(html)


def badge(exam, session, year):
    ec = "mid" if exam == "Mid Sem" else "end"
    sc = "reg" if session == "Regular" else "makeup"
    return (f'<span class="b {ec}">{H.escape(exam)}</span>'
            f'<span class="b {sc}">{H.escape(session)}</span>'
            f'<span class="b yr">{year}</span>')


def enrich(qtext, sol):
    blob = (qtext + " " + sol).lower()
    extra = ""
    for keys, formula, diagram in PRIORITY_ENRICHMENTS + ENRICHMENTS:
        if any(k in blob for k in keys):
            extra += f'<div class="formula">{formula}</div>'
            if diagram:
                extra += svg_figure(diagram, "diagram")
            break
    return extra


def clean(text):
    return "\n".join(l for l in (x.strip() for x in text.split("\n")) if l and not SKIP.match(l))


def split_questions(text):
    text = clean(text)
    # Main questions only (Q1. [5M] ...), not sub-parts like Q1. a)
    parts = re.split(r"\n(?=Q\.?\s*\d+[\.\)]\s*(?:\[|[A-Za-z(]))", text)
    blocks = []
    markers = [
        "Solution:", "Solution", "Answers:", "Answer Keys", "Evaluation:",
        "Ans –", "Ans -", "Rubric",
    ]
    answer_re = re.compile(r"\n(?:Answer|Ans)\s*:", re.I)
    for p in parts:
        p = p.strip()
        if len(p) < 25:
            continue
        m = re.match(r"(Q\.?\s*\d+[\.\)]?)", p, re.I)
        if not m:
            continue
        qid = re.sub(r"\s+", " ", m.group(1).strip())
        body = p[m.end() :].strip()
        qtext, sol, best = body, "", len(body)
        for sm in markers:
            i = body.find(sm)
            if 30 < i < best:
                best = i
        am = answer_re.search(body)
        if am and 30 < am.start() < best:
            best = am.start()
        if best < len(body):
            qtext, sol = body[:best].strip(), body[best:].strip()
        if len(qtext) < 20 or re.match(r"^\[[^\]]+\]\s*Solution:?\s*$", qtext.strip(), re.I):
            marks_m = re.search(r"\[[^\]]+\]", body)
            marks = marks_m.group(0) if marks_m else ""
            qtext = (
                f"<em>Question text missing from PDF extract (may be image-only). "
                f"{marks} — refer to the official PDF.</em>"
            )
            if len(sol) <= 30:
                sol = ""
        blocks.append((qid, qtext, sol))
    return blocks


def june_section():
    sec = '<section id="june2026"><h2>June 2026 EC-2 Regular</h2><p class="src">ML/questions/june mid sem regular 2026/</p>'
    for qid, title, img, body in JUNE2026_BLOCKS:
        sec += f'''<div class="q"><div class="badges">{badge("Mid Sem","Regular","2026")}</div>
        <h4>{H.escape(qid)} — {H.escape(title)}</h4>
        <img class="exam-img" src="{img}" alt="{H.escape(qid)}">
        <div class="sol"><strong>Solution:</strong>{body}</div></div>'''
    sec += "</section>"
    return sec


def validate_html(html: str) -> list:
    """Return list of structural HTML issues that break layout."""
    issues = []
    if html.count("<aside") != html.count("</aside>"):
        issues.append("aside tag mismatch")
    if html.count("<main") != html.count("</main>"):
        issues.append("main tag mismatch")
    if re.search(r"</(?:ul|table|div|section|p|li)(?![\s>/])", html):
        issues.append("malformed closing tags (missing >)")
    if re.search(r"</ul[^>]", html) and not re.search(r"</ul>", html):
        pass
    for m in re.finditer(r"</(?:ul|table|tbody|thead|section)(?![\s>/])", html):
        issues.append(f"broken tag near: ...{html[max(0,m.start()-30):m.end()+20]!r}...")
    return issues


def build():
    reset_uid()
    sections = [june_section()]
    nav = ['<a href="#june2026">June 2026 Mid Regular</a>']
    for fname, exam, session, year, label in PAPERS:
        path = BASE / fname
        text = "\n".join(p.get_text() for p in fitz.open(path))
        sid = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
        short = f"{year} {exam.split()[0]} {session}"
        if "Set 2" in label:
            short += " (Set 2)"
        nav.append(f'<a href="#{sid}">{short}</a>')
        sec = f'<section id="{sid}"><h2>{H.escape(label)}</h2><p class="src">Sem 1/ML/Question papers · {H.escape(fname)}</p>'
        for qid, qtext, sol in split_questions(text):
            extra = enrich(qtext, sol)
            sol_html = esc_sol(sol) if sol else "<em>See official answer key in PDF.</em>"
            sec += f'''<div class="q"><div class="badges">{badge(exam,session,year)}</div>
            <h4>{H.escape(qid)}</h4>
            <div class="stem"><strong>Question:</strong><br>{esc(qtext)}</div>
            {extra}
            <div class="sol"><strong>Solution</strong>{sol_html}</div></div>'''
        sec += "</section>"
        sections.append(sec)

    css_extra = f"""
.formula{{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:1rem 1.15rem;margin:.85rem 0;font-size:1rem;overflow-x:auto;text-align:center;box-shadow:0 1px 2px rgba(0,0,0,.04)}}
.formula h5{{margin:0 0 .55rem;font-size:.72rem;text-transform:uppercase;color:#64748b;letter-spacing:.05em;text-align:left}}
.formula mjx-container{{margin:.35rem 0!important}}
.diagram{{margin:1rem 0;text-align:center}}
.diagram img{{max-width:100%;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff}}
{TABLE_CSS}
{SVG_WRAP_CSS}
{SOL_CSS}
"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ML Past Papers 2023–2026 — Full Solutions</title>
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']], processEscapes: true }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }}
}};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js" async></script>
<style>
:root{{--navy:#1e3a5f;--blue:#2563eb;--green:#059669;--red:#dc2626;--purple:#7c3aed;--amber:#d97706;--bg:#f8fafc;--card:#fff;--border:#e2e8f0;--text:#1e293b;--muted:#64748b}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Georgia,"Segoe UI",serif;background:var(--bg);color:var(--text);line-height:1.65}}
header{{background:var(--navy);color:#fff;padding:1.5rem;text-align:center}}
header a{{color:#93c5fd}}
.shell{{display:flex;max-width:1280px;margin:0 auto;width:100%}}
aside{{width:260px;flex-shrink:0;background:var(--card);border-right:1px solid var(--border);padding:.8rem;position:sticky;top:0;height:100vh;overflow-y:auto;font-size:.75rem}}
aside a{{display:block;padding:.3rem .5rem;color:var(--navy);text-decoration:none;border-radius:4px}}
aside a:hover{{background:#eff6ff}}
aside .grp{{font-weight:700;color:var(--amber);font-size:.65rem;text-transform:uppercase;margin:.8rem 0 .2rem}}
main{{flex:1;min-width:0;max-width:920px;padding:1.5rem 2rem}}
section{{margin-bottom:2.5rem;padding-bottom:1.5rem;border-bottom:2px solid var(--border)}}
h2{{color:var(--navy);font-size:1.2rem;margin-bottom:.75rem}}
.q h4{{color:var(--navy);font-size:1rem;margin:.25rem 0 .5rem}}
.q{{background:var(--card);border:1px solid var(--border);border-left:3px solid #a78bfa;border-radius:10px;padding:1.25rem 1.35rem;margin:1.35rem 0;box-shadow:0 1px 3px rgba(0,0,0,.05);min-width:0;width:100%;box-sizing:border-box}}
.badges{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:.65rem}}
.b{{font-size:.68rem;font-weight:700;padding:3px 9px;border-radius:99px;text-transform:uppercase;letter-spacing:.03em}}
.b.mid{{background:#dbeafe;color:#1d4ed8}} .b.end{{background:#fce7f3;color:#be185d}}
.b.reg{{background:#d1fae5;color:#047857}} .b.makeup{{background:#fef3c7;color:#b45309}}
.b.yr{{background:#f3e8ff;color:#7c3aed}}
.stem{{font-size:.92rem;margin:.75rem 0 1rem;padding:.9rem 1.1rem;background:#f8fafc;border:1px solid var(--border);border-radius:8px;line-height:1.7;min-width:0;width:100%;box-sizing:border-box;overflow-wrap:break-word;word-wrap:break-word;word-break:normal;hyphens:auto}}
.sol{{font-size:.92rem;margin-top:1rem;padding:1.1rem 1.25rem;background:#fff;border:1px solid #e2e8f0;border-left:3px solid #059669;border-radius:8px;line-height:1.65;min-width:0;width:100%;box-sizing:border-box;overflow-wrap:break-word;word-wrap:break-word}}
.sol > strong{{display:block;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;color:#047857;margin-bottom:.75rem;padding-bottom:.35rem;border-bottom:1px solid #ecfdf5}}
.src{{font-size:.78rem;color:var(--muted);margin-bottom:.6rem}}
.exam-img{{max-width:100%;border:1px solid var(--border);border-radius:6px;margin:.5rem 0}}
.legend{{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1rem;margin-bottom:1.5rem;font-size:.85rem}}
{css_extra}
@media(max-width:800px){{.shell{{flex-direction:column}}aside{{width:100%;height:auto;position:relative}}}}
</style>
</head>
<body>
<header>
<h1>ML Past Papers — 2023 to 2026</h1>
<p><a href="index.html">← Hub</a> · Diagrams inlined (works offline)</p>
</header>
<div class="shell">
<aside>
<div class="grp">Legend</div>
<div class="badges" style="margin:.5rem"><span class="b mid">Mid Sem</span><span class="b end">End Sem</span></div>
<div class="badges" style="margin:.5rem"><span class="b reg">Regular</span><span class="b makeup">Makeup</span></div>
<div class="grp">Papers</div>
{"".join(nav)}
</aside>
<main>
<div class="legend">
Diagrams are inlined SVG (no broken images when opened locally). MathJax renders formulas.
</div>
{"".join(sections)}
<p style="color:var(--muted);font-size:.82rem;margin-top:2rem"><a href="ML_PYQ_Workbook.html">PYQ Workbook</a> · <a href="ML_Theory_Guide.html">Theory</a></p>
</main>
</div>
</body>
</html>"""
    OUT.write_text(html, encoding="utf-8")
    issues = validate_html(html)
    if issues:
        print("WARNING: HTML validation issues:")
        for issue in issues[:10]:
            print(" -", issue)
    print("Wrote", OUT, "with", html.count('class="q"'), "questions")


if __name__ == "__main__":
    build()
