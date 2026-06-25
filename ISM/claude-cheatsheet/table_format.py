"""Convert PDF-extracted vertical cell lists into HTML tables; fix PDF line-wrap artifacts."""
import html as H
import re
from typing import Iterable, List, Optional

from solution_format import strip_br_suffix

TABLE_CSS = """
.data-table{border-collapse:collapse;width:100%;margin:.75rem 0;font-size:.82rem;background:#fff}
.data-table th,.data-table td{border:1px solid var(--border);padding:.35rem .5rem;text-align:left;vertical-align:top}
.data-table thead th{background:#eff6ff;font-weight:600;color:var(--navy)}
.data-table tbody tr:nth-child(even){background:#f8fafc}
.data-table .hi{background:#fef2f2;font-weight:600}
.data-table .miss{color:var(--muted);font-style:italic}
.cm-table td,.cm-table th{text-align:center}
"""

TXN_ROWS = [
    ("T001", "RAMA", "45", "145", "62kg", "O+ve", "Positive"),
    ("T002", "SEETHA", "43", "168", "45kg", "B+ve", "Negative"),
    ("T003", "Akbar", "38", "172", "60kg", "Iam+ve", "Positive"),
    ("T004", "BIRBAL", "45", "168", "52kg", "AB+ve", "Negative"),
    ("T005", "THenali", "22", "157", "78kg", "B-ve", "1"),
    ("T006", "Venkat", "36", "157", "54kg", "O-ve", "Negative"),
    ("T007", "Rajuu", "350", "132", "48kg", "O+ve", "Positive"),
    ("T008", "HARI", "32", "180", "120lbs", "AB-ve", "Negative"),
    ("T009", "Inba", "25", "", "85kg", "O+ve", "0"),
    ("T010", "SysUsr789", "20", "165", "68kg", "O-ve", "Negative"),
]

TXN_HIGHLIGHT = {
    ("T003", "BLOOD GROUP"),
    ("T005", "COVID-19 RESULT"),
    ("T007", "AGE"),
    ("T008", "WEIGHT"),
    ("T009", "HEIGHT"),
    ("T010", "NAME"),
}

STUDENT_HEADERS = ["Student Name", "Age", "Email", "Specialization", "Admission Date", "CGPA"]
STUDENT_ROWS = [
    ("Rina", "22", "rina@example.com", "AI", "15-Aug-2022", "8.2"),
    ("Dev", "23", "dev[at]mail.com", "Cybersecurity", "2022-08-15", "7.8"),
    ("Aarav", "22", "aarav@example.com", "Data Science", "15/08/2022", "9.1"),
    ("Shweta", "22", "", "Cybersecurity", "15-Aug-2022", "6.4"),
    ("Rina", "22", "rina@example.com", "Artificial Intelligence", "15-Aug-2022", "8.2"),
    ("Mansi", "58", "mansi123@gmail.com", "Data Science", "15-Aug-2022", "7.0"),
]

STUDENT_HIGHLIGHT = {
    (1, "Email"),
    (2, "Admission Date"),
    (3, "Email"),
    (4, "Student Name"),
    (5, "Age"),
}


def _table_html(
    headers: List[str],
    rows: Iterable[tuple],
    highlights: Optional[set] = None,
    col_highlight: Optional[dict] = None,
) -> str:
    highlights = highlights or set()
    col_highlight = col_highlight or {}
    out = ['<table class="data-table"><thead><tr>']
    for h in headers:
        out.append(f"<th>{H.escape(h)}</th>")
    out.append("</tr></thead><tbody>")
    for ri, row in enumerate(rows):
        out.append("<tr>")
        for ci, val in enumerate(row):
            label = headers[ci] if ci < len(headers) else ""
            cls = []
            if (row[0], label) in highlights or (ri, label) in highlights:
                cls.append("hi")
            if val in ("", "—", None):
                cls.append("miss")
                val = "—"
            attr = f' class="{" ".join(cls)}"' if cls else ""
            out.append(f"<td{attr}>{H.escape(str(val))}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


TXN_TABLE = _table_html(
    ["TXN-ID", "NAME", "AGE", "HEIGHT", "WEIGHT", "BLOOD GROUP", "COVID-19 RESULT"],
    TXN_ROWS,
    highlights={(r, c) for r, c in TXN_HIGHLIGHT},
)

STUDENT_TABLE = _table_html(STUDENT_HEADERS, STUDENT_ROWS, highlights=STUDENT_HIGHLIGHT)

BTECH_HEADERS = ["Name", "Age", "Date of Birth", "Course ID", "CGPA"]
BTECH_ROWS = [
    ("Aishwarya", "24", "01-Jan-1995", "CS104", "7.4"),
    ("Bhargav", "23", "Dec-01-1996", "CS102", "7.5"),
    ("Chandra", "25", "01-Nov-1994", "", "6.7"),
    ("Divya", "24", "Oct-01-1995", "CS104", "7.9"),
    ("Bhargav", "23", "Dec-01-1996", "CS102", "8.1"),
    ("Eshan", "24", "01-Jul-1995", "CS103", "87.5"),
    ("Francis", "54", "01-01-1959", "CS105", "7.0"),
]

BTECH_HIGHLIGHT = {
    ("Chandra", "Course ID"),
    ("Bhargav", "Name"),
    ("Bhargav", "CGPA"),
    ("Eshan", "CGPA"),
    ("Francis", "Age"),
    ("Francis", "Date of Birth"),
    ("Bhargav", "Date of Birth"),
    ("Divya", "Date of Birth"),
}

BTECH_TABLE = _table_html(BTECH_HEADERS, BTECH_ROWS, highlights=BTECH_HIGHLIGHT)

CLUSTER_TABLE = _table_html(
    ["Point", "x₁ (monthly spend)", "x₂ (visit frequency)"],
    [
        ("A", "1", "2"),
        ("B", "2", "1"),
        ("C", "2", "3"),
        ("D", "6", "5"),
        ("E", "7", "6"),
        ("F", "8", "5"),
    ],
)

SVM_TRAIN_TABLE = _table_html(
    ["Point", "x₁", "x₂", "Class y"],
    [
        ("P1", "1", "4", "+1"),
        ("P2", "2", "3", "+1"),
        ("P3", "4", "1", "−1"),
        ("P4", "5", "2", "−1"),
    ],
)

KNN_CUSTOMER_TABLE = _table_html(
    ["Customer", "Age", "Monthly Spend (₹)", "Employment", "City Tier", "Risk"],
    [
        ("A0", "35", "40,000", "Salaried", "Tier-3", "R2"),
        ("A1", "45", "70,000", "Salaried", "Tier-2", "R2"),
        ("A2", "30", "38,000", "Self-Employed", "Tier-3", "R1"),
        ("A3", "50", "90,000", "Salaried", "Tier-1", "R2"),
        ("A4", "28", "42,000", "Self-Employed", "Tier-2", "R1"),
        ("Q (Query)", "32", "41,000", "Self-Employed", "Tier-3", "?"),
    ],
)

GOWER_ORDINAL_TABLE = _table_html(
    ["Customer", "Risk", "d_age", "d_spend", "d_emp", "d_city", "Gower d", "Weight (1/d²)"],
    [
        ("A2", "R1", "0.0909", "0.0577", "0", "0.0", "0.03715", "724.56"),
        ("A4", "R1", "0.1818", "0.0192", "0", "0.5", "0.17526", "32.56"),
        ("A0", "R2", "0.1364", "0.0192", "1", "0.0", "0.28890", "11.98"),
        ("A1", "R2", "0.5909", "0.5577", "1", "0.5", "0.66215", "2.28"),
        ("A3", "R2", "0.8182", "0.9423", "1", "1.0", "0.94012", "1.13"),
    ],
)

GOWER_NOMINAL_TABLE = _table_html(
    ["Customer", "Risk", "Old d_city", "New d_city", "New Gower d", "New weight"],
    [
        ("A2", "R1", "0.0", "0.0", "0.03715", "724.56"),
        ("A4", "R1", "0.5", "1.0", "0.30026", "11.09"),
        ("A0", "R2", "0.0", "0.0", "0.28890", "11.98"),
        ("A1", "R2", "0.5", "1.0", "0.78715", "1.61"),
        ("A3", "R2", "1.0", "1.0", "0.94012", "1.13"),
    ],
)

REGRESSION_RMSE_TABLE = _table_html(
    ["Model", "Training RMSE", "Test RMSE", "R² (Test)", "Features Used"],
    [
        ("A", "$45,000", "$47,000", "0.66", "3"),
        ("B", "$12,000", "$68,000", "0.42", "120"),
        ("C", "$28,000", "$36,500", "0.76", "120"),
        ("D", "$31,000", "$34,800", "0.79", "23"),
    ],
)

ID3_STUDENT_TABLE = _table_html(
    ["Exam Prep. Time", "Attendance Rate", "Extracurricular", "Performance"],
    [
        ("Low", "High", "Yes", "Excellent"),
        ("Medium", "Medium", "No", "Good"),
        ("Low", "Low", "Yes", "Poor"),
        ("High", "Medium", "Yes", "Excellent"),
        ("Medium", "High", "No", "Good"),
        ("Low", "Medium", "Yes", "Poor"),
        ("High", "High", "Yes", "Excellent"),
        ("Medium", "Medium", "Yes", "Good"),
        ("Low", "Low", "No", "Poor"),
        ("High", "High", "No", "Excellent"),
        ("Medium", "High", "Yes", "Good"),
        ("Low", "Medium", "No", "Poor"),
        ("High", "High", "Yes", "Excellent"),
        ("Medium", "Medium", "Yes", "Good"),
        ("Low", "Low", "No", "Poor"),
    ],
)

PURCHASE_TABLE = _table_html(
    ["Agegroup", "Income Level", "Occupation", "Purchased"],
    [
        ("Young", "Low", "Student", "No"),
        ("Young", "High", "Professional", "Yes"),
        ("Young", "Medium", "Student", "Yes"),
        ("Young", "Medium", "Professional", "Yes"),
        ("Middle-aged", "Low", "Retired", "No"),
        ("Middle-aged", "High", "Professional", "Yes"),
        ("Middle-aged", "Low", "Student", "No"),
        ("Middle-aged", "Medium", "Professional", "Yes"),
    ],
)

NAIVE_BAYES_HOURS_TABLE = _table_html(
    ["Study hours", "Gender", "Result"],
    [
        ("4.5", "Male", "Pass"),
        ("7", "Female", "Pass"),
        ("2", "Male", "Fail"),
        ("4", "Female", "Fail"),
        ("2.5", "Male", "Fail"),
        ("3", "Female", "Fail"),
        ("8.3", "Male", "Fail"),
        ("8", "Female", "Pass"),
        ("9", "Male", "Pass"),
    ],
)

ADABOOST_TABLE = _table_html(
    ["Sample", "Weight wᵢ", "True label yᵢ", "Prediction h₃(xᵢ)"],
    [
        ("1", "0.1", "+1", "+1"),
        ("2", "0.3", "+1", "−1"),
        ("3", "0.15", "−1", "−1"),
        ("4", "0.45", "−1", "−1"),
    ],
)

CONFUSION_350_TABLE = """<table class="data-table cm-table"><thead><tr><th></th><th>Pred +</th><th>Pred −</th></tr></thead>
<tbody><tr><th>Actual +</th><td>350 (TP)</td><td>150 (FN)</td></tr>
<tr><th>Actual −</th><td>200 (FP)</td><td>800 (TN)</td></tr></tbody></table>"""

IPL_ZSCORE_TABLE = _table_html(
    ["Team", "Mean (Batsmen)", "Runs (z)", "Wickets (z)"],
    [
        ("A", "7", "−1.41", "−1.41"),
        ("B", "5", "−0.71", "−0.71"),
        ("C", "6", "0", "0"),
        ("D", "8", "0.71", "0.71"),
        ("E", "4", "1.41", "1.41"),
    ],
)

GBM_JOBS_TABLE = _table_html(
    ["Job", "y", "F₀", "Residual", "Traffic", "Distance", "Leaf"],
    [
        ("J1", "34", "40", "−6", "High", "3", "L_B"),
        ("J2", "52", "40", "12", "High", "6", "L_C"),
        ("J3", "28", "40", "−12", "Low", "4", "L_A"),
        ("J4", "46", "40", "6", "Low", "8", "L_A"),
        ("J5", "40", "40", "0", "High", "5", "L_C"),
    ],
)

GBM_LEAF_TABLE = _table_html(
    ["Leaf", "Jobs", "Residuals", "Leaf value"],
    [
        ("L_A", "J3, J4", "−12, +6", "−3"),
        ("L_B", "J1", "−6", "−6"),
        ("L_C", "J2, J5", "+12, 0", "6"),
    ],
)

GBM_J2_UPDATE_TABLE = _table_html(
    ["Job", "F₀", "Leaf", "h₁(x)", "F₁ = F₀ + ηh₁", "New residual"],
    [("J2", "40", "L_C", "6", "41.2", "10.8")],
)

LWLR_NEIGHBORS_TABLE = _table_html(
    ["Pt", "Size", "War", "x₁", "x₂", "Y", "d", "K(d)", "ŷ", "e", "K·e"],
    [
        ("P7", "9", "18", "0.6250", "0.6667", "10.00", "0.2500", "0.9922", "2.2667", "7.7333", "7.6732"),
        ("P2", "7", "24", "0.3750", "1.0000", "12.00", "0.3333", "0.9862", "2.2000", "9.8000", "9.6648"),
        ("P1", "6", "12", "0.2500", "0.3333", "7.50", "0.3560", "0.9843", "1.8333", "5.6667", "5.5776"),
        ("P6", "5", "24", "0.1250", "1.0000", "10.50", "0.4167", "0.9785", "2.0000", "8.5000", "8.3175"),
    ],
)

MAR2026_KNN_SOLUTION = """
<div class="sol-step"><strong>Part (a)</strong> Distance computation &amp; classification <span class="marks">[3 Marks]</span>
<div class="sol-h">Step 1 — Distance measure</div>
<p class="sol-p">Mixed numeric, nominal, and ordinal attributes → <strong>Gower distance</strong></p>
<div class="sol-h">Step 2 — Normalize numeric attributes</div>
<p class="sol-p">Min–max normalization applied to Age and Monthly Spend</p>
<div class="sol-h">Step 3 — Attribute-wise distances</div>
<ul><li>Numeric → absolute normalized difference</li><li>Employment → 0 (match), 1 (mismatch)</li><li>City Tier → ordinal distance using rank normalization</li></ul>
<div class="sol-h">Step 4 — Gower distance</div>
<p class="sol-p">\\(d = (d_{age} + d_{spend} + d_{employment} + d_{city}) / 4\\)</p>
<div class="sol-h">Step 5 — Distance-weighted voting</div>
<p class="sol-p">Weight \\(w = 1/d^2\\)</p>
""" + GOWER_ORDINAL_TABLE + """
<p class="sol-p"><strong>R1 score</strong> = 724.56 + 32.56 = <strong>757.12</strong><br>
<strong>R2 score</strong> = 11.98 + 2.28 + 1.13 = <strong>15.39</strong><br>
<strong>Prediction:</strong> R1 (since 757.12 &gt; 15.39)</p></div>
<div class="sol-step"><strong>Part (b)</strong> Why R1 wins despite fewer samples <span class="marks">[1 Mark]</span>
<ul><li>Distance-weighted KNN emphasizes similarity, not count</li><li>Closest R1 neighbor (A2) has very small distance → very large weight</li></ul></div>
<div class="sol-step"><strong>Part (c)</strong> City Tier as nominal <span class="marks">[2 Marks]</span>
<p class="sol-p">City Tier treated as nominal: 0 if same, 1 if different</p>
""" + GOWER_NOMINAL_TABLE + """
<p class="sol-p"><strong>R1 score</strong> = 724.56 + 11.09 = 735.65 · Prediction remains <strong>R1</strong> · Margin reduces to 757.12 − 735.65 = 21.47</p></div>
"""


def _replace(pattern: str, repl: str, text: str) -> str:
    return re.sub(pattern, repl, text, flags=re.DOTALL)


def fix_pdf_wrapping(html: str) -> str:
    """Merge spurious <br> from PDF column wrapping (one word per line)."""
    if not html:
        return html

    # Keep breaks before sub-parts and list markers
    html = re.sub(r"<br>\s*(?=\([a-div]+\))", "%%SUBPART%%", html, flags=re.I)
    html = re.sub(r"<br>\s*(?=•)", "%%BULLET%%", html)

    # Lone math operators split across lines
    html = re.sub(r"\s*<br>\s*/\s*<br>\s*", " / ", html)
    html = re.sub(r"\s*<br>\s*\+\s*<br>\s*", " + ", html)
    html = re.sub(r"\s*<br>\s*=\s*<br>\s*", " = ", html)
    html = re.sub(r"\s*<br>\s*\(\s*<br>\s*", " (", html)
    html = re.sub(r"\s*<br>\s*\)\s*<br>\s*", ") ", html)

    # Sentence continuations: don't break after . ! ? ] or digit (marks like [1.5])
    for _ in range(40):
        prev = html
        html = re.sub(r"(?<![.!?\]\d>])\s*<br>\s*(?=[a-z(])", " ", html)
        html = re.sub(r"(?<=[a-z,;])\s*<br>\s*(?=[A-Za-z0-9(])", " ", html)
        if html == prev:
            break

    html = re.sub(r"\(\s*(\d+)\s*<br>\s*(mark(?:s)?)\s*\)", r"(\1 \2)", html, flags=re.I)
    # "at least 5<br>potential" — digit mid-sentence, not a mark like [3]
    html = re.sub(r"(?<![\[\d.])(\d)\s*<br>\s*(?=potential|issues|marks)", r"\1 ", html)
    html = re.sub(r"(\d+)\.\s*<br>\s*(?=[A-Z])", r"\1. ", html)
    html = re.sub(r"<br>\s*-\s*<br>\s*", " — ", html)

    html = html.replace("%%SUBPART%%", "<br>")
    html = html.replace("%%BULLET%%", "<br>")
    html = re.sub(r"  +", " ", html)
    return html


def _kmeans_stem_pre_bullets(html: str) -> str:
    if "centroid-based clustering" not in html:
        return html
    html = re.sub(
        r"(memberships are determined)\s+Clearly state",
        r"\1<br>Clearly state",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"\[3 marks\]\s*<br>\s*b\)\s+",
        r"[3 marks]%%UL_BREAK%%<strong>b)</strong> ",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"(GMM\) with two)\s*<br>\s*components having:",
        r"\1 components having:",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"(components having:)\s*<br>\s*",
        r"\1<br>%%UL_BREAK%%",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"\[2 marks\]\s*<br>\s*c\)\s+",
        r"[2 marks]<br><br><strong>c)</strong> ",
        html,
        flags=re.I,
    )
    return html


def _kmeans_stem_post_bullets(html: str) -> str:
    if "centroid-based clustering" not in html:
        return html
    html = re.sub(
        r"(</ul>)(Clearly state[^<]+?\[3 marks\])(<strong>b\)</strong>)",
        r"\1<p>\2</p><br>\3",
        html,
        flags=re.I,
    )
    html = re.sub(r"</ul>Explain one key", r"</ul><br>Explain one key", html)
    return html


def _kmeans_stem_fixes(html: str) -> str:
    html = re.sub(
        r"x1:\s*Average monthly spend\s+x2:\s*Visit frequency",
        r"<strong>x₁</strong>: Average monthly spend · <strong>x₂</strong>: Visit frequency",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"\((\d+),(\d+)\)and\((\d+),(\d+)\)",
        r"(\1, \2) and (\3, \4)",
        html,
    )
    html = re.sub(
        r"(</table>)\s*a\)",
        r"\1<br>a)",
        html,
    )
    return html


def break_long_stems(html: str) -> str:
    """Add breaks to dense single-line question stems from PDF extraction."""
    if not html:
        return html
    html = _kmeans_stem_fixes(html)
    if "<table" in html.lower():
        return html
    if html.count("<br>") >= 4:
        return html

    html = re.sub(
        r"(solution is)\s+(For the given)",
        r"\1<br>\2",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"\.\s+(The (?:closed form|following|model|data|table|algorithm|system|company|institution|bank|committee))",
        r".<br>\1",
        html,
        flags=re.I,
    )
    html = re.sub(r"\?\s*(\[\d)", r"?<br>\1", html)
    html = re.sub(r"(?<!<br>)(?<=[.!?]\s)([b-d]\)\s)", r"<br>\1", html, flags=re.I)

    plain = re.sub(r"<[^>]+>", "", html)
    if len(plain) > 160 and html.count("<br>") <= 2:
        html = re.sub(r"\.\s+(?=[A-Z])", ".<br>", html, count=2)

    return html


def enrich_negative_class_solution(html: str) -> str:
    """Add numeric worked answer for 2023 CM negative-class question."""
    if "800/950" in html:
        return html
    if "Precision for negative class" not in html or "TN + FN" not in html:
        return html
    extra = (
        '<div class="formula"><h5>Negative class (worked)</h5>'
        "Prec = TN/(TN+FN) = 800/(800+150) = <strong>84.2%</strong> · "
        "Rec = TN/(TN+FP) = 800/(800+200) = <strong>80.0%</strong> · "
        "F1 = 2PR/(P+R) = <strong>82.1%</strong></div>"
    )
    marker = "Answers: a) Precision for negative class"
    if marker not in html:
        return html
    return html.replace(marker, extra + marker, 1)


def convert_pipe_tables(html: str) -> str:
    """Convert pipe-separated rows (common in PDF solutions) to HTML tables."""

    def _repl(m: re.Match) -> str:
        header_line = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        headers = [c.strip() for c in header_line.split("|") if c.strip()]
        if len(headers) < 2:
            return m.group(0)
        rows = []
        body = m.group(2)
        for chunk in re.split(r"<br\s*/?>", body):
            line = re.sub(r"<[^>]+>", "", chunk).strip()
            if "|" not in line:
                continue
            cells = [c.strip() for c in line.split("|")]
            if len(cells) == len(headers):
                rows.append(tuple(cells))
        if not rows:
            return m.group(0)
        return _table_html(headers, rows)

    return re.sub(
        r"((?:[A-Za-z0-9().\s_⁻−]+(?:\s*\|\s*[A-Za-z0-9().\s_⁻−]+)+))\s*"
        r"(?:<br\s*/?>)\s*"
        r"((?:(?:[^<]+\|[^<]+)\s*(?:<br\s*/?>)\s*){1,24})",
        _repl,
        html,
    )


def enrich_purchase_stem(html: str) -> str:
    if "purchasing behaviour of customers" not in html.lower():
        return html
    if "data-table" in html:
        return html
    return html.replace(
        "which tracks the purchasing behaviour of customers based on Agegroup, Income Level, and Occupation.",
        "which tracks the purchasing behaviour of customers based on Agegroup, Income Level, and Occupation.<br>"
        + PURCHASE_TABLE,
        1,
    )


def enrich_lwlr_solution(html: str) -> str:
    if "Pt Size War" not in html and "Pt<br>Size<br>War" not in html:
        if "P7<br>9<br>18" not in html and "P7: d=0.2500" not in html:
            return html
    if "Locally Weighted Linear Regression" not in html and "Pt Size" not in html:
        return html
    html = re.sub(
        r"Pt(?:<br>|\s)*Size(?:<br>|\s)*War(?:<br>|\s)*x1(?:<br>|\s)*x2(?:<br>|\s)*Y(?:<br>|\s)*d(?:<br>|\s)*K\(d\)(?:<br>|\s)*ŷ(?:<br>|\s)*e(?:<br>|\s)*K\*e(?:<br>|\s)*"
        r"P7(?:<br>|\s)*9(?:<br>|\s)*18(?:<br>|\s)*0\.6250(?:<br>|\s)*0\.6667(?:<br>|\s)*10\.00(?:<br>|\s)*0\.2500(?:<br>|\s)*0\.9922(?:<br>|\s)*2\.2667(?:<br>|\s)*7\.7333(?:<br>|\s)*7\.6732(?:<br>|\s)*"
        r"P2(?:<br>|\s)*7(?:<br>|\s)*24(?:<br>|\s)*0\.3750(?:<br>|\s)*1\.0000(?:<br>|\s)*12\.00(?:<br>|\s)*0\.3333(?:<br>|\s)*0\.9862(?:<br>|\s)*2\.2000(?:<br>|\s)*9\.8000(?:<br>|\s)*9\.6648(?:<br>|\s)*"
        r"P1(?:<br>|\s)*6(?:<br>|\s)*12(?:<br>|\s)*0\.2500(?:<br>|\s)*0\.3333(?:<br>|\s)*7\.50(?:<br>|\s)*0\.3560(?:<br>|\s)*0\.9843(?:<br>|\s)*1\.8333(?:<br>|\s)*5\.6667(?:<br>|\s)*5\.5776(?:<br>|\s)*"
        r"P6(?:<br>|\s)*5(?:<br>|\s)*24(?:<br>|\s)*0\.1250(?:<br>|\s)*1\.0000(?:<br>|\s)*10\.50(?:<br>|\s)*0\.4167(?:<br>|\s)*0\.9785(?:<br>|\s)*2\.0000(?:<br>|\s)*8\.5000(?:<br>|\s)*8\.3175",
        LWLR_NEIGHBORS_TABLE,
        html,
        flags=re.DOTALL,
    )
    return html


def enrich_gbm_solution(html: str) -> str:
    if "J1" not in html or ("Traffic" not in html and "Leaf" not in html):
        return html
    if re.search(r"<td>J1</td><td>34</td><td>40</td>", html):
        return html
    html = re.sub(
        r"Job(?:<br>|\s)*y(?:<br>|\s)*F₀(?:<br>|\s)*Residual(?:<br>|\s)*\(y − F₀\)(?:<br>|\s)*Traffic(?:<br>|\s)*Distance(?:<br>|\s)*Leaf(?:<br>|\s)*"
        r"J1(?:<br>|\s)*34(?:<br>|\s)*40(?:<br>|\s)*-6(?:<br>|\s)*High(?:<br>|\s)*3(?:<br>|\s)*L_B(?:<br>|\s)*"
        r"J2(?:<br>|\s)*52(?:<br>|\s)*40(?:<br>|\s)*12(?:<br>|\s)*High(?:<br>|\s)*6(?:<br>|\s)*L_C(?:<br>|\s)*"
        r"J3(?:<br>|\s)*28(?:<br>|\s)*40(?:<br>|\s)*-12(?:<br>|\s)*Low(?:<br>|\s)*4(?:<br>|\s)*L_A(?:<br>|\s)*"
        r"J4(?:<br>|\s)*46(?:<br>|\s)*40(?:<br>|\s)*6(?:<br>|\s)*Low(?:<br>|\s)*8(?:<br>|\s)*L_A(?:<br>|\s)*"
        r"J5(?:<br>|\s)*40(?:<br>|\s)*40(?:<br>|\s)*0(?:<br>|\s)*High(?:<br>|\s)*5(?:<br>|\s)*L_C",
        GBM_JOBS_TABLE,
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<p class="sol-p">Job y F₀</p><p class="sol-p">Residual \(y − F₀\)</p>'
        r'<p class="sol-p">Traffic</p><p class="sol-p">Distance</p><p class="sol-p">Leaf</p>'
        r'(?:<p class="sol-p">J1</p><p class="sol-p">34</p><p class="sol-p">40</p><p class="sol-p">-6</p>'
        r'<p class="sol-p">High</p><p class="sol-p">3</p><p class="sol-p">L_B</p>'
        r'<p class="sol-p">J2</p><p class="sol-p">52</p><p class="sol-p">40</p><p class="sol-p">12</p>'
        r'<p class="sol-p">High</p><p class="sol-p">6</p><p class="sol-p">L_C</p>'
        r'<p class="sol-p">J3</p><p class="sol-p">28</p><p class="sol-p">40</p><p class="sol-p">-12</p>'
        r'<p class="sol-p">Low</p><p class="sol-p">4</p><p class="sol-p">L_A</p>'
        r'<p class="sol-p">J4</p><p class="sol-p">46</p><p class="sol-p">40</p><p class="sol-p">6</p>'
        r'<p class="sol-p">Low</p><p class="sol-p">8</p><p class="sol-p">L_A</p>'
        r'<p class="sol-p">J5</p><p class="sol-p">40</p><p class="sol-p">40</p><p class="sol-p">0</p>'
        r'<p class="sol-p">High</p><p class="sol-p">5</p><p class="sol-p">L_C</p>)',
        GBM_JOBS_TABLE,
        html,
    )
    html = re.sub(
        r"Leaf(?:<br>|\s)*Jobs(?:<br>|\s)*Residuals(?:<br>|\s)*Leaf Value(?:<br>|\s)*"
        r"L_A(?:<br>|\s)*J3,J4(?:<br>|\s)*-12, \+6(?:<br>|\s)*-3(?:<br>|\s)*"
        r"L_B(?:<br>|\s)*J1(?:<br>|\s)*-6(?:<br>|\s)*-6(?:<br>|\s)*"
        r"L_C(?:<br>|\s)*J2,J5(?:<br>|\s)*\+12, 0(?:<br>|\s)*6",
        GBM_LEAF_TABLE,
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"Job(?:<br>|\s)*F₀(?:<br>|\s)*Leaf(?:<br>|\s)*h₁\(x\)(?:<br>|\s)*F₁ = F₀ \+(?:<br>|\s)*ηh₁(?:<br>|\s)*New(?:<br>|\s)*Residual(?:<br>|\s)*"
        r"J2(?:<br>|\s)*40(?:<br>|\s)*L_C(?:<br>|\s)*6(?:<br>|\s)*41\.2(?:<br>|\s)*10\.8",
        GBM_J2_UPDATE_TABLE,
        html,
        flags=re.DOTALL,
    )
    return html


def enrich_ipl_zscore_solution(html: str) -> str:
    if "Normalized Dataset:" not in html and "Normalized Dataset" not in html:
        return html
    return re.sub(
        r"Normalized Dataset:<br>Team \| Mean\(Batsmen\) \| Runs\(z\) \| Wickets\(z\)<br>"
        r"A \| 7 \| -1\.41 \| -1\.41<br>"
        r"B \| 5 \| -0\.71 \| -0\.71<br>"
        r"C \| 6 \| 0 \| 0<br>"
        r"D \| 8 \| 0\.71 \| 0\.71<br>"
        r"E \| 4 \| 1\.41 \| 1\.41",
        "Normalized Dataset:<br>" + IPL_ZSCORE_TABLE,
        html,
    )


def format_content(html: str) -> str:
    """Full PDF text post-processing pipeline."""
    html = format_tables(html)
    html = fix_pdf_wrapping(html)
    html = format_tables(html)  # merged-line variants after wrap fix
    html = convert_pipe_tables(html)
    html = enrich_negative_class_solution(html)
    html = enrich_lwlr_solution(html)
    html = enrich_gbm_solution(html)
    html = enrich_ipl_zscore_solution(html)
    return html


JAN2026_Q6_STEM_TABLES = """
<p><strong>Table for Dataset A — Noisy features</strong></p>
<table class="data-table"><thead><tr><th>Model</th><th>Affected / Less Affected</th><th>Short Justification</th></tr></thead>
<tbody><tr><td>Linear Regression (L1)</td><td class="miss">—</td><td class="miss">—</td></tr>
<tr><td>Logistic Regression (L2)</td><td class="miss">—</td><td class="miss">—</td></tr>
<tr><td>Decision Tree (T)</td><td class="miss">—</td><td class="miss">—</td></tr></tbody></table>
<p><strong>Table for Dataset B — Outliers</strong></p>
<table class="data-table"><thead><tr><th>Model</th><th>Affected / Less Affected</th><th>Short Justification</th></tr></thead>
<tbody><tr><td>Linear Regression (L1)</td><td class="miss">—</td><td class="miss">—</td></tr>
<tr><td>Logistic Regression (L2)</td><td class="miss">—</td><td class="miss">—</td></tr>
<tr><td>Decision Tree (T)</td><td class="miss">—</td><td class="miss">—</td></tr></tbody></table>
"""

JAN2026_Q6_SOLUTION = """
<div class="sol-h">Dataset A — Noisy / Irrelevant Features</div>
<table class="data-table"><thead><tr><th>Model</th><th>Verdict</th><th>Justification</th></tr></thead>
<tbody>
<tr><td>Linear Regression (L1)</td><td><strong>Affected</strong></td><td>Fits a weight for every feature; noise gets non-zero weights from spurious correlations → higher variance, worse test performance.</td></tr>
<tr><td>Logistic Regression (L2)</td><td><strong>Affected</strong></td><td>Estimates weights for all features; noise distorts the decision boundary → overfitting, lower test accuracy.</td></tr>
<tr><td>Decision Tree (T)</td><td><strong>Strongly affected</strong></td><td>Greedy splits on any impurity gain; noise features create extra branches → high training accuracy, poor generalisation.</td></tr>
</tbody></table>
<div class="sol-h">Dataset B — Outliers Introduced</div>
<table class="data-table"><thead><tr><th>Model</th><th>Verdict</th><th>Justification</th></tr></thead>
<tbody>
<tr><td>Linear Regression (L1)</td><td><strong>Strongly affected</strong></td><td>Squared error pulls the regression line toward extremes → distorted fit.</td></tr>
<tr><td>Logistic Regression (L2)</td><td><strong>Less affected</strong></td><td>Sigmoid squashes extremes; outliers shift boundary slightly but dominate less than in linear regression.</td></tr>
<tr><td>Decision Tree (T)</td><td><strong>Affected</strong></td><td>Outliers can cause unusual splits for rare extreme points → local overfitting.</td></tr>
</tbody></table>
"""


def _bullets_in_segment(seg: str) -> str:
    if "%%LI%%" not in seg:
        return seg
    chunks = seg.split("%%LI%%")
    out = [strip_br_suffix(chunks[0])]
    items = []
    extras = []
    for c in chunks[1:]:
        c = re.sub(r"^(?:<br>\s*)+", "", c)
        lines = [ln.strip() for ln in c.split("<br>") if ln.strip()]
        if not lines:
            continue
        items.append(f"<li>{lines[0]}</li>")
        if len(lines) > 1:
            extras.append("<br>".join(lines[1:]))
    if items:
        out.append("<ul>" + "".join(items) + "</ul>")
    out.extend(extras)
    return "".join(out)


def normalize_stem_bullets(html: str) -> str:
    html = html.replace("\uf0b7", "•")
    html = re.sub(r"(?:<br>\s*)*•\s*", "<br>%%LI%%", html)
    if "%%LI%%" not in html and "%%UL_BREAK%%" not in html:
        return html
    segments = html.split("%%UL_BREAK%%")
    return "".join(_bullets_in_segment(seg) for seg in segments)


def enrich_jan2026_q6(html: str) -> str:
    if "Table for Dataset A" not in html:
        return html
    html = re.sub(
        r"Table for Dataset A:.*?Decision Tree \(T\)(?:<br>)?Table for Dataset B:.*?Decision Tree \(T\)",
        JAN2026_Q6_STEM_TABLES.strip(),
        html,
        flags=re.DOTALL,
    )
    return html


def enrich_jan2026_q6_solution(html: str) -> str:
    if "Legend" not in html or "Linear Regression (L1)" not in html:
        return html
    return JAN2026_Q6_SOLUTION.strip()


MAR2026_ENDSEM_Q6_SOLUTION = """
<div class="sol-step"><strong>(a)</strong> K-Means — one iteration [3 marks]
<div class="sol-h">Distance-based assignment</div>
<ul><li>Points A, B, C are closer to C₁ = (1, 2)</li><li>Points D, E, F are closer to C₂ = (8, 5)</li></ul>
<p class="sol-p"><strong>Cluster 1:</strong> {A, B, C} — A(1,2), B(2,1), C(2,3)<br>
<strong>Cluster 2:</strong> {D, E, F} — D(6,5), E(7,6), F(8,5)</p>
<div class="sol-h">Updated centroids</div>
<div class="formula">\\(\\mu_1 = \\left(\\frac{1+2+2}{3},\\,\\frac{2+1+3}{3}\\right) = (1.67,\\;2)\\)<br>
\\(\\mu_2 = \\left(\\frac{6+7+8}{3},\\,\\frac{5+6+5}{3}\\right) = (7,\\;5.33)\\)</div></div>
<div class="sol-step"><strong>(b)</strong> K-Means vs GMM assignment [2 marks]
<div class="sol-h">Key difference</div>
<ul><li>K-Means assigns each point <em>hardly</em> to exactly one cluster</li>
<li>GMM assigns soft responsibilities (probabilities) to each cluster</li></ul>
<p class="sol-p"><strong>Example:</strong> Point C (2,3) is clearly in Cluster 1 under K-Means. In GMM, it may still have a non-zero probability of belonging to Cluster 2 depending on covariance and distance.</p></div>
<div class="sol-step"><strong>(c)</strong> When GMM is better [1 mark]
<p class="sol-p">If clusters are elliptical or overlapping, GMM performs better because it:</p>
<ul><li>Models cluster shape via covariance</li><li>Accounts for uncertainty in assignment</li></ul></div>
"""


def enrich_mar2026_endsem_q6_solution(html: str) -> str:
    if "Points A, B, C are closer to C1" not in html and "Points A, B, C are closer to C₁" not in html:
        return html
    return MAR2026_ENDSEM_Q6_SOLUTION.strip()


def enrich_knn_gower_solution(html: str) -> str:
    if "Gower distance computation" not in html and "Gower distance (✓" not in html:
        return html
    return MAR2026_KNN_SOLUTION.strip()


def enrich_closed_form_stem(html: str) -> str:
    if "closed form solution is" not in html.lower():
        return html
    if "X^" in html or "X\\top" in html or "theta = (X" in html.lower():
        return html
    return re.sub(
        r"(The closed form solution is)\s*(?:<br>\s*)*(For the given)",
        r'\1<br><div class="formula">\\(\\theta = (X^\\top X)^{-1} X^\\top y\\)</div><br>\2',
        html,
        flags=re.I,
    )


def format_stem(html: str) -> str:
    """Post-process question stems only (line breaks + tables)."""
    html = format_content(html)
    html = _kmeans_stem_pre_bullets(html)
    html = break_long_stems(html)
    html = normalize_stem_bullets(html)
    html = _kmeans_stem_post_bullets(html)
    html = enrich_jan2026_q6(html)
    html = enrich_closed_form_stem(html)
    html = enrich_purchase_stem(html)
    return html


def format_tables(html: str) -> str:
    if not html:
        return html

    # TXN-ID health dataset (2023 Set 2 and variants)
    html = _replace(
        r"TXN-ID(?:<br>|\s)*NAME(?:<br>|\s)*AGE(?:<br>|\s)*HEIGHT(?:\s|WEIGHT|<br>)*"
        r"(?:WEIGHT(?:<br>|\s)*)?(?:BLOOD(?:<br>|\s)*)?(?:GROUP(?:<br>|\s)*)?"
        r"(?:COVID-19(?:<br>|\s)*)?(?:RESULT(?:<br>|\s)*)?"
        r"T001(?:<br>|\s)*.+?"
        r"T010(?:<br>|\s)*SysUsr789(?:<br>|\s)*20(?:<br>|\s)*165(?:<br>|\s)*68kg(?:<br>|\s)*O-ve(?:<br>|\s)*Negative",
        TXN_TABLE,
        html,
    )

    # M.Tech admissions dataset (2024+)
    html = _replace(
        r"Student(?:<br>|\s)*Name(?:<br>|\s)*Age(?:<br>|\s)*Email(?:<br>|\s)*Specialization(?:<br>|\s)*"
        r"Admission(?:<br>|\s)*Date(?:<br>|\s)*CGPA(?:<br>|\s)*"
        r"Rina(?:<br>|\s)*22(?:<br>|\s)*rina@example\.com(?:<br>|\s)*AI(?:<br>|\s)*15-Aug-2022(?:<br>|\s)*8\.2(?:<br>|\s)*"
        r".+?"
        r"Mansi(?:<br>|\s)*58(?:<br>|\s)*mansi123@gmail\.com(?:<br>|\s)*Data Science(?:<br>|\s)*15-Aug-2022(?:<br>|\s)*7\.0",
        STUDENT_TABLE,
        html,
    )

    # B.Tech CGPA dataset (2023 Regular) — vertical PDF extract (one cell per line)
    html = _replace(
        r"Name(?:<br>|\s)*Age(?:<br>|\s)*Date of Birth(?:<br>|\s)*Course ID(?:<br>|\s)*CGPA(?:<br>|\s)*"
        r"Aishwarya(?:<br>|\s)*24(?:<br>|\s)*01-Jan-1995(?:<br>|\s)*CS104(?:<br>|\s)*7\.4(?:<br>|\s)*"
        r".+?"
        r"Francis(?:<br>|\s)*54(?:<br>|\s)*01-01-1959(?:<br>|\s)*CS105(?:<br>|\s)*7\.0",
        BTECH_TABLE,
        html,
    )

    # B.Tech CGPA dataset — partially merged lines (after wrap fix)
    html = _replace(
        r"Name Age Date of Birth Course ID(?:<br>|\s)*CGPA(?:<br>|\s)*"
        r"Aishwarya(?:<br>|\s)*24(?:<br>|\s)*01-Jan-1995(?:<br>|\s)*CS104(?:<br>|\s)*7\.4(?:<br>|\s)*"
        r".+?"
        r"Francis(?:<br>|\s)*54(?:<br>|\s)*01-01-1959(?:<br>|\s)*CS105(?:<br>|\s)*7\.0",
        BTECH_TABLE,
        html,
    )

    # Medical confusion matrix in Dec 2025 solution
    html = _replace(
        r"Predicted Positive\s+Predicted Negative(?:<br>|\s)*"
        r"Actual Positive\s+120 \(TP\)(?:<br>|\s)*30 \(FN\)(?:<br>|\s)*"
        r"Actual Negative\s+85 \(FP\)(?:<br>|\s)*765 \(TN\)",
        """<table class="data-table cm-table"><thead><tr><th></th><th>Pred +</th><th>Pred −</th></tr></thead>
<tbody><tr><th>Actual +</th><td>120 (TP)</td><td>30 (FN)</td></tr>
<tr><th>Actual −</th><td>85 (FP)</td><td>765 (TN)</td></tr></tbody></table>""",
        html,
    )

    # Fraud confusion matrices (2023 set 2 Q3)
    html = _replace(
        r"Predicted Class(?:<br>|\s)*Fraud(?:<br>|\s)*Not Fraud(?:<br>|\s)*"
        r"(?:True\s*)?Class(?:<br>|\s)*Fraud(?:<br>|\s)*60(?:<br>|\s)*0(?:<br>|\s)*"
        r"Not Fraud(?:<br>|\s)*0(?:<br>|\s)*40",
        """<table class="data-table cm-table"><thead><tr><th></th><th>Pred Fraud</th><th>Pred Not Fraud</th></tr></thead>
<tbody><tr><th>Actual Fraud</th><td>60</td><td>0</td></tr>
<tr><th>Actual Not Fraud</th><td>0</td><td>40</td></tr></tbody></table>""",
        html,
    )

    # K-Means clustering dataset (Mar 2026 End-Sem Q6)
    html = _replace(
        r"Point x[₁₂1][\s]*x[₂2](?:<br>|\s)*"
        r"A(?:<br>|\s)*1(?:<br>|\s)*2(?:<br>|\s)*"
        r"B(?:<br>|\s)*2(?:<br>|\s)*1(?:<br>|\s)*"
        r"C(?:<br>|\s)*2(?:<br>|\s)*3(?:<br>|\s)*"
        r"D(?:<br>|\s)*6(?:<br>|\s)*5(?:<br>|\s)*"
        r"E(?:<br>|\s)*7(?:<br>|\s)*6(?:<br>|\s)*"
        r"F(?:<br>|\s)*8(?:<br>|\s)*5",
        CLUSTER_TABLE,
        html,
    )

    # SVM training points (Mar 2026 End-Sem Q8)
    html = _replace(
        r"Training Data Point x[₁₂1][\s]*x[₂2](?:<br>|\s)*Class y(?:<br>|\s)*"
        r"P1(?:<br>|\s)*1(?:<br>|\s)*4(?:<br>|\s)*\+1(?:<br>|\s)*"
        r"P2(?:<br>|\s)*2(?:<br>|\s)*3(?:<br>|\s)*\+1(?:<br>|\s)*"
        r"P3(?:<br>|\s)*4(?:<br>|\s)*1(?:<br>|\s)*[−-]1(?:<br>|\s)*"
        r"P4(?:<br>|\s)*5(?:<br>|\s)*2(?:<br>|\s)*[−-]1",
        SVM_TRAIN_TABLE,
        html,
    )

    # KNN customer dataset (Mar 2026 End-Sem Q2)
    html = _replace(
        r"Customer Age Monthly Spend \(₹\)(?:<br>|\s)*Employment City Tier Risk(?:<br>|\s)*"
        r"A0(?:<br>|\s)*35(?:<br>|\s)*40,000(?:<br>|\s)*Salaried(?:<br>|\s)*Tier-3(?:<br>|\s)*R2(?:<br>|\s)*"
        r".+?"
        r"Q \(Query\)(?:<br>|\s)*32(?:<br>|\s)*41,000(?:<br>|\s)*Self-Employed(?:<br>|\s)*Tier-3(?:<br>|\s)*\?",
        KNN_CUSTOMER_TABLE,
        html,
    )

    # Regression RMSE comparison (2024 Mid Makeup Q3)
    html = _replace(
        r"Model Training RMSE Test RMSE R² \(Test\) Features Used(?:<br>|\s)*"
        r"A(?:<br>|\s)*\$45,000(?:<br>|\s)*\$47,000(?:<br>|\s)*0\.66(?:<br>|\s)*3(?:<br>|\s)*"
        r"B(?:<br>|\s)*\$12,000(?:<br>|\s)*\$68,000(?:<br>|\s)*0\.42(?:<br>|\s)*120(?:<br>|\s)*"
        r"C(?:<br>|\s)*\$28,000(?:<br>|\s)*\$36,500(?:<br>|\s)*0\.76(?:<br>|\s)*120(?:<br>|\s)*"
        r"D(?:<br>|\s)*\$31,000(?:<br>|\s)*\$34,800(?:<br>|\s)*0\.79(?:<br>|\s)*23",
        REGRESSION_RMSE_TABLE,
        html,
    )

    # ID3 student performance (2023 Mid Q5)
    html = _replace(
        r"Exam Preparation Time Attendance Rate Participation in Extracurricular Activities Performance(?:<br>|\s)*"
        r"Low(?:<br>|\s)*High(?:<br>|\s)*Yes(?:<br>|\s)*Excellent(?:<br>|\s)*"
        r"Medium(?:<br>|\s)*Medium(?:<br>|\s)*No(?:<br>|\s)*Good(?:<br>|\s)*"
        r"Low(?:<br>|\s)*Low(?:<br>|\s)*Yes(?:<br>|\s)*Poor(?:<br>|\s)*"
        r"High(?:<br>|\s)*Medium(?:<br>|\s)*Yes(?:<br>|\s)*Excellent(?:<br>|\s)*"
        r"Medium(?:<br>|\s)*High(?:<br>|\s)*No(?:<br>|\s)*Good(?:<br>|\s)*"
        r"Low(?:<br>|\s)*Medium(?:<br>|\s)*Yes(?:<br>|\s)*Poor(?:<br>|\s)*"
        r"High(?:<br>|\s)*High(?:<br>|\s)*Yes(?:<br>|\s)*Excellent(?:<br>|\s)*"
        r"Medium(?:<br>|\s)*Medium(?:<br>|\s)*Yes(?:<br>|\s)*Good(?:<br>|\s)*"
        r"Low(?:<br>|\s)*Low(?:<br>|\s)*No(?:<br>|\s)*Poor(?:<br>|\s)*"
        r"High(?:<br>|\s)*High(?:<br>|\s)*No(?:<br>|\s)*Excellent(?:<br>|\s)*"
        r"Medium(?:<br>|\s)*High(?:<br>|\s)*Yes(?:<br>|\s)*Good(?:<br>|\s)*"
        r"Low(?:<br>|\s)*Medium(?:<br>|\s)*No(?:<br>|\s)*Poor(?:<br>|\s)*"
        r"High(?:<br>|\s)*High(?:<br>|\s)*Yes(?:<br>|\s)*Excellent(?:<br>|\s)*"
        r"Medium(?:<br>|\s)*Medium(?:<br>|\s)*Yes(?:<br>|\s)*Good(?:<br>|\s)*"
        r"Low(?:<br>|\s)*Low(?:<br>|\s)*No(?:<br>|\s)*Poor",
        ID3_STUDENT_TABLE,
        html,
    )

    # Naïve Bayes study hours (Mar 2026 End Makeup Q2)
    html = _replace(
        r"No of study hours Gender Final result(?:<br>|\s)*"
        r"4\.5(?:<br>|\s)*Male(?:<br>|\s)*Pass(?:<br>|\s)*"
        r"7(?:<br>|\s)*Female(?:<br>|\s)*Pass(?:<br>|\s)*"
        r"2(?:<br>|\s)*Male(?:<br>|\s)*Fail(?:<br>|\s)*"
        r"4(?:<br>|\s)*Female(?:<br>|\s)*Fail(?:<br>|\s)*"
        r"2\.5(?:<br>|\s)*Male(?:<br>|\s)*Fail(?:<br>|\s)*"
        r"3(?:<br>|\s)*Female(?:<br>|\s)*Fail(?:<br>|\s)*"
        r"8\.3(?:<br>|\s)*Male(?:<br>|\s)*Fail(?:<br>|\s)*"
        r"8(?:<br>|\s)*Female(?:<br>|\s)*Pass(?:<br>|\s)*"
        r"9(?:<br>|\s)*Male(?:<br>|\s)*Pass",
        NAIVE_BAYES_HOURS_TABLE,
        html,
    )

    # AdaBoost weights + predictions (Mar 2026 End Regular Q3)
    html = _replace(
        r"At iteration 3, the sample weights are:(?:<br>|\s)*"
        r"Sample(?:<br>|\s)*1(?:<br>|\s)*2(?:<br>|\s)*3(?:<br>|\s)*4(?:<br>|\s)*"
        r"Weight \(wᵢ\)(?:<br>|\s)*0\.1(?:<br>|\s)*0\.3(?:<br>|\s)*0\.15(?:<br>|\s)*0\.45(?:<br>|\s)*"
        r"True Label \(yᵢ\)(?:<br>|\s)*\+1(?:<br>|\s)*\+1(?:<br>|\s)*-1(?:<br>|\s)*-1(?:<br>|\s)*"
        r"A weak learner h₃\(x\) is trained and makes the following predictions:(?:<br>|\s)*"
        r"Sample(?:<br>|\s)*1(?:<br>|\s)*2(?:<br>|\s)*3(?:<br>|\s)*4(?:<br>|\s)*"
        r"Prediction h₃\(xᵢ\)(?:<br>|\s)*\+1(?:<br>|\s)*-1(?:<br>|\s)*-1(?:<br>|\s)*-1",
        "At iteration 3, the sample weights and predictions are:<br>" + ADABOOST_TABLE,
        html,
    )

    # Confusion matrix 350/150/200/800 (2023 Mid Q6)
    html = _replace(
        r"Predicted Positive Predicted Negative Actual Positive 350 \(TP\)(?:<br>|\s)*"
        r"150 \(FN\)(?:<br>|\s)*Actual Negative 200 \(FP\)(?:<br>|\s)*800 \(TN\)",
        CONFUSION_350_TABLE,
        html,
    )

    return html
