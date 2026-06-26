"""Shared light-background styles for ISM HTML pages."""

LIGHT_HEADER = """
header{background:#fff;color:var(--text);border-bottom:1px solid var(--border);padding:1.4rem 1.5rem;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.04)}
header h1{color:var(--navy);margin:0 0 .25rem;font-size:1.35rem}
header p{color:var(--muted);margin:0}
header a{color:var(--blue);text-decoration:none}
header a:hover{text-decoration:underline}
"""

LIGHT_HEADER_FLEX = """
header{background:#fff;color:var(--text);border-bottom:1px solid var(--border);padding:1rem 1.5rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;box-shadow:0 1px 4px rgba(0,0,0,.04)}
header h1{color:var(--navy);margin:0;font-size:1.25rem}
header p{color:var(--muted);margin:.2rem 0 0}
header a{color:var(--blue)}
"""

LIGHT_HERO = """
.hero{background:linear-gradient(135deg,#ecfdf5 0%,#eff6ff 50%,#fdf2f8 100%);color:var(--text);padding:1.6rem 1.8rem;border-radius:var(--radius);margin-bottom:1.5rem;border:1px solid var(--border);box-shadow:0 2px 8px rgba(0,0,0,.04)}
.hero h1{margin:0 0 .35rem;font-size:1.45rem;color:var(--navy)}
.hero .meta{font-size:.82rem;color:var(--muted);margin:0}
"""

LIGHT_SIDEBAR = """
#sidebar{width:var(--sidebar-w);flex-shrink:0;background:#f8fafc;color:var(--text);border-right:1px solid var(--border);padding:1rem .75rem 2rem;font-size:.74rem;position:sticky;top:0;height:100vh;overflow-y:auto}
#sidebar .brand{font-weight:800;font-size:.9rem;color:var(--navy);margin-bottom:.15rem}
#sidebar .brand-sub{font-size:.68rem;color:var(--muted);margin-bottom:1rem}
#sidebar .brand-sub a{color:var(--blue)}
#sidebar nav h3{font-size:.58rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:1rem 0 .3rem;font-weight:700}
#sidebar ol{list-style:none;padding:0;margin:0}
#sidebar li a{display:block;padding:.3rem .55rem;border-radius:6px;color:#475569;line-height:1.3}
#sidebar li a:hover{background:#eff6ff;color:var(--navy);text-decoration:none}
#sidebar li.sub a{padding-left:1.1rem;font-size:.68rem;color:var(--muted)}
#sidebar li.guide-link a{color:#059669;font-weight:600}
"""

LIGHT_DAY_HEADER = """
.day-h{background:#ecfdf5;color:var(--navy);border-bottom:2px solid #6ee7b7;padding:.8rem 1.2rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem;align-items:center}
.day-h h2{margin:0;font-size:1.05rem;color:var(--navy)}
.day-h span{color:var(--muted);font-size:.88rem}
"""

LIGHT_HUB_HERO = """
.hero{background:linear-gradient(135deg,#ecfdf5,#eff6ff);color:var(--text);padding:2.5rem 1.5rem;text-align:center;border-bottom:1px solid var(--border)}
.hero h1{font-size:1.75rem;margin-bottom:.4rem;color:var(--navy)}
.hero p{color:var(--muted);max-width:620px;margin:0 auto;font-size:.95rem}
.hero code{background:#fff;padding:2px 6px;border-radius:4px;border:1px solid var(--border);font-size:.85rem}
"""

LIGHT_PLAN_BANNER = """
.plan-banner a{display:block;background:#fff;border:2px solid #059669;color:var(--navy);text-decoration:none;padding:1rem 1.4rem;border-radius:12px;text-align:center;font-weight:600;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.plan-banner a:hover{background:#ecfdf5}
.plan-banner span{display:block;font-size:.82rem;font-weight:400;color:var(--muted);margin-top:.25rem}
"""
