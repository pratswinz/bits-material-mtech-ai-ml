"""Structure past-paper solution text for readable HTML."""
import re


def strip_br_prefix(html: str) -> str:
    return re.sub(r"^(?:<br\s*/?>\s*)+", "", html)


def strip_br_suffix(html: str) -> str:
    return re.sub(r"(?:<br\s*/?>\s*)+$", "", html)


def strip_br_edges(html: str) -> str:
    return strip_br_suffix(strip_br_prefix(html.strip()))


SOL_CSS = """
.sol-body{display:flex;flex-direction:column;gap:1rem;padding:.15rem 0}
.sol-h{font-weight:600;color:var(--navy);font-size:.92rem;margin:1.1rem 0 .45rem;padding-bottom:.35rem;border-bottom:1px solid #cbd5e1;line-height:1.35}
.sol-h:first-child{margin-top:0}
.sol-p{margin:.45rem 0;line-height:1.7;color:#334155}
.sol-step{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:.85rem 1rem;margin:.5rem 0;line-height:1.65;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.sol ul{margin:.55rem 0 .75rem 1.5rem;padding:0;list-style:disc}
.sol li{margin:.4rem 0;line-height:1.55}
.sol .marks{color:var(--muted);font-size:.78rem;font-weight:400}
.sol-rubric{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:.9rem 1.1rem;margin-top:.75rem;font-size:.84rem;color:#78350f;line-height:1.6}
.sol-rubric .sol-h{border-bottom:1px solid #fde68a;color:#92400e;margin:0 0 .55rem;padding-bottom:.35rem}
.sol-rubric ul{margin:.35rem 0 0 1.25rem}
.sol .formula{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:1rem 1.15rem;margin:.55rem 0;font-size:1.02rem;line-height:1.7;overflow-x:auto;text-align:center;box-shadow:inset 0 1px 0 #f8fafc}
.sol .formula mjx-container{display:inline-block!important;margin:.25rem 0!important}
"""


def _bullets_to_ul(html: str) -> str:
    if "%%LI%%" not in html:
        return html
    chunks = html.split("%%LI%%")
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


def _trim_embedded_question(html: str) -> str:
    return re.sub(r"(?:<br>|\n)Q\.?\s*\d+[\.\)].*$", "", html, flags=re.I | re.DOTALL)


def _strip_noise(html: str) -> str:
    html = re.sub(r"^(?:Answer:|Answers:|Solution:|<br\s*/?>)+", "", html, flags=re.I)
    return html.strip()


def _strip_repeated_subquestions(html: str) -> str:
    """Remove question stem text accidentally merged into part (b) answers."""
    html = re.sub(
        r"(<strong>b\)</strong>\s*)(?:[^<]|<br\s*/?>)*?(?=1\.\s*Answer:|Answer:\s*Learning)",
        r"\1",
        html,
        flags=re.I,
    )
    return html


def _wrap_dimension_answer(html: str) -> str:
    """Wrap matrix-dimension answers as part (a) step."""
    return re.sub(
        r'^(X is \d+×\d+.*?θ is \d+×\d+.*?(?:<br>If any[^<]+)?)(?=<div class="sol-step"><strong>b\)</strong>)',
        r'<div class="sol-step"><strong>a)</strong> \1</div>',
        html,
        flags=re.I | re.DOTALL,
    )


def _section_headers(html: str) -> str:
    patterns = [
        r"Calculate [^<]{8,90}:",
        r"Select Feature [^<]{5,80}:",
        r"Feature: Exam Preparation Time",
        r"Information Gain:",
        r"Select Feature with Highest Information Gain:",
        r"Conclusion:",
        r"Rubric(?: \(\d+ Marks\))?:",
    ]
    for pat in patterns:
        html = re.sub(
            rf"(?:<br>|^|(?<=</div>)|(?<=</p>))({pat})(?=<br>|$|<p|<ul|<div|The feature|&quot;Exam)",
            r'<div class="sol-h">\1</div>',
            html,
        )
    if "Evaluation:" in html:
        html = re.sub(
            r"(?:<br>|^)(Evaluation:)(?=<br>|$|<p|<ul|<div)",
            r'<div class="sol-rubric"><div class="sol-h">\1</div>',
            html,
            count=1,
        )
    return html


def _wrap_h_if_standalone(match: re.Match) -> str:
    text = match.string
    start = match.start()
    ctx = text[max(0, start - 40):start]
    if re.search(r"IG\([^)]+\)=$", ctx.replace(" ", "")):
        return match.group(0)
    return f'<div class="formula">{match.group(0)}</div>'


def _wrap_formulas(html: str) -> str:
    html = re.sub(
        r"IG\([A-Za-z ]+\)=[^<]{0,160}",
        r'<div class="formula">\g<0></div>',
        html,
    )
    html = re.sub(
        r"p\([A-Za-z]+\)=[^<]+(?:,\s*p\([A-Za-z]+\)=[^<]+)+",
        r'<div class="formula">\g<0></div>',
        html,
    )
    html = re.sub(
        r"H\(S\)[^<]{0,160}",
        _wrap_h_if_standalone,
        html,
    )
    html = re.sub(
        r"( Entropy =[^<]{10,120})(?=<div class=\"sol-h\">|<br>|$)",
        r'<div class="formula">\1</div>',
        html,
    )
    html = re.sub(
        r"(Gain = )(<div class=\"formula\">H\(S\)[^<]+</div>)",
        r'<div class="formula">\1\2</div>',
        html,
    )
    return _flatten_nested_formulas(html)


def _flatten_nested_formulas(html: str) -> str:
    prev = None
    while prev != html:
        prev = html
        html = re.sub(
            r'<div class="formula">([^<]*)<div class="formula">([^<]*)</div></div>',
            r'<div class="formula">\1\2</div>',
            html,
        )
    html = re.sub(r'<div class="formula"><div class="formula">', r'<div class="formula">', html)
    return html


def _wrap_orphan_text(html: str) -> str:
    """Wrap loose text sitting between structural blocks."""
    html = re.sub(
        r'(?<=</div>)(Feature: Exam Preparation Time)(?=<div class="formula">| Entropy)',
        r'<div class="sol-h">\1</div>',
        html,
    )
    html = re.sub(
        r'(<div class="sol-h">[^<]+</div>)((?!Feature: )[^<\s][^<]{4,240}?)(?=<ul>|<div class="formula">|<div class="sol-h">|<br>Total |<br>Excellent:|<br>\d+\.)',
        r'\1<p class="sol-p">\2</p>',
        html,
    )
    html = re.sub(
        r'(</ul>)(?!<p)([^<]{10,280}?)(?=<div class="sol-h">|<div class="formula">)',
        r'\1<p class="sol-p">\2</p>',
        html,
    )
    html = re.sub(
        r'(Feature: Participation[^<]{10,200})(?=<div class="sol-h">|Select Feature)',
        r'<p class="sol-p">\1</p>',
        html,
    )
    html = re.sub(
        r'(Select Feature with Highest Information Gain:<br>)(The feature &quot;[^<]{10,200})',
        r'\1<p class="sol-p">\2</p>',
        html,
    )
    return html


def _split_parts_before_bullets(html: str) -> str:
    """Split (a)/(b)/(c) sections before bullet lists merge across parts."""
    html = re.sub(
        r"(?:<br>|^)\(([a-d])\)\s+",
        r"%%SOLPART(\1)%%",
        html,
    )
    if "%%SOLPART(" not in html:
        return html
    chunks = re.split(r"%%SOLPART\(([a-d])\)%%", html)
    out = []
    preamble = strip_br_edges(chunks[0])
    if preamble:
        out.append(preamble)
    for i in range(1, len(chunks), 2):
        label = chunks[i]
        body = chunks[i + 1] if i + 1 < len(chunks) else ""
        body = _bullets_to_ul(strip_br_edges(body))
        body = strip_br_edges(body)
        out.append(f'<div class="sol-step"><strong>({label})</strong> {body}</div>')
    return "".join(out)


def _split_parts(html: str) -> str:
    """Split merged a) b) c) parts into sol-step blocks."""
    if '<div class="sol-step"><strong>(' in html:
        return html
    html = re.sub(
        r"(?:<br>|^)([a-d]\)\s+)(?=[^<])",
        r'<br><span class="sol-part">\1</span>',
        html,
    )
    parts = re.split(r'<span class="sol-part">([a-d]\)\s*)</span>', html)
    if len(parts) <= 1:
        return html
    out = [parts[0]]
    for i in range(1, len(parts), 2):
        label, body = parts[i], parts[i + 1] if i + 1 < len(parts) else ""
        body = strip_br_edges(body)
        out.append(f'<div class="sol-step"><strong>{label.strip()}</strong> {body}</div>')
    return "".join(out)


def _numbered_steps(html: str) -> str:
    html = re.sub(
        r"(?:<br>|^)(\d+\.\s+(?:Answer:)?[^<]{8,180}?)(?=<br>\d+\.|<div |<br>[a-d]\)|$)",
        r'<div class="sol-step">\1</div>',
        html,
    )
    # Fix PDF line breaks like "1.<br>{Young,..."
    html = re.sub(
        r"(?:<br>|^)(\d+\.)<br>(\{[^<]{5,80}\})",
        r'<div class="sol-step">\1 \2</div>',
        html,
    )
    return html


def _format_rubric(html: str) -> str:
    if '<div class="sol-rubric">' not in html:
        return html
    html = re.sub(
        r'(<div class="sol-rubric"><div class="sol-h">Evaluation:</div>)([^<]+(?:<br>[^<]+)*)',
        lambda m: m.group(1) + _rubric_body(m.group(2)),
        html,
        count=1,
    )
    if html.count('<div class="sol-rubric">') > html.count("</div></div>"):
        html += "</div>"
    return html


def _rubric_body(text: str) -> str:
    lines = [ln.strip() for ln in text.split("<br>") if ln.strip()]
    if len(lines) <= 1:
        return f'<p class="sol-p">{lines[0] if lines else ""}</p></div>'
    items = "".join(f"<li>{ln}</li>" for ln in lines)
    return f"<ul>{items}</ul></div>"


def _wrap_marks(html: str) -> str:
    return re.sub(
        r"\[(\d+(?:\.\d+)?\s*marks?[^\]]*)\]",
        r'<span class="marks">[\1]</span>',
        html,
        flags=re.I,
    )


def _cleanup_br(html: str) -> str:
    html = re.sub(r"(?:<br\s*/?>\s*){2,}", "<br>", html)
    html = re.sub(r"<br>(?=<div )", "", html)
    html = re.sub(r"</div><br>", "</div>", html)
    html = re.sub(r"<br></div>", "</div>", html)
    html = re.sub(r'<br>(?=<p class="sol-p">)', "", html)
    return html


def _split_br_paragraphs(html: str) -> str:
    """Turn long <br>-only runs into sol-p blocks when no structure yet."""
    if any(
        x in html
        for x in (
            '<ul>',
            '<div class="sol-h">',
            '<div class="sol-step">',
            '<div class="formula">',
            '<p class="sol-p">',
        )
    ):
        return html
    chunks = [c.strip() for c in re.split(r"<br>", html) if c.strip()]
    if len(chunks) <= 1:
        return html
    return "".join(f'<p class="sol-p">{c}</p>' for c in chunks)


def _paragraphs(html: str) -> str:
    if any(
        x in html
        for x in (
            "<ul>",
            '<div class="sol-h">',
            '<div class="sol-step">',
            '<div class="formula">',
        )
    ):
        html = re.sub(
            r"(?<![>])((?:The target|The feature|Similarly|Rather than|If any|Since the|First,)[^<]{20,400})(?=<div |<ul>|$)",
            r'<p class="sol-p">\1</p>',
            html,
        )
        return html
    chunks = [c.strip() for c in re.split(r"<br>", html) if c.strip()]
    if len(chunks) <= 3:
        return f'<p class="sol-p">{" ".join(chunks)}</p>' if chunks else html
    return "".join(f'<p class="sol-p">{c}</p>' for c in chunks)


def prepare_solution_raw(text: str) -> str:
    text = re.split(r"\nQ\.?\s*\d+[\.\)]", text)[0]
    text = text.replace("\uf0b7", "%%LI%%").replace("•", "%%LI%%")
    return text


def format_solution(html: str) -> str:
    if not html:
        return html
    html = _trim_embedded_question(html)
    html = _strip_noise(html)
    html = _split_parts_before_bullets(html)
    if '<div class="sol-step"><strong>(' not in html:
        html = _bullets_to_ul(html)
    html = _section_headers(html)
    html = _wrap_formulas(html)
    html = _wrap_orphan_text(html)
    html = _numbered_steps(html)
    html = _split_parts(html)
    html = _strip_repeated_subquestions(html)
    html = _wrap_dimension_answer(html)
    html = _wrap_marks(html)
    html = _cleanup_br(html)
    html = _paragraphs(html)
    html = _split_br_paragraphs(html)
    html = _wrap_orphan_text(html)
    html = _section_headers(html)
    html = _format_rubric(html)
    html = _cleanup_br(html)
    return f'<div class="sol-body">{html}</div>'
