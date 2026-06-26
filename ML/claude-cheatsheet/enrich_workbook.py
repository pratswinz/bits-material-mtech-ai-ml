#!/usr/bin/env python3
"""Ensure ML_PYQ_Workbook.html has all TYPE sections + inlined SVG diagrams."""
from pathlib import Path

from svg_inline import patch_html_file, reset_uid, svg_figure

ROOT = Path(__file__).resolve().parent
WORKBOOK = ROOT / "ML_PYQ_Workbook.html"

TYPE10_11 = """
<!-- TYPE 10 -->
<section id="type10">
<h2>TYPE 10 — Model Robustness</h2>
<div class="q">
<p class="src">ML/questions/_Resources/ML_MidSem_Practice_PastPapers_Mock.pdf — TYPE 10</p>
<p>Three models on two datasets (noise vs outliers). State <strong>Affected</strong> or <strong>Less Affected</strong> with justification.</p>
<div class="step"><strong>LR + noise/outliers:</strong> MSE squares errors — every point pulls the line; outliers dominate.</div>
<div class="step"><strong>Tree + noise:</strong> Overfits with extra splits. <strong>Tree + outliers:</strong> Outlier often isolated in its own leaf.</div>
<div class="step"><strong>RF:</strong> Bagging + averaging many trees smooths noise and dilutes outlier impact.</div>
<table><tr><th>Model</th><th>Noise</th><th>Outliers</th></tr>
<tr><td>Linear Regression</td><td><strong>Affected</strong></td><td><strong>Affected</strong></td></tr>
<tr><td>Decision Tree</td><td><strong>Affected</strong></td><td><strong>Less Affected</strong></td></tr>
<tr><td>Random Forest</td><td><strong>Less Affected</strong></td><td><strong>Less Affected</strong></td></tr></table>
{diag}
</div>
</section>

<!-- TYPE 11 -->
<section id="type11">
<h2>TYPE 11 — Normal Equation Dimensions</h2>
<div class="q">
<p class="src">ML/questions/_Resources/ML_MidSem_Practice_PastPapers_Mock.pdf — TYPE 11</p>
<p>\(m=28\) samples, \(n=4\) features (add bias \(x_0=1\)). Dimensions of \(X\), \(y\), \(\theta\) in \(\theta=(X^TX)^{-1}X^Ty\)?</p>
<div class="ans"><strong>\(X\): 28×5</strong> · <strong>\(y\): 28×1</strong> · <strong>\(\theta\): 5×1</strong></div>
<div class="step">\(X^T\): 5×28 · \(X^TX\): 5×5 · \((X^TX)^{-1}X^Ty\): 5×1 ✓</div>
<div class="step">Wrong coordinate in any dimension → 0 marks (per official rubric).</div>
</div>
</section>
"""

NAV_LINKS = """<a href="#type10">TYPE 10 — Robustness</a>
<a href="#type11">TYPE 11 — Normal Eq.</a>
"""

DIAGRAM_CSS = """
.formula{background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:.65rem 1rem;margin:.6rem 0;font-size:.92rem}
.formula h5{margin:0 0 .35rem;font-size:.72rem;text-transform:uppercase;color:var(--blue);letter-spacing:.04em}
.diagram{margin:.75rem 0;text-align:center}
.diagram img{max-width:100%;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff}
.diagram figcaption{font-size:.75rem;color:var(--muted);margin-top:.35rem}
"""


def ensure_css(html: str) -> str:
    if ".diagram{" not in html:
        html = html.replace(".tag{display:inline-block", DIAGRAM_CSS + ".tag{display:inline-block")
    return html


def ensure_nav(html: str) -> str:
    if 'href="#type10"' not in html:
        html = html.replace(
            '<a href="#type9">TYPE 9 — Scaling T/F</a>\n<a href="#midsem">',
            '<a href="#type9">TYPE 9 — Scaling T/F</a>\n' + NAV_LINKS + '<a href="#midsem">',
        )
    return html


def ensure_type10_11(html: str) -> str:
    if 'id="type10"' in html:
        return html
    reset_uid()
    block = TYPE10_11.replace("{diag}", svg_figure("bias-variance.svg", "Robustness"))
    return html.replace("<!-- MID SEM NUMERICAL -->", block + "\n<!-- MID SEM NUMERICAL -->")


def ensure_diagram_placeholders(html: str) -> str:
    """Insert img placeholders only where diagrams are still missing."""
    inserts = [
        (
            '<h4>(b) \\(\\partial J/\\partial\\theta_2 = -12\\)</h4>\n<div class="formula">',
            None,  # already has diagram if formula present
        ),
    ]
    # img-based placeholders for re-inline after rebuild
    img_inserts = [
        (
            '<h4>(b) \\(\\partial J/\\partial\\theta_2 = -12\\)</h4>\n<div class="formula">',
            '<h4>(b) \\(\\partial J/\\partial\\theta_2 = -12\\)</h4>\n'
            '<div class="formula"><h5>Gradient descent</h5>\\(\\theta_j \\leftarrow \\theta_j - \\alpha\\frac{\\partial J}{\\partial\\theta_j}\\)</div>\n'
            '<figure class="diagram"><img src="assets/gd-flow.svg" alt="GD flow"><figcaption>Predict → error → gradient → update</figcaption></figure>\n'
            '<div class="formula">',
            'svg-wrap" role="img" aria-label="GD flow"',
        ),
        (
            '<div class="ans"><strong>Entropy ≈ 0.971 bits</strong></div>\n<h4>Bonus',
            '<div class="ans"><strong>Entropy ≈ 0.971 bits</strong></div>\n'
            '<figure class="diagram"><img src="assets/entropy-ig-tree.svg" alt="IG tree"></figure>\n<h4>Bonus',
            'entropy-ig-tree',
        ),
        (
            '<div class="step">Logistic update: \\(z=w^Tx\\)',
            None,
            'logistic-sigmoid',
        ),
        (
            'Prefer Model B (80% recall) for fraud.</div>\n</div>\n\n<div class="q">\n<h3>Q5',
            'Prefer Model B (80% recall) for fraud.</div>\n'
            '<figure class="diagram"><img src="assets/confusion-matrix.svg" alt="CM"></figure>\n</div>\n\n<div class="q">\n<h3>Q5',
            'confusion-matrix',
        ),
        (
            'High variance</strong> — overfitting</td></tr></table>\n</div>\n</section>\n\n<!-- TYPE 2 -->',
            'High variance</strong> — overfitting</td></tr></table>\n'
            '<figure class="diagram"><img src="assets/bias-variance.svg" alt="BV"></figure>\n</div>\n</section>\n\n<!-- TYPE 2 -->',
            'bias-variance',
        ),
        (
            'Self-play → Reinforcement</div>\n</div>\n</section>\n\n<!-- TYPE 2 -->',
            'Self-play → Reinforcement</div>\n'
            '<figure class="diagram"><img src="assets/mitchell-etp.svg" alt="Mitchell"></figure>\n</div>\n</section>\n\n<!-- TYPE 2 -->',
            'mitchell-etp',
        ),
        (
            'Cost: 4.667 → 3.006 ✓</div>\n</div>\n<div class="q">\n<p class="src">Revision',
            'Cost: 4.667 → 3.006 ✓</div>\n'
            '<figure class="diagram"><img src="assets/gd-flow.svg" alt="GD"></figure>\n</div>\n<div class="q">\n<p class="src">Revision',
            'GD flow"></figcaption>',
        ),
        (
            'prioritize recall</div>\n</div>\n</section>\n\n<!-- TYPE 5 -->',
            'prioritize recall</div>\n'
            '<figure class="diagram"><img src="assets/confusion-matrix.svg" alt="CM"></figure>\n</div>\n</section>\n\n<!-- TYPE 5 -->',
            'confusion-matrix',
        ),
        (
            'high variance</strong></div>\n<div class="ans">Don\'t use higher degree',
            'high variance</strong></div>\n'
            '<figure class="diagram"><img src="assets/bias-variance.svg" alt="BV"></figure>\n<div class="ans">Don\'t use higher degree',
            'bias-variance',
        ),
        (
            'tune λ via CV</p>\n</div>\n</section>\n\n<!-- TYPE 7 -->',
            'tune λ via CV</p>\n'
            '<figure class="diagram"><img src="assets/ridge-lasso.svg" alt="Ridge Lasso"></figure>\n</div>\n</section>\n\n<!-- TYPE 7 -->',
            'ridge-lasso',
        ),
        (
            'compare other features for root</div>\n</div>\n<div class="q">\n<p class="src">4 equal classes',
            'compare other features for root</div>\n'
            '<figure class="diagram"><img src="assets/entropy-ig-tree.svg" alt="IG"></figure>\n</div>\n<div class="q">\n<p class="src">4 equal classes',
            'entropy-ig-tree',
        ),
        (
            'ellipse</div>\n</div>\n</section>\n\n<!-- TYPE 9 -->',
            'ellipse</div>\n'
            '<figure class="diagram"><img src="assets/logistic-sigmoid.svg" alt="Logistic"></figure>\n</div>\n</section>\n\n<!-- TYPE 9 -->',
            'logistic-sigmoid',
        ),
        (
            'FALSE</strong> (unbounded)</div>\n</div>\n</section>\n\n<!-- TYPE 10 -->',
            'FALSE</strong> (unbounded)</div>\n'
            '<figure class="diagram"><img src="assets/min-max-scaling.svg" alt="Scale"></figure>\n</div>\n</section>\n\n<!-- TYPE 10 -->',
            'min-max-scaling',
        ),
        (
            '<p>RR-CHD from Diastolic (x₁) &amp; BMI (x₂). w₀=5, w₁=w₂=−0.03, α=0.02, λ=5</p>\n<table>',
            '<p>RR-CHD from Diastolic (x₁) &amp; BMI (x₂). w₀=5, w₁=w₂=−0.03, α=0.02, λ=5</p>\n'
            '<figure class="diagram"><img src="assets/ridge-lasso.svg" alt="Ridge"><img src="assets/gd-flow.svg" alt="GD" style="margin-top:.5rem"></figure>\n<table>',
            'ridge-lasso',
        ),
    ]
    for old, new, marker in img_inserts:
        if marker and marker in html:
            continue
        if new and old in html:
            html = html.replace(old, new, 1)
    # Q3 min-max + logistic (two diagrams)
    if 'min-max-scaling' not in html.split('Q3 — Min-Max')[1].split('Q4')[0] if 'Q3 — Min-Max' in html else '':
        old = (
            '<div class="step">Logistic update: \\(z=w^Tx\\), \\(\\hat y=\\sigma(z)\\), '
            '\\(\\nabla w_j=\\frac1m\\sum(\\hat y-y)x_j\\), \\(w_j\\leftarrow w_j-\\eta\\nabla w_j\\)</div>\n</div>\n\n<div class="q">\n<h3>Q4'
        )
        new = (
            '<div class="step">Logistic update: \\(z=w^Tx\\), \\(\\hat y=\\sigma(z)\\), '
            '\\(\\nabla w_j=\\frac1m\\sum(\\hat y-y)x_j\\), \\(w_j\\leftarrow w_j-\\eta\\nabla w_j\\)</div>\n'
            '<figure class="diagram"><img src="assets/min-max-scaling.svg" alt="Min-max">'
            '<img src="assets/logistic-sigmoid.svg" alt="Sigmoid" style="margin-top:.5rem"></figure>\n</div>\n\n<div class="q">\n<h3>Q4'
        )
        if old in html:
            html = html.replace(old, new, 1)
    return html


def main() -> None:
    html = WORKBOOK.read_text(encoding="utf-8")
    html = ensure_css(html)
    html = ensure_nav(html)
    html = ensure_type10_11(html)
    html = ensure_diagram_placeholders(html)
    WORKBOOK.write_text(html, encoding="utf-8")
    n = patch_html_file(WORKBOOK)
    remaining = WORKBOOK.read_text(encoding="utf-8").count('src="assets/')
    print(f"Workbook updated — {n} diagrams, {remaining} external asset refs left")


if __name__ == "__main__":
    main()
