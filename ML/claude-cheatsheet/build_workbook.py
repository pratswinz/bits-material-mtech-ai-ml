#!/usr/bin/env python3
"""Build ML_PYQ_Workbook.html — ISM-style TYPE sections + PYQ links."""
import html as H
import re
from pathlib import Path

from ml_workbook_catalog import collect_by_type
from svg_inline import SVG_WRAP_CSS, reset_uid, svg_figure

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ML_PYQ_Workbook.html"

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
header{background:#fff;color:var(--text);border-bottom:1px solid var(--border);padding:1.4rem 1.5rem;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.04)}
header h1{color:var(--navy);margin:0 0 .25rem;font-size:1.35rem}
header p{color:var(--muted);margin:0;font-size:.88rem}
header a{color:var(--blue);text-decoration:none}
header a:hover{text-decoration:underline}
.shell{display:flex;max-width:1280px;margin:0 auto;width:100%}
aside{width:260px;flex-shrink:0;background:var(--card);border-right:1px solid var(--border);padding:.8rem;position:sticky;top:0;height:100vh;overflow-y:auto;font-size:.72rem}
aside a{display:block;padding:.28rem .45rem;color:var(--navy);text-decoration:none;border-radius:4px}
aside a.nav-type{line-height:1.4;padding:.35rem .5rem}
aside a.nav-type .nav-num{font-weight:600;display:block}
aside a.nav-type .nav-topic{color:var(--muted);font-size:.68rem;display:block;margin-top:.05rem}
aside a.nav-type .nav-exam{color:var(--blue);font-weight:600;font-size:.64rem;margin-left:.25rem}
aside a:hover{background:#eff6ff}
aside .grp{font-weight:700;color:var(--purple);font-size:.62rem;text-transform:uppercase;margin:.7rem 0 .15rem}
.pyq-group{margin:1rem 0 0;padding:.85rem 0 0;border-top:1px dashed var(--border)}
.pyq-group .grp-head{font-size:.72rem;font-weight:700;text-transform:uppercase;color:var(--purple);letter-spacing:.04em;margin:0 0 .5rem}
.pyq-list{list-style:none;margin:0;padding:0;font-size:.82rem}
.pyq-list li{padding:.35rem 0;border-bottom:1px solid #f1f5f9;display:flex;flex-wrap:wrap;gap:.35rem .5rem;align-items:baseline}
.pyq-list li:last-child{border-bottom:none}
.pyq-paper{font-weight:600;color:var(--navy)}
.pyq-q{color:var(--muted)}
.pyq-label{color:var(--text)}
.pyq-list a{font-size:.75rem;color:var(--blue);text-decoration:none;white-space:nowrap}
.pyq-list a:hover{text-decoration:underline}
.tag.mid{background:#dbeafe;color:#1d4ed8}
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
.exam-img{max-width:100%;border:1px solid var(--border);border-radius:8px;margin:.5rem 0}
""" + SVG_WRAP_CSS

# (id, title, exam, svg, formula, solution_html)
TYPES = [
    ("type1", "TYPE 1 — Mitchell & Learning Paradigms", "Mid EC-2", "mitchell-etp.svg",
     r"\text{Learn from } E \text{ to improve } P \text{ on task } T",
     r"""<p><strong>PYQ:</strong> 2023 Regular Q1 — AlphaGo supervised → reinforcement</p>
<div class="step">(a) Self-driving + rewards → <strong>Reinforcement learning</strong></div>
<div class="step">(b) Labelled review sentiment → <strong>Supervised classification</strong></div>
<div class="step">(c) Unlabelled DNA clusters → <strong>Unsupervised clustering</strong></div>
<div class="step">(d) Predict claim amount → <strong>Supervised regression</strong></div>
<div class="step">Weather: E = history · T = predict rainfall · P = RMSE → <strong>regression</strong></div>
<div class="ans">AlphaGo v1: supervised on human games → v2: self-play reinforcement</div>"""),
    ("type2", "TYPE 2 — Data Quality & Preprocessing", "Mid EC-2", None,
     r"\text{Detect: missing, duplicate, outlier, inconsistent format, invalid type}",
     r"""<p><strong>PYQ:</strong> 2023 Regular Q2 — student admission table</p>
<div class="step">Duplicate Bhargav · CGPA 12.3 / −1.5 · Missing CGPA/DOB · Mixed date formats · Branch casing · Invalid Feb 30</div>
<div class="step">Fix: dedupe, impute missing, standardize dates/categories, cap invalid CGPA, parse DOB → derive age</div>
<div class="ans">List 5–6 issues + fix for each (0.25 marks each in official rubric)</div>"""),
    ("type3", "TYPE 3 — Gradient Descent", "Mid EC-2", "gd-flow.svg",
     r"\theta_j \leftarrow \theta_j - \alpha\frac{\partial J}{\partial\theta_j} \quad \text{Ridge: } +\frac{\lambda}{m}\theta_j",
     r"""<p><strong>PYQ:</strong> Dec 2025 Q5 — \(x=[1,2,3], y=[2,5,7], \theta_0=0, \theta_1=1, \alpha=0.05, \lambda=2, m=3\)</p>
<div class="step">Predictions \(h=[1,2,3]\), errors \(e=[-1,-3,-4]\)</div>
<div class="step">\(\partial J/\partial\theta_0 = -8/3\), \(\partial J/\partial\theta_1 = -19/3 + 2/3\) (Ridge on \(\theta_1\))</div>
<div class="step">Update: \(\theta_0=0.133, \theta_1=1.283\) · Cost drops 4.667 → 3.006 ✓</div>
<div class="ans">Negative gradient on \(\theta_j\) → increase that weight in GD update</div>"""),
    ("type4", "TYPE 4 — Confusion Matrix & Metrics", "Mid EC-2", "confusion-matrix.svg",
     r"\text{Acc}=\frac{TP+TN}{N} \quad \text{Prec}=\frac{TP}{TP+FP} \quad \text{Rec}=\frac{TP}{TP+FN} \quad F_1=\frac{2PR}{P+R}",
     r"""<p><strong>PYQ:</strong> June 2026 Q4 — fraud detection (imbalanced)</p>
<div class="step">Model A: Acc=98.55% but Prec=33.3%, Rec=45% — accuracy misleading</div>
<div class="step">Model B: lower accuracy, TPR=80% — better for catching fraud</div>
<div class="step">Dec 2025 medical: FN cost \$10,000 vs FP \$500 → prioritize <strong>recall</strong></div>
<div class="ans">Pick metric to match business cost of FN vs FP</div>"""),
    ("type5", "TYPE 5 — Bias–Variance Tradeoff", "Mid EC-2", "bias-variance.svg",
     r"R^2 = 1 - \frac{SS_{res}}{SS_{tot}} \quad \text{Train}\approx\text{Test high} \Rightarrow \text{bias}",
     r"""<p><strong>PYQ:</strong> June 2026 Q5 — spam classifier learning curves</p>
<div class="step">Model A: train 61%, val 60% → <strong>high bias</strong> (underfit); more data won't help</div>
<div class="step">Model B: train 99%, val 67% → <strong>high variance</strong> (overfit); use L1/L2, fewer features</div>
<div class="ans">Improved: logistic + moderate features + L2 + cross-validation</div>"""),
    ("type6", "TYPE 6 — Regularization (Ridge / Lasso)", "Mid EC-2", "ridge-lasso.svg",
     r"J_{Ridge}=MSE+\lambda\sum\theta_j^2 \quad J_{Lasso}=MSE+\lambda\sum|\theta_j|",
     r"""<p><strong>PYQ:</strong> 2024 Regular Q1 — overfitting with many features</p>
<div class="step">(a) Many irrelevant features → <strong>Lasso (L1)</strong> zeros weights (feature selection)</div>
<div class="step">(b) Large logistic weights → L2/L1 penalty shrinks them; tune \(\lambda\) via CV</div>
<div class="step">Ridge update: \(\theta_j \leftarrow (1-\alpha\lambda/m)\theta_j - \alpha\partial MSE\) · Lasso subtracts \(\alpha\lambda\,\mathrm{sign}(\theta_j)\)</div>
<div class="ans">See also <a href="#practice-ridge">Ridge/Lasso numerical</a> (2 iterations)</div>"""),
    ("type7", "TYPE 7 — Decision Trees / Entropy / IG", "Mid EC-2", "entropy-ig-tree.svg",
     r"H(S)=-\sum_k p_k\log_2 p_k \quad IG=H(S)-\sum_v\frac{|S_v|}{|S|}H(S_v)",
     r"""<p><strong>PYQ:</strong> June 2026 Q2 — loan approval (10 applicants)</p>
<div class="step">Parent: 5 Yes / 5 No → \(H(S)=1.0\) bit</div>
<div class="step">Split <em>Existing Loan</em>: No branch 5Y/0N (H=0), Yes branch 0Y/5N (H=0) → <strong>IG = 1.0</strong></div>
<div class="step">Tree: Existing Loan=No → Approve; Yes → Deny (pure leaves)</div>
<div class="ans">Always pick attribute with maximum information gain at each node</div>"""),
    ("type8", "TYPE 8 — Logistic Regression", "Mid EC-2", "logistic-sigmoid.svg",
     r"\sigma(z)=\frac{1}{1+e^{-z}} \quad z=\theta^T x \quad \text{BCE: } -[y\log\hat p+(1-y)\log(1-\hat p)]",
     r"""<p><strong>PYQ:</strong> June 2026 Q3 — min-max + logistic default prediction</p>
<div class="step">Min-max credit scores → \(x'\in[0,1]\) · Sigmoid probabilities for each student</div>
<div class="step">BCE loss \(L=0.864\) · One GD step: \(w_0^*=0.006, w_1^*=0.393, w_2^*=-0.424\)</div>
<div class="step">Large positive coef ≠ guaranteed class (probability, not deterministic)</div>
<div class="ans">Decision boundary: set \(\theta^T x=0\) (or \(p=0.5\))</div>"""),
    ("type9", "TYPE 9 — Feature Scaling", "Mid EC-2", "min-max-scaling.svg",
     r"x'=\frac{x-x_{min}}{x_{max}-x_{min}} \quad x'=\frac{x-\mu}{\sigma}",
     r"""<p><strong>PYQ:</strong> Practice T/F — scaling &amp; trees</p>
<div class="step">(a) GD needs scaling for fast convergence → <strong>TRUE</strong></div>
<div class="step">(b) Decision trees need scaling → <strong>FALSE</strong> (split-invariant)</div>
<div class="step">(c) Min-max sensitive to outliers → <strong>TRUE</strong></div>
<div class="step">(d) Z-score maps to [0,1] → <strong>FALSE</strong></div>
<div class="ans">Scale before GD/logistic; trees &amp; Naïve Bayes often unaffected</div>"""),
    ("type10", "TYPE 10 — Model Robustness", "Mid EC-2", "bias-variance.svg",
     r"\text{LR: sensitive to outliers} \quad \text{Tree: isolates outliers} \quad \text{RF: bagging smooths}",
     r"""<p><strong>PYQ:</strong> ML/questions/_Resources/ML_MidSem_Practice_PastPapers_Mock.pdf</p>
<div class="step">Linear regression + noise/outliers → <strong>Affected</strong> (squared error)</div>
<div class="step">Decision tree + outliers → often <strong>Less affected</strong> (isolated leaf)</div>
<div class="step">Random forest → <strong>Less affected</strong> on both (averaging)</div>
<div class="ans">Match model inductive bias to data noise profile</div>"""),
    ("type11", "TYPE 11 — Normal Equation / Dimensions", "Mid EC-2", None,
     r"\theta=(X^TX)^{-1}X^Ty \quad X\in\mathbb{R}^{m\times(n+1)},\ y\in\mathbb{R}^{m\times 1}",
     r"""<p><strong>PYQ:</strong> 2023 Regular Q6 — \(m=28\) samples, \(n=4\) features + bias</p>
<div class="step">\(\mathbf{X}\in\mathbb{R}^{28\times 5}\), \(\mathbf{y}\in\mathbb{R}^{28\times 1}\), \(\boldsymbol{\theta}\in\mathbb{R}^{5\times 1}\)</div>
<div class="step">\(X^TX\in\mathbb{R}^{5\times 5}\) · wrong dimension on any axis → 0 marks</div>
<div class="ans">Add column of 1s for intercept before matrix multiply</div>"""),
]

PRACTICE = r"""
<section id="practice-ridge"><h2>Practice — Ridge &amp; Lasso (2 iterations)</h2>
<span class="tag mid">Mid</span>
<p class="src"><code>ML/mid sem/ML_LinReg_Regularization_Solution.pdf</code></p>
<div class="q"><p><strong>RR-CHD:</strong> Diastolic BP \(x_1\), BMI \(x_2\). \(w_0=5, w_1=w_2=-0.03, \alpha=0.02, \lambda=5, m=3\).</p>
<div class="step"><strong>Ridge iter 1:</strong> \(1-\alpha\lambda=0.9\) → \(w_0=5.0016, w_1=0.1823, w_2=0.0507\)</div>
<div class="step"><strong>Lasso:</strong> subtract \(\alpha\lambda\,\mathrm{sign}(w_j)\) each step — can zero weights</div>
<div class="ans">Show matrix dimensions + one full iteration with cost decrease (exam rubric)</div></div></section>

<section id="practice-mock"><h2>Practice — Mock Exam (6 questions)</h2>
<span class="tag mid">Mid</span>
<p class="src"><code>ML/questions/_Resources/ML_MidSem_Practice_PastPapers_Mock.pdf</code></p>
<div class="q"><p><strong>Mock Q1:</strong> Hospital readmission — Mitchell E/T/P, classification, overfitting fixes</p>
<div class="step">E = records · T = 30-day readmission · P = F1/AUC · Fix overfit: L2 + early stopping</div></div>
<div class="q"><p><strong>Mock Q3:</strong> GD one step — \(x=[2,4,6], y=[3,7,11], \theta_0=\theta_1=0.5, \alpha=0.1, \lambda=1\)</p>
<div class="ans">\(\theta_0=0.933, \theta_1=0.9\) after one iteration</div></div>
<div class="q"><p><strong>Mock Q4:</strong> Spam 2000 emails — precision/recall/F1; FN \$50 vs FP \$5 → lower threshold if FN costly</p></div></section>

<section id="practice-june"><h2>June 2026 — Full Paper</h2>
<span class="tag mid">Mid</span>
<p class="src"><code>ML/questions/MidSem/2026-06_Regular/</code> · detailed solutions with exam images</p>
<div class="q"><p>Q1–Q5 covered across TYPE 3, 4, 5, 7, 8 above. Full stems + images:</p>
<div class="ans"><a href="ML_Past_Papers.html#june2026">Open June 2026 in Past Papers →</a></div></div></section>
"""


def _type_parts(title: str) -> tuple[str, str]:
    if "—" in title:
        num, topic = title.split("—", 1)
        return num.strip(), topic.strip()
    return title.strip(), ""


def _render_pyq_group(type_num: int, catalog: dict) -> str:
    items = catalog.get(type_num, [])
    if not items:
        return ""
    rows = []
    for row in items:
        q = row["qid"]
        sess = "Makeup" if row["session"] == "Makeup" else "Reg"
        rows.append(
            f'<li><span class="pyq-paper">{H.escape(row["label"])}</span>'
            f'<span class="pyq-q">{H.escape(q)}</span>'
            f'<span class="pyq-label">— {H.escape(row["brief"])}</span>'
            f'<span class="pyq-q">({row["year"]} {sess})</span>'
            f'<a href="{row["href"]}">Past paper →</a></li>'
        )
    return (
        '<div class="pyq-group"><p class="grp-head">Mid-sem PYQs of this type</p>'
        f'<ul class="pyq-list">{"".join(rows)}</ul></div>'
    )


def build():
    reset_uid()
    catalog = collect_by_type(mid_sem_only=True)
    nav = ['<a href="#overview">Overview</a>']
    overview_rows = ""

    for tid, title, exam, svg, formula, solution in TYPES:
        num, topic = _type_parts(title)
        type_num = int(re.search(r"\d+", num).group())
        overview_rows += (
            f"<tr><td><strong>{H.escape(num)}</strong></td>"
            f"<td>{H.escape(topic)}</td><td>Mid</td></tr>\n"
        )
        nav.append(
            f'<a href="#{tid}" class="nav-type">'
            f'<span class="nav-num">{H.escape(num)}</span>'
            f'<span class="nav-topic">{H.escape(topic)} '
            f'<span class="nav-exam">Mid</span></span></a>'
        )

    nav.extend([
        '<div class="grp">Practice</div>',
        '<a href="#practice-june">June 2026 Full Paper</a>',
        '<a href="#practice-ridge">Ridge / Lasso Numerical</a>',
        '<a href="#practice-mock">Mock Exam</a>',
        '<div class="grp">Also</div>',
        '<a href="ML_Past_Papers.html">Past Papers</a>',
        '<a href="ML_Theory_Guide.html">Theory</a>',
        '<a href="index.html">Hub</a>',
    ])

    body = f"""<section id="overview"><h2>Question Type Index</h2>
<p class="src">Organised by exam pattern · Sources: <code>ML/questions/MidSem/</code> + practice mock</p>
<p>Each TYPE has the core formula, a diagram where helpful, a worked PYQ, and links to all matching past-paper questions.</p>
<table class="data-table"><thead><tr><th>Type</th><th>Problem type</th><th>Exam</th></tr></thead><tbody>
{overview_rows}</tbody></table></section>"""

    for tid, title, exam, svg, formula, solution in TYPES:
        type_num = int(re.search(r"\d+", tid).group())
        diag = svg_figure(svg, title) if svg else ""
        pyq_block = _render_pyq_group(type_num, catalog)
        body += f"""<section id="{tid}"><h2>{H.escape(title)}</h2>
<span class="tag mid">Mid</span>
<span class="tag">{H.escape(exam)}</span>
<div class="formula"><h5>Core formula</h5>\\[{formula}\\]</div>
{diag}
<div class="q">{solution}</div>
{pyq_block}</section>"""

    body += PRACTICE

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ML PYQ Workbook — By Question Type</title>{SHARED_HEAD}
<style>{SHARED_CSS}</style></head><body>
<header><h1>ML PYQ Workbook</h1><p><a href="index.html">← Hub</a> · 11 question types · AIMLCZG565</p></header>
<div class="shell"><aside><div class="grp">Types</div>{"".join(nav)}
</aside><main>{body}</main></div></body></html>"""
    OUT.write_text(html, encoding="utf-8")
    linked = sum(len(catalog.get(i, [])) for i in range(1, 12))
    print(f"Wrote {OUT} — {len(TYPES)} types, {linked} PYQ links")


if __name__ == "__main__":
    build()
