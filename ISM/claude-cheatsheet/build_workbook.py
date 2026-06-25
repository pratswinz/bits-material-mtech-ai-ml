#!/usr/bin/env python3
"""Build ISM_PYQ_Workbook.html — question types with formulas, diagrams, detailed solutions."""
import html as H
from pathlib import Path

from svg_inline import SVG_WRAP_CSS, reset_uid, svg_figure

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ISM_PYQ_Workbook.html"

SHARED_HEAD = """
<script>
window.MathJax = {
  tex: { inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']], processEscapes: true },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js" async></script>
"""

SHARED_CSS = """
:root{--navy:#1e3a5f;--blue:#2563eb;--green:#059669;--purple:#7c3aed;--amber:#d97706;--bg:#f8fafc;--card:#fff;--border:#e2e8f0;--text:#1e293b;--muted:#64748b}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Georgia,"Segoe UI",serif;background:var(--bg);color:var(--text);line-height:1.65}
header{background:var(--navy);color:#fff;padding:1.5rem;text-align:center}
header a{color:#93c5fd}
.shell{display:flex;max-width:1280px;margin:0 auto;width:100%}
aside{width:260px;flex-shrink:0;background:var(--card);border-right:1px solid var(--border);padding:.8rem;position:sticky;top:0;height:100vh;overflow-y:auto;font-size:.72rem}
aside a{display:block;padding:.28rem .45rem;color:var(--navy);text-decoration:none;border-radius:4px}
aside a:hover{background:#eff6ff}
aside .grp{font-weight:700;color:var(--purple);font-size:.62rem;text-transform:uppercase;margin:.7rem 0 .15rem}
main{flex:1;min-width:0;max-width:920px;padding:1.5rem 2rem}
section{margin-bottom:2.5rem;padding-bottom:1.5rem;border-bottom:2px solid var(--border)}
h2{color:var(--navy);font-size:1.15rem;margin-bottom:.6rem}
.q{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--purple);border-radius:10px;padding:1.2rem;margin:1rem 0}
.formula{background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:.85rem 1rem;margin:.75rem 0;font-size:.95rem;text-align:center}
.formula h5{margin:0 0 .4rem;font-size:.72rem;text-transform:uppercase;color:var(--blue);letter-spacing:.04em;text-align:left}
.src{font-size:.78rem;color:var(--muted);margin-bottom:.5rem}
.step{background:#f8fafc;border:1px solid var(--border);border-radius:8px;padding:.75rem 1rem;margin:.5rem 0;font-size:.92rem}
.step strong{color:var(--navy)}
.ans{background:#ecfdf5;border:1px solid #bbf7d0;border-radius:8px;padding:.65rem 1rem;margin:.65rem 0;font-weight:600;color:#047857}
.data-table{border-collapse:collapse;width:100%;margin:.75rem 0;font-size:.82rem}
.data-table th,.data-table td{border:1px solid var(--border);padding:.35rem .5rem}
.data-table thead th{background:#eff6ff;font-weight:600}
.diagram{margin:.75rem 0;text-align:center}
.tag{display:inline-block;font-size:.68rem;background:#f3e8ff;color:var(--purple);padding:2px 8px;border-radius:99px;margin-right:4px}
""" + SVG_WRAP_CSS

TYPES = [
    ("type1", "TYPE 1 — Descriptive Statistics", "Mid EC-2", "box-plot.svg",
     r"\bar{x}=\frac{1}{n}\sum x_i \quad \text{Median = middle sorted value} \quad s=\sqrt{\frac{\sum(x_i-\bar{x})^2}{n-1}} \quad \text{IQR}=Q_3-Q_1",
     """<p><strong>PYQ:</strong> Dec 2025 Q1 — chicken sandwich fat (7,4,20,23,25,19,30,30,40,56)</p>
<div class="step"><strong>Step 1 — Sort &amp; centre:</strong> Sorted: 4,7,19,20,23,25,30,30,40,56 → \(\bar{x}=25.4\), Median = (23+25)/2 = <strong>22</strong></div>
<div class="step"><strong>Step 2 — Spread:</strong> Sample SD ≈ <strong>14.6 g</strong>, Q1=19, Q3=30, IQR=11</div>
<div class="step"><strong>Step 3 — Outliers:</strong> Upper fence = 30+1.5(11)=46.5 → <strong>56 is outlier</strong></div>
<div class="step"><strong>Interpret:</strong> Right-skewed (mean &gt; median); high variability; one extreme sandwich.</div>
<div class="ans">Answer: Mean=25.4, Median=22, SD≈14.6, IQR=11, outlier=56</div>"""),
    ("type2", "TYPE 2 — Five-Number Summary", "Mid EC-2", "box-plot.svg",
     r"\text{Min, Q1, Median, Q3, Max} \quad \text{Outlier if } x>Q_3+1.5\cdot\text{IQR}",
     """<p><strong>PYQ:</strong> Jan 2026 Makeup Q1 — production output (190…380)</p>
<div class="step">Sorted: 190,230,240,245,250,265,270,280,285,380</div>
<div class="step">Min=190, Q1≈237.5, Med=257.5, Q3≈281.25, Max=380 (official key method)</div>
<div class="step">IQR≈43.75, upper fence≈346.9 → <strong>380 is outlier</strong> (process shift on day 10)</div>
<div class="ans">Five-number: 190, 237.5, 257.5, 281.25, 380 · Outlier: 380</div>"""),
    ("type3", "TYPE 3 — Inclusion–Exclusion", "Mid EC-2", "venn-three.svg",
     r"|A\cup B\cup C|=|A|+|B|+|C|-|A\cap B|-|A\cap C|-|B\cap C|+|A\cap B\cap C|",
     """<p><strong>PYQ:</strong> June 2026 Q2 — NEET 600 students, P/C/B sets</p>
<div class="step">Given: |P|=380, |C|=260, |B|=420, pairwise intersections 150,250,180</div>
<div class="step">All three: \(600=1060-580+|P\cap C\cap B|\) → <strong>|P∩C∩B|=120</strong>, P=0.20</div>
<div class="step">Exactly two: (150+250+180)−3(120)=<strong>220</strong></div>
<div class="ans">P(exactly 2 subjects) = 220/600 ≈ 0.367</div>"""),
    ("type4", "TYPE 4 — Conditional & Total Probability", "Mid EC-2", "bayes-tree.svg",
     r"P(A|B)=\frac{P(A\cap B)}{P(B)} \quad P(B)=\sum P(B|A_i)P(A_i)",
     """<p><strong>PYQ:</strong> June 2026 Q1(b) — coding competition</p>
<div class="step">\(P(B\text{ wins})=P(A\text{ fails})P(B|A\text{ fails})+P(A\text{ wins})P(B|A\text{ wins})\)</div>
<div class="step">\(=0.5(0.85)+0.5(0.25)=0.425+0.125=\mathbf{0.55}\)</div>
<div class="ans">P(B wins) = 0.55</div>"""),
    ("type5", "TYPE 5 — Bayes Theorem", "Mid EC-2", "bayes-tree.svg",
     r"P(A|R)=\frac{P(R|A)P(A)}{P(R)} \quad P(R)=\sum P(R|A_i)P(A_i)",
     """<p><strong>PYQ:</strong> Jan 2026 Makeup Q2 — VC appointment &amp; research (official key)</p>
<div class="step">\(P(A)=0.5, P(B)=0.3, P(P)=0.2\); \(P(R|A)=0.8, P(R|B)=0.6, P(R|P)=0.4\)</div>
<div class="step">\(P(R)=0.4+0.18+0.08=0.66\)</div>
<div class="step">\(P(A|R)=0.4/0.66=20/33\approx\mathbf{0.606}\)</div>
<div class="ans">P(academician | research promoted) ≈ 0.606</div>"""),
    ("type6", "TYPE 6 — Naïve Bayes Classifier", "Mid EC-2", "naive-bayes.svg",
     r"P(C|w_1,\ldots,w_n)\propto P(C)\prod_i P(w_i|C) \quad \text{Laplace: }\frac{count+\alpha}{total+V\alpha}",
     """<p><strong>PYQ:</strong> Dec 2025 Q2 — "assignment urgent" (α=1, official key)</p>
<table class="data-table"><thead><tr><th>Word</th><th>Count U</th><th>Count N</th></tr></thead>
<tbody><tr><td>assignment</td><td>1</td><td>0</td></tr><tr><td>urgent</td><td>1</td><td>0</td></tr></tbody></table>
<div class="step">\(P(U)=P(N)=0.5\), |V|=16, totals after smoothing: U=25, N=23</div>
<div class="step">Urgent path: \(0.5\times(2/25)\times(2/25)=0.0032\)</div>
<div class="step">Not urgent: \(0.5\times(1/23)\times(1/23)\approx0.000945\)</div>
<div class="ans">Classify as <strong>Urgent</strong></div>"""),
    ("type7", "TYPE 7 — Discrete PMF", "Mid EC-2", None,
     r"\sum p(x)=1 \quad E[X]=\sum x\,p(x) \quad \mathrm{Var}(X)=E[X^2]-(E[X])^2",
     """<p><strong>PYQ:</strong> Dec 2025 Q3(a) — find k for custom PMF</p>
<div class="step">Sum all terms in terms of k → solve \(11k+8k^2=1\)</div>
<div class="step">Then compute \(P(X<6)\), \(P(X\ge6)\), \(P(0<X<5)\) by adding pmf values</div>
<div class="ans">Find k first, then sum relevant probabilities</div>"""),
    ("type8", "TYPE 8 — Binomial & Poisson", "Mid EC-2", "distributions.svg",
     r"P(X=k)=\binom{n}{k}p^k(1-p)^{n-k} \quad P(X=k)=\frac{e^{-\lambda}\lambda^k}{k!} \quad \lambda=np",
     """<p><strong>PYQ:</strong> June 2026 Q3 — 40 chips, p=0.03 defective</p>
<div class="step">\(X\sim\text{Binomial}(40,0.03)\)</div>
<div class="step">\(P(X=4)\approx0.062\), \(P(2\le X\le5)\approx0.238\), \(P(X>4)\approx0.096\)</div>
<p><strong>PYQ:</strong> Dec 2025 Q3(b) — Poisson approx, 0.2% defect, 10 blades/packet</p>
<div class="step">\(\lambda=10\times0.002=0.02\) per packet → scale to 10,000 packets</div>
<div class="ans">Use Binomial exact; Poisson when n large, p small</div>"""),
    ("type9", "TYPE 9 — Normal Distribution", "Mid EC-2", "normal-curve.svg",
     r"Z=\frac{X-\mu}{\sigma} \quad P(a<X<b)=P\left(\frac{a-\mu}{\sigma}<Z<\frac{b-\mu}{\sigma}\right)",
     """<p><strong>PYQ:</strong> Jan 2026 Makeup Q3 — scores N(73,8²)</p>
<div class="step">(i) \(P(X<91)=P(Z<2.25)\approx0.988\) → yes, "most" below 91</div>
<div class="step">(ii) \(P(65<X<89)\approx0.818\)</div>
<div class="step">(iii) Dean's List top 5%: \(c=73+1.645(8)\approx86.2\)</div>
<div class="ans">Cut-off ≈ 86.2 marks</div>"""),
    ("type10", "TYPE 10 — Joint PDF (Continuous)", "Mid EC-2", None,
     r"\iint f(x,y)\,dy\,dx=1 \quad f_X(x)=\int f(x,y)\,dy \quad \text{Independent if } f(x,y)=f_X(x)f_Y(y)",
     """<p><strong>PYQ:</strong> Dec 2025 Q4 — \(f(x,y)=6x^2y\) on [0,1]²</p>
<div class="step">Verify integral = 1 ✓ · Marginals: \(f_X=3x^2\), \(f_Y=6y\)</div>
<div class="step">\(P(X<0.5,Y>0.5)=3/32\) · Not independent · \(E[X]=3/4\), \(E[Y]=1/2\)</div>"""),
    ("type11", "TYPE 11 — CDF Problems", "Mid EC-2", None,
     r"F(x)=P(X\le x) \quad f(x)=F'(x) \quad P(a\le X\le b)=F(b)-F(a)",
     """<p><strong>PYQ:</strong> Jan 2026 Makeup Q5 — overheating index CDF</p>
<div class="step">Find k so CDF goes from 0 to 1 · Warning zone P(1≤X≤2) · PDF = derivative of CDF</div>"""),
    ("type12", "TYPE 12 — Pearson Correlation", "End EC-3", "correlation.svg",
     r"r=\frac{\sum(X-\bar{X})(Y-\bar{Y})}{\sqrt{\sum(X-\bar{X})^2\sum(Y-\bar{Y})^2}}",
     """<p><strong>PYQ:</strong> Feb 2026 End-Sem Q1 — Delhi temperature vs electricity (official key)</p>
<table class="data-table"><thead><tr><th>Month</th><th>X °C</th><th>Y kWh</th></tr></thead>
<tbody><tr><td>May–Sep</td><td>38,41,35,33,31</td><td>320,380,290,270,240</td></tr></tbody></table>
<div class="step">\(\bar{X}=35.6\), \(\bar{Y}=300\) → <strong>r ≈ 0.989</strong> (very strong positive)</div>
<div class="ans">Strong AC-driven demand spike in heatwaves</div>"""),
    ("type13", "TYPE 13 — Exponential Smoothing", "End EC-3", None,
     r"F_{t+1}=\alpha Y_t+(1-\alpha)F_t",
     """<p><strong>PYQ:</strong> Feb 2026 End-Sem Q2 — demand Jan–Jun (official key)</p>
<div class="step">\(F_1=82\). α=0.4 → \(F_{July}\approx96.37\); α=0.7 → \(F_{July}\approx99.88\)</div>
<div class="ans">Higher α (0.7) for sudden spikes — reacts faster to recent demand</div>"""),
    ("type14", "TYPE 14 — Hypothesis Testing", "End EC-3", None,
     r"H_0:\mu=\mu_0 \quad z=\frac{\bar{x}-\mu_0}{\sigma/\sqrt{n}} \quad \text{Paired: test } d_i=\text{After}-\text{Before}",
     """<p><strong>PYQ:</strong> Feb 2026 End-Sem Q3 — paired t (before/after scores) &amp; z-test (Derm Assist)</p>
<div class="step">(a) All differences positive → reject H₀ at 5% — strategy helps</div>
<div class="step">(b) \(z=(18.2-20)/(7.5/6)=-1.44\), one-tailed p≈0.075 → fail to reject 20 min claim</div>"""),
    ("type15", "TYPE 15 — ANOVA / RBD", "End EC-3", None,
     r"\text{Two-way ANOVA: test row (blocks) and column (treatment) effects}",
     """<p><strong>PYQ:</strong> Feb 2026 End-Sem Q4 — mango irrigation × orchard blocks</p>
<div class="step">Drip &gt; Sprinkler &gt; Flood consistently → reject H₀ for irrigation method</div>"""),
    ("type16", "TYPE 16 — Linear Regression", "End EC-3", "correlation.svg",
     r"\hat{Y}=\beta_0+\beta_1 X \quad \beta_1=\frac{S_{xy}}{S_{xx}}",
     """<p><strong>PYQ:</strong> Feb 2026 End-Sem Q5 — MUFI water vs yield (10 gardens)</p>
<div class="step">Fit \(\hat{Y}\approx0.35+0.47X\), strong linear fit (r≈0.93)</div>
<div class="ans">Optimal efficiency ~3–4 L/m²/day</div>"""),
    ("type17", "TYPE 17 — Confidence Intervals", "End EC-3", "clt-ci.svg",
     r"\bar{x}\pm t_{\alpha/2,\,n-1}\cdot\frac{s}{\sqrt{n}}",
     """<p><strong>PYQ:</strong> Feb 2026 End-Sem Q7(a) — cadence of 20 men</p>
<div class="step">\(\bar{x}\approx0.917\), 95% CI ≈ [0.880, 0.954]</div>
<div class="step">(b) Residual series mean≈0 → plausibly white noise</div>"""),
    ("type18", "TYPE 18 — Two-Proportion & F-Test", "End EC-3", None,
     r"z=\frac{\hat{p}_1-\hat{p}_2}{\sqrt{\hat{p}(1-\hat{p})(1/n_1+1/n_2)}} \quad F=\frac{s_1^2}{s_2^2}",
     """<p><strong>PYQ:</strong> Feb 2026 End-Sem Q8 — vaccination cities &amp; chip thickness</p>
<div class="step">(a) 180/300 vs 135/250 → no significant difference at 5%</div>
<div class="step">(b) Line A more variable than Line B (F-test, one-tailed)</div>"""),
]


def build():
    reset_uid()
    nav = ['<a href="#overview">Overview</a>']
    body = """<section id="overview"><h2>Question Type Index</h2>
<p class="src">Organised by exam pattern · Sources: <code>ISM/previous question papers/</code> answer keys + June 2026</p>
<p>Each TYPE has the core formula, a diagram where helpful, and a fully worked PYQ from official papers.</p>
<table class="data-table"><thead><tr><th>Type</th><th>Topic</th><th>Exam</th></tr></thead><tbody>
<tr><td>1–2</td><td>Descriptive stats, five-number summary</td><td>Mid</td></tr>
<tr><td>3–5</td><td>Inclusion–exclusion, conditional, Bayes</td><td>Mid</td></tr>
<tr><td>6</td><td>Naïve Bayes</td><td>Mid</td></tr>
<tr><td>7–11</td><td>PMF, Binomial/Poisson, Normal, Joint PDF, CDF</td><td>Mid</td></tr>
<tr><td>12–18</td><td>Correlation, smoothing, tests, ANOVA, regression, CI</td><td>End</td></tr>
</tbody></table></section>"""

    for tid, title, exam, svg, formula, solution in TYPES:
        nav.append(f'<a href="#{tid}">{title.split("—")[0].strip()}</a>')
        diag = svg_figure(svg, title) if svg else ""
        body += f"""<section id="{tid}"><h2>{H.escape(title)}</h2>
<span class="tag">{H.escape(exam)}</span>
<div class="formula"><h5>Core formula</h5>\\[{formula}\\]</div>
{diag}
<div class="q">{solution}</div></section>"""

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ISM PYQ Workbook — By Question Type</title>{SHARED_HEAD}
<style>{SHARED_CSS}</style></head><body>
<header><h1>ISM PYQ Workbook</h1><p><a href="index.html">← Hub</a> · 18 question types · AIMLCZC418</p></header>
<div class="shell"><aside><div class="grp">Types</div>{"".join(nav)}
<div class="grp">Also</div><a href="ISM_Past_Papers.html">Past Papers</a><a href="ISM_Theory_Guide.html">Theory</a>
</aside><main>{body}</main></div></body></html>"""
    OUT.write_text(html, encoding="utf-8")
    print("Wrote", OUT, "—", len(TYPES), "types")


if __name__ == "__main__":
    build()
