#!/usr/bin/env python3
"""Build ISM_Theory_Guide.html from companion docs PDFs — cleaned & formatted."""
import html as H
import re
from pathlib import Path

from math_format import format_math_in_html
from ism_theory_enrich import (
    SECTION_ENRICH,
    SESSION_DIAGRAM,
    clean_section_text,
    formula_strip_html,
    render_enrichment,
    render_session_hero,
)
from ism_theory_format import format_condensed, gist_banner, session_badge
from svg_inline import SVG_WRAP_CSS, reset_uid

ROOT = Path(__file__).resolve().parent
SRC = Path("/Volumes/disc 2/bits pilani/ISM/companion docs")
OUT = ROOT / "ISM_Theory_Guide.html"

SESSIONS = [
    {
        "id": "session1",
        "file": "ISM_Session1_Descriptive_Statistics.pdf",
        "title": "Session 1 — Descriptive Statistics",
        "subtitle": "Centre, spread, shape, box plots, outliers",
        "skip_pages": 2,
        "sections": [
            ("intro", r"Statistics: turning raw numbers into decisions"),
            ("step0", r"Step 0 — Know your data before you touch it"),
            ("step1", r"Step 1 — Where is the centre\? \(mean, median, mode\)"),
            ("step2", r"Step 2 — How spread out is it\? \(range, variance, SD\)"),
            ("step3", r"Step 3 — What is its shape\? \(skew and symmetry\)"),
            ("step4", r"Step 4 — One tidy picture: the five-number summary & box plot"),
            ("summary", r"Putting it all together"),
        ],
    },
    {
        "id": "session2",
        "file": "ISM_Session2_Probability_Basics.pdf",
        "title": "Session 2 — Probability Basics",
        "subtitle": "Sample space, events, axioms, addition rule, counting",
        "skip_pages": 2,
        "sections": [
            ("intro", r'From "what happened" to "what could happen"'),
            ("nested", r"The three nested ideas: sample space, outcome, event"),
            ("building", r"Building new events from old ones"),
            ("me-vs-ind", r"The classic confusion: mutually exclusive vs\. independent"),
            ("axioms", r"What exactly is a probability\?"),
            ("addition", r"The addition rule: don't double-count the overlap"),
            ("counting", r"Counting your way to a probability"),
            ("practice", r"Practice problems"),
        ],
    },
    {
        "id": "session3",
        "file": "ISM_Session3_Conditional_Probability.pdf",
        "title": "Session 3 — Conditional Probability",
        "subtitle": "P(A|B), independence, total probability, tree diagrams",
        "skip_pages": 2,
        "sections": [
            ("intro", r"Probability changes when you learn something"),
            ("conditional", r"Conditional probability: shrinking the world"),
            ("mult", r"The multiplication rule: chaining events together"),
            ("indep", r"Independence: when a clue tells you nothing"),
            ("total", r"Total probability: assemble the whole from clean pieces"),
            ("practice", r"Practice problems"),
        ],
    },
    {
        "id": "session4",
        "file": "ISM_Session4_Bayes_and_NaiveBayes.pdf",
        "title": "Session 4 — Bayes & Naïve Bayes",
        "subtitle": "Bayes theorem, posterior, Naïve Bayes classifier",
        "skip_pages": 1,
        "sections": [
            ("intro", r"The question runs backwards"),
            ("bayes", r"Bayes' theorem, built from what we already know"),
            ("naive", r"From one feature to many: the Naïve Bayes classifier"),
        ],
    },
    {
        "id": "session5",
        "file": "ISM_Session5_Random_Variables.pdf",
        "title": "Session 5 — Random Variables",
        "subtitle": "PMF, expectation, variance, joint/marginal distributions",
        "skip_pages": 1,
        "sections": [
            ("intro", r"Random variables: a number for every outcome"),
            ("discrete", r"Discrete distributions: how the probability is shared out"),
            ("expectation", r"Expected value: the balance point of a distribution"),
            ("continuous", r"Continuous variables: probability becomes area"),
            ("joint", r"Two variables at once: joint, marginal, conditional"),
        ],
    },
    {
        "id": "session6",
        "file": "ISM Session 6 Companion - Probability Distributions.pdf",
        "title": "Session 6 — Probability Distributions",
        "subtitle": "Bernoulli, Binomial, Poisson, Normal, Z-scores, χ²/t/F intro",
        "skip_pages": 1,
        "sections": [
            ("big-idea", r"The big idea: distributions are reusable moulds"),
            ("bernoulli", r"Bernoulli: the atom of randomness"),
            ("binomial", r"Binomial: Bernoulli on repeat"),
            ("poisson", r"Poisson: counting rare events in a window"),
            ("normal", r"Normal: the shape that keeps showing up"),
            ("zscore", r"Z-scores: one table to rule them all"),
            ("approx", r"When Binomial wears the bell"),
            ("inference-trio", r"First hello to the inference trio"),
            ("practice", r"Practice problems from the slides"),
        ],
    },
    {
        "id": "session7",
        "file": "ISM Session 7 Companion - Sampling and Estimation.pdf",
        "title": "Session 7 — Sampling & Estimation",
        "subtitle": "CLT, confidence intervals, sample size, point estimates",
        "skip_pages": 1,
        "sections": [
            ("soup", r"The soup-tasting problem"),
            ("pick-sample", r"How to pick a sample"),
            ("variation", r"Sampling variation"),
            ("sampling-dist", r"The sampling distribution"),
            ("clt", r"The Central Limit Theorem"),
            ("finite", r"Finite populations"),
            ("proportions", r"Proportions ride the same train"),
            ("point-est", r"Point estimates"),
            ("ci", r"Confidence intervals"),
            ("sample-size", r"Designing the study: how big a sample"),
        ],
    },
]

DROP_LINE = re.compile(
    r"^(Session \d+ •|Prof\. Saurabh • ISM|Prepared by Prof\.|"
    r"ISM • SESSION|BITS Pilani|Work Integrated|M\.Tech\.|"
    r"What.s inside|A friendly companion|Making Sense of Data|"
    r"The Language of Chance|Updating Beliefs with|Reasoning Backwards from|"
    r"Putting Numbers on Chance|Centre, Spread|Sample Spaces, Events|"
    r"Conditional Probability, Independence|Bayes' Theorem, Updating|"
    r"Random Variables, Expectation|ISM Companion|Probability Distributions|Sampling and Estimation|"
    r"INTRODUCTION TO STATISTICAL METHODS|Session 6 ·|Session 7 ·|\d+$)",
    re.I,
)

SENTENCE_END = re.compile(r"[.!?:;\"'\)»]$")


def extract_pdf(path: Path, skip_pages: int) -> str:
    import fitz
    doc = fitz.open(path)
    pages = []
    for i in range(skip_pages, len(doc)):
        lines = []
        for line in doc[i].get_text().splitlines():
            s = line.strip()
            if not s or DROP_LINE.match(s):
                continue
            if re.match(r"^\d+$", s):
                continue
            lines.append(s)
        pages.append("\n".join(lines))
    return reflow("\n\n".join(pages))


def reflow(text: str) -> str:
    """Merge PDF line-breaks into paragraphs."""
    text = re.sub(r"(\d)\n(\d)", r"\1\2", text)
    text = re.sub(r"([¯xyμσ])\n", r"\1", text)
    text = re.sub(r"=\n\s*1\n\s*n", "= 1/n", text)
    paras = re.split(r"\n{2,}", text)
    out = []
    for para in paras:
        lines = [ln.strip() for ln in para.split("\n") if ln.strip()]
        if not lines:
            continue
        merged = []
        buf = lines[0]
        for ln in lines[1:]:
            if SENTENCE_END.search(buf) or re.match(
                r"^(Step \d+ —|Definition |Key formula |Worked example |What, why, where|• )",
                ln,
            ):
                merged.append(buf)
                buf = ln
            elif re.match(r"^•\s", ln):
                merged.append(buf)
                merged.append(ln)
                buf = ""
            elif buf.endswith("-"):
                buf = buf[:-1] + ln
            elif re.match(r"^[a-z]\)$", buf) or re.match(r"^[ivx]+\)$", buf, re.I):
                merged.append(buf)
                buf = ln
            else:
                buf = buf + " " + ln
        if buf:
            merged.append(buf)
        out.append("\n".join(merged))
    return "\n\n".join(out)


def slice_sections(full: str, sections_spec: list) -> list:
    """Return [(id, title, body), ...] using regex markers."""
    hits = []
    for sid, pattern in sections_spec:
        m = re.search(pattern, full, re.I)
        if m:
            hits.append((m.start(), sid, pattern, m.group(0).strip()))
    hits.sort(key=lambda x: x[0])
    result = []
    for i, (start, sid, pattern, title) in enumerate(hits):
        end = hits[i + 1][0] if i + 1 < len(hits) else len(full)
        body = full[start + len(title) : end].strip()
        body = re.sub(r"^[\n\s\d]+", "", body)
        if len(body) > 60:
            result.append((sid, title, body))
    return result


def esc_para(text: str) -> str:
    return H.escape(text.strip())


def _format_prose(text: str) -> str:
    """Paragraphs and bullets only (no nested callouts). Break long paragraphs."""
    if not text or not text.strip():
        return ""
    text = clean_section_text(text)
    
    # Split on sentence boundaries to keep paragraphs short
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z"])', text)
    
    html = []
    current_para = []
    para_length = 0
    
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        
        # Start bullet list if found
        if sent.startswith("•"):
            if current_para:
                html.append(f"<p>{format_math_in_html(H.escape(' '.join(current_para)))}</p>")
                current_para = []
                para_length = 0
            sent = re.sub(r"^•\s*", "", sent)
            html.append(f"<ul><li>{format_math_in_html(H.escape(sent))}</li></ul>")
            continue
        
        # Accumulate sentences, but break into new paragraph every ~400 chars or 4 sentences
        current_para.append(sent)
        para_length += len(sent)
        
        if para_length > 320 or len(current_para) > 3:
            html.append(f"<p>{format_math_in_html(H.escape(' '.join(current_para)))}</p>")
            current_para = []
            para_length = 0
    
    if current_para:
        html.append(f"<p>{format_math_in_html(H.escape(' '.join(current_para)))}</p>")
    
    return "".join(html)


def format_block(text: str) -> str:
    """Turn reflowed section text into structured HTML."""
    text = clean_section_text(text)
    chunks = re.split(
        r"\n(?=• )|\n(?=Definition \d+\.\d+:)|\n(?=Key formula \d+\.\d+:)|\n(?=Worked example \d+\.\d+:)",
        text,
    )
    html = []
    bullet_buf = []

    def flush_bullets():
        nonlocal bullet_buf
        if bullet_buf:
            items = []
            for b in bullet_buf:
                b = b.strip()
                if len(b) < 4:
                    continue
                if re.match(r"^\d+$", b):
                    continue
                items.append(f"<li>{format_math_in_html(H.escape(b))}</li>")
            if items:
                html.append("<ul>" + "".join(items) + "</ul>")
            bullet_buf = []

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk or len(chunk) < 3:
            continue
        if chunk.startswith("•"):
            chunk = re.sub(r"^•\s*", "", chunk)
            parts = re.split(
                r"(?<=[.!?])\s+(?=[A-Z])|(?<=\))\s+(?=[A-Z][a-z]+ —)",
                chunk,
            )
            for s in parts:
                s = s.strip()
                if s and len(s) > 8:
                    bullet_buf.append(s)
            continue
        flush_bullets()

        if chunk.startswith("Definition "):
            m = re.match(r"(Definition \d+\.\d+:.*?)(?:\n|$)(.*)", chunk, re.S)
            title = m.group(1).strip() if m else chunk.split("\n", 1)[0]
            rest = m.group(2).strip() if m and m.group(2) else ""
            if " For data" in title:
                bits = title.split(" For data", 1)
                title, rest = bits[0].strip(), ("For data" + bits[1] + "\n" + rest).strip()
            title = re.sub(r"(Definition \d+\.\d+:)\s*(.+)", r"\1 \2", title)
            if len(title) > 120 and " — " in title:
                title, extra = title[:120].rsplit(" ", 1)[0] + "…", title
                rest = extra + "\n" + rest if rest else extra
            html.append(
                f'<div class="callout concept"><div class="callout-label">Definition</div>'
                f"<p><strong>{format_math_in_html(H.escape(title))}</strong></p>"
                f"{_format_prose(rest)}</div>"
            )
            continue
        if chunk.startswith("Key formula "):
            m = re.match(r"(Key formula \d+\.\d+:.*?)(?:\n|$)(.*)", chunk, re.S)
            title = m.group(1).strip() if m else chunk
            rest = m.group(2).strip() if m and m.group(2) else ""
            inner = format_math_in_html(f"<p>{H.escape(rest).replace(chr(10), '<br>')}</p>") if rest else ""
            html.append(
                f'<div class="callout formula-box"><div class="callout-label">Key formula</div>'
                f"<p><strong>{format_math_in_html(H.escape(title))}</strong></p>{inner}</div>"
            )
            continue
        if chunk.startswith("Worked example "):
            m = re.match(r"(Worked example \d+\.\d+:.*?)(?:\n|$)(.*)", chunk, re.S)
            title = m.group(1).strip() if m else chunk.split("\n", 1)[0]
            rest = m.group(2).strip() if m and m.group(2) else ""
            html.append(
                f'<div class="callout worked-example"><div class="callout-label">Worked example</div>'
                f"<p><strong>{format_math_in_html(H.escape(title))}</strong></p>"
                f"{_format_prose(rest)}</div>"
            )
            continue
        if re.match(r"^What, why, where", chunk, re.I):
            html.append(
                f'<div class="callout exam-tip"><div class="callout-label">What · Why · Where</div>'
                f"<p>{format_math_in_html(H.escape(chunk).replace(chr(10), '<br>'))}</p></div>"
            )
            continue
        # Split long run-on paragraphs at sentence boundaries
        if len(chunk) > 400 and chunk.count(". ") > 2:
            sents = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'])", chunk)
            for s in sents:
                s = s.strip()
                if len(s) > 20:
                    html.append(f"<p>{format_math_in_html(H.escape(s))}</p>")
        else:
            html.append(f"<p>{format_math_in_html(H.escape(chunk).replace(chr(10), '<br>'))}</p>")

    flush_bullets()
    return "".join(html)


THEORY_CSS = """
:root{--bg:#f1f5f9;--paper:#fff;--text:#1e293b;--muted:#64748b;--accent:#2563eb;--border:#e2e8f0;--sidebar-w:260px;--radius:12px}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;font-size:15px}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.55;color:var(--text);background:var(--bg)}
a{color:#2563eb;text-decoration:none;font-weight:500}a:hover{text-decoration:underline}
.page{display:flex;min-height:100vh;max-width:1280px;margin:0 auto;background:var(--paper);box-shadow:0 4px 24px rgba(0,0,0,.06)}
#sidebar{width:var(--sidebar-w);flex-shrink:0;background:#1e293b;color:#e2e8f0;border-right:none;padding:1rem .75rem 2rem;font-size:.74rem;position:sticky;top:0;height:100vh;overflow-y:auto}
#sidebar .brand{font-weight:800;font-size:.9rem;color:#fff;margin-bottom:.15rem}
#sidebar .brand-sub{font-size:.68rem;color:#94a3b8;margin-bottom:1rem}
#sidebar .brand-sub a{color:#67e8f9}
#sidebar nav h3{font-size:.58rem;text-transform:uppercase;letter-spacing:.1em;color:#64748b;margin:1rem 0 .3rem;font-weight:700}
#sidebar ol{list-style:none;padding:0;margin:0}
#sidebar li a{display:block;padding:.3rem .55rem;border-radius:6px;color:#cbd5e1;line-height:1.3}
#sidebar li a:hover{background:#334155;color:#fff;text-decoration:none}
#sidebar li.sub a{padding-left:1.1rem;font-size:.68rem;color:#94a3b8}
#sidebar li.guide-link a{color:#6ee7b7}
#content{flex:1;min-width:0;padding:1.5rem 2rem 3rem;max-width:780px}
.hero{background:linear-gradient(135deg,#1e3a8a 0%,#7c3aed 50%,#059669 100%);color:#fff;padding:1.6rem 1.8rem;border-radius:var(--radius);margin-bottom:1.5rem;box-shadow:0 8px 24px rgba(37,99,235,.25)}
.hero h1{margin:0 0 .35rem;font-size:1.45rem;color:#fff}
.hero .meta{font-size:.82rem;opacity:.92;margin:0}
h2.session-header{font-size:1.2rem;margin:2rem 0 .5rem;padding:.85rem 1.1rem;border-radius:var(--radius);border:none;display:flex;align-items:center;gap:.6rem;flex-wrap:wrap}
h2#overview{margin-top:0;font-size:1.2rem;border-bottom:3px solid #2563eb;padding-bottom:.4rem;color:#1e3a8a}
.src{font-size:.75rem;color:var(--muted);margin:0 0 1rem}
.lead{font-size:.92rem;color:var(--muted);margin-bottom:1rem}
.sess-badge{font-size:.65rem;font-weight:800;padding:3px 10px;border-radius:99px;text-transform:uppercase;letter-spacing:.04em}
.sec-block{border:1px solid var(--border);border-radius:var(--radius);padding:1rem 1.15rem 1.15rem;margin:1.25rem 0;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.04)}
.sec-block h3{margin:0 0 .65rem;font-size:.98rem;color:#1e293b;display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}
.gist-banner{border-left:4px solid;padding:.65rem .9rem;border-radius:0 8px 8px 0;margin:.5rem 0 1rem;font-size:.88rem;line-height:1.45}
.gist-banner strong{color:inherit;opacity:.85;font-size:.72rem;text-transform:uppercase;letter-spacing:.04em;display:block;margin-bottom:.2rem}
.wwwh-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.55rem;margin:.75rem 0}
@media(max-width:640px){.wwwh-grid{grid-template-columns:1fr}}
.wwwh-card{padding:.65rem .75rem;border-radius:8px;font-size:.8rem;line-height:1.4}
.wwwh-card.what{background:#eff6ff;border:1px solid #93c5fd}
.wwwh-card.why{background:#ecfdf5;border:1px solid #6ee7b7}
.wwwh-card.where{background:#f5f3ff;border:1px solid #c4b5fd}
.wwwh-label{display:block;font-size:.62rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.25rem}
.wwwh-card.what .wwwh-label{color:#1d4ed8}
.wwwh-card.why .wwwh-label{color:#047857}
.wwwh-card.where .wwwh-label{color:#6d28d9}
.wwwh-card p{margin:0}
.point-grid{list-style:none;padding:0;margin:.75rem 0;display:grid;gap:.45rem}
.point-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:.55rem .75rem;font-size:.84rem;line-height:1.45;margin:0}
.point-card::before{content:"▸ ";color:#2563eb;font-weight:700}
.mini-card{border-radius:8px;padding:.75rem .9rem;margin:.65rem 0;font-size:.84rem;line-height:1.45}
.mini-label{display:block;font-size:.65rem;font-weight:800;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.35rem}
.mini-card.def{background:#eff6ff;border:1px solid #93c5fd}.mini-card.def .mini-label{color:#1d4ed8}
.mini-card.formula{background:#f5f3ff;border:2px solid #a78bfa}.mini-card.formula .mini-label{color:#6d28d9}
.mini-card.example{background:#fffbeb;border:1px solid #fcd34d}.mini-card.example .mini-label{color:#b45309}
.mini-card.warn{background:#fef2f2;border:1px solid #fca5a5}.mini-card.warn .mini-label{color:#dc2626}
.mini-card.tip{background:#ecfdf5;border:1px solid #6ee7b7}.mini-card.tip .mini-label{color:#047857}
.mini-card.analogy{background:#fdf4ff;border:1px solid #e879f9}.mini-card.analogy .mini-label{color:#a21caf}
.mini-card p{margin:.35rem 0}
.eq-block{font-size:1rem;text-align:center;padding:.4rem;background:#fff;border-radius:6px;margin-top:.3rem}
.formula-strip{background:linear-gradient(135deg,#eff6ff,#fdf4ff);border:2px solid #818cf8;border-radius:var(--radius);padding:.9rem 1rem;margin:.75rem 0}
.formula-strip .f-item{padding:.55rem 0;border-bottom:1px dashed #c7d2fe}
.formula-strip .f-item:last-child{border-bottom:none}
.formula-strip .f-label{font-size:.68rem;font-weight:800;color:#4338ca;text-transform:uppercase;letter-spacing:.05em}
.formula-strip .f-eq{font-size:1rem;margin-top:.25rem;display:block}
.session-visual{background:#fff;border:2px solid #bbf7d0;border-radius:var(--radius);padding:.85rem;margin:.75rem 0 1rem}
.fig-cap{font-size:.78rem;color:var(--muted);margin-top:.45rem;line-height:1.45}
.diagram-img,.svg-wrap svg{width:100%;max-width:100%;height:auto;border-radius:8px;border:1px solid var(--border)}
.key-takeaway{background:linear-gradient(90deg,#fef3c7,#fce7f3);border:2px solid #f59e0b;border-radius:8px;padding:.65rem .85rem;margin:.65rem 0;font-size:.82rem}
.key-takeaway p{margin:0}
.exam-map{background:linear-gradient(135deg,#ecfdf5,#eff6ff);border:2px solid #34d399;border-radius:var(--radius);padding:1rem;margin:1rem 0}
.exam-map h4{color:#047857;font-size:.8rem;margin:0 0 .5rem;text-transform:uppercase;letter-spacing:.05em}
.exam-map ul{margin:0;padding-left:1.2rem;font-size:.85rem}
.exam-map li{margin:.3rem 0}
.session-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:.5rem;margin:1rem 0}
.session-chip{display:block;padding:.55rem .65rem;border-radius:8px;text-align:center;font-size:.75rem;font-weight:600;text-decoration:none;color:inherit;border:2px solid;transition:transform .15s}
.session-chip:hover{transform:translateY(-2px);text-decoration:none}
""" + SVG_WRAP_CSS + """
@media(max-width:900px){.page{flex-direction:column}#sidebar{width:100%;height:auto;position:relative}}
"""


def build():
    from ism_theory_format import SESSION_THEME
    from svg_inline import reset_uid

    reset_uid()
    nav_sessions = ['<li><a href="#overview">Overview</a></li>']

    chips = ""
    for sid, (color, bg, label) in SESSION_THEME.items():
        num = sid.replace("session", "")
        chips += (
            f'<a class="session-chip" href="#{sid}" '
            f'style="background:{bg};border-color:{color};color:{color}">'
            f'S{num} · {H.escape(label)}</a>'
        )

    body = f"""
<section id="overview">
<h2 id="overview">Overview</h2>
<p class="lead">Scannable cards — formulas, diagrams, practice links. Not a PDF dump.</p>
<div class="session-grid">{chips}</div>
<div class="exam-map">
<h4>Exam map</h4>
<ul>
<li><strong>Mid-sem EC-2:</strong> Sessions 1–5 + S6 distributions</li>
<li><strong>End-sem EC-3:</strong> S6–7 + correlation, tests — <a href="ISM_PYQ_Workbook.html">Workbook</a> · <a href="ISM_Past_Papers.html">Papers</a></li>
</ul>
</div>
</section>
"""

    for sess in SESSIONS:
        path = SRC / sess["file"]
        full = extract_pdf(path, sess["skip_pages"])
        slices = slice_sections(full, sess["sections"])
        sid = sess["id"]
        short = sess["title"].split("—")[1].strip()
        color, bg, _ = SESSION_THEME.get(sid, ("#2563eb", "#eff6ff", ""))
        nav_sessions.append(f'<li><a href="#{sid}">{H.escape(short)}</a></li>')
        sub_links = []

        body += (
            f'<section id="{sid}">'
            f'<h2 class="session-header" style="background:{bg};color:{color};border-left:5px solid {color}">'
            f'{session_badge(sid)} {H.escape(sess["title"])}</h2>'
            f'<p class="src">{H.escape(sess["subtitle"])}</p>'
        )
        if SESSION_DIAGRAM.get(sid):
            body += f'<div class="session-visual">{render_session_hero(sid, sess["title"])}</div>'

        if not slices:
            body += f'<div class="sec-block">{format_condensed(full[:4000], sid)}</div>'
        else:
            for sec_id, title, sec_body in slices:
                anchor = f"{sid}-{sec_id}"
                sub_links.append(f'<li class="sub"><a href="#{anchor}">{H.escape(title[:50])}</a></li>')
                body += f'<div class="sec-block" id="{anchor}">'
                body += f'<h3>{H.escape(title)}</h3>'
                body += gist_banner(anchor)
                body += render_enrichment(anchor)
                body += format_condensed(sec_body[:3500], anchor)
                body += "</div>"
        body += "</section>"
        nav_sessions.extend(sub_links)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ISM Theory Guide — AIMLCZC418</title>
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']], processEscapes: true }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }}
}};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js" async></script>
<style>{THEORY_CSS}</style>
</head>
<body>
<div class="page">
<aside id="sidebar">
<div class="brand">ISM Theory Guide</div>
<div class="brand-sub">AIMLCZC418 · <a href="index.html">← Hub</a></div>
<nav>
<h3>Sessions</h3>
<ol>{"".join(nav_sessions)}</ol>
<h3>Also</h3>
<ol>
<li class="guide-link"><a href="ISM_Revision_Sheet.html">Revision Sheet</a></li>
<li class="guide-link"><a href="ISM_Past_Papers.html">Past Papers</a></li>
</ol>
</nav>
</aside>
<main id="content">
<div class="hero">
<h1>Introduction to Statistical Methods</h1>
<p class="meta">Prof. Saurabh companion sessions · Sessions 1–7</p>
</div>
{body}
</main>
</div>
</body>
</html>"""
    OUT.write_text(html, encoding="utf-8")
    print("Wrote", OUT, "—", html.count("<h3"), "sections")


if __name__ == "__main__":
    build()
