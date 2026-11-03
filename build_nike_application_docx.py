"""Create a Word-readable version of the NIKE FCFF application output."""

from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).parent
OUTPUT = ROOT / "NIKE_FCFF_Application_Results.docx"


def shade(cell, fill):
    properties = cell._tc.get_or_add_tcPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    properties.append(shading)


def set_cell_text(cell, text, bold=False, white=False):
    cell.text = ""
    paragraph = cell.paragraphs[0]
    run = paragraph.add_run(text)
    run.bold = bold
    run.font.size = Pt(9)
    if white:
        run.font.color.rgb = RGBColor(255, 255, 255)


def add_markdown_table(document, lines):
    rows = [[part.strip() for part in line.strip().strip("|").split("|")] for line in lines]
    rows = [row for row in rows if not all(set(cell) <= {"-", ":"} for cell in row)]
    table = document.add_table(rows=0, cols=len(rows[0]))
    table.style = "Table Grid"
    for row_index, values in enumerate(rows):
        cells = table.add_row().cells
        for col_index, value in enumerate(values):
            set_cell_text(cells[col_index], value, bold=row_index == 0, white=row_index == 0)
            if row_index == 0:
                shade(cells[col_index], "1F4E78")
            elif row_index % 2 == 0:
                shade(cells[col_index], "EAF2F8")
    document.add_paragraph()


def main():
    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

    normal = document.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(10)
    normal.paragraph_format.space_after = Pt(5)

    title = document.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run("NIKE FCFF Application Results")
    subtitle = document.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.add_run("Word readable version of the locally runnable valuation application").italic = True

    opening = document.add_paragraph()
    opening.add_run("Purpose. ").bold = True
    opening.add_run(
        "This document presents the visible output of the NIKE five-year FCFF valuation application. "
        "It is intended for review and presentation; the calculations remain in nike_fcff_application.py."
    )

    lines = (ROOT / "nike_fcff_output.md").read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("# "):
            index += 1
            continue
        if line.startswith("## "):
            document.add_heading(line[3:], level=1)
            index += 1
            continue
        if line.startswith("| "):
            table_lines = []
            while index < len(lines) and lines[index].startswith("|"):
                table_lines.append(lines[index])
                index += 1
            add_markdown_table(document, table_lines)
            continue
        if line.startswith("- "):
            document.add_paragraph(line[2:], style="List Bullet")
        elif line.strip():
            document.add_paragraph(line.replace("**", ""))
        index += 1

    document.add_paragraph("Educational analysis only; not investment advice.").italic = True
    document.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
