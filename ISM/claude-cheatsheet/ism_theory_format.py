"""Visual formatting helpers — cards, grids, condensed content."""
import html as H
import re

from math_format import format_math_in_html

# Session accent colors (border + badge)
SESSION_THEME = {
    "session1": ("#059669", "#ecfdf5", "Descriptive"),
    "session2": ("#2563eb", "#eff6ff", "Probability"),
    "session3": ("#7c3aed", "#f5f3ff", "Conditional"),
    "session4": ("#db2777", "#fdf2f8", "Bayes"),
    "session5": ("#d97706", "#fffbeb", "Random Vars"),
    "session6": ("#dc2626", "#fef2f2", "Distributions"),
    "session7": ("#0891b2", "#ecfeff", "Sampling"),
}

# One-line gist per section (shown in colored banner — replaces wall of intro text)
SECTION_GIST = {
    "session1-intro": "Turn raw numbers into decisions: organise → summarise → interpret.",
    "session1-step0": "Check data type first — nominal, ordinal, interval, or ratio.",
    "session1-step1": "Three centres: mean (balance), median (robust), mode (most frequent).",
    "session1-step2": "Spread: range, variance s², SD s — how far values scatter.",
    "session1-step3": "Skew: mean follows the tail; use median when skewed.",
    "session1-step4": "Five-number summary + box plot; 1.5×IQR flags outliers.",
    "session1-summary": "Centre + spread + shape + outliers = full picture before probability.",
    "session2-intro": "Probability = long-run frequency of events in sample space S.",
    "session2-nested": "S (all outcomes) → outcome (one result) → event (subset of S).",
    "session2-building": "Union, intersection, complement — set ops on events.",
    "session2-me-vs-ind": "Mutually exclusive ≠ independent (common exam trap).",
    "session2-axioms": "P(A)≥0, P(S)=1, additivity for disjoint events.",
    "session2-addition": "P(A∪B) = P(A)+P(B)−P(A∩B); drop overlap term if disjoint.",
    "session2-counting": "Count outcomes → divide by |S| when equally likely.",
    "session3-intro": "New info shrinks the sample space — probabilities update.",
    "session3-conditional": "P(A|B) = P(A∩B)/P(B) — probability of A given B occurred.",
    "session3-mult": "Chain events: P(A∩B) = P(A|B)·P(B).",
    "session3-indep": "Independent if P(A∩B) = P(A)P(B).",
    "session3-total": "P(B) = Σ P(B|Aᵢ)P(Aᵢ) over partition {Aᵢ}.",
    "session4-intro": "Reverse question: given effect, infer cause.",
    "session4-bayes": "Posterior = (likelihood × prior) / evidence.",
    "session4-naive": "Score each class: P(C) × ∏ P(word|C); pick max.",
    "session5-intro": "Random variable X assigns a number to each outcome.",
    "session5-discrete": "PMF f(x)=P(X=x); sums to 1. CDF accumulates left.",
    "session5-expectation": "E[X] = balance point; Var(X) = spread around mean.",
    "session5-continuous": "PDF: probability = area under curve.",
    "session5-joint": "Joint table → marginals (row/col sums) → conditionals.",
    "session6-big-idea": "Named distributions = reusable probability moulds.",
    "session6-bernoulli": "One trial, two outcomes: P(X=1)=p.",
    "session6-binomial": "n trials, fixed p — count successes.",
    "session6-poisson": "Events in a window; λ = rate × time.",
    "session6-normal": "Bell curve: μ centre, σ spread; 68-95-99.7 rule.",
    "session6-zscore": "Z = (X−μ)/σ — one table for all normals.",
    "session6-approx": "Binomial→Poisson (λ=np); Binomial→Normal (np,nq≥15).",
    "session6-inference-trio": "χ² (variance), t (unknown σ), F (two variances).",
    "session7-soup": "Sample a spoonful to learn about the whole pot.",
    "session7-pick-sample": "SRS, stratified, cluster — probability vs convenience.",
    "session7-variation": "Every sample gives a different x̄ — that's sampling variation.",
    "session7-sampling-dist": "Distribution of all possible x̄ values from repeated samples.",
    "session7-clt": "x̄ → Normal(μ, σ²/n) for large n regardless of population shape.",
    "session7-finite": "FPC shrinks SE when n/N > 5%.",
    "session7-proportions": "p̂ is a mean of 0/1 data — same CLT machinery.",
    "session7-point-est": "Point estimate = best single guess (x̄, p̂).",
    "session7-ci": "Interval estimate: x̄ ± margin — 95% of intervals capture μ.",
    "session7-sample-size": "n = (z·σ/E)² — quadruple n to halve error.",
}

SKIP_LINE_RE = re.compile(
    r"^(The thread to the next session|Imagine someone|Picture the|"
    r"Statistics is detective|That is why statistics|What, why, where — for this whole|"
    r"★Everyday picture|✗Watch out|✓Key takeaway|✎Worked example|"
    r"Where you meet|Alone it is almost|Formally, X has|The formula looks|"
    r"Mean and variance, and what|This one curve is worth|"
    r"Read the figure|Note the question|Foreshadowing|Sanity-check|"
    r"Cultivate exactly|Heads-up|Whenever your|Most .+ marks are lost|"
    r"Phrase translator|Quick self-check|Counting or measuring|"
    r"10 The one-page cheat|Bridges between moulds|Mould Use when)",
    re.I,
)

TIP_MARKERS = [
    (re.compile(r"^✗Watch out|^Watch out", re.I), "warn", "⚠ Watch out"),
    (re.compile(r"^✓Key takeaway|^Key takeaway", re.I), "tip", "✓ Key point"),
    (re.compile(r"^★Everyday picture|^Everyday picture", re.I), "analogy", "💡 Analogy"),
]


def gist_banner(anchor: str) -> str:
    gist = SECTION_GIST.get(anchor, "")
    if not gist:
        return ""
    sid = anchor.rsplit("-", 1)[0] if "-" in anchor else anchor
    color, bg, _ = SESSION_THEME.get(sid, ("#2563eb", "#eff6ff", ""))
    return (
        f'<div class="gist-banner" style="border-color:{color};background:{bg}">'
        f"<strong>In one line:</strong> {H.escape(gist)}</div>"
    )


def session_badge(session_id: str) -> str:
    color, bg, label = SESSION_THEME.get(session_id, ("#2563eb", "#eff6ff", "ISM"))
    return f'<span class="sess-badge" style="background:{bg};color:{color};border:1px solid {color}">{H.escape(label)}</span>'


def wwwh_grid(text: str) -> str:
    m = re.search(
        r"What:?(.+?)Why:?(.+?)Where:?(.+?)(?:To understand|$)",
        text,
        re.I | re.S,
    )
    if not m:
        return ""
    what, why, where = (s.strip()[:220] for s in m.groups())
    return f"""<div class="wwwh-grid">
<div class="wwwh-card what"><span class="wwwh-label">What</span><p>{H.escape(what)}</p></div>
<div class="wwwh-card why"><span class="wwwh-label">Why</span><p>{H.escape(why)}</p></div>
<div class="wwwh-card where"><span class="wwwh-label">Where</span><p>{H.escape(where)}</p></div>
</div>"""


def bullet_grid(items: list[str], css_class: str = "point-grid") -> str:
    if not items:
        return ""
    lis = "".join(
        f'<li class="point-card">{format_math_in_html(H.escape(it[:280]))}</li>'
        for it in items[:8]
    )
    return f'<ul class="{css_class}">{lis}</ul>'


def extract_bullets(text: str) -> list[str]:
    """Pull scannable bullet points from PDF text; skip narrative."""
    text = re.sub(r"\s+", " ", text)
    chunks = re.split(r"(?<=[.!?])\s+(?=[A-Z✗✓★•])", text)
    out = []
    for c in chunks:
        c = c.strip()
        if len(c) < 25 or len(c) > 300:
            continue
        if SKIP_LINE_RE.match(c):
            continue
        if re.match(r"^(Definition |Key formula |Worked example )", c):
            continue
        if c.startswith("•"):
            c = c[1:].strip()
        # Prefer short actionable lines
        if re.search(r"\b(use|when|if|then|means|rule|formula|P\(|E\[|Var)\b", c, re.I):
            out.append(c)
        elif len(c) < 120:
            out.append(c)
        if len(out) >= 6:
            break
    return out


def format_condensed(text: str, anchor: str = "") -> str:
    """Card-based layout: gist + WWWH + bullets + callouts only — no prose walls."""
    if not text or not text.strip():
        return ""

    from ism_theory_enrich import clean_section_text

    text = clean_section_text(text)
    html_parts = []

    # WWWH block
    ww = wwwh_grid(text)
    if ww:
        html_parts.append(ww)

    chunks = re.split(
        r"\n(?=• )|\n(?=Definition \d+\.\d+:)|\n(?=Key formula \d+\.\d+:)|"
        r"\n(?=Worked example \d+\.\d+:)|\n(?=✎Worked example)",
        text,
    )
    bullet_buf = []

    def flush_bullets():
        nonlocal bullet_buf
        if bullet_buf:
            html_parts.append(bullet_grid(bullet_buf))
            bullet_buf = []

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk or len(chunk) < 3:
            continue

        # Special tip markers
        for pat, cls, label in TIP_MARKERS:
            if pat.match(chunk):
                body = pat.sub("", chunk).strip()[:400]
                html_parts.append(
                    f'<div class="mini-card {cls}"><span class="mini-label">{label}</span>'
                    f"<p>{format_math_in_html(H.escape(body))}</p></div>"
                )
                chunk = ""
                break
        if not chunk:
            continue

        if chunk.startswith("•"):
            chunk = re.sub(r"^•\s*", "", chunk)
            for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", chunk):
                s = s.strip()
                if s and 15 < len(s) < 280 and not SKIP_LINE_RE.match(s):
                    bullet_buf.append(s)
            continue

        flush_bullets()

        if chunk.startswith("Definition "):
            m = re.match(r"Definition \d+\.\d+:\s*(.+?)(?:\n|$)(.*)", chunk, re.S)
            title = (m.group(1) if m else chunk)[:100]
            rest = (m.group(2) if m and m.group(2) else "")[:200]
            rest_html = f'<p class="def-rest">{format_math_in_html(H.escape(rest))}</p>' if rest else ""
            html_parts.append(
                f'<div class="mini-card def"><span class="mini-label">📘 Definition</span>'
                f"<p><strong>{format_math_in_html(H.escape(title))}</strong></p>"
                f"{rest_html}</div>"
            )
            continue

        if chunk.startswith("Key formula "):
            m = re.match(r"Key formula \d+\.\d+:\s*(.+?)(?:\n|$)(.*)", chunk, re.S)
            title = m.group(1).strip() if m else chunk
            rest = m.group(2).strip()[:300] if m and m.group(2) else ""
            eq = rest or title
            html_parts.append(
                f'<div class="mini-card formula"><span class="mini-label">📐 Formula</span>'
                f'<div class="eq-block">{format_math_in_html(H.escape(eq))}</div></div>'
            )
            continue

        if chunk.startswith("Worked example ") or chunk.startswith("✎Worked example"):
            m = re.match(r"(?:✎)?Worked example \d+\.\d+:\s*(.+?)(?:\n|$)(.*)", chunk, re.S)
            title = (m.group(1) if m else chunk)[:120]
            rest = (m.group(2) if m and m.group(2) else "")[:350]
            ex_rest = f'<p>{format_math_in_html(H.escape(rest))}</p>' if rest else ""
            html_parts.append(
                f'<div class="mini-card example"><span class="mini-label">✏ Example</span>'
                f"<p><strong>{format_math_in_html(H.escape(title))}</strong></p>"
                f"{ex_rest}</div>"
            )
            continue

        if re.match(r"^What, why, where", chunk, re.I):
            continue  # handled by wwwh_grid

        # Skip long narrative — extract bullets only
        if len(chunk) > 80:
            for s in extract_bullets(chunk):
                bullet_buf.append(s)
        elif not SKIP_LINE_RE.match(chunk):
            bullet_buf.append(chunk[:200])

    flush_bullets()

    if not html_parts and anchor:
        # Fallback: show gist only
        return ""

    return "".join(html_parts)
