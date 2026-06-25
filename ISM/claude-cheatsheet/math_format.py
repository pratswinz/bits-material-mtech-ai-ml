"""Convert plain-text ML formulas to MathJax LaTeX."""
import re

_GREEK = {
    "θ": r"\theta",
    "Θ": r"\Theta",
    "α": r"\alpha",
    "β": r"\beta",
    "λ": r"\lambda",
    "σ": r"\sigma",
    "μ": r"\mu",
    "∂": r"\partial",
    "−": "-",
    "×": r"\times",
    "≈": r"\approx",
    "→": r"\to",
    "≤": r"\le",
    "≥": r"\ge",
    "·": r"\cdot",
}


def _has_mathjax(text: str) -> bool:
    t = text.strip()
    return bool(re.search(r"\\[\(\[]|\$\$?", t)) or (
        (t.startswith(r"\(") and t.endswith(r"\)"))
        or (t.startswith(r"\[") and t.endswith(r"\]"))
    )


def _greek(text: str) -> str:
    for char, latex in _GREEK.items():
        text = text.replace(char, latex)
    return text


def _logs(text: str) -> str:
    text = re.sub(
        r"LOG\(([^,]+),2\)",
        lambda m: f"\\log_2({m.group(1)})",
        text,
        flags=re.I,
    )
    text = re.sub(r"(?<!\\)log_?2\s*\(", lambda _m: "\\log_2(", text, flags=re.I)
    text = re.sub(
        r"log\s*\(\s*p\s*/\s*1\s*-\s*p\s*\)",
        r"\\log\\frac{p}{1-p}",
        text,
        flags=re.I,
    )
    return text


def _fracs(text: str) -> str:
    return re.sub(
        r"(?<![\\/\d])(\d+)\/(\d+)(?![\\/\d])",
        lambda m: f"\\frac{{{m.group(1)}}}{{{m.group(2)}}}",
        text,
    )


def _ig_label(match: re.Match) -> str:
    inner = match.group(1)
    if inner.startswith(r"\text{") or inner == "S":
        return match.group(0)
    return f"\\mathrm{{IG}}(\\text{{{inner}}})"


def _labels(text: str) -> str:
    text = re.sub(
        r"p\(([^)]+)\)",
        lambda m: f"p(\\text{{{m.group(1)}}})",
        text,
    )
    text = text.replace("H(S)", "§HS§")
    text = re.sub(
        r"H\(([^)]+)\)",
        lambda m: f"H(\\text{{{m.group(1)}}})",
        text,
    )
    text = text.replace("§HS§", "H(S)")
    text = text.replace("IG(", "\\mathrm{IG}(")
    text = re.sub(r"\\mathrm\{IG\}\(([^)]+)\)", _ig_label, text)
    return text


def _entropy_prefix(text: str) -> str:
    return re.sub(r"^\s*Entropy\s*=", r"H =", text.strip(), flags=re.I)


def _matrix_dims(text: str) -> str:
    text = re.sub(
        r"\bX\s+is\s+(\d+)\s*\\times\s*(\d+)\b",
        r"\\mathbf{X} \\in \\mathbb{R}^{\1 \\times \2}",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"\by\s+is\s+(\d+)\s*\\times\s*(\d+)\b",
        r"\\mathbf{y} \\in \\mathbb{R}^{\1 \\times \2}",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"\\theta\s+is\s+(\d+)\s*\\times\s*(\d+)\b",
        r"\\boldsymbol{\\theta} \\in \\mathbb{R}^{\1 \\times \2}",
        text,
        flags=re.I,
    )
    return text


def _metrics(text: str) -> str:
    text = re.sub(
        r"\bPrec\s*=\s*TN\s*/\s*\(([^)]+)\)",
        r"\\text{Prec} = \\frac{TN}{\1}",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"\bRec\s*=\s*TN\s*/\s*\(([^)]+)\)",
        r"\\text{Rec} = \\frac{TN}{\1}",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"\bF1\s*=\s*2PR\s*/\s*\(([^)]+)\)",
        r"F_1 = \\frac{2PR}{\1}",
        text,
        flags=re.I,
    )
    text = re.sub(r"\bGain\s*=\s*", lambda _m: "\\mathrm{IG} = ", text, flags=re.I)
    return text


def _sigmoid_logit(text: str) -> str:
    text = re.sub(
        r"p\s*=\s*\\sigma\(z\)\s*=\s*1/1\+e\^\-\(([^)]+)\)",
        r"p = \\sigma(z) = \\frac{1}{1 + e^{-\1}}",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"logit\s*\(\s*p\s*\)\s*=\s*log\s*\(\s*p/1-p\s*\)\s*=\s*([^,\s<]+)",
        r"\\mathrm{logit}(p) = \\log\\frac{p}{1-p} = \1",
        text,
        flags=re.I,
    )
    return text


def _cleanup_ops(text: str) -> str:
    text = re.sub(r"\s*=\s*", " = ", text)
    text = re.sub(r"\s*\+\s*", " + ", text)
    text = re.sub(r"\s*\*\s*", r" \\cdot ", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    return text.strip()


def latexize_plain(text: str) -> str:
    if not text or _has_mathjax(text):
        return text
    text = _entropy_prefix(text)
    text = _greek(text)
    text = _logs(text)
    text = _fracs(text)
    text = _labels(text)
    text = _matrix_dims(text)
    text = _metrics(text)
    text = _sigmoid_logit(text)
    return _cleanup_ops(text)


def wrap_math(text: str) -> str:
    plain = latexize_plain(text.strip())
    if not plain or _has_mathjax(plain):
        return plain
    return f"\\({plain}\\)"


def wrap_display_math(text: str) -> str:
    plain = latexize_plain(text.strip())
    if not plain:
        return plain
    if plain.startswith(r"\(") and plain.endswith(r"\)"):
        plain = plain[2:-2].strip()
    elif plain.startswith(r"\[") and plain.endswith(r"\]"):
        return plain
    if _has_mathjax(plain) and not (plain.startswith(r"\[") and plain.endswith(r"\]")):
        return plain
    return f"\\[{plain}\\]"


def _latexize_mixed(text: str) -> str:
    if _has_mathjax(text):
        return text
    parts = re.split(r"(<[^>]+>)", text)
    out = []
    buf = []
    for part in parts:
        if part.startswith("<"):
            if buf:
                chunk = "".join(buf).strip()
                if chunk:
                    out.append(wrap_math(chunk))
                buf = []
            out.append(part)
        else:
            buf.append(part)
    if buf:
        chunk = "".join(buf).strip()
        if chunk:
            out.append(wrap_math(chunk))
    return "".join(out)


def _convert_formula_inner(inner: str) -> str:
    inner = inner.strip()
    if not inner:
        return inner
    header = ""
    hm = re.match(r"(<h5>[^<]*</h5>)(.*)", inner, re.DOTALL | re.I)
    if hm:
        header, inner = hm.group(1), hm.group(2).strip()
    if not inner:
        return header
    if _has_mathjax(inner):
        return header + inner
    body = _latexize_mixed(inner) if re.search(r"<[^>]+>", inner) else wrap_display_math(inner)
    return header + body


def format_formula_divs(html: str) -> str:
    def repl(match: re.Match) -> str:
        return f'<div class="formula">{_convert_formula_inner(match.group(1))}</div>'

    return re.sub(r'<div class="formula">(.*?)</div>', repl, html, flags=re.DOTALL)


def _inline_math_fragment(html: str) -> str:
    for pat in (
        r"X is \d+×\d+",
        r"y is \d+×\d+",
        r"θ is \d+×\d+",
    ):
        html = re.sub(pat, lambda m: wrap_math(m.group(0)), html, flags=re.I)
    html = re.sub(
        r"(Income = (?:High|Low):<br>)H = [^<]{10,120}",
        lambda m: m.group(1) + wrap_math(m.group(0).split("<br>")[-1]),
        html,
        flags=re.I,
    )
    html = re.sub(
        r"(?<!<div class=\"formula\">)(?<=\d\. )(?:Entropy of parent set:|Weighted entropy after splitting:)<br>(H[^<]{10,100})",
        lambda m: wrap_display_math(m.group(1)),
        html,
    )
    return html


def format_inline_math(html: str) -> str:
    parts = re.split(r'(<div class="formula">.*?</div>)', html, flags=re.DOTALL)
    out = []
    for part in parts:
        if part.startswith('<div class="formula">'):
            out.append(part)
        else:
            out.append(_inline_math_fragment(part))
    return "".join(out)


def format_math_in_html(html: str) -> str:
    html = format_formula_divs(html)
    html = format_inline_math(html)
    return html
