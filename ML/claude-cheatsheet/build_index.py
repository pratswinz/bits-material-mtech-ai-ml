#!/usr/bin/env python3
"""Rebuild ML/claude-cheatsheet/index.html with topic-wise PYQ links."""
import html as H
from pathlib import Path

from ml_pyq_catalog import render_pyq_list
from ml_topics import TOPIC_GROUPS

OUT = Path(__file__).resolve().parent / "index.html"


def topic_cards_html() -> str:
    parts = []
    for grp_id, title, subtopics in TOPIC_GROUPS:
        subs = "".join(f"<li>{H.escape(s)}</li>" for s in subtopics)
        pyq = render_pyq_list(grp_id, mid_sem_only=False)
        parts.append(
            f"""<div class="topic-card {grp_id}">
<h3>{H.escape(title)}</h3>
<ul class="subtopics">{subs}</ul>
<div class="pyq-group">
<p class="grp-head">Past paper PYQs · <code>ML/questions/</code></p>
{pyq}
</div>
</div>"""
        )
    return "\n\n".join(parts)


def build() -> None:
    cards = topic_cards_html()
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ML Mid-Sem — Study Hub</title>
<style>
:root{{--navy:#1e3a5f;--blue:#2563eb;--green:#059669;--purple:#7c3aed;--amber:#d97706;--bg:#f8fafc;--card:#fff;--border:#e2e8f0;--text:#1e293b;--muted:#64748b}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--text);line-height:1.6}}
.hero{{background:linear-gradient(135deg,#ecfdf5,#eff6ff);color:var(--text);padding:2.5rem 1.5rem;text-align:center;border-bottom:1px solid var(--border)}}
.hero h1{{font-size:1.75rem;margin-bottom:.4rem;color:var(--navy)}}
.hero p{{color:var(--muted);max-width:620px;margin:0 auto;font-size:.95rem}}
.hero code{{background:#fff;padding:2px 6px;border-radius:4px;border:1px solid var(--border);font-size:.85rem}}
.plan-banner{{max-width:900px;margin:1.5rem auto 0;padding:0 1rem}}
.plan-banner a{{display:block;background:#fff;border:2px solid #059669;color:var(--navy);text-decoration:none;padding:1rem 1.4rem;border-radius:12px;text-align:center;font-weight:600;box-shadow:0 2px 8px rgba(0,0,0,.04)}}
.plan-banner a:hover{{background:#ecfdf5}}
.plan-banner span{{display:block;font-size:.82rem;font-weight:400;color:var(--muted);margin-top:.25rem}}
.topics-wrap{{max-width:900px;margin:1.5rem auto 0;padding:0 1rem}}
.topics-wrap h2{{font-size:1rem;color:var(--navy);margin-bottom:.35rem}}
.topics-wrap .topics-note{{font-size:.8rem;color:var(--muted);margin-bottom:1rem}}
.topics-grid{{display:grid;gap:.75rem}}
@media(min-width:640px){{.topics-grid{{grid-template-columns:repeat(2,1fr)}}}}
.topic-card{{border-radius:10px;padding:.85rem 1rem;border:1px solid var(--border);background:var(--card)}}
.topic-card h3{{font-size:.82rem;font-weight:800;text-transform:uppercase;letter-spacing:.04em;margin:0 0 .5rem;padding-bottom:.35rem;border-bottom:2px solid}}
.topic-card .subtopics{{list-style:none;padding:0;margin:0 0 .65rem}}
.topic-card .subtopics li{{font-size:.8rem;color:var(--text);padding:.18rem 0 .18rem .85rem;position:relative;line-height:1.35}}
.topic-card .subtopics li::before{{content:"";position:absolute;left:0;top:.5rem;width:5px;height:5px;border-radius:50%;background:currentColor;opacity:.5}}
.pyq-group{{margin-top:.5rem;padding-top:.55rem;border-top:1px dashed var(--border)}}
.pyq-group .grp-head{{font-size:.68rem;font-weight:700;text-transform:uppercase;color:var(--purple);letter-spacing:.04em;margin:0 0 .4rem}}
.pyq-list{{list-style:none;margin:0;padding:0;font-size:.78rem}}
.pyq-list li{{padding:.28rem 0;border-bottom:1px solid #f1f5f9;display:flex;flex-wrap:wrap;gap:.25rem .45rem;align-items:baseline;line-height:1.35}}
.pyq-list li:last-child{{border-bottom:none}}
.pyq-meta{{color:var(--muted);font-size:.72rem;white-space:nowrap}}
.pyq-list a{{font-weight:700;color:var(--blue);text-decoration:none}}
.pyq-list a:hover{{text-decoration:underline}}
.pyq-label{{color:var(--text);font-size:.75rem}}
.pyq-empty{{font-size:.75rem;color:var(--muted);margin:0}}
.t1 h3{{color:#059669;border-color:#6ee7b7}}.t1 .subtopics li::before{{color:#059669}}
.t2 h3{{color:#2563eb;border-color:#93c5fd}}.t2 .subtopics li::before{{color:#2563eb}}
.t3 h3{{color:#d97706;border-color:#fcd34d}}.t3 .subtopics li::before{{color:#d97706}}
.t4 h3{{color:#7c3aed;border-color:#c4b5fd}}.t4 .subtopics li::before{{color:#7c3aed}}
.t5 h3{{color:#db2777;border-color:#f9a8d4}}.t5 .subtopics li::before{{color:#db2777}}
.t6 h3{{color:#0891b2;border-color:#67e8f9}}.t6 .subtopics li::before{{color:#0891b2}}
.grid{{max-width:900px;margin:1.5rem auto 2rem;padding:0 1rem;display:grid;gap:1.2rem}}
@media(min-width:700px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
@media(min-width:900px){{.grid{{grid-template-columns:repeat(3,1fr)}}}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.4rem;text-decoration:none;color:inherit;transition:box-shadow .2s,transform .2s;display:block}}
.card:hover{{box-shadow:0 8px 24px rgba(0,0,0,.08);transform:translateY(-2px)}}
.card h2{{font-size:1.1rem;margin-bottom:.5rem;color:var(--navy)}}
.card p{{font-size:.88rem;color:var(--muted);margin-bottom:.8rem}}
.card .tag{{display:inline-block;font-size:.72rem;font-weight:600;padding:3px 10px;border-radius:99px}}
.tag.theory{{background:#eff6ff;color:var(--blue)}}
.tag.pyq{{background:#f3e8ff;color:var(--purple)}}
.tag.rev{{background:#ecfdf5;color:var(--green)}}
.sources{{max-width:900px;margin:0 auto 3rem;padding:0 1rem}}
.sources h3{{font-size:.85rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.6rem}}
.sources ul{{font-size:.82rem;color:var(--muted);padding-left:1.2rem}}
.sources li{{margin:.25rem 0}}
.sources code{{background:#f1f5f9;padding:1px 5px;border-radius:3px;font-size:.78rem}}
</style>
</head>
<body>
<div class="hero">
<h1>Machine Learning — Mid-Sem Hub</h1>
<p>AIMLCZG565 · Topic-wise PYQs linked to <code>ML/questions/</code> · All files in <code>ML/claude-cheatsheet/</code></p>
</div>
<div class="plan-banner">
<a href="ML_3Day_Plan.html">📅 Start with the 3-Day Plan<span>Theory → PYQs → revision · ~6–7 hrs/day</span></a>
</div>

<div class="topics-wrap">
<h2>Important topics &amp; past-paper PYQs</h2>
<p class="topics-note">Every link opens the question in <a href="ML_Past_Papers.html">Past Papers</a> (2023–2026 mid + end sem from <code>ML/questions/MidSem/</code> &amp; <code>EndSem/</code>)</p>
<div class="topics-grid">

{cards}

</div>
</div>

<div class="grid">
<a class="card" href="ML_3Day_Plan.html" style="grid-column:1/-1;border-color:#059669">
<h2>📅 3-Day Study Plan</h2>
<p>Day-by-day schedule linking theory → PYQs → revision.</p>
<span class="tag rev">Start here</span>
</a>
<a class="card" href="ML_Theory_Guide.html">
<h2>📘 Theory Guide</h2>
<p>CS1–CS7 concepts, formulas, worked examples. From <code>companion docs/</code>.</p>
<span class="tag theory">Concepts</span>
</a>
<a class="card" href="ML_Past_Papers.html">
<h2>📋 Past Papers 2023–2026</h2>
<p>Official papers from <code>ML/questions/</code> — tagged by topic above.</p>
<span class="tag pyq">Tagged PYQs</span>
</a>
<a class="card" href="ML_PYQ_Workbook.html">
<h2>📝 PYQ Workbook</h2>
<p>TYPE 1–11 practice, mock exam, Ridge/Lasso numerical.</p>
<span class="tag pyq">By TYPE</span>
</a>
<a class="card" href="ML_Revision_Sheet.html">
<h2>⚡ Revision Sheet</h2>
<p>One-page formulas — print before exam.</p>
<span class="tag rev">Print</span>
</a>
</div>
<div class="sources">
<h3>Source folders</h3>
<ul>
<li><code>ML/companion docs/</code> — CS1–CS7 companions</li>
<li><code>ML/questions/MidSem/</code> — mid-sem papers (2023–2026) + June 2026 photos</li>
<li><code>ML/questions/EndSem/</code> — end-sem papers (2021, 2026)</li>
<li><code>ML/questions/_Resources/</code> — practice QPs, study guides, sample papers</li>
<li><code>ML/mid sem/</code> — Ridge/Lasso numerical</li>
<li>Rebuild: <code>python3 build_all.py</code> in <code>ML/claude-cheatsheet/</code></li>
</ul>
</div>
</body>
</html>"""
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
