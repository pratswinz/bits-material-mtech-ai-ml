"""Format ISM past-paper question stems — tables, sub-parts, cleanup."""
import html as H
import re

PMF_TABLE = """
<table class="data-table cm-table"><thead><tr><th>x</th><th>0</th><th>1</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th></tr></thead>
<tbody><tr><td>p(x)</td><td>0</td><td>k</td><td>2k</td><td>2k</td><td>3k</td><td>k²</td><td>7k²+k</td></tr></tbody></table>"""

SPAM_REGULAR_TABLE = """
<table class="data-table"><thead><tr><th>ID</th><th>Text (Bag of Words)</th><th>Label</th></tr></thead><tbody>
<tr><td>1</td><td>Congratulations, you have won a free prize</td><td>Spam</td></tr>
<tr><td>2</td><td>Monthly meeting scheduled for Monday</td><td>Not Spam</td></tr>
<tr><td>3</td><td>Earn money quickly with this simple trick</td><td>Spam</td></tr>
<tr><td>4</td><td>Project report attached. Review by Friday</td><td>Not Spam</td></tr>
</tbody></table>"""

SPAM_MAKEUP_TABLE = """
<table class="data-table"><thead><tr><th>Message</th><th>Label</th></tr></thead><tbody>
<tr><td>Win money</td><td>Spam</td></tr>
<tr><td>Free prize</td><td>Spam</td></tr>
<tr><td>See you soon</td><td>Ham</td></tr>
<tr><td>Call me now</td><td>Ham</td></tr>
</tbody></table>"""

URGENT_MSG_TABLE = """
<table class="data-table"><thead><tr><th>ID</th><th>Words in Message</th><th>Label</th></tr></thead><tbody>
<tr><td>1</td><td>assignment due tomorrow please help</td><td>Urgent</td></tr>
<tr><td>2</td><td>lunch plans today?</td><td>Not Urgent</td></tr>
<tr><td>3</td><td>exam rescheduled urgent attention</td><td>Urgent</td></tr>
<tr><td>4</td><td>thanks for the notes</td><td>Not Urgent</td></tr>
</tbody></table>"""


def _strip_marks(html: str) -> str:
    html = re.sub(r"(?:<br>)?\[\s*\d+\s*Marks?\s*\]", "", html, flags=re.I)
    html = re.sub(r"(?:<br>)?\[\s*\d+M\s*\]", "", html, flags=re.I)
    return html


def _structure_parts(html: str) -> str:
    """Turn (a), (b), i), (ii) breaks into readable blocks."""
    html = re.sub(
        r"(?:<br>|\n)\s*([a-z]\))\s*",
        r'</p><p class="stem-part"><strong>\1</strong> ',
        html,
        flags=re.I,
    )
    html = re.sub(
        r"(?:<br>|\n)\s*\(([ivx]+)\)\s*",
        r'</p><p class="stem-part"><strong>(\1)</strong> ',
        html,
        flags=re.I,
    )
    html = re.sub(
        r"(?:<br>|\n)\s*([ivx]+)\)\s*",
        r'</p><p class="stem-part"><strong>\1)</strong> ',
        html,
        flags=re.I,
    )
    if 'class="stem-part"' in html and not html.startswith("<p"):
        html = "<p>" + html
    return html


def format_ism_stem(text: str) -> str:
    if not text:
        return ""
    blob = text.lower()
    html = H.escape(text.strip())
    html = re.sub(r"\s*\n\s*", "<br>", html)
    html = _strip_marks(html)

    if "probability function" in blob or ("p (x)" in blob and "7k" in blob.replace(" ", "")):
        html = re.sub(
            r"probability function:.*?(?=<br>[a-z]\)|<br>i\)|$)",
            "probability function:</p>" + PMF_TABLE + "<p>",
            html,
            flags=re.I | re.S,
        )
    if "sample dataset" in blob and "congratulations" in blob:
        html = re.sub(
            r"Sample Dataset:.*",
            "Sample Dataset:</p>" + SPAM_REGULAR_TABLE,
            html,
            flags=re.I | re.S,
        )
        html = re.sub(r"</table></p>", "</table>", html)
    if "win free money" in blob or ("message" in blob and "ham" in blob and "spam" in blob):
        if "Sample Dataset" not in html:
            html = re.sub(
                r"(Test the new message.*?)(?=<br>Q|$)",
                r"\1</p>" + SPAM_MAKEUP_TABLE,
                html,
                flags=re.I | re.S,
            )
    if "naïve bayes" in blob or "naive bayes" in blob:
        if "urgent" in blob and "assignment" in blob and "Message" in text:
            html = re.sub(
                r"Here is a small sample dataset:.*?(?=New Message|$)",
                "Sample dataset:</p>" + URGENT_MSG_TABLE + "<p>",
                html,
                flags=re.I | re.S,
            )

    html = _structure_parts(html)
    html = re.sub(r"(<br>){3,}", "<br><br>", html)
    html = re.sub(r"^<br>|(?:<br>)+$", "", html)
    if html and not html.startswith("<p") and not html.startswith("<table"):
        html = "<p>" + html + "</p>"
    elif html.startswith("<p>") and not html.endswith("</p>") and "stem-part" in html:
        html = html + "</p>"
    return html
