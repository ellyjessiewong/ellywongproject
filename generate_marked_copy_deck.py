#!/usr/bin/env python3
"""Generate the AC7988 READ patient-education copy deck with reference markup."""

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor, Cm, Emu, Twips
from docx.oxml.ns import nsmap

ALCON_TEAL = RGBColor(0x00, 0x73, 0x8A)
ALCON_DARK = RGBColor(0x1A, 0x3A, 0x4A)
BODY = RGBColor(0x2B, 0x2B, 0x2B)
MUTED = RGBColor(0x5A, 0x5A, 0x5A)
GREEN = RGBColor(0x1B, 0x6B, 0x3A)
AMBER = RGBColor(0x8A, 0x5A, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_TEAL = "E6F3F6"
LIGHT_GRAY = "F4F6F7"
LIGHT_AMBER = "FFF6E5"
LIGHT_GREEN = "EAF6EE"
ROW_ALT = "F7FBFC"


def set_run_font(run, name="Calibri", size=11, bold=False, italic=False, color=None, superscript=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    run.font.superscript = superscript


def shade_cell(cell, hex_color):
    tc = cell._tePr if hasattr(cell, "_tePr") else cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_cell_borders(cell, color="C5D5DA", sz="4"):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        tcBorders.append(el)
    tcPr.append(tcBorders)


def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def clear_paragraph(p):
    p.clear() if hasattr(p, "clear") else None
    for child in list(p._element):
        if child.tag.endswith("}r") or child.tag.endswith("}hyperlink"):
            p._element.remove(child)


def add_text(paragraph, text, **kwargs):
    run = paragraph.add_run(text)
    set_run_font(run, **kwargs)
    return run


def add_super(paragraph, refs, size=9, color=ALCON_TEAL):
    """refs is a string like '1,2' or '3'."""
    run = paragraph.add_run(refs)
    set_run_font(run, size=size, bold=True, color=color, superscript=True)
    return run


def set_spacing(paragraph, before=0, after=6, line=1.08):
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line


def prevent_split(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    keep = OxmlElement("w:keepNext")
    pPr.append(keep)


def set_table_widths(table, widths):
    table.autofit = False
    table.allow_autofit = False
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    total = sum(widths)
    tblW.set(qn("w:w"), str(total))
    tblW.set(qn("w:type"), "dxa")
    grid = tbl.find(qn("w:tblGrid"))
    if grid is not None:
        for child in list(grid):
            grid.remove(child)
        for w in widths:
            gc = OxmlElement("w:gridCol")
            gc.set(qn("w:w"), str(w))
            grid.append(gc)
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcW = tcPr.find(qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW")
                tcPr.append(tcW)
            tcW.set(qn("w:w"), str(widths[i]))
            tcW.set(qn("w:type"), "dxa")


def cell_para(cell, text="", **kwargs):
    p = cell.paragraphs[0]
    p.clear() if False else None
    # wipe existing runs
    for child in list(p._element):
        if not child.tag.endswith("}pPr"):
            p._element.remove(child)
    if text:
        add_text(p, text, **kwargs)
    set_spacing(p, before=0, after=2, line=1.08)
    return p


def add_cell_para(cell, **kwargs):
    p = cell.add_paragraph()
    set_spacing(p, before=2, after=2, line=1.08)
    return p


def banner(doc, text, fill="00738A"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    shade_cell(cell, fill)
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    p = cell_para(cell, text, name="Calibri", size=16, bold=True, color=WHITE)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_table_widths(table, [10080])
    return table


def section_label(doc, text):
    p = doc.add_paragraph()
    set_spacing(p, before=14, after=2, line=1.0)
    add_text(p, text, size=9, bold=True, color=ALCON_TEAL, italic=False)
    p.paragraph_format.keep_with_next = True
    return p


def heading_copy(doc, text):
    p = doc.add_paragraph()
    set_spacing(p, before=2, after=8, line=1.05)
    add_text(p, text, size=20, bold=True, color=ALCON_DARK)
    return p


def subhead_copy(doc, text):
    p = doc.add_paragraph()
    set_spacing(p, before=10, after=4, line=1.05)
    add_text(p, text, size=14, bold=True, color=ALCON_TEAL)
    p.paragraph_format.keep_with_next = True
    return p


def meta_line(doc, label, value):
    p = doc.add_paragraph()
    set_spacing(p, before=0, after=0, line=1.05)
    add_text(p, label, size=10, bold=True, color=ALCON_DARK)
    add_text(p, value, size=10, color=BODY)
    return p


def add_horizontal_line(doc):
    p = doc.add_paragraph()
    set_spacing(p, before=4, after=8)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "00738A")
    pBdr.append(bottom)
    pPr.append(pBdr)


def bullet(doc, pieces, hanging=0.25):
    """pieces: list of tuples ('text', kwargs) or ('super', '1,2')."""
    p = doc.add_paragraph()
    set_spacing(p, before=1, after=2, line=1.12)
    p.paragraph_format.left_indent = Inches(hanging)
    p.paragraph_format.first_line_indent = Inches(-0.18)
    add_text(p, "•  ", size=11, color=ALCON_TEAL, bold=True)
    for item in pieces:
        if item[0] == "super":
            add_super(p, item[1])
        else:
            add_text(p, item[0], **item[1] if len(item) > 1 else {"size": 11, "color": BODY})
    return p


def body_para(doc, pieces, before=2, after=6):
    p = doc.add_paragraph()
    set_spacing(p, before=before, after=after, line=1.15)
    for item in pieces:
        if item[0] == "super":
            add_super(p, item[1])
        else:
            add_text(p, item[0], **item[1] if len(item) > 1 else {"size": 11, "color": BODY})
    return p


def note_box(doc, title, body, fill=LIGHT_AMBER):
    table = doc.add_table(rows=1, cols=1)
    cell = table.cell(0, 0)
    shade_cell(cell, fill)
    set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
    set_cell_borders(cell, "E0D2A8", "6")
    p = cell_para(cell, title, size=9, bold=True, color=AMBER)
    p2 = cell.add_paragraph()
    set_spacing(p2, before=2, after=0, line=1.1)
    add_text(p2, body, size=9, color=MUTED)
    set_table_widths(table, [10080])
    return table


def make_header_table(doc):
    table = doc.add_table(rows=5, cols=2)
    rows = [
        ("Client", "Alcon LATAM"),
        ("Brand", "READ"),
        ("Job Code", "AC7988"),
        ("Project", "READ Patient Education Brochure"),
        ("Document", "D5 copy deck — reference markup"),
    ]
    for i, (k, v) in enumerate(rows):
        left, right = table.cell(i, 0), table.cell(i, 1)
        shade_cell(left, "00738A")
        shade_cell(right, LIGHT_TEAL)
        set_cell_margins(left, 50, 50, 80, 80)
        set_cell_margins(right, 50, 50, 80, 80)
        cell_para(left, k, size=9, bold=True, color=WHITE)
        cell_para(right, v, size=9, color=ALCON_DARK)
        set_cell_borders(left, "00738A")
        set_cell_borders(right, "C5D5DA")
    set_table_widths(table, [2200, 7880])
    return table


def version_table(doc):
    data = [
        ("Date", "Version", "Edits / Notes"),
        ("July 30, 2026", "D1", "Copy deck creation"),
        ("August 7, 2026", "D2", "Revised deck"),
        ("August 13, 2026", "D3", "Revised deck after client review"),
        ("August 19, 2026", "D4", "Client feedback + updates"),
        ("August 28, 2026", "D5", "Copy cut down"),
        ("September 8, 2026", "D5 + refs", "Reference markup against REF-15633, REF-20457, REF-29185"),
    ]
    table = doc.add_table(rows=len(data), cols=3)
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            set_cell_margins(cell, 40, 50, 70, 70)
            set_cell_borders(cell)
            if i == 0:
                shade_cell(cell, "00738A")
                cell_para(cell, val, size=9, bold=True, color=WHITE)
            else:
                shade_cell(cell, LIGHT_TEAL if i == len(data) - 1 else ("FFFFFF" if i % 2 else ROW_ALT))
                cell_para(cell, val, size=9, bold=(j == 1), color=ALCON_DARK)
    set_table_widths(table, [2400, 2000, 5680])
    return table


def legend_table(doc):
    table = doc.add_table(rows=4, cols=2)
    rows = [
        ("Markup", "Meaning"),
        ("Superscript 1", "REF-29185 — National Eye Institute (NIH). Presbyopia. Last updated December 4, 2024."),
        ("Superscript 2", "REF-15633 — Cleveland Clinic. Presbyopia. Last reviewed June 8, 2020."),
        ("Superscript 3", "REF-20457 — Gatinel D, Azar DT, Dumas L, Malet J. J Refract Surg. 2014;30(10):708-715."),
    ]
    for i, (a, b) in enumerate(rows):
        c0, c1 = table.cell(i, 0), table.cell(i, 1)
        set_cell_margins(c0, 45, 50, 70, 70)
        set_cell_margins(c1, 45, 50, 70, 70)
        set_cell_borders(c0)
        set_cell_borders(c1)
        if i == 0:
            shade_cell(c0, "1A3A4A")
            shade_cell(c1, "1A3A4A")
            cell_para(c0, a, size=9, bold=True, color=WHITE)
            cell_para(c1, b, size=9, bold=True, color=WHITE)
        else:
            shade_cell(c0, LIGHT_TEAL)
            shade_cell(c1, "FFFFFF")
            p = cell_para(c0, "", size=9)
            add_text(p, a.split()[0] + " ", size=9, color=BODY)
            add_super(p, a.split()[-1])
            cell_para(c1, b, size=9, color=BODY)
    set_table_widths(table, [2200, 7880])
    return table


def support_row(table, i, section, copy, refs, status, quote):
    values = [section, copy, refs, status, quote]
    fills = {
        "Supported": LIGHT_GREEN,
        "Partial": LIGHT_AMBER,
        "Not supported": "FDECEC",
        "N/A — product/legal": ROW_ALT,
    }
    for j, val in enumerate(values):
        cell = table.cell(i, j)
        set_cell_margins(cell, 45, 55, 70, 70)
        set_cell_borders(cell)
        if i == 0:
            shade_cell(cell, "00738A")
            cell_para(cell, val, size=8, bold=True, color=WHITE)
        else:
            shade_cell(cell, fills.get(status, "FFFFFF") if j == 3 else ("FFFFFF" if i % 2 else ROW_ALT))
            color = GREEN if status == "Supported" and j == 3 else (
                AMBER if status == "Partial" and j == 3 else (
                    RGBColor(0x9B, 0x1C, 0x1C) if status == "Not supported" and j == 3 else BODY
                )
            )
            bold = j in (0, 2, 3)
            size = 8 if j != 4 else 8
            cell_para(cell, val, size=size, bold=bold, color=color if j == 3 else BODY)


def build():
    doc = Document()

    # Page setup
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)

    # Header / footer
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    add_text(hp, "AC7988  |  READ™ Patient Education Brochure  |  Copy Deck D5 + Reference Markup", size=8, color=MUTED)
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_text(fp, "CONFIDENTIAL — For medical/legal review  •  References: REF-29185, REF-15633, REF-20457  •  ", size=8, color=MUTED)
    add_text(fp, "© 2026 Alcon Inc. 09/26 GLB/IMG-WLO-2600010", size=8, color=MUTED)

    banner(doc, "AC7988  ·  READ™ Patient Education  ·  Copy Deck with Reference Markup")
    doc.add_paragraph()
    make_header_table(doc)

    subhead_copy(doc, "Version History")
    version_table(doc)

    subhead_copy(doc, "How this markup works")
    body_para(doc, [(
        "Each claim in the D5 copy was checked against the three provided source PDFs. "
        "Where a source supports the wording (or the same medical meaning), a superscript citation was added. "
        "Reference numbers follow first appearance in the copy. Claims with no matching support in the three PDFs "
        "are left unmarked in the copy and flagged in the support grid at the end of this document.",
        {"size": 10, "color": BODY},
    )])
    legend_table(doc)

    p = doc.add_paragraph()
    set_spacing(p, before=8, after=2)
    add_text(p, "Citation style in copy:  ", size=10, italic=True, color=MUTED)
    add_text(p, "Presbyopia is a normal part of aging.", size=10, color=BODY)
    add_super(p, "1,2")
    add_text(p, "  Combined superscripts mean more than one source independently supports the same claim.", size=10, italic=True, color=MUTED)

    add_horizontal_line(doc)

    # ========== COPY START ==========
    p = doc.add_paragraph()
    set_spacing(p, before=4, after=10)
    add_text(p, "[COPY DECK]", size=11, bold=True, color=ALCON_TEAL)

    section_label(doc, "[Header]")
    heading_copy(doc, "See Life Up Close Again")
    body_para(doc, [
        ("Learn more about READ™, presbyopia laser vision correction", {"size": 12, "italic": True, "color": ALCON_DARK}),
        ("super", "2,3"),
    ])

    section_label(doc, "[Subhead]")
    subhead_copy(doc, "Is My Vision Changing?")

    section_label(doc, "[Body]")
    body_para(doc, [
        ("If you have difficulty with close-up tasks, such as reading a book, checking your phone, or looking at a restaurant menu, it may be a sign of presbyopia.", {"size": 11, "color": BODY}),
        ("super", "1,2"),
    ])
    body_para(doc, [
        ("Presbyopia is a normal part of aging.", {"size": 11, "color": BODY}),
        ("super", "1,2"),
        (" Over time, the natural lens in your eye becomes less flexible, and stops focusing light correctly on the retina, which makes nearby objects look blurry.", {"size": 11, "color": BODY}),
        ("super", "1,2"),
    ])

    p = doc.add_paragraph()
    set_spacing(p, before=8, after=4)
    add_text(p, "Common Symptoms Include:", size=11, bold=True, color=ALCON_DARK)

    bullet(doc, [
        ("Blurred vision up close", {"size": 11, "color": BODY}),
        ("super", "1,2"),
    ])
    bullet(doc, [
        ("Holding reading material farther away to see it clearly", {"size": 11, "color": BODY}),
        ("super", "1,2"),
    ])
    bullet(doc, [
        ("Tired or strained eyes during close-up tasks", {"size": 11, "color": BODY}),
        ("super", "1,2"),
    ])
    bullet(doc, [
        ("Headaches after reading or other close-up work", {"size": 11, "color": BODY}),
        ("super", "1,2"),
    ])

    section_label(doc, "[Subhead]")
    subhead_copy(doc, "How is Presbyopia Managed?")

    section_label(doc, "[Body]")
    body_para(doc, [
        ("Your eye care professional may suggest any of the following to manage your vision:", {"size": 11, "color": BODY}),
        ("super", "1,2"),
    ])
    bullet(doc, [
        ("Reading or prescription glasses", {"size": 11, "color": BODY}),
        ("super", "1,2"),
    ])
    bullet(doc, [
        ("Progressive lenses", {"size": 11, "color": BODY}),
        ("super", "2"),
    ])
    bullet(doc, [
        ("Contact lenses", {"size": 11, "color": BODY}),
        ("super", "1,2"),
    ])
    bullet(doc, [
        ("Lens replacement procedures", {"size": 11, "color": BODY}),
        ("super", "2"),
    ])
    bullet(doc, [
        ("Laser vision correction", {"size": 11, "color": BODY}),
        ("super", "2,3"),
    ])
    body_para(doc, [
        ("A modern approach to laser vision correction that may be recommended for presbyopia is READ™, which stands for Refractive Enhanced Adjusted Distance.", {"size": 11, "color": BODY}),
        ("super", "2,3"),
    ], before=8)

    note_box(
        doc,
        "MLR note — product name expansion",
        "The scientific sources support laser vision correction as a presbyopia option (2) and aspheric/"
        "Custom Q–type corneal ablation as a proposed surgical approach to compensate for presbyopia (3). "
        "The brand name READ™ and the expansion “Refractive Enhanced Adjusted Distance” are product nomenclature "
        "and are not named in the three source PDFs.",
    )

    section_label(doc, "[Subhead]")
    subhead_copy(doc, "What is READ™?")

    section_label(doc, "[Body]")
    body_para(doc, [
        ("The READ™ procedure is designed to address presbyopia", {"size": 11, "color": BODY}),
        ("super", "3"),
        (" and optimize each eye so they can continue working together to support vision across near, intermediate, and far distances", {"size": 11, "color": BODY}),
        ("super", "2,3"),
        (" – with less dependence on glasses or contact lenses.", {"size": 11, "color": BODY}),
        ("super", "2"),
    ])

    note_box(
        doc,
        "MLR note — mechanism vs. product claim",
        "Source 3 supports modifying corneal asphericity / inducing negative spherical aberration to extend depth of focus "
        "as a surgical approach to compensate for presbyopia (including Alcon Custom Q aspheric profiles). "
        "Source 2 supports binocular strategies (monovision / modified monovision / multifocal optics) covering near, "
        "intermediate, and distance, and lists laser refractive surgery among options that can reduce the need to rely "
        "only on spectacles or contact lenses. The three PDFs do not report READ™-specific clinical outcomes.",
        fill=LIGHT_TEAL,
    )

    section_label(doc, "[Visual]")
    body_para(doc, [
        ("How READ™ Works", {"size": 12, "italic": True, "color": ALCON_DARK}),
    ])
    body_para(doc, [
        ("[Visual placeholder — no body copy to reference in D5]", {"size": 10, "italic": True, "color": MUTED}),
    ])

    section_label(doc, "[Subhead]")
    subhead_copy(doc, "Could READ™ Be Right for Me?")

    section_label(doc, "[Body copy]")
    body_para(doc, [
        ("Get back to the activities you love — comfortably and clearly", {"size": 11, "bold": True, "color": ALCON_DARK}),
        ("super", "2"),
    ])
    bullet(doc, [
        ("Read with ease without straining or searching for your glasses.", {"size": 11, "color": BODY}),
        ("super", "2"),
    ])
    bullet(doc, [
        ("Stay connected and scroll through your day with clarity.", {"size": 11, "color": BODY}),
    ])
    bullet(doc, [
        ("Pursue your passions and hobbies with greater comfort.", {"size": 11, "color": BODY}),
        ("super", "2"),
    ])
    bullet(doc, [
        ("Greater freedom from glasses and reclaim the freedom of natural vision.", {"size": 11, "color": BODY}),
        ("super", "2"),
    ])
    body_para(doc, [
        ("READ™ may be an option if you have presbyopia and are interested in reducing your dependence on glasses.", {"size": 11, "color": BODY}),
        ("super", "2,3"),
    ], before=8)

    note_box(
        doc,
        "MLR note — lifestyle lines",
        "“Stay connected and scroll through your day with clarity” is promotional and is not specifically supported by the three PDFs. "
        "Source 2 describes returning to near tasks (reading menus/novels, hobbies) after choosing a correction option, "
        "and lists surgery among options for people who want to see up close again. It does not quantify “freedom from glasses.”",
    )

    section_label(doc, "[Subhead]")
    subhead_copy(doc, "Frequently Asked Questions")

    p = doc.add_paragraph()
    set_spacing(p, before=8, after=4)
    add_text(p, "1. What happens if I decide to have the procedure?", size=11, bold=True, color=ALCON_DARK)

    body_para(doc, [
        ("Your eye care professional may perform an eye exam, review your health history and lifestyle to confirm if you’re a candidate for READ™.", {"size": 11, "color": BODY}),
        ("super", "1,2"),
    ])
    body_para(doc, [
        ("The procedure is quick, usually a few minutes per eye.", {"size": 11, "color": BODY}),
    ])
    note_box(
        doc,
        "Unreferenced — needs a source beyond the three PDFs",
        "Procedure duration (“a few minutes per eye”) is not stated in REF-15633, REF-20457, or REF-29185. "
        "Source 2 only describes refractive surgery as a minimally invasive outpatient procedure.",
    )

    p = doc.add_paragraph()
    set_spacing(p, before=10, after=4)
    add_text(p, "2. Will I still need glasses after READ™?", size=11, bold=True, color=ALCON_DARK)
    body_para(doc, [
        ("Individual results may vary but READ™ can reduce your dependence on glasses or contact lenses.", {"size": 11, "color": BODY}),
        ("super", "2"),
    ])
    note_box(
        doc,
        "MLR note — results language",
        "“Individual results may vary” is a disclaimer, not a cited claim. Source 2 supports that refractive surgery is among "
        "options used so patients are not limited to glasses or contacts for near work. The three PDFs do not contain "
        "READ™-specific spectacle-independence rates.",
        fill=LIGHT_TEAL,
    )

    p = doc.add_paragraph()
    set_spacing(p, before=10, after=4)
    add_text(p, "3. Will I experience discomfort?", size=11, bold=True, color=ALCON_DARK)
    body_para(doc, [
        ("Numbing eye drops are typically used to help you experience little to no discomfort. After the procedure, your doctor may recommend or prescribe medication or eye drops to help manage any temporary discomfort. Individual results may vary.", {"size": 11, "color": BODY}),
    ])
    note_box(
        doc,
        "Unreferenced — needs a source beyond the three PDFs",
        "Anesthetic drops, postoperative medication, and expected comfort are not described in the three provided references. "
        "Source 1 and Source 2 discuss diagnostic dilating drops (exam), not surgical anesthesia.",
    )

    p = doc.add_paragraph()
    set_spacing(p, before=10, after=4)
    add_text(p, "4. How soon can I get back to my routine?", size=11, bold=True, color=ALCON_DARK)
    body_para(doc, [
        ("Many people are able to return to normal activities the next day, while others may experience temporary side effects. Each person’s recovery after laser eye surgery is different.", {"size": 11, "color": BODY}),
    ])
    note_box(
        doc,
        "Unreferenced — needs a source beyond the three PDFs",
        "Return-to-activity timing and temporary postoperative side effects are not stated in REF-15633, REF-20457, or REF-29185.",
    )

    section_label(doc, "[General Note]")
    body_para(doc, [
        ("The information provided in this FAQ is intended for general educational and informational purposes only and is not intended to replace the professional judgment, clinical assessment, or individualized recommendations of a qualified eye care professional. Please consult with and follow the recommendations of your eye care professional regarding your eye care or treatment.", {"size": 10, "italic": True, "color": MUTED}),
        ("super", "1"),
    ])

    section_label(doc, "[CTA]")
    p = doc.add_paragraph()
    set_spacing(p, before=4, after=2)
    add_text(p, "See What’s Possible.", size=16, bold=True, color=ALCON_DARK)
    body_para(doc, [
        ("Talk with your eye care professional to see if READ™ is right for you.", {"size": 11, "color": BODY}),
        ("super", "2"),
    ])

    add_horizontal_line(doc)

    # ========== MICE / REFERENCES ==========
    section_label(doc, "[MICE]")
    subhead_copy(doc, "References")

    refs = [
        (
            "1",
            "REF-29185",
            "National Eye Institute (National Institutes of Health). Presbyopia. National Eye Institute website. Last updated December 4, 2024. Available at: https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/presbyopia",
        ),
        (
            "2",
            "REF-15633",
            "Cleveland Clinic. Presbyopia. Cleveland Clinic website. Last reviewed June 8, 2020. Available at: https://my.clevelandclinic.org/health/diseases/8577-presbyopia",
        ),
        (
            "3",
            "REF-20457",
            "Gatinel D, Azar DT, Dumas L, Malet J. Effect of anterior corneal surface asphericity modification on fourth-order Zernike spherical aberrations. J Refract Surg. 2014;30(10):708-715. doi:10.3928/1081597X-20140903-10",
        ),
    ]

    table = doc.add_table(rows=4, cols=3)
    headers = ("No.", "Alcon REF ID", "Citation")
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        shade_cell(cell, "00738A")
        set_cell_margins(cell, 50, 55, 70, 70)
        set_cell_borders(cell)
        cell_para(cell, h, size=9, bold=True, color=WHITE)
    for i, (num, refid, cite) in enumerate(refs, start=1):
        vals = (num, refid, cite)
        for j, val in enumerate(vals):
            cell = table.cell(i, j)
            set_cell_margins(cell, 50, 55, 70, 70)
            set_cell_borders(cell)
            shade_cell(cell, LIGHT_TEAL if j < 2 else "FFFFFF")
            cell_para(cell, val, size=9, bold=(j < 2), color=ALCON_DARK if j < 2 else BODY)
    set_table_widths(table, [800, 1800, 7480])

    p = doc.add_paragraph()
    set_spacing(p, before=12, after=4)
    add_text(p, "© 2026 Alcon Inc. 09/26 GLB/IMG-WLO-2600010", size=9, color=MUTED)

    section_label(doc, "[WATCHOUT]")
    note_box(
        doc,
        "WATCHOUT: THIS IS A GLOBAL TEMPLATE.",
        "IN ACCORDANCE WITH THE ALCON GLOBAL POLICY ON PROFESSIONAL PRACTICES (THE LENS) AND APPLICABLE LAWS, "
        "REGULATIONS, LOCAL INDUSTRY CODES AND LOCAL POLICIES (E.G., IMPORTANT PRODUCT INFORMATION (IPI)), THIS DOCUMENT "
        "MUST BE REVIEWED AND APPROVED VIA A LOCAL MATERIAL APPROVAL PROCESS (LMAP) BEFORE IT MAY BE USED IN PROMOTIONAL ACTIVITIES.",
        fill="FDECEC",
    )

    # ========== SUPPORT GRID ==========
    doc.add_page_break()
    banner(doc, "Appendix  —  Claim-by-claim support from the three REF PDFs")

    body_para(doc, [(
        "This grid is the working annotation for medical/legal review. Green = the cited source(s) state the same meaning. "
        "Amber = related support, but the copy is broader than the source or is a product-framed interpretation. "
        "Red = no support in the three PDFs provided. Quotes are taken from the supplied PDFs.",
        {"size": 10, "color": BODY},
    )])

    claims = [
        ("Section / Copy", "Copy excerpt", "Ref(s)", "Status", "Supporting excerpt from source PDF"),
        (
            "[Header] Subhead",
            "Learn more about READ™, presbyopia laser vision correction",
            "2, 3",
            "Partial",
            "2: LASIK, PRK, and SMILE “correct presbyopia by using monovision.” 3: “modifying the corneal asphericity by creating a hyperprolate corneal surface has been proposed as a surgical approach to compensate for presbyopia.” READ™ is not named.",
        ),
        (
            "Is My Vision Changing?",
            "Difficulty with close-up tasks (reading a book, checking your phone, looking at a restaurant menu) may be a sign of presbyopia",
            "1, 2",
            "Supported",
            "1: “Presbyopia is a refractive error that makes it hard for middle-aged and older adults to see things up close.” 2: “Have you noticed you’re holding your phone farther away… squinting to read that text? Having trouble with up-close tasks… you may be experiencing… presbyopia.” 2 also: “you’ll be reading menus again.”",
        ),
        (
            "Is My Vision Changing?",
            "Presbyopia is a normal part of aging",
            "1, 2",
            "Supported",
            "1: “Presbyopia is a normal part of aging. Everyone gets presbyopia as they get older — usually after age 45.” 2: “Presbyopia is part of the natural aging process of the eye… It’s not a disease, it’s as normal as wrinkles.”",
        ),
        (
            "Is My Vision Changing?",
            "The natural lens becomes less flexible and stops focusing light correctly on the retina, which makes nearby objects look blurry",
            "1, 2",
            "Supported",
            "1 (near-verbatim): “As you age, the lens in your eye gets harder and less flexible, and it stops focusing light correctly on the retina. This makes nearby objects look blurry.” 2: “Presbyopia occurs when the aging lens of your eye becomes less flexible and can no longer focus on objects up-close… This causes close items to blur.”",
        ),
        (
            "Common symptoms",
            "Blurred vision up close",
            "1, 2",
            "Supported",
            "1: “Trouble seeing things up close.” 2: “Blurred vision at a normal reading distance.”",
        ),
        (
            "Common symptoms",
            "Holding reading material farther away to see it clearly",
            "1, 2",
            "Supported",
            "1: “Needing to hold reading materials farther away to focus on them.” 2: “The need to hold reading material at arm's length.”",
        ),
        (
            "Common symptoms",
            "Tired or strained eyes during close-up tasks",
            "1, 2",
            "Supported",
            "1: “Eye strain (when your eyes feel tired or sore).” 2: “Eye strain.” Also 2: “Headaches from doing close work.”",
        ),
        (
            "Common symptoms",
            "Headaches after reading or other close-up work",
            "1, 2",
            "Supported",
            "1: Symptom list includes “Headache.” 2: “Headaches from doing close work.”",
        ),
        (
            "How is Presbyopia Managed?",
            "Your eye care professional may suggest options to manage your vision",
            "1, 2",
            "Supported",
            "1: As presbyopia gets worse, “you’ll probably need glasses or contact lenses.” 2: “Discuss the best choice for you with your eye care provider. Depending upon your overall health and lifestyle, your provider may suggest any of the following…”",
        ),
        (
            "Management bullets",
            "Reading or prescription glasses",
            "1, 2",
            "Supported",
            "1: OTC reading glasses or prescribed lenses. 2: “prescription glasses… reading glasses.”",
        ),
        (
            "Management bullets",
            "Progressive lenses",
            "2",
            "Supported",
            "2: “progressive addition lenses” / “Progressives are multifocal lenses, similar to bifocals, but have a more gradual shift between the prescriptions.”",
        ),
        (
            "Management bullets",
            "Contact lenses",
            "1, 2",
            "Supported",
            "1: “glasses or contact lenses to help you read.” 2: bifocal, multifocal, monovision, and modified monovision contact lenses.",
        ),
        (
            "Management bullets",
            "Lens replacement procedures",
            "2",
            "Supported",
            "2: “Lens replacement: Some people are better suited for procedures that remove the natural lens… refractive lens exchange (RLE).”",
        ),
        (
            "Management bullets",
            "Laser vision correction",
            "2, 3",
            "Supported",
            "2: LASIK, PRK, SMILE listed as laser procedures that correct presbyopia (via monovision). 3: excimer laser keratorefractive surgery for “presbyopic compensation”; Custom Q (Alcon) Q-factor-optimized ablation profiles.",
        ),
        (
            "How is Presbyopia Managed?",
            "A modern approach… READ™… may be recommended for presbyopia",
            "2, 3",
            "Partial",
            "Laser for presbyopia is supported (2, 3). READ™ as a named procedure is not in the PDFs. 3 discusses Alcon Custom Q aspheric treatments that can plan induction of spherical aberration and are relevant to presbyopia compensation.",
        ),
        (
            "What is READ™?",
            "Designed to address presbyopia",
            "3",
            "Partial",
            "3: “modifying the corneal asphericity by creating a hyperprolate corneal surface has been proposed as a surgical approach to compensate for presbyopia.” Also: implications “during excimer laser keratorefractive surgery for both emmetropization and presbyopic compensation.”",
        ),
        (
            "What is READ™?",
            "Optimize each eye so they can continue working together across near, intermediate, and far distances",
            "2, 3",
            "Partial",
            "2: monovision (one eye distance, one near); modified monovision; multifocal lenses “include more than two focal points, including the intermediate zone of about 3 feet.” 3: induction of negative spherical aberration “may also serve to extend the depth of focus and through-focus visual acuity,” allowing a target to move closer with relatively small decrease of visual quality. Binocular “working together” is inferred from 2, not stated for READ™.",
        ),
        (
            "What is READ™?",
            "With less dependence on glasses or contact lenses",
            "2",
            "Partial",
            "2 presents refractive surgery as an alternative to glasses and contacts so patients can “see things up close again,” and notes that if glasses are used only part of the time, surgery may be more risk than reward. No spectacle-independence rate is given.",
        ),
        (
            "Could READ™ Be Right for Me?",
            "Get back to the activities you love / read with ease / passions and hobbies",
            "2",
            "Partial",
            "2 closing note: once you choose a correction option, “you’ll be able to focus again on all your favorite things in fine detail — whether it’s reading the latest novel, painting… or sewing.” Also: “you’ll be reading menus again in no time.”",
        ),
        (
            "Could READ™ Be Right for Me?",
            "Stay connected and scroll through your day with clarity",
            "—",
            "Not supported",
            "No matching statement in REF-15633, REF-20457, or REF-29185.",
        ),
        (
            "Could READ™ Be Right for Me?",
            "Greater freedom from glasses and reclaim the freedom of natural vision",
            "2",
            "Partial",
            "2 frames surgery/contacts/glasses as options to restore near focus. “Freedom of natural vision” is promotional and not sourced. Cite 2 only for the glasses-alternative meaning.",
        ),
        (
            "Could READ™ Be Right for Me?",
            "READ™ may be an option if you have presbyopia and are interested in reducing dependence on glasses",
            "2, 3",
            "Partial",
            "2: discuss with provider whether surgery is right; laser/lens options exist for presbyopia. 3: aspheric laser approach proposed to compensate for presbyopia. Candidacy for READ™ specifically is not in the PDFs.",
        ),
        (
            "FAQ 1",
            "Eye exam, health history and lifestyle to confirm if you’re a candidate",
            "1, 2",
            "Supported",
            "1: “Eye doctors can check for presbyopia as part of a comprehensive eye exam.” 2: diagnosis by thorough eye exam; before surgery, “Discuss your eye health, family history and lifestyle with your provider before you decide if surgery is right for you, and which option fits your lifestyle best.”",
        ),
        (
            "FAQ 1",
            "The procedure is quick, usually a few minutes per eye",
            "—",
            "Not supported",
            "Not stated in the three PDFs. 2 only: refractive surgery is “considered a minimally-invasive outpatient surgery.”",
        ),
        (
            "FAQ 2",
            "READ™ can reduce your dependence on glasses or contact lenses",
            "2",
            "Partial",
            "Same support as the glasses-dependence claim above. No READ™ outcomes data in the three PDFs. “Individual results may vary” is uncited disclaimer language.",
        ),
        (
            "FAQ 3",
            "Numbing eye drops; little to no discomfort; postoperative medication/drops for temporary discomfort",
            "—",
            "Not supported",
            "Not in the three PDFs. Dilating drops in 1/2 refer to the diagnostic exam, not surgical anesthesia.",
        ),
        (
            "FAQ 4",
            "Many people return to normal activities the next day; temporary side effects; recovery differs",
            "—",
            "Not supported",
            "Not stated in REF-15633, REF-20457, or REF-29185.",
        ),
        (
            "[General Note]",
            "Educational only; not a substitute for professional judgment; consult your eye care professional",
            "1",
            "Partial",
            "1: “The National Eye Institute does not diagnose diseases, offer specific treatment recommendations, or provide physician referrals.” Supports the educational-not-advice meaning; Alcon legal wording is its own.",
        ),
        (
            "[CTA]",
            "Talk with your eye care professional to see if READ™ is right for you",
            "2",
            "Supported",
            "2: “Discuss the best choice for you with your eye care provider.” and “Discuss your eye health, family history and lifestyle with your provider before you decide if surgery is right for you.”",
        ),
    ]

    table = doc.add_table(rows=len(claims), cols=5)
    for i, row in enumerate(claims):
        support_row(table, i, *row)
    set_table_widths(table, [1600, 2100, 900, 1300, 4180])

    subhead_copy(doc, "Source snapshot (what each PDF is good for)")
    bullets_src = [
        "REF-29185 (1) — NIH patient page. Best support for: definition of presbyopia, “normal part of aging,” lens flexibility / light not focusing on the retina / near blur, symptom list, glasses and contact lenses, comprehensive eye exam, educational disclaimer tone. Does not cover surgery, laser, READ™, recovery, or comfort.",
        "REF-15633 (2) — Cleveland Clinic patient page. Best support for: near-task examples (phone, menus), aging lens, symptoms, the management menu (readers, prescription glasses, progressives, contacts, laser, lens replacement), candidacy conversation (exam, health history, lifestyle), and returning to close-up activities. Laser for presbyopia is described as monovision LASIK/PRK/SMILE, not as READ™.",
        "REF-20457 (3) — Gatinel et al., Journal of Refractive Surgery, 2014. Best support for: aspheric / Q-value customized excimer ablation (including Alcon Custom Q) to induce negative spherical aberration, extend depth of focus, and compensate for presbyopia. Does not name READ™ and does not contain patient-facing outcome, comfort, or recovery data.",
    ]
    for t in bullets_src:
        bullet(doc, [(t, {"size": 10, "color": BODY})])

    p = doc.add_paragraph()
    set_spacing(p, before=16, after=0)
    add_text(p, "[Logo]  Alcon", size=11, bold=True, color=ALCON_TEAL)

    out = "/workspace/AC7988_READ_Patient_Education_Copy_Deck_D5_Reference_Markup.docx"
    doc.save(out)
    print(out)


if __name__ == "__main__":
    build()
