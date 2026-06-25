#!/usr/bin/env python3
"""Build ISM_Study_Plan.html — 5-day plan linking Sessions 1-7, workbook, past papers."""
import html as H
from pathlib import Path

from svg_inline import SVG_WRAP_CSS, reset_uid, svg_figure

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ISM_Study_Plan.html"

DAYS = [
    ("Day 1", "Sessions 1–2", "Descriptive stats + Probability basics", [
        ("Morning", "ISM_Theory_Guide.html#session1", "Session 1 — mean, median, IQR, box plot", "box-plot.svg"),
        ("Afternoon", "ISM_PYQ_Workbook.html#type1", "Workbook TYPE 1–2 + Dec 2025 Q1", None),
        ("Evening", "ISM_Past_Papers.html#dec-2025-mid-sem-ec-2-regular-key", "Past paper Q1 full numerical", None),
    ]),
    ("Day 2", "Sessions 3–4", "Conditional probability + Bayes", [
        ("Morning", "ISM_Theory_Guide.html#session3", "Session 3 — P(A|B), total probability, trees", "bayes-tree.svg"),
        ("Afternoon", "ISM_PYQ_Workbook.html#type4", "Workbook TYPE 4–6 (Bayes + Naïve Bayes)", "naive-bayes.svg"),
        ("Evening", "ISM_Past_Papers.html#june2026", "June 2026 Q1(b), Q2, Q6(a) Bayes", "bayes-tree.svg"),
    ]),
    ("Day 3", "Sessions 5–6", "Random variables + Distributions", [
        ("Morning", "ISM_Theory_Guide.html#session5", "Session 5 — PMF, E[X], Var, joint", "distributions.svg"),
        ("Afternoon", "ISM_Theory_Guide.html#session6", "Session 6 — Bernoulli, Binomial, Poisson, Normal", "distributions.svg"),
        ("Evening", "ISM_PYQ_Workbook.html#type7", "Workbook TYPE 7–9 + June 2026 Q3–Q4", "normal-curve.svg"),
    ]),
    ("Day 4", "Session 7 + Mid mock", "Sampling, CI + timed mid-sem", [
        ("Morning", "ISM_Theory_Guide.html#session7", "Session 7 — CLT, confidence intervals", "clt-ci.svg"),
        ("Afternoon", "ISM_PYQ_Workbook.html#type10", "Workbook TYPE 10–11 (Joint PDF, CDF)", None),
        ("Evening", "ISM_Past_Papers.html#jan-2026-mid-sem-ec-2-makeup", "Timed mock: Jan 2026 Makeup (2 hr)", None),
    ]),
    ("Day 5", "End-sem topics", "Correlation, tests, ANOVA (EC-3)", [
        ("Morning", "ISM_PYQ_Workbook.html#type12", "Workbook TYPE 12–15 (End-sem core)", "correlation.svg"),
        ("Afternoon", "ISM_Past_Papers.html#feb-2026-end-sem-ec-3-regular", "Feb 2026 End-Sem all 8 Qs", None),
        ("Evening", "ISM_Revision_Sheet.html", "Print revision sheet + skim weak TYPEs", None),
    ]),
]


def build():
    reset_uid()
    cards = ""
    for day, sessions, subtitle, blocks in DAYS:
        cards += f'<div class="day"><div class="day-h"><h2>{H.escape(day)} — {H.escape(sessions)}</h2><span>{H.escape(subtitle)}</span></div><div class="day-b">'
        for when, link, task, svg in blocks:
            fig = svg_figure(svg, task) if svg else ""
            cards += f'<div class="block"><h3>{H.escape(when)}</h3><ul><li><a href="{link}">{H.escape(task)}</a></li></ul>{fig}</div>'
        cards += "</div></div>"

    css = """
:root{--navy:#1e3a5f;--blue:#2563eb;--green:#059669;--bg:#f8fafc;--card:#fff;--border:#e2e8f0;--text:#1e293b;--muted:#64748b}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,"Segoe UI",sans-serif;background:var(--bg);color:var(--text);line-height:1.65}
header{background:linear-gradient(135deg,#1e3a5f,#059669);color:#fff;padding:1.8rem;text-align:center}
header a{color:#a7f3d0}
.wrap{max-width:820px;margin:0 auto;padding:1.5rem 1rem 3rem}
.day{background:var(--card);border:1px solid var(--border);border-radius:12px;margin:1.2rem 0;overflow:hidden}
.day-h{background:var(--navy);color:#fff;padding:.8rem 1.2rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem}
.day-h h2{font-size:1.05rem;margin:0}
.day-h span{font-size:.75rem;opacity:.85}
.day-b{padding:1rem 1.2rem}
.block{margin:.8rem 0;padding:.75rem 1rem;background:#f8fafc;border-radius:8px;border-left:4px solid var(--blue)}
.block h3{font-size:.88rem;color:var(--navy);margin-bottom:.4rem}
.block a{color:var(--blue)}
.formula-strip{background:#eff6ff;border-radius:8px;padding:.8rem 1rem;margin:1rem 0;text-align:center;font-size:.95rem}
.diagram{margin:.5rem 0;text-align:center}
.note{font-size:.82rem;color:var(--muted);padding:1rem;background:#fffbeb;border-radius:8px;border:1px solid #fcd34d;margin-top:1rem}
""" + SVG_WRAP_CSS

    mathjax = """
<script>
window.MathJax = {
  tex: { inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']], processEscapes: true }
};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js" async></script>
"""

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ISM 5-Day Study Plan — AIMLCZC418</title>
{mathjax}
<style>
{css}
</style></head><body>
<header><h1>ISM — 5-Day Study Plan</h1><p><a href="index.html">← Hub</a> · Sessions 1–7 · Mid + End sem</p></header>
<div class="wrap">
<div class="formula-strip">
<strong>Sessions covered:</strong> S1 Descriptive · S2 Probability · S3 Conditional · S4 Bayes · S5 RV · S6 Distributions · S7 Sampling/CI
</div>
{cards}
<p class="note"><strong>Sources:</strong> <code>ISM/companion docs/</code> (Sessions 1–7) · <code>ISM/previous question papers/</code> (answer keys) · <code>ISM/claude-cheatsheet/</code> generated HTML.</p>
</div></body></html>"""
    OUT.write_text(html, encoding="utf-8")
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
