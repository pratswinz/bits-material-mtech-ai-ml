#!/usr/bin/env python3
"""Rebuild ML_PYQ_Workbook.html — detailed questions + collapsible solutions."""
import re
import shutil
from pathlib import Path

from workbook_format import TOGGLE_CSS, TOGGLE_JS, apply_prompts, extract_q_blocks, wrap_q_block

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ML_PYQ_Workbook.html"
JUNE_SRC = Path("/Volumes/disc 2/bits pilani/ML/questions/MidSem/2026-06_Regular")
EXAM_IMG = ROOT / "assets/exam-2026-06"

HEADER_CSS = """
header{background:#fff;color:var(--text);border-bottom:1px solid var(--border);padding:1.4rem 1.5rem;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.04)}
header h1{color:var(--navy);font-size:1.35rem;margin:0 0 .25rem}
header p{color:var(--muted);margin:0;font-size:.88rem}
header a{color:var(--blue)}
"""

IMG_MAP = [
    ("Q1.jpeg", "Q1.jpeg"),
    ("Q2.jpeg", "Q2.jpeg"),
    ("Q3.jpeg", "Q3.jpeg"),
    ("Q4.jpeg", "Q4.jpeg"),
    ("Q5.jpeg", "Q5.jpeg"),
]


def sync_images():
    EXAM_IMG.mkdir(parents=True, exist_ok=True)
    for src_name, dst_name in IMG_MAP:
        src = JUNE_SRC / src_name
        if src.exists():
            shutil.copy2(src, EXAM_IMG / dst_name)


def unwrap_wrapped_inner(inner: str) -> str:
    """Strip q-stem / sol-toggle wrapper back to flat question content."""
    s = inner.strip()
    if s.startswith('<div class="q-stem">') and "sol-toggle" not in s and s.endswith("</div>"):
        return s[len('<div class="q-stem">') : -len("</div>")]
    if "sol-toggle" not in s:
        return inner
    if not s.startswith('<div class="q-stem">'):
        return inner
    det = s.find('<details class="sol-toggle">')
    if det == -1:
        return inner
    stem_part = s[:det].rstrip()
    if not stem_part.endswith("</div>"):
        return inner
    stem = stem_part[len('<div class="q-stem">') : -len("</div>")]
    body_open = s.find('<div class="sol-body">', det)
    if body_open == -1:
        return inner
    body_open += len('<div class="sol-body">')
    det_close = s.rfind("</details>")
    if det_close == -1:
        return inner
    body_close = s.rfind("</div>", body_open, det_close)
    if body_close == -1:
        return inner
    sol = s[body_open:body_close]
    return stem + sol


def flatten_toggles(html: str) -> str:
    """Unwrap prior build so rebuild is idempotent."""
    if "sol-toggle" not in html:
        return html
    blocks = extract_q_blocks(html)
    if not blocks:
        return html
    out = []
    last = 0
    for start, end, inner in blocks:
        flat = unwrap_wrapped_inner(inner)
        out.append(html[last:start] + f'<div class="q">{flat}</div>')
        last = end
    out.append(html[last:])
    return "".join(out)


def fix_images(html: str) -> str:
    replacements = [
        ("../questions/MidSem/2026-06_Regular/Q1.jpeg", "assets/exam-2026-06/Q1.jpeg"),
        ("../questions/june mid sem regular 2026/WhatsApp Image 2026-06-21 at 11.43.21.jpeg", "assets/exam-2026-06/Q1.jpeg"),
        ("../questions/june mid sem regular 2026/WhatsApp Image 2026-06-21 at 11.43.22.jpeg", "assets/exam-2026-06/Q2.jpeg"),
        ("../questions/june mid sem regular 2026/WhatsApp Image 2026-06-21 at 11.43.23.jpeg", "assets/exam-2026-06/Q3.jpeg"),
        ("../questions/june mid sem regular 2026/WhatsApp Image 2026-06-21 at 11.43.24.jpeg", "assets/exam-2026-06/Q4.jpeg"),
        ("../questions/june mid sem regular 2026/WhatsApp Image 2026-06-21 at 11.43.21 (1).jpeg", "assets/exam-2026-06/Q5.jpeg"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    return html


def fix_theta(html: str) -> str:
    return html.replace("\t" + "heta", r"\theta")


def inject_sol_css(html: str) -> str:
    """Patch solution formatting CSS into existing workbook."""
    marker = ".sol-body .sol-part{"
    if marker in html:
        return html
    block = """
.sol-body{line-height:1.75}
.sol-body p{margin:.45rem 0}
.sol-body .sol-part{margin:1.1rem 0;padding:.85rem 0 .5rem;border-bottom:1px dashed var(--border)}
.sol-body .sol-part:last-child{border-bottom:none;margin-bottom:0}
.sol-body .part-head{font-weight:700;color:var(--navy);font-size:.92rem;margin:0 0 .55rem}
.sol-body .sol-lines{margin:.35rem 0 .5rem 1.35rem}
.sol-body .sol-lines li{margin:.35rem 0}
.sol-body .calc-block{background:#f8fafc;border-left:3px solid var(--blue);padding:.55rem .85rem;margin:.55rem 0;border-radius:0 6px 6px 0}
.sol-body .calc-line{margin:.25rem 0}
.sol-body .sol-table{margin:.65rem 0}
.sol-body .ans p{margin:.35rem 0}
"""
    anchor = ".sol-body .step,.sol-body .ans"
    if anchor in html:
        return html.replace(anchor, block.strip() + "\n" + anchor)
    return html.replace(".sol-body{padding:1rem 1.15rem 1.2rem}", block.strip())


def inject_css_js(html: str) -> str:
    if ".sol-toggle" not in html:
        html = html.replace(
            ".tag{display:inline-block",
            TOGGLE_CSS + ".tag{display:inline-block",
        )
    html = re.sub(
        r"header\{[^}]+\}\s*header h1\{[^}]+\}\s*header p\{[^}]+\}\s*header a\{[^}]+\}",
        HEADER_CSS.strip(),
        html,
        count=1,
    )
    html = re.sub(
        r"header h1\{font-size:1\.4rem\}\s*header p\{font-size:[^}]+\}\s*header a\{color:#93c5fd\}\s*",
        "",
        html,
    )
    if "toggleAllSolutions" not in html:
        html = html.replace("</body>", TOGGLE_JS + "\n</body>")
    if "Expand all solutions" not in html:
        html = html.replace(
            "<h1>ML PYQ Workbook",
            '<div class="toolbar">'
            '<button type="button" onclick="toggleAllSolutions(true)">Expand all solutions</button>'
            '<button type="button" onclick="toggleAllSolutions(false)">Collapse all</button>'
            "</div>\n<h1>ML PYQ Workbook",
        )
    return html


def wrap_midsem_section(html: str) -> str:
    m = re.search(r'(<section id="midsem">)(.*?)(</section>)', html, re.S)
    if not m:
        return html
    body = m.group(2)
    if "Ridge &amp; Lasso for RR-CHD" in body:
        return html
    if "<h3>Ridge — Iteration 1</h3>" not in body:
        return html

    head, _, tail = body.partition("<h3>Ridge — Iteration 1</h3>")
    r1, _, rest = tail.partition("<h3>Ridge — Iteration 2")
    r2, _, rest2 = rest.partition("<h3>Lasso — Final")
    lasso = rest2

    prompt = r"""<div class="q-prompt"><p><strong>Question.</strong> Ridge &amp; Lasso for RR-CHD risk from Diastolic BP (\(x_1\)) and BMI (\(x_2\)). Initial \(w_0=5\), \(w_1=w_2=-0.03\), \(\alpha=0.02\), \(\lambda=5\), \(m=3\). Using the patient table below, perform <strong>2 Ridge iterations</strong> then <strong>2 Lasso iterations</strong>.</p></div>"""

    new_body = (
        head
        + prompt
        + wrap_q_block("<h3>Ridge — Iteration 1</h3>" + r1)
        + wrap_q_block("<h3>Ridge — Iteration 2 → final</h3>" + r2)
        + wrap_q_block("<h3>Lasso — Final after 2 iter</h3>" + lasso)
    )
    return html[: m.start()] + m.group(1) + new_body + m.group(3) + html[m.end() :]


def clean_workbook_source(html: str) -> str:
    """Move answer leaks out of question stems into solution bodies."""
    html = html.replace(
        '<p class="src">L1 vs L2 — many irrelevant features → <strong>Lasso (L1)</strong> zeros them out</p>',
        '<p class="src">Regularization — L1 vs L2 (practice)</p>',
    )
    html = html.replace(
        '<p class="src">Overfit logistic with large weights → add L2/L1, reduce features, tune λ via CV</p>',
        '<div class="step">(a) <strong>Lasso (L1)</strong> zeros irrelevant weights → feature selection. '
        "Ridge shrinks but rarely zeros.</div>\n"
        '<div class="step">(b) L2/L1 penalize large weights → smoother boundary; tune λ via cross-validation.</div>',
    )
    html = html.replace(
        '<p class="src">4 equal classes → H = log₂(4) = <strong>2 bits</strong></p>',
        '<p class="src">Practice — entropy &amp; leaf labelling</p>',
    )
    html = re.sub(
        r'(<section id="type6">.*?<div class="q-prompt">.*?</div>\s*)'
        r'(<figure class="diagram"><div class="svg-wrap" role="img" aria-label="Ridge vs Lasso">)',
        r'\1<div class="step">(a) <strong>Lasso (L1)</strong> zeros irrelevant weights → feature selection. '
        r"Ridge shrinks but rarely zeros.</div>\n"
        r'<div class="step">(b) L2/L1 penalize large weights → smoother boundary; tune λ via cross-validation.</div>\n\2',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<p class="src">Practice — entropy &amp; leaf labelling</p>\s*<div class="q-prompt">.*?</div>\s*)'
        r'<div class="step">Leaf 3 Yes',
        r'\1<div class="step">(a) 4 equal classes → H = log₂(4) = <strong>2 bits</strong></div>\n'
        r'<div class="step">(b) Leaf 3 Yes',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<section id="type10">.*?<div class="q-prompt">.*?</div>)\s*'
        r'<p>Three models on two datasets.*?</p>\s*',
        r"\1\n",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<section id="type11">.*?<div class="q-prompt">.*?</div>)\s*'
        r'<p>\\\(m=28\\\) samples.*?</p>\s*',
        r"\1\n",
        html,
        count=1,
        flags=re.S,
    )
    html = html.replace("6 Approved, 4 Denied", "5 Approved, 5 Denied")
    html = html.replace("6 Approved / 4 Denied", "5 Approved / 5 Denied")
    html = html.replace("p_{Yes}=0.6,\\ p_{No}=0.4", "p_{Yes}=0.5,\\ p_{No}=0.5")
    html = html.replace("Entropy ≈ 0.971 bits", "Entropy = 1.0 bit")
    html = html.replace("Entropy ≈ 0.971", "Entropy = 1.0")
    html = html.replace("\\partial J/\\partial\\theta_3 = -12", "\\partial J/\\partial\\theta_2 = -12")
    html = html.replace("\\partial J/\\partial\\theta_3=-12", "\\partial J/\\partial\\theta_2=-12")
    html = html.replace("\\theta_3 \\leftarrow \\theta_3 + 12\\alpha", "\\theta_2 \\leftarrow \\theta_2 + 12\\alpha")
    html = html.replace("increasing \\(\\theta_3\\)", "increasing \\(\\theta_2\\)")
    html = html.replace("(Bonus) Split on", "(ii) Split on")
    html = html.replace(
        r"\(H = -0.6\log_2(0.6) - 0.4\log_2(0.4) = 0.442 + 0.529\)",
        r"\(H = -0.5\log_2(0.5) - 0.5\log_2(0.5) = 1.0\) bit",
    )
    html = html.replace("IG = 1.0 − 0.361 = 0.639", "IG = 1.0 − 0 = 1.0")
    html = html.replace("No loan branch: 5 Yes, 0 No → H=0 · Has loan: 1 Yes, 4 No → H≈0.722", "No loan: 5 Yes, 0 No → H=0 · Has loan: 0 Yes, 5 No → H=0")
    html = html.replace("Weighted H = 0.361 · <strong>IG = 1.0 − 0.361 = 0.639</strong>", "<strong>IG = 1.0 − 0 = 1.0 bit</strong> (perfect split)")
    return html


def fix_malformed_html(html: str) -> str:
    """Repair known bad patterns from older workbook versions."""
    html = re.sub(
        r'<p class="src">([^<]*(?:<strong>[^<]*</strong>[^<]*)*)</div>',
        r'<p class="src">\1</p>',
        html,
    )
    html = html.replace("\boldsymbol", r"\boldsymbol")
    return html


def validate_html(html: str) -> list[str]:
    issues = []
    if html.count('<div class="q">') != html.count('</details>') + html.count('<div class="q"><div class="q-stem">') - html.count("sol-toggle"):
        pass  # rough check only
    if re.search(r'<div class="q-stem">(?!.*?<div class="q-prompt">).*?<table\b', html, re.S):
        issues.append("answer table visible in q-stem (outside q-prompt)")
    if re.search(r'<div class="q-stem">(?!.*?<div class="q-prompt">).*?<div class="(?:step|ans)"', html, re.S):
        issues.append("solution step visible in q-stem (outside q-prompt)")
    if re.search(r'<div class="q-stem"><p\s*$', html, re.M):
        issues.append("unclosed <p> in q-stem")
    if 'class="src">' in html and re.search(r'class="src">[^<]*</div>', html):
        issues.append("src paragraph closed with </div>")
    if re.search(r"<div class=\"q-stem\"><p\s*\n<div class=\"q-prompt\">", html):
        issues.append("broken q-stem/p before q-prompt")
    return issues


def build():
    sync_images()
    html = OUT.read_text(encoding="utf-8")
    html = fix_malformed_html(html)
    html = flatten_toggles(html)
    html = fix_theta(html)
    html = fix_images(html)
    html = clean_workbook_source(html)
    html = apply_prompts(html)
    html = fix_theta(html)
    html = wrap_midsem_section(html)
    html = inject_sol_css(html)
    html = inject_css_js(html)
    issues = validate_html(html)
    if issues:
        print("WARNING:", "; ".join(issues))
    OUT.write_text(html, encoding="utf-8")
    n_q = html.count('<div class="q">')
    n_t = html.count("sol-toggle")
    print(f"Wrote {OUT} — {n_q} questions, {n_t} toggles")


if __name__ == "__main__":
    build()
