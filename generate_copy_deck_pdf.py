#!/usr/bin/env python3
"""Convert the marked-up copy deck Word file to a print-ready PDF."""

from pathlib import Path
import re
import subprocess

import mammoth

DOCX = Path("/workspace/AC7988_READ_Patient_Education_Copy_Deck_D5_Reference_Markup.docx")
HTML_OUT = Path("/tmp/AC7988_READ_copy_deck_markup.html")
PDF_OUT = Path("/workspace/AC7988_READ_Patient_Education_Copy_Deck_D5_Reference_Markup.pdf")
ARTIFACT = Path("/opt/cursor/artifacts/AC7988_READ_Patient_Education_Copy_Deck_D5_Reference_Markup.pdf")

CSS = """
@page {
  size: letter;
  margin: 0.65in 0.65in 0.75in 0.65in;
  @top-left {
    content: "AC7988  |  READ™ Patient Education Brochure  |  Copy Deck D5 + Reference Markup";
    font-size: 8pt;
    color: #5a5a5a;
    font-family: Calibri, Arial, sans-serif;
  }
  @bottom-center {
    content: "CONFIDENTIAL — For medical/legal review  ·  © 2026 Alcon Inc. 09/26 GLB/IMG-WLO-2600010  ·  Page " counter(page);
    font-size: 8pt;
    color: #5a5a5a;
    font-family: Calibri, Arial, sans-serif;
  }
}
* { box-sizing: border-box; }
html, body {
  font-family: Calibri, Arial, Helvetica, sans-serif;
  font-size: 10.5pt;
  line-height: 1.35;
  color: #2b2b2b;
  margin: 0;
  padding: 0;
}
h1, h2, h3 { page-break-after: avoid; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 8px 0 12px;
  page-break-inside: auto;
}
tr { page-break-inside: avoid; }
td, th {
  border: 0.5pt solid #c5d5da;
  padding: 6px 8px;
  vertical-align: top;
  font-size: 9pt;
}
p { margin: 0 0 8px; }
sup {
  font-size: 7.5pt;
  font-weight: 700;
  color: #00738a;
  vertical-align: super;
}
.banner {
  background: #00738a;
  color: #fff;
  padding: 10px 14px;
  font-size: 14pt;
  font-weight: 700;
  margin: 0 0 12px;
}
.banner p { margin: 0; color: #fff; }
.banner td { border: none; background: #00738a; color: #fff; }
/* First table is the teal banner */
body > table:first-of-type td {
  background: #00738a;
  color: #fff;
  border: none;
  padding: 12px 14px;
  font-size: 14pt;
}
/* Meta table (client/brand) */
body > table:nth-of-type(2) td:first-child {
  background: #00738a;
  color: #fff;
  width: 22%;
  font-weight: 700;
}
body > table:nth-of-type(2) td:last-child {
  background: #e6f3f6;
  color: #1a3a4a;
}
.status-supported { background: #eaf6ee; color: #1b6b3a; font-weight: 700; }
.status-partial { background: #fff6e5; color: #8a5a00; font-weight: 700; }
.status-not { background: #fdecec; color: #9b1c1c; font-weight: 700; }
.note td {
  background: #fff6e5;
  border: 0.75pt solid #e0d2a8;
}
.note-red td {
  background: #fdecec;
  border: 0.75pt solid #e8b4b4;
}
.header-row td {
  background: #00738a !important;
  color: #fff !important;
  font-weight: 700;
}
"""


def colorize(html: str) -> str:
    html = html.replace(
        "<td><p><strong>Supported</strong></p></td>",
        '<td class="status-supported"><p><strong>Supported</strong></p></td>',
    )
    html = html.replace(
        "<td><p><strong>Partial</strong></p></td>",
        '<td class="status-partial"><p><strong>Partial</strong></p></td>',
    )
    html = html.replace(
        "<td><p><strong>Not supported</strong></p></td>",
        '<td class="status-not"><p><strong>Not supported</strong></p></td>',
    )
    html = html.replace(
        "<td><p><strong>Section / Copy</strong></p></td>",
        '<td class="header-row"><p><strong>Section / Copy</strong></p></td>',
    )
    # Header cells of first row of support grid
    html = html.replace(
        "<td><p><strong>Copy excerpt</strong></p></td>",
        '<td class="header-row"><p><strong>Copy excerpt</strong></p></td>',
    )
    html = html.replace(
        "<td><p><strong>Ref(s)</strong></p></td>",
        '<td class="header-row"><p><strong>Ref(s)</strong></p></td>',
    )
    html = html.replace(
        "<td><p><strong>Status</strong></p></td>",
        '<td class="header-row"><p><strong>Status</strong></p></td>',
    )
    html = html.replace(
        "<td><p><strong>Supporting excerpt from source PDF</strong></p></td>",
        '<td class="header-row"><p><strong>Supporting excerpt from source PDF</strong></p></td>',
    )
    # MLR / unreferenced note boxes
    html = re.sub(
        r"<table><tr><td><p><strong>(MLR note[^<]*)</strong></p>",
        r'<table class="note"><tr><td><p><strong>\1</strong></p>',
        html,
    )
    html = re.sub(
        r"<table><tr><td><p><strong>(Unreferenced[^<]*)</strong></p>",
        r'<table class="note-red"><tr><td><p><strong>\1</strong></p>',
        html,
    )
    html = re.sub(
        r"<table><tr><td><p><strong>(WATCHOUT:[^<]*)</strong></p>",
        r'<table class="note-red"><tr><td><p><strong>\1</strong></p>',
        html,
    )
    return html


def main():
    with DOCX.open("rb") as f:
        body = mammoth.convert_to_html(f).value
    body = colorize(body)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AC7988 READ Patient Education Copy Deck — Reference Markup</title>
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""
    HTML_OUT.write_text(html, encoding="utf-8")

    chrome = "/opt/google/chrome/chrome"
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--user-data-dir=/tmp/chrome-pdf-profile-ac7988",
            "--no-pdf-header-footer",
            f"--print-to-pdf={PDF_OUT}",
            f"file://{HTML_OUT}",
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    ARTIFACT.write_bytes(PDF_OUT.read_bytes())
    print(f"Wrote {PDF_OUT} ({PDF_OUT.stat().st_size} bytes)")
    print(f"Wrote {ARTIFACT}")


if __name__ == "__main__":
    main()
