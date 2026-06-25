#!/usr/bin/env python3
"""Build ISM_Revision_Sheet.html from Cheat_Sheet/Cheat_Sheet_ISM.pdf."""
import fitz
import html as H
import re
from pathlib import Path

from math_format import format_math_in_html

ROOT = Path(__file__).resolve().parent
SRC = Path("/Volumes/disc 2/bits pilani/ISM/Cheat_Sheet/Cheat_Sheet_ISM.pdf")
OUT = ROOT / "ISM_Revision_Sheet.html"

SECTIONS = [
    ("descriptive", "1. Descriptive Statistics", [
        ("Mean", r"\bar{x} = \frac{1}{n}\sum x_i"),
        ("Median", "Middle value (sorted); average of two middles if n even"),
        ("Mode", "Most frequent value"),
        (r"Variance.*?Sample", r"s^2 = \frac{\sum(x_i-\bar{x})^2}{n-1} \quad \text{(sample — divide by } n-1\text{)}"),
        ("Std Dev", r"\sigma \text{ or } s = \sqrt{\text{variance}}"),
        ("Coef. of Variation", r"CV = \frac{s}{\bar{x}} \times 100\%"),
    ]),
    ("probability", "2. Probability Theory", [
        ("Axioms", r"0 \le P(A) \le 1,\; P(S)=1"),
        ("Addition Rule", r"P(A \cup B) = P(A)+P(B)-P(A \cap B)"),
        ("Mutually Exclusive", r"P(A \cap B)=0"),
        ("Independence", r"P(A \cap B)=P(A)P(B)"),
        ("Conditional", r"P(A|B)=\frac{P(A \cap B)}{P(B)}"),
        ("Total Probability", r"P(B)=\sum P(B|A_i)P(A_i)"),
        ("Bayes", r"P(A_k|B)=\frac{P(B|A_k)P(A_k)}{\sum_i P(B|A_i)P(A_i)}"),
        ("Naïve Bayes", r"P(Y|X_1,\ldots,X_n) \propto P(Y)\prod_i P(X_i|Y)"),
    ]),
    ("rv", "3. Random Variables", [
        ("E[X] discrete", r"E[X]=\sum x\,p(x)"),
        ("Variance", r"\mathrm{Var}(X)=E[X^2]-(E[X])^2"),
        ("E[aX+b]", r"aE[X]+b"),
        ("Var(aX+b)", r"a^2\mathrm{Var}(X)"),
        ("Covariance", r"\mathrm{Cov}(X,Y)=E[XY]-E[X]E[Y]"),
        ("Independence check", r"p(x,y)=p_X(x)p_Y(y) \;\forall x,y"),
    ]),
    ("discrete", "4. Discrete Distributions", [
        ("Bernoulli", r"P(X=x)=p^x(1-p)^{1-x},\; x\in\{0,1\};\; E=p,\; \mathrm{Var}=p(1-p)"),
        ("Binomial", r"P(X=k)=\binom{n}{k}p^k(1-p)^{n-k};\; E=np,\; \mathrm{Var}=np(1-p)"),
        ("Poisson", r"P(X=k)=\frac{e^{-\lambda}\lambda^k}{k!};\; E=\lambda,\; \mathrm{Var}=\lambda"),
        ("Poisson approx", "Use when n large, p small, np = λ"),
    ]),
    ("continuous", "5. Continuous Distributions", [
        ("Normal", r"X \sim N(\mu,\sigma^2),\; Z=\frac{X-\mu}{\sigma}"),
        ("Z-table", r"P(Z>a)=1-P(Z<a)"),
        ("t-distribution", "Fatter tails; n < 30, σ unknown"),
        ("Chi-square", "Sum of squared Z — variance tests"),
        ("F-distribution", "Ratio of χ² — ANOVA"),
    ]),
    ("strategy", "6. Smart Student Strategy", [
        ("Keywords → Binomial", '"out of n", success/failure → Binomial(n,p)'),
        ("Keywords → Poisson", '"rate per hour" → Poisson(λ)'),
        ("Keywords → Normal", '"normally distributed" → Z-score'),
        ("Bayes hack", "Tree diagram → total prob denominator → pick branch"),
        ("At least one", r"P(X \ge 1)=1-P(X=0)"),
        ("Sample variance", "Always n−1 in denominator for sample data"),
    ]),
]

SECTION_FIGURES = {
    "descriptive": (
        "Skewness — mean, median, mode",
        "Left skew, symmetric, and right skew with mean/median/mode order.",
    ),
    "continuous": (
        "Normal distribution — bell curve & empirical rule",
        "68% within ±1σ, 95% within ±2σ, 99.7% within ±3σ.",
    ),
}


def build():
    from svg_inline import asset_figure

    cards = ""
    for sid, title, items in SECTIONS:
        fig = ""
        if sid in SECTION_FIGURES:
            alt, cap = SECTION_FIGURES[sid]
            fig = asset_figure(alt, cap, png="bell-curve-skewness.png")
        cards += f'<div class="part" id="{sid}"><h2>{H.escape(title)}</h2>{fig}<div class="grid">'
        for label, formula in items:
            tex = formula if "\\" in formula or "{" in formula else H.escape(formula)
            wrap = f"\\({tex}\\)" if "\\" in str(tex) or "=" in str(formula) else tex
            cards += f"""<div class="card">
            <div class="label">{H.escape(str(label))}</div>
            <div class="formula">{wrap}</div>
            </div>"""
        cards += "</div></div>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ISM Revision Sheet — AIMLCZC418</title>
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']], processEscapes: true }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }}
}};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js" async></script>
<style>
:root{{--navy:#1e3a5f;--green:#059669;--bg:#f8fafc;--card:#fff;--border:#e2e8f0;--text:#1e293b;--muted:#64748b}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,"Segoe UI",sans-serif;background:var(--bg);color:var(--text);line-height:1.5;font-size:13px}}
header{{background:linear-gradient(135deg,#1e3a5f,#059669);color:#fff;padding:1rem 1.5rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}}
header h1{{font-size:1.3rem}}
header a{{color:#a7f3d0}}
.container{{max-width:1200px;margin:0 auto;padding:1rem}}
.part{{margin:1.2rem 0}}
.part h2{{font-size:.82rem;text-transform:uppercase;letter-spacing:.06em;color:var(--green);background:#ecfdf5;padding:.4rem .8rem;border-radius:6px;margin-bottom:.6rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.6rem}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:.65rem .85rem}}
.label{{font-size:.72rem;font-weight:700;color:var(--navy);margin-bottom:.25rem;text-transform:uppercase;letter-spacing:.04em}}
.formula{{font-size:.95rem;overflow-x:auto}}
.diagram{{margin:.75rem 0;text-align:center}}
.diagram-img{{width:100%;max-width:640px;height:auto;display:block;margin:0 auto;border:1px solid var(--border);border-radius:8px;background:#fff}}
.fig-cap{{font-size:.78rem;color:var(--muted);margin-top:.4rem;max-width:640px;margin-left:auto;margin-right:auto;text-align:left}}
.note{{font-size:.78rem;color:var(--muted);margin-top:1rem;padding:.8rem;background:#fffbeb;border-radius:8px;border:1px solid #fcd34d}}
@media print{{header{{background:#1e3a5f;-webkit-print-color-adjust:exact}}}}
</style>
</head>
<body>
<header>
<div><h1>ISM Exam Cheat Sheet</h1><p>From <code>ISM/Cheat_Sheet/Cheat_Sheet_ISM.pdf</code></p></div>
<a href="index.html">← Hub</a>
</header>
<div class="container">
{cards}
<p class="note">Print this page before a closed-book exam. For worked PYQs see <a href="ISM_Past_Papers.html">Past Papers</a>.</p>
</div>
</body>
</html>"""
    OUT.write_text(format_math_in_html(html), encoding="utf-8")
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
