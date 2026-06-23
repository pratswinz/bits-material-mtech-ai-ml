"""Inline SVG assets into HTML so diagrams work when opened via file://."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
_CACHE: dict[str, str] = {}
_UID = 0

SVG_WRAP_CSS = """
.svg-wrap{display:inline-block;max-width:100%;vertical-align:top}
.svg-wrap svg{max-width:100%;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff;display:block}
"""


def load_svg(name: str) -> str:
    if name not in _CACHE:
        path = ASSETS / name
        if not path.suffix == ".svg":
            raise ValueError(f"Not an SVG: {name}")
        _CACHE[name] = path.read_text(encoding="utf-8").strip()
    return _CACHE[name]


def reset_uid() -> None:
    global _UID
    _UID = 0


def _unique_ids(svg: str) -> str:
    global _UID
    _UID += 1
    suffix = f"u{_UID}"

    def id_repl(m: re.Match) -> str:
        base = re.sub(r"-u\d+$", "", m.group(1))
        return f'id="{base}-{suffix}"'

    svg = re.sub(r'\bid="([^"]+)"', id_repl, svg)

    def url_repl(m: re.Match) -> str:
        base = re.sub(r"-u\d+$", "", m.group(1))
        return f"url(#{base}-{suffix})"

    svg = re.sub(r"url\(#([^)]+)\)", url_repl, svg)
    return svg


def svg_div(name: str, alt: str = "diagram", style: str = "") -> str:
    svg = _unique_ids(load_svg(name))
    style_attr = f' style="{style}"' if style else ""
    return f'<div class="svg-wrap" role="img" aria-label="{alt}"{style_attr}>{svg}</div>'


def svg_figure(name: str, alt: str = "diagram", style: str = "") -> str:
    return f'<figure class="diagram">{svg_div(name, alt, style)}</figure>'


def inline_img_tags(html: str) -> str:
    pattern = re.compile(
        r'<img\s+src="assets/([^"]+\.svg)"\s+alt="([^"]*)"(?:\s+style="([^"]*)")?\s*/?>'
    )

    def repl(m: re.Match) -> str:
        name, alt, style = m.group(1), m.group(2), m.group(3) or ""
        try:
            return svg_div(name, alt, style)
        except (FileNotFoundError, ValueError):
            return m.group(0)

    return pattern.sub(repl, html)


def refresh_svg_wrap_ids(html: str) -> str:
    pattern = re.compile(
        r'(<div class="svg-wrap"[^>]*>)(<svg.*?</svg>)(</div>)',
        re.DOTALL,
    )

    def repl(m: re.Match) -> str:
        return m.group(1) + _unique_ids(m.group(2)) + m.group(3)

    return pattern.sub(repl, html)


def patch_html_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    before = text.count('src="assets/')
    if before:
        text = inline_img_tags(text)
    else:
        text = refresh_svg_wrap_ids(text)
    if ".svg-wrap" not in text.split("</style>")[0]:
        text = text.replace(
            ".diagram img{max-width:100%;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff}",
            ".diagram img{max-width:100%;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff}"
            + SVG_WRAP_CSS,
        )
        if ".svg-wrap" not in text:
            text = text.replace("</style>", SVG_WRAP_CSS + "\n</style>", 1)
    path.write_text(text, encoding="utf-8")
    return before if before else text.count("svg-wrap")


if __name__ == "__main__":
    reset_uid()
    for name in ("ML_PYQ_Workbook.html",):
        p = ROOT / name
        if p.exists():
            n = patch_html_file(p)
            kind = "img tags inlined" if n and 'src="assets/' in p.read_text(encoding="utf-8") else "svg ids refreshed"
            print(f"Patched {name}: {n} ({kind})")
