"""Convert PDF-extracted vertical cell lists into HTML tables; fix PDF line-wrap artifacts."""
import html as H
import re
from typing import Iterable, List, Optional

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

    html = html.replace("%%SUBPART%%", "<br>")
    html = html.replace("%%BULLET%%", "<br>")
    html = re.sub(r"  +", " ", html)
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


def format_content(html: str) -> str:
    """Full PDF text post-processing pipeline."""
    html = format_tables(html)
    html = fix_pdf_wrapping(html)
    html = enrich_negative_class_solution(html)
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

    # Confusion matrix in question stem (2023 set 1)
    html = _replace(
        r"Predicted Positive(?:<br>|\s)*Predicted Negative(?:<br>|\s)*"
        r"Actual Positive(?:<br>|\s)*350 \(TP\)(?:<br>|\s)*150 \(FN\)(?:<br>|\s)*"
        r"Actual Negative(?:<br>|\s)*200 \(FP\)(?:<br>|\s)*800 \(TN\)",
        """<table class="data-table cm-table"><thead><tr><th></th><th>Pred +</th><th>Pred −</th></tr></thead>
<tbody><tr><th>Actual +</th><td>350 (TP)</td><td>150 (FN)</td></tr>
<tr><th>Actual −</th><td>200 (FP)</td><td>800 (TN)</td></tr></tbody></table>""",
        html,
    )

    return html
