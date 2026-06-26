"""Full worked solutions — June 2026 EC2 Regular mid-sem."""
import re

# ── strip helper ──────────────────────────────────────────────────────────────

def strip_solution_tail(inner: str) -> str:
    """Keep h3 + prompt + exam image only; drop old h4 headers and solution body."""
    img = re.search(r'<img class="exam-img"[^>]*>', inner)
    if img:
        return inner[: img.end()]
    m = re.search(r'<div class="(?:step|ans|formula|sol-part)"|<figure class="diagram"|<table\b', inner)
    return inner[: m.start()].rstrip() if m else inner


# ── solutions (h4 tags move to q-stem on wrap) ────────────────────────────────

JUNE_SOLUTIONS = {
    1: """
<h4>(a)(i) Interpret coefficients</h4>
<h4>(a)(ii) kWh → Wh</h4>
<h4>(b) \\(\\partial J/\\partial\\theta_2 = -12\\)</h4>
<h4>(c) Strongest feature?</h4>

<div class="formula"><h5>Model</h5>\\(\\hat y = 120 + 7.5X_1 + 45X_2 - 4X_3 + 18X_4\\)</div>

<div class="sol-part">
<p class="part-head">(a)(i) Interpret each coefficient</p>
<ul class="sol-lines">
<li><strong>Intercept \\(120\\):</strong> base bill of \\(\\$120\\) when all features are zero.</li>
<li><strong>\\(7.5\\) on \\(X_1\\) (kWh):</strong> each extra kWh adds \\(\\$7.50\\) to the bill.</li>
<li><strong>\\(45\\) on \\(X_2\\) (AC units):</strong> each additional AC adds \\(\\$45\\).</li>
<li><strong>\\(-4\\) on \\(X_3\\) (°C):</strong> each 1°C rise <em>reduces</em> the bill by \\(\\$4\\) (ceteris paribus).</li>
<li><strong>\\(18\\) on \\(X_4\\) (family size):</strong> each extra person adds \\(\\$18\\).</li>
</ul>
</div>

<div class="sol-part">
<p class="part-head">(a)(ii) Change \\(X_1\\) from kWh to Wh</p>
<p>Given: \\(1\\) kWh \\(= 1000\\) Wh.</p>
<div class="calc-block">
<p class="calc-line">New coefficient \\(= 7.5 / 1000 = 0.0075\\) per Wh</p>
</div>
<p>If inputs are also multiplied by 1000 when switching units, \\(\\hat y\\) stays the same.</p>
<p>If only the coefficient is rescaled without rescaling \\(X_1\\), predictions become wrong.</p>
</div>

<div class="sol-part">
<p class="part-head">(b) Negative gradient for \\(\\theta_2\\)</p>
<div class="formula"><h5>Update rule</h5>\\(\\theta_j \\leftarrow \\theta_j - \\alpha\\,\\partial J/\\partial\\theta_j\\)</div>
<p>\\(\\partial J/\\partial\\theta_2 = -12 &lt; 0\\) means cost <em>decreases</em> when \\(\\theta_2\\) increases.</p>
<p>GD therefore <strong>increases</strong> the AC weight:</p>
<div class="calc-block">
<p class="calc-line">\\(\\theta_2 \\leftarrow \\theta_2 - \\alpha(-12) = \\theta_2 + 12\\alpha\\)</p>
</div>
</div>

<div class="sol-part">
<p class="part-head">(c) Strongest feature by raw magnitude</p>
<div class="ans">
<p>Largest \\(|\\text{coefficient}|\\) is <strong>AC count (45)</strong>.</p>
<p><strong>Caveat:</strong> features are on different scales (kWh vs °C vs headcount). Raw magnitudes ≠ true importance until features are normalized.</p>
</div>
</div>
""",
    2: """
<h4>(i) Entropy of Loan Approved</h4>
<h4>(ii) IG on Existing Loan</h4>
<h4>(iii) Full decision tree</h4>

<div class="sol-part">
<p class="part-head">Dataset (10 applicants)</p>
<table class="sol-table"><thead><tr><th>ID</th><th>Credit</th><th>Income</th><th>Employment</th><th>Existing Loan</th><th>Approved</th></tr></thead><tbody>
<tr><td>A1</td><td>High</td><td>High</td><td>Salaried</td><td>No</td><td>Yes</td></tr>
<tr><td>A2</td><td>Low</td><td>Low</td><td>Self-employed</td><td>Yes</td><td>No</td></tr>
<tr><td>A3</td><td>Medium</td><td>High</td><td>Salaried</td><td>No</td><td>Yes</td></tr>
<tr><td>A4</td><td>Low</td><td>Medium</td><td>Unemployed</td><td>Yes</td><td>No</td></tr>
<tr><td>A5</td><td>High</td><td>Medium</td><td>Self-employed</td><td>No</td><td>Yes</td></tr>
<tr><td>A6</td><td>Medium</td><td>Low</td><td>Salaried</td><td>Yes</td><td>No</td></tr>
<tr><td>A7</td><td>High</td><td>Low</td><td>Salaried</td><td>No</td><td>Yes</td></tr>
<tr><td>A8</td><td>Medium</td><td>Medium</td><td>Self-employed</td><td>Yes</td><td>No</td></tr>
<tr><td>A9</td><td>Low</td><td>High</td><td>Salaried</td><td>No</td><td>Yes</td></tr>
<tr><td>A10</td><td>Medium</td><td>Medium</td><td>Unemployed</td><td>Yes</td><td>No</td></tr>
</tbody></table>
</div>

<div class="sol-part">
<p class="part-head">(i) Entropy of target</p>
<p>Class counts: \\(5\\) Yes, \\(5\\) No \\(\\Rightarrow p_{Yes} = p_{No} = 0.5\\).</p>
<div class="calc-block">
<p class="calc-line">\\(H(S) = -0.5\\log_2 0.5 - 0.5\\log_2 0.5\\)</p>
<p class="calc-line">\\(= 0.5 + 0.5 = \\mathbf{1.0\\ bit}\\)</p>
</div>
</div>

<div class="sol-part">
<p class="part-head">(ii) Split on Existing Loan</p>
<p><strong>Branch Existing Loan = No</strong> (A1, A3, A5, A7, A9):</p>
<p>\\(5\\) Yes, \\(0\\) No \\(\\Rightarrow H = 0\\)</p>
<p><strong>Branch Existing Loan = Yes</strong> (A2, A4, A6, A8, A10):</p>
<p>\\(0\\) Yes, \\(5\\) No \\(\\Rightarrow H = 0\\)</p>
<div class="calc-block">
<p class="calc-line">\\(H_{after} = \\tfrac{5}{10}(0) + \\tfrac{5}{10}(0) = 0\\)</p>
<p class="calc-line">\\(\\mathrm{IG} = H(S) - H_{after} = 1.0 - 0 = \\mathbf{1.0\\ bit}\\)</p>
</div>
<p>Maximum possible IG — both child nodes are pure.</p>
<p>Comparison: Credit Score IG \\(\\approx 0.40\\), Income IG \\(\\approx 0.60\\), Employment IG \\(\\approx 0.36\\).</p>
</div>

<div class="sol-part">
<p class="part-head">(iii) Complete decision tree</p>
<div class="ans">
<p><strong>Root:</strong> Existing Loan (highest IG)</p>
<ul class="sol-lines">
<li>Existing Loan = <strong>No</strong> \\(\\rightarrow\\) leaf <strong>Yes</strong> (Approve)</li>
<li>Existing Loan = <strong>Yes</strong> \\(\\rightarrow\\) leaf <strong>No</strong> (Deny)</li>
</ul>
<p>One split achieves 100% training accuracy.</p>
</div>
</div>

<div class="sol-part">
<p class="part-head">Unseen attribute values</p>
<p>If test data has categories not seen in training (e.g. Employment = Contract):</p>
<ul class="sol-lines">
<li>No learned branch exists for that value.</li>
<li>Use a fallback: majority class at parent, surrogate split, or manual review.</li>
</ul>
</div>
""",
    3: """
<h4>(a) Min-max normalization</h4>
<h4>(b)(i) Sigmoid predictions</h4>
<h4>(b)(ii) Binary cross-entropy</h4>
<h4>(b)(iii) One GD step</h4>
<h4>(c) Regularization</h4>

<div class="sol-part">
<p class="part-head">(a) Min-max normalize Credit Score</p>
<p>From training data: \\(x_{min} = 590\\), \\(x_{max} = 710\\), range \\(= 120\\).</p>
<p>Formula: \\(x' = (x - x_{min}) / (x_{max} - x_{min})\\)</p>
<table class="sol-table"><thead><tr><th>Sample</th><th>Raw score</th><th>Calculation</th><th>\\(x_1\\)</th></tr></thead><tbody>
<tr><td>S1</td><td>620</td><td>\\((620-590)/120\\)</td><td><strong>0.25</strong></td></tr>
<tr><td>S2</td><td>680</td><td>\\((680-590)/120\\)</td><td><strong>0.75</strong></td></tr>
<tr><td>S3</td><td>590</td><td>\\((590-590)/120\\)</td><td><strong>0.00</strong></td></tr>
<tr><td>S4</td><td>710</td><td>\\((710-590)/120\\)</td><td><strong>1.00</strong></td></tr>
<tr><td>New</td><td>650</td><td>\\((650-590)/120\\)</td><td><strong>0.50</strong></td></tr>
</tbody></table>
</div>

<div class="sol-part">
<p class="part-head">(b)(i) Predicted probabilities</p>
<p>\\(z = w_0 + w_1 x_1 + w_2 x_2\\), &nbsp; \\(\\hat p = \\sigma(z) = 1/(1+e^{-z})\\)</p>
<p>Initial weights: \\(w_0=0\\), \\(w_1=0.5\\), \\(w_2=-0.5\\). Debt ratio used as raw \\(x_2\\).</p>
<table class="sol-table"><thead><tr><th>Sample</th><th>\\(x_1\\)</th><th>\\(x_2\\)</th><th>\\(z\\)</th><th>\\(\\hat p\\)</th><th>\\(y\\)</th></tr></thead><tbody>
<tr><td>S1</td><td>0.25</td><td>0.80</td><td>\\(-0.275\\)</td><td><strong>0.432</strong></td><td>1</td></tr>
<tr><td>S2</td><td>0.75</td><td>0.40</td><td>\\(0.175\\)</td><td><strong>0.544</strong></td><td>0</td></tr>
<tr><td>S3</td><td>0.00</td><td>0.90</td><td>\\(-0.450\\)</td><td><strong>0.389</strong></td><td>1</td></tr>
<tr><td>S4</td><td>1.00</td><td>0.30</td><td>\\(0.350\\)</td><td><strong>0.587</strong></td><td>0</td></tr>
</tbody></table>
</div>

<div class="sol-part">
<p class="part-head">(b)(ii) Binary cross-entropy loss</p>
<div class="formula"><h5>Loss</h5>\\(L = -\\tfrac{1}{m}\\sum_i \\big[y_i\\ln\\hat p_i + (1-y_i)\\ln(1-\\hat p_i)\\big]\\), &nbsp; \\(m=4\\)</div>
<table class="sol-table"><thead><tr><th>Sample</th><th>Term</th><th>Value</th></tr></thead><tbody>
<tr><td>S1</td><td>\\(-\\ln(0.432)\\)</td><td>0.839</td></tr>
<tr><td>S2</td><td>\\(-\\ln(1-0.544)\\)</td><td>0.785</td></tr>
<tr><td>S3</td><td>\\(-\\ln(0.389)\\)</td><td>0.944</td></tr>
<tr><td>S4</td><td>\\(-\\ln(1-0.587)\\)</td><td>0.886</td></tr>
</tbody></table>
<div class="calc-block">
<p class="calc-line">\\(L = (0.839 + 0.785 + 0.944 + 0.886) / 4 = \\mathbf{0.864}\\)</p>
</div>
</div>

<div class="sol-part">
<p class="part-head">(b)(iii) One gradient-descent step</p>
<p>\\(\\partial L/\\partial w_j = \\tfrac{1}{m}\\sum_i (\\hat p_i - y_i)\\,x_{j,i}\\)</p>
<table class="sol-table"><thead><tr><th>Weight</th><th>Gradient</th><th>Update (\\(\\eta=0.5\\))</th><th>New value</th></tr></thead><tbody>
<tr><td>\\(w_0\\)</td><td>\\(-0.0121\\)</td><td>\\(0 - 0.5(-0.0121)\\)</td><td><strong>0.006</strong></td></tr>
<tr><td>\\(w_1\\)</td><td>\\(0.2131\\)</td><td>\\(0.5 - 0.5(0.2131)\\)</td><td><strong>0.393</strong></td></tr>
<tr><td>\\(w_2\\)</td><td>\\(-0.1527\\)</td><td>\\(-0.5 - 0.5(-0.1527)\\)</td><td><strong>−0.424</strong></td></tr>
</tbody></table>
</div>

<div class="sol-part">
<p class="part-head">(c) Regularization</p>
<div class="ans">
<p><strong>(c)(i)</strong> Use <strong>L1 (Lasso)</strong> to drive weights to exactly zero.</p>
<p>L1 penalty \\(|w|\\) has corners at 0; L2 (Ridge) shrinks but rarely zeros weights.</p>
</div>
<div class="ans">
<p><strong>(c)(ii)</strong> As \\(\\lambda \\to \\infty\\): \\(w_1^*, w_2^* \\to 0\\).</p>
<p>Predictions collapse toward \\(\\sigma(w_0) \\approx 0.5\\) — high bias / underfitting.</p>
<p>\\(\\lambda\\) too large → poor generalization on new loan applicants.</p>
</div>
</div>
""",
    4: """
<h4>(a)(i) Accuracy &amp; error rate</h4>
<h4>(a)(ii) Precision, recall, FPR, F1</h4>
<h4>(a)(iii) Is high accuracy enough?</h4>
<h4>(b)(i) ROC points</h4>
<h4>(b)(ii) Model choice</h4>
<h4>(b)(iii) Diagonal ROC</h4>

<div class="sol-part">
<p class="part-head">Setup</p>
<p>10,000 transactions: 100 fraud (positive), 9,900 legit (negative).</p>
<table class="sol-table"><thead><tr><th>Model</th><th></th><th>Pred Fraud</th><th>Pred Legit</th></tr></thead><tbody>
<tr><td rowspan="2"><strong>A</strong></td><td>Actual Fraud</td><td>45 (TP)</td><td>55 (FN)</td></tr>
<tr><td>Actual Legit</td><td>90 (FP)</td><td>9810 (TN)</td></tr>
<tr><td rowspan="2"><strong>B</strong></td><td>Actual Fraud</td><td>80 (TP)</td><td>20 (FN)</td></tr>
<tr><td>Actual Legit</td><td>500 (FP)</td><td>9400 (TN)</td></tr>
</tbody></table>
</div>

<div class="sol-part">
<p class="part-head">(a)(i) Model A — accuracy &amp; error rate</p>
<div class="calc-block">
<p class="calc-line">Accuracy \\(= (TP + TN) / N = (45 + 9810) / 10000\\)</p>
<p class="calc-line">\\(= \\mathbf{98.55\\%}\\)</p>
<p class="calc-line">Error rate \\(= 100\\% - 98.55\\% = \\mathbf{1.45\\%}\\)</p>
</div>
</div>

<div class="sol-part">
<p class="part-head">(a)(ii) Model A — precision, recall, FPR, F1</p>
<table class="sol-table"><thead><tr><th>Metric</th><th>Formula</th><th>Result</th></tr></thead><tbody>
<tr><td>Precision</td><td>\\(TP/(TP+FP) = 45/135\\)</td><td><strong>33.33%</strong></td></tr>
<tr><td>Recall (TPR)</td><td>\\(TP/(TP+FN) = 45/100\\)</td><td><strong>45%</strong></td></tr>
<tr><td>FPR</td><td>\\(FP/(FP+TN) = 90/9900\\)</td><td><strong>0.91%</strong></td></tr>
<tr><td>F1</td><td>\\(2PR/(P+R)\\)</td><td><strong>38.3%</strong></td></tr>
</tbody></table>
</div>

<div class="sol-part">
<p class="part-head">(a)(iii) Is Model A excellent?</p>
<div class="ans">
<p><strong>No.</strong> With only 1% fraud, a dummy “always legit” classifier gets ~99% accuracy but catches zero fraud.</p>
<p>Model A detects only 45 of 100 fraud cases (55 missed).</p>
</div>
</div>

<div class="sol-part">
<p class="part-head">Model B summary</p>
<table class="sol-table"><thead><tr><th>Metric</th><th>Result</th></tr></thead><tbody>
<tr><td>Accuracy</td><td>94.80%</td></tr>
<tr><td>Recall (TPR)</td><td><strong>80%</strong></td></tr>
<tr><td>FPR</td><td>5.05%</td></tr>
<tr><td>Precision</td><td>13.79%</td></tr>
<tr><td>F1</td><td>23.5%</td></tr>
</tbody></table>
</div>

<div class="sol-part">
<p class="part-head">(b)(i) ROC curve points</p>
<p>Plot \\((\\text{FPR}, \\text{TPR})\\):</p>
<ul class="sol-lines">
<li><strong>Model A:</strong> \\((0.0091,\\; 0.45)\\)</li>
<li><strong>Model B:</strong> \\((0.0505,\\; 0.80)\\) — higher recall, more false alarms</li>
</ul>
</div>

<div class="sol-part">
<p class="part-head">(b)(ii) Which model for fraud detection?</p>
<div class="ans">
<p>Recommend <strong>Model B</strong>.</p>
<p>Missing fraud (FN) is costlier than flagging legit transactions (FP).</p>
<p>B catches 80% of fraud vs 45% for A, despite lower accuracy.</p>
</div>
</div>

<div class="sol-part">
<p class="part-head">(b)(iii) Point on diagonal</p>
<div class="ans">
<p>Diagonal \\(\\Rightarrow\\) TPR = FPR (random guessing).</p>
<p>AUC \\(= 0.5\\) — no discriminative power.</p>
</div>
</div>
""",
    5: """
<h4>(a) Bias–variance diagnosis</h4>
<h4>(b) Regularization strategies</h4>
<h4>(c) Improved balanced model</h4>

<div class="sol-part">
<p class="part-head">(a) Model A — high bias</p>
<p>Train 61%, test 60% — small gap but both low.</p>
<p><strong>Diagnosis:</strong> high bias / underfitting (too simple).</p>
<p><strong>Learning curve:</strong> train &amp; CV plateau together at ~61%.</p>
<p><strong>More data?</strong> Unlikely to help — model capacity is the bottleneck.</p>
</div>

<div class="sol-part">
<p class="part-head">(a) Model B — high variance</p>
<p>Train 99%, test 67% — large gap.</p>
<p><strong>Diagnosis:</strong> high variance / overfitting.</p>
<p><strong>Learning curve:</strong> train stays ~99%; CV only reaches ~70% at full data.</p>
<p><strong>More data?</strong> Helps CV slowly, but 47 features + interactions need regularization or feature reduction.</p>
</div>

<div class="sol-part">
<p class="part-head">(b) Regularization strategies</p>
<p><strong>For Model B (high variance):</strong></p>
<ul class="sol-lines">
<li>L2 Ridge or L1 Lasso — penalize large / irrelevant weights</li>
<li>Drop interaction terms; reduce feature count</li>
<li>Cross-validate \\(\\lambda\\); early stopping</li>
</ul>
<p><strong>For Model A (high bias):</strong></p>
<ul class="sol-lines">
<li>Add informative features (word frequencies, sender reputation)</li>
<li>Selective interaction terms</li>
<li>Reduce regularization if currently over-penalized</li>
</ul>
</div>

<div class="sol-part">
<p class="part-head">(c) Improved balanced model</p>
<div class="ans">
<p>Logistic regression with a <strong>moderate</strong> feature set (10–15 curated features + selective interactions).</p>
<p>Add <strong>L2 regularization</strong> tuned by cross-validation.</p>
<p>Enough capacity to beat 61% test (lower bias), but penalty + fewer parameters control variance.</p>
<p>Target: train/test gap \\(&lt;\\) 10%, test accuracy above both A and B.</p>
</div>
</div>
""",
}
