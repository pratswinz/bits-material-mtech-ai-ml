#!/usr/bin/env python3
"""Rebuild ISM_Past_Papers.html from ISM/previous question papers."""
import fitz
import html as H
import re
from pathlib import Path

from solution_format import SOL_CSS, format_solution, prepare_solution_raw
from ism_stem_format import format_ism_stem
from table_format import TABLE_CSS, format_content
from math_format import format_math_in_html

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ISM_Past_Papers.html"
BASE = Path("/Volumes/disc 2/bits pilani/ISM/previous question papers")
JUNE = BASE / "june 2026"

PAPERS = [
    ("S2-24_ISM_MID-EXAM_REGULAR.pdf", "Mid Sem", "Regular", "2025", "Jan 2025 Mid-Sem EC-2 Regular"),
    ("S2-24_ISM_MID-Exam_Makeup.pdf", "Mid Sem", "Makeup", "2025", "Jun 2025 Mid-Sem EC-2 Makeup"),
    ("Dec 2025 ISM Midsem Regular QP & answer key.pdf", "Mid Sem", "Regular", "2025", "Dec 2025 Mid-Sem EC-2 Regular (Key)"),
    ("Jan 2026 ISM Midsem Makeup QP & answer key.pdf", "Mid Sem", "Makeup", "2026", "Jan 2026 Mid-Sem EC-2 Makeup (Key)"),
]

DOCX_PAPERS = []

SKIP = re.compile(
    r"^(BIRLA INSTITUTE|Work Integrated|First Semester|Second Semester|Mid-Semester|Comprehensive|"
    r"Course No|Course Title|Nature of Exam|Weightage|Duration|Date of Exam|Note to Students|"
    r"Please follow|All parts|Assumptions|No\. of Pages|No\. of Questions|\*{3,}|Answer all)",
    re.I,
)

NAIVE_URGENT_TABLE = """
<table class="data-table"><thead><tr><th>ID</th><th>Words</th><th>Label</th></tr></thead><tbody>
<tr><td>1</td><td>assignment due tomorrow please help</td><td>Urgent</td></tr>
<tr><td>2</td><td>lunch plans today?</td><td>Not Urgent</td></tr>
<tr><td>3</td><td>exam rescheduled urgent attention</td><td>Urgent</td></tr>
<tr><td>4</td><td>thanks for the notes</td><td>Not Urgent</td></tr>
</tbody></table>"""

NAIVE_BUY_TABLE = """
<table class="data-table"><thead><tr><th>Age</th><th>Income</th><th>Buy Yes</th><th>Buy No</th></tr></thead><tbody>
<tr><td>Young</td><td>Low</td><td>5</td><td>15</td></tr>
<tr><td>Young</td><td>High</td><td>20</td><td>5</td></tr>
<tr><td>Middle</td><td>Low</td><td>10</td><td>10</td></tr>
<tr><td>Middle</td><td>High</td><td>30</td><td>10</td></tr>
<tr><td>Senior</td><td>Low</td><td>3</td><td>12</td></tr>
<tr><td>Senior</td><td>High</td><td>12</td><td>8</td></tr>
</tbody></table>"""

PMF_TABLE = """
<table class="data-table cm-table"><thead><tr><th>x</th><th>0</th><th>1</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th></tr></thead>
<tbody><tr><td>p(x)</td><td>0</td><td>k</td><td>2k</td><td>2k</td><td>3k</td><td>k²</td><td>7k²+k</td></tr></tbody></table>"""

JUNE2026_BLOCKS = [
    ("Q1", "Five-number summary + conditional probability [5M]",
     "WhatsApp Image 2026-06-21 at 18.24.10 (1).jpeg",
     """<div class="sol-body">
<div class="sol-step"><strong>(a)(i)</strong> Sorted waits (min): 1.5, 2.1, 2.2, 2.8, 2.9, 3.0, 3.3, 3.5, 3.7, 4.0, 4.1, 4.5, 4.9, 5.2, 5.8, 6.0, 6.8, 7.2, 7.5, 8.0 (n=20)<br>
Min=1.5 · Q1≈2.95 · Median=(4.1+4.5)/2=4.3 · Q3≈6.4 · Max=8.0</div>
<div class="sol-step"><strong>(a)(ii)</strong> IQR≈3.45 — half the customers wait 3–6.4 min (efficient). Max 8.0 min is not an outlier under 1.5×IQR; tail is moderate, not extreme.</div>
<div class="sol-step"><strong>(b)</strong> Law of total probability:<br>
\\(P(B\\text{ wins}) = P(A\\text{ fails})P(B|A\\text{ fails}) + P(A\\text{ completes})P(B|A\\text{ completes})\\)<br>
\\(= 0.5(0.85) + 0.5(0.25) = 0.425 + 0.125 = \\mathbf{0.55}\\)</div>
</div>"""),
    ("Q2", "NEET inclusion–exclusion [6M]",
     "WhatsApp Image 2026-06-21 at 18.24.09 (2).jpeg",
     """<div class="sol-body">
<div class="sol-step"><strong>Given</strong> N=600, |P|=380, |C|=260, |B|=420, |P∩C|=150, |P∩B|=250, |C∩B|=180</div>
<div class="sol-step"><strong>(a)</strong> \\(|P\\cup C\\cup B| = |P|+|C|+|B| - |P\\cap C| - |P\\cap B| - |C\\cap B| + |P\\cap C\\cap B|\\)<br>
\\(600 = 1060 - 580 + |P\\cap C\\cap B| \\Rightarrow |P\\cap C\\cap B| = \\mathbf{120}\\), \\(P=120/600=0.20\\)</div>
<div class="sol-step"><strong>(b)</strong> Exactly two = (150+250+180) − 3(120) = 580−360 = <strong>220</strong> → P = 220/600 ≈ 0.367</div>
<div class="sol-step"><strong>(c)</strong> P but not B: 380 − 250 = <strong>130</strong> → P = 130/600 ≈ 0.217</div>
<div class="sol-step"><strong>(d)</strong> Only B: 420 − 250 − 180 + 120 = <strong>110</strong> → P = 110/600 ≈ 0.183</div>
<div class="sol-step"><strong>(e)</strong> (P∪B) \\ C: (380+420−250) − 120 − (130+110) = 550−360 = <strong>190</strong> → P ≈ 0.317</div>
<div class="sol-step"><strong>(f)</strong> Biology has largest solo qualification; all-three overlap 20% — strong cross-subject dependence.</div>
</div>"""),
    ("Q3", "Binomial — defective chips [4M]",
     "WhatsApp Image 2026-06-21 at 18.24.10 (2).jpeg",
     """<div class="sol-body">
<div class="sol-step"><strong>Model</strong> \\(X \\sim \\text{Binomial}(n=40, p=0.03)\\)</div>
<div class="sol-step"><strong>(i)</strong> \\(P(X=4) = \\binom{40}{4}(0.03)^4(0.97)^{36} \\approx \\mathbf{0.062}\\)</div>
<div class="sol-step"><strong>(ii)</strong> \\(P(2\\le X\\le 5) = P(X=2)+P(X=3)+P(X=4)+P(X=5) \\approx \\mathbf{0.238}\\)</div>
<div class="sol-step"><strong>(iii)</strong> Flag if \\(X>4\\): \\(P(X>4) = 1 - P(X\\le 4) \\approx \\mathbf{0.096}\\)</div>
</div>"""),
    ("Q4", "Continuous PDF — battery lifetime [5M]",
     "WhatsApp Image 2026-06-21 at 18.24.09.jpeg",
     """<div class="sol-body">
<div class="sol-step"><strong>PDF</strong> \\(f(x)=x/50\\) for \\(0\\le x\\le 10\\), else 0</div>
<div class="sol-step"><strong>(i)</strong> \\(\\int_0^{10} x/50\\,dx = [x^2/100]_0^{10} = 1\\) → valid PDF ✓</div>
<div class="sol-step"><strong>(ii)</strong> \\(P(X>8) = \\int_8^{10} x/50\\,dx = (100-64)/100 = \\mathbf{0.36}\\)</div>
<div class="sol-step"><strong>(iii)</strong> \\(E[X] = \\int_0^{10} x^2/50\\,dx = 1000/150 = \\mathbf{20/3 \\approx 6.67}\\) years</div>
<div class="sol-step"><strong>(iv)</strong> \\(E[X^2]=50\\), \\(\\text{Var}(X)=50-(20/3)^2 = \\mathbf{50/9 \\approx 5.56}\\)</div>
<div class="sol-step"><strong>(v)</strong> Mean ~6.7 yr with moderate spread — most batteries fail before 10 yr cap; 36% last beyond 8 yr.</div>
</div>"""),
    ("Q5", "Naïve Bayes — customer purchase [5M]",
     "WhatsApp Image 2026-06-21 at 18.24.10.jpeg",
     NAIVE_BUY_TABLE + """
<div class="sol-body">
<div class="sol-step"><strong>(a)</strong> Total Yes=80, No=60, N=140 → \\(P(\\text{Yes})=4/7\\), \\(P(\\text{No})=3/7\\)</div>
<div class="sol-step"><strong>(b)</strong> Middle+High: \\(P(M,H|\\text{Yes})=30/80=3/8\\), \\(P(M,H|\\text{No})=10/60=1/6\\)</div>
<div class="sol-step"><strong>(c)</strong> Posterior Yes \\(\\propto (4/7)(3/8)=3/14\\); No \\(\\propto (3/7)(1/6)=1/14\\) → \\(P(\\text{Yes}|M,H)=\\mathbf{3/4}\\), \\(P(\\text{No}|M,H)=1/4\\)</div>
<div class="sol-step"><strong>(d)</strong> Predict <strong>Buy = Yes</strong> (75% posterior). Target Middle+High income segment in marketing.</div>
</div>"""),
    ("Q6", "Bayes fraud + Normal delivery [5M]",
     "WhatsApp Image 2026-06-21 at 18.24.09 (1).jpeg",
     """<div class="sol-body">
<div class="sol-step"><strong>(a)(i) Bayes</strong> F=fraud, S=flagged:<br>
\\(P(F)=0.02\\), \\(P(S|F)=0.90\\), \\(P(S|F^c)=0.05\\)<br>
\\(P(S)=0.02(0.90)+0.98(0.05)=0.067\\)<br>
\\(P(F|S)=0.018/0.067 \\approx \\mathbf{0.269}\\) (27%)</div>
<div class="sol-step"><strong>(a)(ii)</strong> Flag is <em>not</em> strong evidence — ~73% flagged txns are legitimate → high false-alarm rate hurts trust.</div>
<div class="sol-step"><strong>(b)(i)</strong> \\(X\\sim N(5,1.2^2)\\), \\(Z=(4-5)/1.2=-0.833\\) → \\(P(X<4)=P(Z<-0.83)\\approx\\mathbf{0.20}\\)</div>
<div class="sol-step"><strong>(b)(ii)</strong> \\(P(4<X<6)=P(-0.83<Z<0.83)\\approx 0.793-0.207=\\mathbf{0.586}\\)</div>
</div>"""),
]

# Hand-written solutions for PDF papers (key = paper slug, q number)
SOLUTIONS = {
    "dec-2025-mid-sem-ec-2-regular-key": {
        1: """<div class="sol-body">
<div class="sol-step"><strong>(a)</strong> Data: 7,4,20,23,25,19,30,30,40,56 → Mean=\\(\\bar x=25.4\\), Median=22, SD≈\\(14.6\\), Q1=19, Q3=30, IQR=11</div>
<div class="sol-step">Outliers: \\(Q1-1.5\\cdot IQR=2.5\\), \\(Q3+1.5\\cdot IQR=46.5\\) → <strong>56</strong> is outlier</div>
<div class="sol-step"><strong>(b)</strong> Right-skewed (mean > median); high variability — one sandwich (56g) far above typical ~20–30g range.</div>
</div>""",
        2: NAIVE_URGENT_TABLE + """
<div class="sol-body">
<div class="sol-step">Laplace α=1. Vocab with α: urgent×2, assignment×1, due×1, tomorrow×1, help×1, lunch×1, plans×1, today×1, exam×1, rescheduled×1, attention×1, thanks×1, notes×1</div>
<div class="sol-step">\\(P(\\text{Urgent})=2/6\\), \\(P(\\text{Not})=4/6\\). Test "assignment urgent":<br>
\\(P(\\text{U}|\\text{assign})=2/8\\), \\(P(\\text{U}|\\text{urgent})=3/8\\) vs \\(P(\\text{NU}|\\text{assign})=1/8\\), \\(P(\\text{NU}|\\text{urgent})=1/8\\)</div>
<div class="sol-step">Posterior Urgent \\(\\propto (2/6)(2/8)(3/8)=12/384\\); Not \\(\\propto (4/6)(1/8)(1/8)=4/384\\) → <strong>Classify Urgent</strong> (3:1 ratio)</div>
</div>""",
        3: PMF_TABLE + """
<div class="sol-body">
<div class="sol-step"><strong>(a)(i)</strong> Sum pmf = 11k + 8k² = 1 → k ≈ 0.083 (check: 8k²+11k-1=0)</div>
<div class="sol-step"><strong>(ii)</strong> \\(P(X<6)=P(0)+P(1)+P(3)+P(4)+P(5)\\); \\(P(X\\ge6)=P(6)+P(7)\\)</div>
<div class="sol-step"><strong>(iii)</strong> \\(P(0<X<5)=P(1)+P(3)+P(4)\\)</div>
<div class="sol-step"><strong>(b)</strong> Poisson λ=np=10×0.002=0.02 per packet. \\(P(0)=e^{-0.02}\\), \\(P(1)=0.02e^{-0.02}\\). Scale to 10,000 packets.</div>
</div>""",
        4: """<div class="sol-body">
<div class="sol-step"><strong>(i)</strong> \\(\\int_0^1\\int_0^1 6x^2y\\,dy\\,dx = \\int_0^1 3x^2\\,dx = 1\\) ✓</div>
<div class="sol-step"><strong>(ii)</strong> \\(f_X(x)=3x^2\\), \\(f_Y(y)=6y\\) on [0,1]</div>
<div class="sol-step"><strong>(iii)</strong> \\(P(X<0.5,Y>0.5)=\\int_0^{0.5}\\int_{0.5}^1 6x^2y\\,dy\\,dx = 3/32\\)</div>
<div class="sol-step"><strong>(iv)</strong> \\(f(0.5,0.5)=1.5 \\ne f_X(0.5)f_Y(0.5)=0.75\\) → <strong>not independent</strong></div>
<div class="sol-step"><strong>(v)</strong> \\(E[X]=3/4\\), \\(E[Y]=1/2\\), \\(E[XY]=3/8\\)</div>
</div>""",
        5: """<div class="sol-body">
<div class="sol-step">\\(X\\sim N(0.500, 0.005^2)\\). Defective if \\(X<0.492\\) or \\(X>0.506\\)</div>
<div class="sol-step">\\(Z_1=(0.492-0.500)/0.005=-1.6\\), \\(Z_2=(0.506-0.500)/0.005=1.2\\)</div>
<div class="sol-step">\\(P(\\text{defect}) = P(Z<-1.6)+P(Z>1.2) \\approx 0.055+0.115 = \\mathbf{17\\%}\\)</div>
<div class="sol-step"><strong>(b)</strong> Process not fully capable — ~17% scrap/rework expected at current σ.</div>
</div>""",
        6: """<div class="sol-body">
<div class="sol-step">Given \\(P(A\\cap B)=P(B\\cap C)=P(C\\cap A)=1/8\\), \\(P(A\\cap B\\cap C)=1/16\\), \\(P(\\text{none})=1/4\\)</div>
<div class="sol-step">From inclusion–exclusion with equal singles: solve \\(3p - 3/8 + 1/16 = 3/4\\) → \\(P(A)=P(B)=P(C)=\\mathbf{11/32}\\)</div>
<div class="sol-step">Exactly two: \\(3(1/8)-3(1/16)=3/16\\). At least one: \\(1-1/4=3/4\\). Exactly one: \\(3/4 - 3/16 - 1/16 = 1/2\\)</div>
</div>""",
    },
    "jan-2026-mid-sem-ec-2-makeup-key": {
        1: """<div class="sol-body">
<div class="sol-step">Sorted: 190,230,240,245,250,265,270,280,285,380 → Min=190, Q1=240, Med=257.5, Q3=280, Max=380</div>
<div class="sol-step">IQR=40; fence upper=280+60=340 → <strong>380 is outlier</strong> (possible process shift on day 10)</div>
</div>""",
        2: """<div class="sol-body">
<div class="sol-step">Bayes: \\(P(A)=0.5\\), \\(P(B)=0.3\\), \\(P(C)=0.2\\); \\(P(R|A)=0.8\\), \\(P(R|B)=0.6\\), \\(P(R|C)=0.4\\)</div>
<div class="sol-step">\\(P(R)=0.5(0.8)+0.3(0.6)+0.2(0.4)=0.66\\)</div>
<div class="sol-step">\\(P(A|R)=0.40/0.66 \\approx \\mathbf{0.606}\\)</div>
</div>""",
        3: """<div class="sol-body">
<div class="sol-step">\\(X\\sim N(73,8^2)\\). (i) \\(P(X<91)=P(Z<2.25)\\approx 0.988\\) → yes, "most" (&gt;97%)</div>
<div class="sol-step">(ii) \\(P(65<X<89)=P(-1<Z<2)\\approx 0.977-0.159=0.818\\)</div>
<div class="sol-step">(iii) Dean's List top 5%: \\(P(X>c)=0.05\\) → \\(c=73+1.645(8)\\approx \\mathbf{86.2}\\)</div>
</div>""",
        6: """<div class="sol-body">
<div class="sol-step"><strong>(a)</strong> Rate 1.2/100 → λ=2.5 per 250 cheques → \\(X\\sim\\text{Poisson}(2.5)\\)</div>
<div class="sol-step">\\(P(X\\le2)\\approx e^{-2.5}(1+2.5+3.125)\\approx 0.544\\); \\(P(X>4)=1-P(X\\le4)\\approx 0.108\\)</div>
<div class="sol-step"><strong>(b)</strong> Inclusion–exclusion: at least one defect \\(P(W\\cup C\\cup S)\\approx 0.285\\); defect-free ≈ 7150 discs</div>
</div>""",
    },
    "jan-2025-mid-sem-ec-2-regular": {
        1: """<div class="sol-body">
<div class="sol-step"><strong>(a)</strong> Weights with outlier 100: Q1≈65, Q2=72, Q3=78, IQR=13 → outlier fence 97.5 → <strong>100 kg</strong></div>
<div class="sol-step"><strong>(b)</strong> Astronaut times: mean≈25.3 min, SD≈4.2 min — moderate spread around mid-20s</div>
</div>""",
        2: """<div class="sol-body">
<div class="sol-step"><strong>(a)</strong> \\(X\\sim N(12,4)\\): \\(P(X<7)=P(Z<-2.5)\\approx 0.006\\); \\(P(7<X<12)=P(-2.5<Z<0)\\approx 0.494\\)</div>
<div class="sol-step"><strong>(b)</strong> Binomial(40,0.15): \\(P(X=5)\\approx 0.176\\); Poisson λ=6: \\(P(X=5)\\approx 0.161\\) — close agreement</div>
</div>""",
        3: """<div class="sol-body">
<div class="sol-step">Naïve Bayes spam filter for "Congratulations! You have won money quickly" — compute \\(P(\\text{Spam}|\\text{words})\\) vs Ham using training counts + Laplace smoothing; high spam-word density → classify <strong>Spam</strong></div>
</div>""",
    },
    "jun-2025-mid-sem-ec-2-makeup": {
        1: """<div class="sol-body">
<div class="sol-step">Marks: mean≈17.1; five-number summary from sorted data; slight left skew (mean &lt; median)</div>
<div class="sol-step"><strong>(b)</strong> Sample mean height \\(\\bar X\\sim N(70, 9/49)\\): \\(P(69<\\bar X<71)=P(-2.33<Z<2.33)\\approx 0.98\\)</div>
</div>""",
        2: """<div class="sol-body">
<div class="sol-step">Naïve Bayes for "Win free money" — both words appear in spam training → classify <strong>Spam</strong></div>
</div>""",
        4: """<div class="sol-body">
<div class="sol-step">DNA match Bayes: prior \\(P(\\text{guilty})\\) small; \\(P(\\text{match}|\\text{innocent})=10^{-6}\\) → posterior still depends strongly on base rate — avoid prosecutor's fallacy</div>
</div>""",
    },
}


def esc(s):
    if not s:
        return ""
    return format_math_in_html(format_ism_stem(s))


def esc_sol(s):
    if not s:
        return ""
    s = prepare_solution_raw(s)
    html = format_content(H.escape(s).replace("\n", "<br>"))
    html = format_solution(html)
    return format_math_in_html(html)


def badge(exam, session, year):
    ec = "mid" if exam == "Mid Sem" else "end"
    sc = "reg" if session == "Regular" else "makeup"
    return (
        f'<span class="b {ec}">{H.escape(exam)}</span>'
        f'<span class="b {sc}">{H.escape(session)}</span>'
        f'<span class="b yr">{year}</span>'
    )


def clean(text):
    return "\n".join(l for l in (x.strip() for x in text.split("\n")) if l and not SKIP.match(l))


def split_question_body(body: str) -> tuple:
    """Split question stem from embedded Solution/Sol block."""
    for marker in (r"\nSolution:\s*\n", r"\nSol:\s*\n", r"\nSolution\s*\n"):
        m = re.search(marker, body, re.I)
        if m and m.start() > 30:
            return body[: m.start()].strip(), body[m.end() :].strip()
    return body, ""


def split_questions(text):
    text = clean(text)
    m = re.search(r"Answer all the questions:?\s*", text, re.I)
    if m:
        text = text[m.end() :]
    parts = re.split(
        r"\n(?="
        r"(?:Q\.?\s*\d+(?:[\.\)]|\s+[a-z(])"
        r"|\d+\.\s+(?!(?:Please follow|All parts|Assumptions made))[A-Za-z\"'])"
        r")",
        text,
    )
    blocks = []
    seen = set()
    for p in parts:
        p = p.strip()
        if len(p) < 40:
            continue
        m = re.match(r"Q\.?\s*(\d+)[\.\)]?\s*", p, re.I) or re.match(r"(\d+)\.\s*", p)
        if not m:
            continue
        qnum = int(m.group(1))
        if qnum > 10 or qnum in seen:
            continue
        seen.add(qnum)
        body = p[m.end() :].strip()
        qtext, sol = split_question_body(body)
        blocks.append((qnum, f"Q{qnum}", qtext, sol))
    blocks.sort(key=lambda x: x[0])
    return blocks


def html_table(headers, rows, cls="data-table"):
    th = "".join(f"<th>{H.escape(str(c))}</th>" for c in headers)
    body = ""
    for row in rows:
        body += "<tr>" + "".join(f"<td>{H.escape(str(c))}</td>" for c in row) + "</tr>"
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


DELHI_TEMP_ELEC = html_table(
    ["Month", "Avg Temp °C (X)", "Avg Electricity kWh (Y)"],
    [("May", 38, 320), ("June", 41, 380), ("July", 35, 290), ("August", 33, 270), ("September", 31, 240)],
)

DEMAND_TABLE = html_table(
    ["Month", "Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    [("Demand (×1000 req)", 82, 88, 91, 97, 95, 102)],
)

BEFORE_AFTER = html_table(
    ["", "S1", "S2", "S3", "S4", "S5", "S6"],
    [("Before", 32, 35, 30, 33, 31, 34), ("After", 36, 38, 34, 37, 35, 39)],
)

ANOVA_IRRIGATION = html_table(
    ["Irrigation ↓ / Block →", "Block 1", "Block 2", "Block 3", "Block 4"],
    [("Drip", 22, 20, 24, 22), ("Sprinkler", 21, 19, 23, 21), ("Flood", 18, 16, 20, 18)],
)

WATER_YIELD = html_table(
    ["Garden", "X (L/m²/day)", "Y (kg/m²)"],
    [
        ("G1", 3.0, 1.8), ("G2", 4.2, 2.5), ("G3", 2.5, 1.6), ("G4", 5.1, 2.9),
        ("G5", 3.8, 2.3), ("G6", 6.0, 2.7), ("G7", 2.0, 1.2), ("G8", 4.5, 2.6),
        ("G9", 5.5, 2.8), ("G10", 3.3, 2.0),
    ],
)

CADENCE_TABLE = html_table(
    ["Student", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"],
    [
        ("Cadence", 0.95, 0.85, 0.92, 0.95, 0.93, 0.86, 1.00, 0.92, 0.85, 0.81,
         0.78, 0.93, 0.93, 1.05, 0.93, 1.06, 1.06, 0.96, 0.81, 0.96),
    ],
)

EC3_QUESTIONS = [
    ("Q1", "Karl Pearson correlation — Delhi electricity [5M]",
     f"""<p>The Delhi Government studies the link between summer temperature and household electricity use (AC-driven load).</p>
{DELHI_TEMP_ELEC}
<ol>
<li>Calculate Karl Pearson's \\(r\\) between average monthly temperature \\(X\\) and electricity usage \\(Y\\).</li>
<li>Interpret for urban energy planning during heatwaves.</li>
</ol>""",
     """<div class="sol-body">
<div class="sol-step">\\(n=5\\), \\(\\bar X=35.6\\), \\(\\bar Y=300\\)</div>
<div class="sol-step">\\(S_{xy}=840\\), \\(S_{xx}=63.2\\), \\(S_{yy}=11400\\)</div>
<div class="sol-step">\\(r = S_{xy}/\\sqrt{S_{xx}S_{yy}} = 840/\\sqrt{720480} \\approx \\mathbf{0.99}\\) — very strong positive linear association</div>
<div class="sol-step"><strong>Interpret:</strong> As temperature rises, electricity demand rises almost proportionally → grid must plan for sharp AC-driven peaks in extreme heat.</div>
</div>"""),
    ("Q2", "Simple exponential smoothing — ML inference demand [5M]",
     f"""<p>A logistics company forecasts monthly demand (thousands of requests) for a cloud ML inference service:</p>
{DEMAND_TABLE}
<p>Initial forecast for January = actual January demand. Using <strong>Simple Exponential Smoothing</strong> only:</p>
<ol type="a">
<li>Forecast July demand with \\(\\alpha=0.4\\)</li>
<li>Forecast July demand with \\(\\alpha=0.7\\)</li>
<li>Which \\(\\alpha\\) suits sudden demand spikes in real-time AI workloads?</li>
</ol>""",
     """<div class="sol-body">
<div class="sol-step">\\(F_t = \\alpha A_{t-1} + (1-\\alpha)F_{t-1}\\), \\(F_1=A_{Jan}=82\\)</div>
<div class="sol-step"><strong>\\(\\alpha=0.4\\):</strong> \\(F_{Feb}=84.4\\), \\(F_{Mar}=87.0\\), \\(F_{Apr}=91.0\\), \\(F_{May}=92.6\\), \\(F_{Jun}=96.4\\) → <strong>July ≈ 96.4</strong></div>
<div class="sol-step"><strong>\\(\\alpha=0.7\\):</strong> chain gives <strong>July ≈ 99.9</strong> (tracks recent spike in June=102 more closely)</div>
<div class="sol-step"><strong>(c)</strong> \\(\\alpha=0.7\\) — higher \\(\\alpha\\) weights recent observations → reacts faster to sudden spikes.</div>
</div>"""),
    ("Q3", "Hypothesis tests — paired t &amp; z-test [5M]",
     f"""<p><strong>(a) [3M]</strong> Scores of 6 students before/after a revision strategy:</p>
{BEFORE_AFTER}
<p>At 5% significance, test whether the strategy improves performance.</p>
<p><strong>(b) [2M]</strong> Derm Assist claims 20 min average time reduction; hospital test: \\(n=36\\), \\(\\bar x=18.2\\) min, \\(\\sigma=7.5\\) min. Test at 5% and interpret for clinical deployment.</p>""",
     """<div class="sol-body">
<div class="sol-step"><strong>(a)</strong> Differences (After−Before): 4,3,4,4,4,5 → all positive, \\(\\bar d=4\\). Paired t-test → reject \\(H_0\\) at 5% → <strong>strategy significantly improves scores</strong>.</div>
<div class="sol-step"><strong>(b)</strong> \\(H_0:\\mu=20\\) vs \\(H_a:\\mu<20\\). \\(z=(18.2-20)/(7.5/\\sqrt{36})=-1.44\\), one-tailed \\(p\\approx0.075>0.05\\)</div>
<div class="sol-step">Fail to reject \\(H_0\\) — insufficient evidence for full 20 min claim; Type II error risk if deployed without stronger evidence.</div>
</div>"""),
    ("Q4", "Randomized block ANOVA — mango irrigation [5M]",
     f"""<p>Effect of three irrigation methods on mango yield (kg/tree) across four orchard blocks:</p>
{ANOVA_IRRIGATION}
<p>No interaction between method and block. At 5% significance test:</p>
<p>\\(H_0\\): orchards do not differ and irrigation methods do not differ<br>
\\(H_1\\): orchards differ and/or irrigation methods differ</p>""",
     """<div class="sol-body">
<div class="sol-step">Two-way ANOVA (RBD): row means Drip=22, Sprinkler=21, Flood=18; block means vary 17.5–23.5</div>
<div class="sol-step">Method SS dominates — Drip &gt; Sprinkler &gt; Flood consistently across blocks</div>
<div class="sol-step">Reject \\(H_0\\) for irrigation methods at 5% → <strong>irrigation method significantly affects yield</strong>; Drip best.</div>
</div>"""),
    ("Q5", "Simple linear regression — rooftop irrigation [5M]",
     f"""<p>MUFI pilot: water input \\(X\\) (L/m²/day) vs crop yield \\(Y\\) (kg/m²) for 10 gardens:</p>
{WATER_YIELD}
<ol type="a">
<li>Fit \\(Y = \\beta_0 + \\beta_1 X\\)</li>
<li>Is the linear model appropriate? What pattern do you see?</li>
<li>Optimal water range for yield per unit water (efficiency)?</li>
</ol>""",
     """<div class="sol-body">
<div class="sol-step">\\(\\bar X=4.07\\), \\(\\bar Y=2.24\\). Regression: \\(\\hat Y \\approx 0.35 + 0.47 X\\), \\(r\\approx0.93\\)</div>
<div class="sol-step"><strong>(b)</strong> Strong linear fit — yield rises with water; slight diminishing returns at highest X (G6).</div>
<div class="sol-step"><strong>(c)</strong> Efficiency \\(Y/X\\) peaks around <strong>3–4 L/m²/day</strong> — beyond ~5 L/m² gains are small; over-irrigation wastes water (Mumbai scarcity).</div>
</div>"""),
    ("Q6", "Gaussian mixture model — cafeteria lunch [5M]",
     """<p>Lunch duration (min) for 10 students: {18, 20, 22, 25, 27, 35, 38, 40, 42, 45} — bimodal, modelled as 2-component GMM.</p>
<p>Component 1: first 5 (quick eaters); Component 2: last 5 (leisurely eaters).</p>
<ol type="a">
<li>Write the PDF of a two-component GMM</li>
<li>Estimate mean and variance of each component</li>
<li>Compute mixing coefficients</li>
<li>How does GMM identify different lunch behaviours?</li>
</ol>""",
     """<div class="sol-body">
<div class="sol-step"><strong>(a)</strong> \\(f(x)=\\pi_1\\mathcal{N}(x;\\mu_1,\\sigma_1^2)+\\pi_2\\mathcal{N}(x;\\mu_2,\\sigma_2^2)\\), \\(\\pi_1+\\pi_2=1\\)</div>
<div class="sol-step"><strong>(b)</strong> C1: \\(\\mu_1=22.4\\), \\(\\sigma_1^2\\approx10.3\\); C2: \\(\\mu_2=40\\), \\(\\sigma_2^2\\approx10.8\\)</div>
<div class="sol-step"><strong>(c)</strong> \\(\\pi_1=\\pi_2=0.5\\) (5 points each)</div>
<div class="sol-step"><strong>(d)</strong> GMM captures two sub-populations (quick vs leisurely) that a single normal would blur.</div>
</div>"""),
    ("Q7", "Confidence interval &amp; white noise [5M]",
     f"""<p><strong>(a) [2M]</strong> Cadence data for 20 healthy men:</p>
{CADENCE_TABLE}
<p>Calculate a 95% confidence interval for population mean cadence.</p>
<p><strong>(b) [3M]</strong> Residual series after forecasting: {{2, −1, 0, 1, −2, 1, −1, 0}}</p>
<ol type="i">
<li>Sample mean and variance</li>
<li>Can this be considered white noise?</li>
</ol>""",
     """<div class="sol-body">
<div class="sol-step"><strong>(a)</strong> \\(\\bar x\\approx0.917\\), \\(s\\approx0.078\\), \\(t_{0.025,19}\\approx2.093\\)</div>
<div class="sol-step">95% CI: \\(0.917 \\pm 2.093\\times0.078/\\sqrt{20}\\) → <strong>[0.880, 0.954]</strong></div>
<div class="sol-step"><strong>(b)(i)</strong> Mean \\(\\approx0\\), variance \\(\\approx1.71\\)</div>
<div class="sol-step"><strong>(b)(ii)</strong> Mean ≈ 0 is consistent with white noise, but series is short; no obvious autocorrelation pattern → <strong>plausibly white noise</strong> (residuals look random).</div>
</div>"""),
    ("Q8", "Two-proportion z-test &amp; F-test for variances [5M]",
     """<p><strong>(a) [3M]</strong> Vaccination rates: City A 180/300, City B 135/250. At 5%, test if proportions differ.</p>
<p><strong>(b) [2M]</strong> Chip thickness (μm):<br>
Line A: 12.5, 12.8, 12.6, 12.9, 12.7, 12.4, 12.6, 12.8 (n=8)<br>
Line B: 12.6, 12.5, 12.7, 12.6, 12.5, 12.6 (n=6)<br>
Test at 5% whether Line A has <em>greater</em> thickness variability than Line B.</p>""",
     """<div class="sol-body">
<div class="sol-step"><strong>(a)</strong> \\(\\hat p_A=0.60\\), \\(\\hat p_B=0.54\\), pooled test \\(z\\approx1.35\\), two-tailed \\(p\\approx0.18>0.05\\) → <strong>no significant difference</strong></div>
<div class="sol-step"><strong>(b)</strong> \\(s_A^2\\approx0.025\\), \\(s_B^2\\approx0.0007\\), \\(F=s_A^2/s_B^2\\approx35.7\\)</div>
<div class="sol-step">One-tailed F-test at 5% → reject \\(H_0\\) → <strong>Line A is significantly more variable</strong> than Line B.</div>
</div>"""),
]


def ec3_section(exam, session, year, label, fname):
    sid = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
    sec = f'<section id="{sid}"><h2>{H.escape(label)}</h2><p class="src">ISM/previous question papers · {H.escape(fname)}</p>'
    for qid, title, stem, sol in EC3_QUESTIONS:
        sec += f"""<div class="q"><div class="badges">{badge(exam, session, year)}</div>
        <h4>{H.escape(qid)} — {title}</h4>
        <div class="stem"><strong>Question:</strong>{stem}</div>
        <div class="sol"><strong>Solution</strong>{format_math_in_html(sol)}</div></div>"""
    sec += "</section>"
    return sid, sec


def june_section():
    sec = (
        '<section id="june2026"><h2>June 2026 EC-2 Regular</h2>'
        '<p class="src">ISM/previous question papers/june 2026/ (screenshots)</p>'
    )
    for qid, title, img, body in JUNE2026_BLOCKS:
        img_path = f"../previous question papers/june 2026/{img}"
        sol = format_math_in_html(body)
        sec += f"""<div class="q"><div class="badges">{badge("Mid Sem","Regular","2026")}</div>
        <h4>{H.escape(qid)} — {H.escape(title)}</h4>
        <img class="exam-img" src="{img_path}" alt="{H.escape(qid)}">
        <div class="sol"><strong>Solution</strong>{sol}</div></div>"""
    sec += "</section>"
    return sec


def build():
    sections = [june_section()]
    nav = ['<a href="#june2026">June 2026 Mid Regular</a>']

    for fname, exam, session, year, label in PAPERS:
        path = BASE / fname
        text = "\n".join(p.get_text() for p in fitz.open(path))
        sid = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
        short = f"{year} {exam.split()[0]} {session}"
        nav.append(f'<a href="#{sid}">{short}</a>')
        sec = f'<section id="{sid}"><h2>{H.escape(label)}</h2><p class="src">ISM/previous question papers · {H.escape(fname)}</p>'
        sols = SOLUTIONS.get(sid, {})
        for qnum, qid, qtext, pdf_sol in split_questions(text):
            if pdf_sol and len(pdf_sol) > 80:
                sol_html = format_math_in_html(
                    f'<div class="sol-body"><p>{H.escape(pdf_sol[:4000]).replace(chr(10), "<br>")}</p></div>'
                )
            else:
                sol_html = sols.get(qnum, "<em>See workbook TYPE section or official PDF.</em>")
                if isinstance(sol_html, str) and sol_html.lstrip().startswith(("<div", "<table")):
                    sol_html = format_math_in_html(sol_html)
                else:
                    sol_html = esc_sol(sol_html)
            sec += f"""<div class="q"><div class="badges">{badge(exam,session,year)}</div>
            <h4>{H.escape(qid)}</h4>
            <div class="stem"><strong>Question:</strong><br>{esc(qtext)}</div>
            <div class="sol"><strong>Solution</strong>{sol_html}</div></div>"""
        sec += "</section>"
        sections.append(sec)

    sid, sec = ec3_section("End Sem", "Regular", "2026", "Feb 2026 End-Sem EC-3 Regular", "Feb 2026 ISM endsem regular QP & answer key.pdf")
    nav.append(f'<a href="#{sid}">2026 End Regular</a>')
    sections.append(sec)

    css_extra = f"""
.formula{{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:1rem;margin:.85rem 0;font-size:.95rem;text-align:center}}
{TABLE_CSS}
{SOL_CSS}
"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ISM Past Papers — AIMLCZC418</title>
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']], processEscapes: true }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }}
}};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js" async></script>
<style>
:root{{--navy:#1e3a5f;--blue:#2563eb;--green:#059669;--purple:#7c3aed;--bg:#f8fafc;--card:#fff;--border:#e2e8f0;--text:#1e293b;--muted:#64748b}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Georgia,"Segoe UI",serif;background:var(--bg);color:var(--text);line-height:1.65}}
header{{background:var(--navy);color:#fff;padding:1.5rem;text-align:center}}
header a{{color:#93c5fd}}
.shell{{display:flex;max-width:1280px;margin:0 auto;width:100%}}
aside{{width:260px;flex-shrink:0;background:var(--card);border-right:1px solid var(--border);padding:.8rem;position:sticky;top:0;height:100vh;overflow-y:auto;font-size:.75rem}}
aside a{{display:block;padding:.3rem .5rem;color:var(--navy);text-decoration:none;border-radius:4px}}
aside a:hover{{background:#eff6ff}}
aside .grp{{font-weight:700;color:var(--green);font-size:.65rem;text-transform:uppercase;margin:.8rem 0 .2rem}}
main{{flex:1;min-width:0;max-width:920px;padding:1.5rem 2rem}}
section{{margin-bottom:2.5rem;padding-bottom:1.5rem;border-bottom:2px solid var(--border)}}
h2{{color:var(--navy);font-size:1.2rem;margin-bottom:.75rem}}
.q h4{{color:var(--navy);font-size:1rem;margin:.25rem 0 .5rem}}
.q{{background:var(--card);border:1px solid var(--border);border-left:3px solid #059669;border-radius:10px;padding:1.25rem;margin:1.35rem 0;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
.badges{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:.65rem}}
.b{{font-size:.68rem;font-weight:700;padding:3px 9px;border-radius:99px;text-transform:uppercase}}
.b.mid{{background:#dbeafe;color:#1d4ed8}} .b.end{{background:#fce7f3;color:#be185d}}
.b.reg{{background:#d1fae5;color:#047857}} .b.makeup{{background:#fef3c7;color:#b45309}}
.b.yr{{background:#f3e8ff;color:#7c3aed}}
.stem{{font-size:.92rem;margin:.75rem 0;padding:.9rem 1.1rem;background:#f8fafc;border:1px solid var(--border);border-radius:8px;line-height:1.7}}
.stem p{{margin:.5rem 0}}
.stem ol,.stem ul{{margin:.5rem 0 .75rem 1.4rem}}
.stem li{{margin:.35rem 0}}
.stem .stem-part{{margin:.65rem 0 .35rem}}
.stem .stem-part:first-child{{margin-top:0}}
.stem .data-table{{margin:.75rem 0}}
.sol{{font-size:.92rem;margin-top:1rem;padding:1.1rem 1.25rem;background:#fff;border:1px solid #e2e8f0;border-left:3px solid #059669;border-radius:8px}}
.sol > strong{{display:block;font-size:.75rem;text-transform:uppercase;color:#047857;margin-bottom:.75rem}}
.src{{font-size:.78rem;color:var(--muted);margin-bottom:.6rem}}
.exam-img{{max-width:100%;border:1px solid var(--border);border-radius:6px;margin:.5rem 0}}
{css_extra}
@media(max-width:800px){{.shell{{flex-direction:column}}aside{{width:100%;height:auto;position:relative}}}}
</style>
</head>
<body>
<header>
<h1>ISM Past Papers — 2025–2026</h1>
<p><a href="index.html">← Hub</a> · AIMLCZC418 · Mid &amp; End Sem</p>
</header>
<div class="shell">
<aside>
<div class="grp">Legend</div>
<div class="badges"><span class="b mid">Mid Sem</span><span class="b end">End Sem</span></div>
<div class="badges"><span class="b reg">Regular</span><span class="b makeup">Makeup</span></div>
<div class="grp">Papers</div>
{"".join(nav)}
</aside>
<main>
{"".join(sections)}
<p style="color:var(--muted);font-size:.82rem;margin-top:2rem"><a href="ISM_Theory_Guide.html">Theory Guide</a> · <a href="ISM_Revision_Sheet.html">Revision Sheet</a></p>
</main>
</div>
</body>
</html>"""
    OUT.write_text(html, encoding="utf-8")
    print("Wrote", OUT, "with", html.count('class="q"'), "questions")


if __name__ == "__main__":
    build()
