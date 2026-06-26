"""Q / answer layout helpers for ML_PYQ_Workbook.html."""
import re

from june_solutions import JUNE_SOLUTIONS, strip_solution_tail

TOGGLE_CSS = """
.q-stem{padding:.2rem 0 .85rem}
.q-stem h3{color:var(--navy);font-size:1rem;margin:0 0 .45rem}
.q-stem h4{color:var(--blue);font-size:.92rem;margin:.55rem 0 .25rem}
.q-prompt{font-size:.91rem;line-height:1.65;margin:.55rem 0;padding:.8rem 1rem;background:#f8fafc;border-radius:8px;border:1px solid var(--border)}
.q-prompt p{margin:.35rem 0}
.q-prompt ol,.q-prompt ul{margin:.4rem 0 .25rem 1.25rem}
.q-prompt li{margin:.2rem 0}
.q-stem .exam-img{margin:.6rem 0}
details.sol-toggle{margin-top:.5rem;border:1px solid #bbf7d0;border-radius:8px;background:#fff;overflow:hidden}
details.sol-toggle summary{cursor:pointer;padding:.7rem 1rem;font-weight:600;font-size:.88rem;color:#047857;background:#ecfdf5;list-style:none;display:flex;align-items:center;gap:.45rem;user-select:none}
details.sol-toggle summary::-webkit-details-marker{display:none}
details.sol-toggle summary::before{content:"▸";font-size:.72rem;color:var(--green);transition:transform .15s}
details.sol-toggle[open] summary::before{transform:rotate(90deg)}
details.sol-toggle[open] summary{border-bottom:1px solid #bbf7d0}
.sol-body{padding:1rem 1.15rem 1.2rem;line-height:1.75}
.sol-body h4{color:var(--purple);font-size:.9rem;margin:.65rem 0 .3rem}
.sol-body p{margin:.45rem 0}
.sol-body .sol-part{margin:1.1rem 0;padding:.85rem 0 .5rem;border-bottom:1px dashed var(--border)}
.sol-body .sol-part:last-child{border-bottom:none;margin-bottom:0}
.sol-body .part-head{font-weight:700;color:var(--navy);font-size:.92rem;margin:0 0 .55rem}
.sol-body .sol-lines{margin:.35rem 0 .5rem 1.35rem}
.sol-body .sol-lines li{margin:.35rem 0}
.sol-body .calc-block{background:#f8fafc;border-left:3px solid var(--blue);padding:.55rem .85rem;margin:.55rem 0;border-radius:0 6px 6px 0}
.sol-body .calc-line{margin:.25rem 0;font-family:Georgia,serif}
.sol-body .sol-table{margin:.65rem 0}
.sol-body .step,.sol-body .ans,.sol-body .formula,.sol-body .diagram{margin-top:.55rem}
.sol-body .ans p{margin:.35rem 0}
.sol-body .ans p:first-child{margin-top:0}
.sol-body .ans p:last-child{margin-bottom:0}
.toolbar{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;margin-top:.45rem}
.toolbar button{background:#fff;border:1px solid var(--border);padding:.35rem .85rem;border-radius:6px;cursor:pointer;color:var(--navy);font-size:.8rem}
.toolbar button:hover{background:#eff6ff}
"""

TOGGLE_JS = """
<script>
function toggleAllSolutions(open) {
  document.querySelectorAll('details.sol-toggle').forEach(d => { d.open = open; });
}
</script>
"""

# Insert before first solution block if stem lacks a q-prompt
QUESTION_PROMPTS = {
    "type1": """<div class="q-prompt"><p><strong>Question.</strong> For each scenario, name the learning paradigm (supervised / unsupervised / reinforcement) and task type (classification / regression / clustering).</p>
<ol><li>Self-driving car learns from reward signals after each trip.</li>
<li>Classify product reviews as positive/negative using labelled data.</li>
<li>Group DNA sequences by similarity with no labels.</li>
<li>Predict insurance claim amount from policy features.</li></ol>
<p>Also: (i) For weather prediction, identify Mitchell's <em>E, T, P</em>. Is predicting rainfall amount regression or classification? (ii) AlphaGo — was the first version supervised or reinforcement?</p></div>""",
    "type2": """<div class="q-prompt"><p><strong>Question.</strong> Inspect each messy dataset table below (Student records and B.Tech admissions). List at least 5–6 <em>data quality issues</em> per dataset (missing values, outliers, duplicates, inconsistent formats, invalid types, etc.) and state how you would fix each <em>without writing code</em>.</p></div>""",
    "type3-gd": """<div class="q-prompt"><p><strong>Question.</strong> Perform <strong>one iteration</strong> of batch gradient descent with Ridge penalty on linear regression.</p>
<p>Given: \(x=[1,2,3]\), \(y=[2,5,7]\), \(\\theta_0=0\), \(\\theta_1=1\), \(\\alpha=0.05\), \(\\lambda=2\), \(m=3\). Compute \(h(x)\), errors, \(\\partial J/\\partial\\theta_0\), \(\\partial J/\\partial\\theta_1\) (include Ridge term on \(\\theta_1\)), updated weights, and verify cost decreases.</p></div>""",
    "type3-rev": """<div class="q-prompt"><p><strong>Question.</strong> For \(x=[2,4,7,8,10]\), \(y=[1,2,2.5,3.5,5.5]\), bias included, \(\\theta_1=0.5\), find \(\\partial J/\\partial\\theta_1\) for one GD step (MSE, no regularization).</p></div>""",
    "type4": """<div class="q-prompt"><p><strong>Question.</strong> A medical diagnostic system is tested on 1,000 patients (150 have the disease). Given TP and FP counts from the confusion matrix, compute accuracy, precision, recall, and F1. Then estimate total cost if each FN costs $10,000 and each FP costs $500 — which metric should drive model selection?</p></div>""",
    "type5-poly": """<div class="q-prompt"><p><strong>Question.</strong> Two polynomial models: A (degree 2) and B (degree 15). Training error is similar but test error differs greatly. Diagnose bias vs variance and recommend what to do instead of raising degree.</p></div>""",
    "type5-rmse": """<div class="q-prompt"><p><strong>Question.</strong> Four models report train vs test RMSE. Rank them, identify overfitting/underfitting, and explain using \(R^2 = 1 - SS_{res}/SS_{tot}\).</p></div>""",
    "type5-data": """<div class="q-prompt"><p><strong>Question.</strong> A student doubled the dataset but validation RMSE stayed high while training RMSE also stayed high. Explain what this indicates and what fixes would help.</p></div>""",
    "type6": """<div class="q-prompt"><p><strong>Question.</strong> (a) High-dimensional data with many irrelevant features — choose Ridge vs Lasso and justify. (b) Logistic regression overfits with very large weights — how does L1/L2 regularization help?</p></div>""",
    "type7-dec": """<div class="q-prompt"><p><strong>Question.</strong> Given 14 customers (9 Repaid, 5 Default) and Income split High/Low, compute parent entropy \(H(S)\), branch entropies, weighted average, and information gain for Income. Should Income be the root split?</p></div>""",
    "type7-bits": """<div class="q-prompt"><p><strong>Question.</strong> (a) What is the entropy of a set with 4 equally likely classes? (b) A leaf has 3 Yes and 1 No — what class label does the tree assign?</p></div>""",
    "type8": """<div class="q-prompt"><p><strong>Question.</strong> Logistic regression interpretation: (a) Does a large positive CGPA coefficient guarantee admission? (b) If experience was recorded in months but model trained on years, how do you rescale the coefficient? (c) Given weights on \([1, x_1, x_2, x_1^2, x_2^2]\), write the decision boundary equation.</p></div>""",
    "type9": """<div class="q-prompt"><p><strong>Question.</strong> True or false with one-line justification each:</p>
<ol><li>Feature scaling is needed for gradient descent convergence speed.</li>
<li>Decision trees require feature scaling before training.</li>
<li>Min-max normalization is sensitive to outliers.</li>
<li>Z-score scaling always maps values into [0, 1].</li></ol></div>""",
    "type10": """<div class="q-prompt"><p><strong>Question.</strong> Three models (Linear Regression, Decision Tree, Random Forest) are trained on Dataset A (noisy labels) and Dataset B (outliers in features). For each model × dataset, state whether performance is <strong>Affected</strong> or <strong>Less Affected</strong> and justify in 1–2 sentences.</p></div>""",
    "type11": """<div class="q-prompt"><p><strong>Question.</strong> \(m=28\) training examples, \(n=4\) features (excluding bias). Using \(\\boldsymbol{\\theta}=(X^TX)^{-1}X^Ty\) with bias column \(x_0=1\), state the matrix dimensions of \(X\), \(\\mathbf{y}\), and \(\\boldsymbol{\\theta}\). Show \(X^TX\) size and final product shape.</p></div>""",
}

JUNE_PROMPTS = {
    1: """<div class="q-prompt"><p><strong>Question [5M].</strong> Monthly bill model: \(\hat y = 120 + 7.5X_1 + 45X_2 - 4X_3 + 18X_4\) where \(X_1\)=kWh, \(X_2\)=AC units, \(X_3\)=temperature (°C), \(X_4\)=family size.</p>
<ol><li>(a)(i) Interpret each coefficient in dollars. (ii) If \(X_1\) is re-recorded in Wh instead of kWh (1 kWh = 1000 Wh), what happens to the coefficient of \(X_1\)? Will the predicted bill change?</li>
<li>(b) Gradients observed: \(\partial J/\partial\\theta_0=18\), \(\partial J/\partial\\theta_1=0.02\), \(\partial J/\partial\\theta_2=-12\), \(\partial J/\partial\\theta_3=0.001\). What does the <strong>negative</strong> gradient for \(\\theta_2\) indicate?</li>
<li>(c) Which feature has the strongest influence based on coefficient magnitudes alone? Why treat this conclusion carefully?</li></ol></div>""",
    2: """<div class="q-prompt"><p><strong>Question [6M].</strong> Decision tree for loan approval — 10 applicants (A1–A10). Target: Loan Approved (Yes/No).</p>
<ol><li>(i) Calculate entropy of Loan Approved. [2M]</li>
<li>(ii) Compute entropy and Information Gain for split on <em>Existing Loan</em>. [2M]</li>
<li>(iii) Build the full tree (root = max IG attribute). [2M]</li></ol>
<p><em>Dataset: 5 Yes / 5 No overall. Features: Credit Score, Income Level, Employment Type, Existing Loan.</em></p></div>""",
    3: """<div class="q-prompt"><p><strong>Question [8M].</strong> Loan default prediction (1=default, 0=not) from Credit Score and Debt-to-Income Ratio.</p>
<table><tr><th>Sample</th><th>Credit Score</th><th>Debt-to-Income</th><th>y</th></tr>
<tr><td>S1</td><td>620</td><td>0.80</td><td>1</td></tr>
<tr><td>S2</td><td>680</td><td>0.40</td><td>0</td></tr>
<tr><td>S3</td><td>590</td><td>0.90</td><td>1</td></tr>
<tr><td>S4</td><td>710</td><td>0.30</td><td>0</td></tr></table>
<p>\(w_0=0, w_1=0.5, w_2=-0.5, \eta=0.5\)</p>
<ol><li>(a) Min-max normalize Credit Score (\(x'=(x-x_{min})/(x_{max}-x_{min})\)): (i) all 4 samples, (ii) new applicant score 650.</li>
<li>(b) Using normalized credit score as \(x_1\) and raw debt ratio as \(x_2\): (i) compute \(\hat p=\sigma(w_0+w_1 x_1+w_2 x_2)\) for each sample, (ii) binary cross-entropy loss, (iii) one GD step for updated weights.</li>
<li>(c) Overfitting — L1 vs L2 to drive some weights to exactly zero? Effect of large \(\lambda\)?</li></ol></div>""",
    4: """<div class="q-prompt"><p><strong>Question [6M].</strong> Fraud detection on 10,000 transactions (100 fraud, 9,900 legit). Confusion matrices:</p>
<table><tr><th></th><th>Pred Fraud</th><th>Pred Legit</th></tr>
<tr><td><strong>Model A — Actual Fraud</strong></td><td>45 (TP)</td><td>55 (FN)</td></tr>
<tr><td><strong>Model A — Actual Legit</strong></td><td>90 (FP)</td><td>9810 (TN)</td></tr>
<tr><td><strong>Model B — Actual Fraud</strong></td><td>80 (TP)</td><td>20 (FN)</td></tr>
<tr><td><strong>Model B — Actual Legit</strong></td><td>500 (FP)</td><td>9400 (TN)</td></tr></table>
<ol><li>(a)(i) Model A: accuracy and error rate. (ii) Precision, recall (TPR), FPR, F1. (iii) Colleague says Model A is excellent from accuracy alone — agree?</li>
<li>(b)(i) TPR and FPR for both models — ROC points. (ii) Which model for fraud? (FN vs FP trade-off.) (iii) What if ROC point lies on diagonal? AUC?</li></ol></div>""",
    5: """<div class="q-prompt"><p><strong>Question [3M].</strong> Spam classifier (y=1 spam, y=0 legit). 70/30 train-test split.</p>
<table><tr><th>Model</th><th>Description</th><th>Train acc</th><th>Test acc</th></tr>
<tr><td>A</td><td>Logistic — email length + punctuation only (2 features)</td><td>61%</td><td>60%</td></tr>
<tr><td>B</td><td>Logistic — all features + interactions (47 total)</td><td>99%</td><td>67%</td></tr></table>
<p>Learning curves: A — train &amp; CV both plateau ~61%. B — train ~99%, CV rises slowly to ~70% only at full data.</p>
<ol><li>(a) Bias/variance diagnosis + learning-curve interpretation; would more data help each?</li>
<li>(b) Regularization strategies to address each model's failure.</li>
<li>(c) One improved model balancing bias and variance.</li></ol></div>""",
}

MOCK_PROMPTS = {
    1: """<div class="q-prompt"><p><strong>Mock Q1.</strong> Hospital wants to predict 30-day readmission. Identify Mitchell E/T/P, classify task type, explain overfitting harm, and suggest regularization fixes.</p></div>""",
    2: """<div class="q-prompt"><p><strong>Mock Q2.</strong> List data quality issues in a hospital patient table (duplicates, missing fields, invalid ages, mixed date formats, categorical in numeric columns, outliers).</p></div>""",
    3: """<div class="q-prompt"><p><strong>Mock Q3.</strong> One GD iteration: \(x=[2,4,6]\), \(y=[3,7,11]\), \(\\theta_0=\\theta_1=0.5\), \(\\alpha=0.1\), Ridge \(\\lambda=1\), \(m=3\). Find gradients and updated \(\\theta\).</p></div>""",
    4: """<div class="q-prompt"><p><strong>Mock Q4.</strong> Spam filter: 400 spam, 1600 ham; TP=350, FP=100. Compute precision, recall, F1. FN cost $50 vs FP cost $5 — discuss threshold choice.</p></div>""",
    5: """<div class="q-prompt"><p><strong>Mock Q5.</strong> Two models' train vs test RMSE — which to deploy and why?</p></div>""",
    6: """<div class="q-prompt"><p><strong>Mock Q6.</strong> Fruit basket: 6 Apples, 4 Oranges. Split on Color: Red branch 5A/1O, Green branch 1A/3O. Compute \(H(S)\), weighted child entropy, and IG. Is Color a good split?</p></div>""",
}

SOLUTION_START = re.compile(
    r'<div class="(?:step|ans|formula)"|<figure class="diagram"'
    r'|<table\b',
    re.I,
)


def split_stem_solution(inner: str) -> tuple[str, str]:
    if "sol-toggle" in inner:
        return inner, ""

    stem_end = 0
    m = re.search(r'<div class="q-prompt">.*?</div>', inner, re.S)
    if m:
        stem_end = m.end()
        img = re.match(r'\s*<img class="exam-img"[^>]*>', inner[stem_end:], re.S)
        if img:
            stem_end += img.end()
    else:
        src = re.search(r'<p class="src">.*?</p>', inner, re.S)
        if src:
            stem_end = src.end()
        elif "<h3>" in inner:
            stem_end = inner.find("</h3>") + 5
        else:
            m = SOLUTION_START.search(inner)
            if not m:
                return inner.strip(), ""
            return inner[: m.start()].rstrip(), inner[m.start() :].lstrip()

    stem = inner[:stem_end].rstrip()
    sol = inner[stem_end:].lstrip()
    if not sol:
        return inner.strip(), ""

    h4_parts = re.findall(r"<h4>[^<]*</h4>", sol)
    if h4_parts:
        sol = re.sub(r"<h4>[^<]*</h4>\s*", "", sol)
        stem = stem.rstrip() + "\n" + "\n".join(h4_parts)

    return stem, sol


def wrap_q_block(inner: str) -> str:
    stem, sol = split_stem_solution(inner)
    if not sol.strip():
        return f'<div class="q"><div class="q-stem">{stem}</div></div>'
    return (
        f'<div class="q">\n<div class="q-stem">{stem}</div>\n'
        f'<details class="sol-toggle">\n'
        f'<summary>Show detailed solution</summary>\n'
        f'<div class="sol-body">{sol}</div>\n</details>\n</div>'
    )


def extract_q_blocks(html: str) -> list[tuple[int, int, str]]:
    """Return (start, end, inner_html) for each top-level div.q."""
    blocks = []
    marker = '<div class="q">'
    i = 0
    while True:
        start = html.find(marker, i)
        if start == -1:
            break
        pos = start + len(marker)
        depth = 1
        while depth > 0 and pos < len(html):
            o = html.find("<div", pos)
            c = html.find("</div>", pos)
            if c == -1:
                break
            if o != -1 and o < c:
                depth += 1
                pos = o + 4
            else:
                depth -= 1
                pos = c + 6
        inner = html[start + len(marker) : pos - len("</div>")]
        blocks.append((start, pos, inner))
        i = pos
    return blocks


def inject_prompt(stem: str, prompt: str) -> str:
    if not prompt:
        return stem
    stem = re.sub(r'<div class="q-prompt">.*?</div>\s*', "", stem, count=1, flags=re.S)
    m = re.search(r'<p class="src">.*?</p>', stem, re.S)
    if m:
        idx = m.end()
        return stem[:idx] + "\n" + prompt + stem[idx:]
    if "<h3>" in stem:
        idx = stem.find("</h3>") + 5
        return stem[:idx] + "\n" + prompt + stem[idx:]
    if "<h4>" in stem:
        idx = stem.find("<h4>")
        return stem[:idx] + prompt + "\n" + stem[idx:]
    return prompt + "\n" + stem


def apply_prompts(html: str) -> str:
    blocks = extract_q_blocks(html)
    if not blocks:
        return html

    out = []
    last = 0
    type3_n = 0
    mock_n = 0
    june_n = 0

    for start, end, inner in blocks:
        prefix = html[:start]
        sec_m = list(re.finditer(r'<section id="([^"]+)"', prefix))
        section = sec_m[-1].group(1) if sec_m else ""

        if "sol-toggle" in inner:
            out.append(html[last:start] + f'<div class="q">{inner}</div>')
            last = end
            continue

        if section == "june2026":
            june_n += 1
            inner = inject_prompt(inner, JUNE_PROMPTS.get(june_n, ""))
            inner = strip_solution_tail(inner) + JUNE_SOLUTIONS.get(june_n, "")
        elif section == "mock":
            mock_n += 1
            inner = inject_prompt(inner, MOCK_PROMPTS.get(mock_n, ""))
        elif section == "type1":
            inner = inject_prompt(inner, QUESTION_PROMPTS["type1"])
        elif section == "type2":
            inner = inject_prompt(inner, QUESTION_PROMPTS["type2"])
        elif section == "type3":
            type3_n += 1
            key = "type3-gd" if type3_n == 1 else "type3-rev"
            inner = inject_prompt(inner, QUESTION_PROMPTS[key])
        elif section == "type4":
            inner = inject_prompt(inner, QUESTION_PROMPTS["type4"])
        elif section == "type5":
            if "Doubled" in inner or "doubled" in inner:
                inner = inject_prompt(inner, QUESTION_PROMPTS["type5-data"])
            elif "deg" in inner.lower() or "Polynomial" in inner:
                inner = inject_prompt(inner, QUESTION_PROMPTS["type5-poly"])
            else:
                inner = inject_prompt(inner, QUESTION_PROMPTS["type5-rmse"])
        elif section == "type6":
            inner = inject_prompt(inner, QUESTION_PROMPTS["type6"])
        elif section == "type7":
            key = "type7-dec" if "14 samples" in inner or "Dec 2025" in inner else "type7-bits"
            inner = inject_prompt(inner, QUESTION_PROMPTS[key])
        elif section == "type8":
            inner = inject_prompt(inner, QUESTION_PROMPTS["type8"])
        elif section == "type9":
            inner = inject_prompt(inner, QUESTION_PROMPTS["type9"])
        elif section == "type10":
            inner = inject_prompt(inner, QUESTION_PROMPTS["type10"])
        elif section == "type11":
            inner = inject_prompt(inner, QUESTION_PROMPTS["type11"])

        out.append(html[last:start] + wrap_q_block(inner))
        last = end

    out.append(html[last:])
    return "".join(out)
