"""Build the printable A5 pocket reference from its Markdown source."""

from __future__ import annotations

import html
import hashlib
import re
import shutil
import unicodedata
from pathlib import Path

import cairosvg
import ziamath
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph as ReportLabParagraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "qiskit-pocket-reference.md"
OUTPUT = ROOT / "qiskit-pocket-reference.pdf"
FORMULA_DIR = ROOT.parent / "tmp" / "pdfs" / "pocket-reference-formulas"

PAGE_WIDTH, PAGE_HEIGHT = A5
MARGIN_X = 10 * mm
MARGIN_TOP = 13 * mm
MARGIN_BOTTOM = 12 * mm
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN_X

INK = colors.HexColor("#17233C")
MUTED = colors.HexColor("#526078")
BLUE = colors.HexColor("#2D5BFF")
CYAN = colors.HexColor("#14B8A6")
PALE_BLUE = colors.HexColor("#EAF0FF")
PALE_GRAY = colors.HexColor("#F4F6F8")
GRID = colors.HexColor("#C8D0DD")
CODE_BACKGROUND = colors.HexColor("#F1F5FB")
CODE_BORDER = colors.HexColor("#B7C4D6")
WHITE = colors.white
MATH_DPI = 300
INLINE_MATH_COLOR = "#173F8F"
DISPLAY_MATH_COLOR = "#17233C"


def register_fonts() -> tuple[str, str]:
    candidates = [
        Path(r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"),
        Path(r"C:\Windows\Fonts\NotoSansJP-VF.ttf"),
        Path(r"C:\Windows\Fonts\meiryo.ttc"),
    ]
    bold_candidates = [
        Path(r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"),
        Path(r"C:\Windows\Fonts\NotoSansJP-VF.ttf"),
        Path(r"C:\Windows\Fonts\meiryob.ttc"),
    ]

    regular = next((path for path in candidates if path.exists()), None)
    bold = next((path for path in bold_candidates if path.exists()), regular)
    if regular is None or bold is None:
        raise FileNotFoundError("A Japanese TrueType font was not found.")

    pdfmetrics.registerFont(TTFont("PocketJP", str(regular)))
    pdfmetrics.registerFont(TTFont("PocketJP-Bold", str(bold)))
    return "PocketJP", "PocketJP-Bold"


FONT, FONT_BOLD = register_fonts()


def formula_dimensions(path: Path) -> tuple[float, float]:
    with PILImage.open(path) as image:
        width_px, height_px = image.size
    return width_px * 72 / MATH_DPI, height_px * 72 / MATH_DPI


def render_formula(
    source: str,
    *,
    font_size: float,
    inline: bool,
    color: str,
) -> Path:
    """Render LaTeX consistently with STIX Two Math through Ziamath."""
    source = source.strip()
    render_key = f"{source}\0{font_size}\0{inline}\0{color}\0ziamath-0.13"
    digest = hashlib.sha256(render_key.encode("utf-8")).hexdigest()[:16]
    mode = "inline" if inline else "display"
    path = FORMULA_DIR / f"{mode}-{digest}.png"
    if path.exists():
        return path

    FORMULA_DIR.mkdir(parents=True, exist_ok=True)
    margin = 0.35 if inline else 1.0
    try:
        svg = ziamath.Latex(
            source,
            size=font_size,
            color=color,
            inline=inline,
            margin=margin,
        ).svg()
        cairosvg.svg2png(
            bytestring=svg.encode("utf-8"),
            write_to=str(path),
            scale=MATH_DPI / 72,
        )
    except Exception as error:
        raise ValueError(f"Could not render LaTeX formula: {source}") from error
    return path


def inline_markup(
    text: str,
    *,
    color_override: str | None = None,
    math_size: float = 8.2,
) -> str:
    protected: dict[str, str] = {}
    math_color = color_override or INLINE_MATH_COLOR
    link_color = color_override or "#2D5BFF"
    code_color = color_override or "#163B78"

    def protect_math(match: re.Match[str]) -> str:
        token = f"@@MATH{len(protected)}@@"
        path = render_formula(
            match.group(1),
            font_size=math_size,
            inline=True,
            color=math_color,
        )
        width, height = formula_dimensions(path)
        source_path = html.escape(path.as_posix(), quote=True)
        protected[token] = (
            f'<img src="{source_path}" width="{width:.3f}" '
            f'height="{height:.3f}" valign="middle"/>'
        )
        return token

    text = re.sub(r"(?<!\$)\$([^$\n]+)\$(?!\$)", protect_math, text)
    escaped = html.escape(text, quote=False)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        rf'<link href="\2" color="{link_color}"><u>\1</u></link>',
        escaped,
    )
    escaped = re.sub(
        r"\x60([^\x60]+)\x60",
        rf'<font name="{FONT}" color="{code_color}">\1</font>',
        escaped,
    )
    escaped = re.sub(r"\*\*([^*]+)\*\*", rf'<font name="{FONT_BOLD}">\1</font>', escaped)
    for token, replacement in protected.items():
        escaped = escaped.replace(token, replacement)
    return escaped


class Paragraph(ReportLabParagraph):
    """Keep ReportLab's CJK wrapping safe around inline-math images."""

    def breakLinesCJK(self, widths):
        # ReportLab represents an inline image as a fragment whose text is an
        # empty string.  Its CJK line breaker calls ord() on that placeholder
        # when the image reaches a line boundary.  A private-use placeholder
        # keeps it atomic; drawing still uses cbDefn and emits only the image.
        for fragment in self.frags:
            if hasattr(fragment, "cbDefn") and fragment.text == "":
                fragment.text = "\uf8ff"
        return super().breakLinesCJK(widths)


class FormulaBox(Flowable):
    """An indivisible display-math box with predictable pagination."""

    def __init__(self, path: Path, formula_width: float, formula_height: float):
        super().__init__()
        self.path = path
        self.formula_width = formula_width
        self.formula_height = formula_height
        self.width = CONTENT_WIDTH
        self.height = formula_height + 10
        self.spaceAfter = 4

    def wrap(self, available_width, available_height):
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(PALE_BLUE)
        canvas.setStrokeColor(colors.HexColor("#AFC1F6"))
        canvas.setLineWidth(0.45)
        canvas.rect(0, 0, self.width, self.height, stroke=1, fill=1)
        canvas.drawImage(
            str(self.path),
            (self.width - self.formula_width) / 2,
            5,
            width=self.formula_width,
            height=self.formula_height,
            mask="auto",
        )
        canvas.restoreState()


def make_formula_block(source: str) -> FormulaBox:
    path = render_formula(
        source,
        font_size=16,
        inline=False,
        color=DISPLAY_MATH_COLOR,
    )
    width, height = formula_dimensions(path)
    max_width = CONTENT_WIDTH - 12
    if width > max_width:
        scale = max_width / width
        width *= scale
        height *= scale
    return FormulaBox(path, width, height)


def display_width(text: str) -> int:
    width = 0
    for char in text:
        width += 2 if unicodedata.east_asian_width(char) in {"F", "W", "A"} else 1
    return width


def wrap_code_line(line: str, limit: int = 66) -> list[str]:
    if display_width(line) <= limit:
        return [line]

    indent = len(line) - len(line.lstrip(" "))
    continuation = " " * min(indent + 2, 12)
    output: list[str] = []
    current = ""
    current_width = 0
    for char in line:
        char_width = 2 if unicodedata.east_asian_width(char) in {"F", "W", "A"} else 1
        if current and current_width + char_width > limit:
            output.append(current.rstrip())
            current = continuation + char
            current_width = display_width(current)
        else:
            current += char
            current_width += char_width
    if current:
        output.append(current.rstrip())
    return output


def make_code_block(code: str) -> Table:
    """Place preformatted code in a shaded panel distinct from body text."""
    content = Preformatted(code, STYLES["PocketCode"])
    block = Table([[content]], colWidths=[CONTENT_WIDTH], hAlign="LEFT")
    block.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BACKGROUND),
                ("BOX", (0, 0), (-1, -1), 0.55, CODE_BORDER),
                ("LINEBEFORE", (0, 0), (0, -1), 2.4, BLUE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    block.spaceBefore = 2
    block.spaceAfter = 5
    return block


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="PocketBody",
            fontName=FONT,
            fontSize=8.2,
            leading=11.6,
            textColor=INK,
            wordWrap="CJK",
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PocketTitle",
            fontName=FONT_BOLD,
            fontSize=22,
            leading=29,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PocketBodyKeep",
            parent=styles["PocketBody"],
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PocketH1",
            fontName=FONT_BOLD,
            fontSize=14,
            leading=18,
            textColor=WHITE,
            backColor=BLUE,
            borderPadding=(5, 6, 5, 6),
            spaceBefore=8,
            spaceAfter=7,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PocketH2",
            fontName=FONT_BOLD,
            fontSize=11.3,
            leading=14.5,
            textColor=INK,
            borderColor=CYAN,
            borderWidth=0,
            borderPadding=(2, 0, 2, 5),
            spaceBefore=7,
            spaceAfter=4,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PocketH3",
            fontName=FONT_BOLD,
            fontSize=9.3,
            leading=12,
            textColor=BLUE,
            spaceBefore=5,
            spaceAfter=3,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PocketBullet",
            parent=styles["PocketBody"],
            leftIndent=10,
            firstLineIndent=-7,
            bulletIndent=2,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PocketNumber",
            parent=styles["PocketBody"],
            leftIndent=14,
            firstLineIndent=-12,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PocketCode",
            fontName=FONT,
            fontSize=6.9,
            leading=9.1,
            textColor=colors.HexColor("#14213D"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="PocketTable",
            fontName=FONT,
            fontSize=6.7,
            leading=8.9,
            autoLeading="max",
            textColor=INK,
            wordWrap="CJK",
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PocketTableHead",
            fontName=FONT_BOLD,
            fontSize=6.8,
            leading=9,
            autoLeading="max",
            textColor=WHITE,
            wordWrap="CJK",
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PocketSmall",
            parent=styles["PocketBody"],
            fontSize=7.1,
            leading=9.5,
            textColor=MUTED,
        )
    )
    return styles


STYLES = build_styles()


def split_table_row(line: str) -> list[str]:
    content = line.strip()
    if content.startswith("|"):
        content = content[1:]
    if content.endswith("|"):
        content = content[:-1]

    cells: list[str] = []
    current: list[str] = []
    inside_code = False
    inside_math = False
    for char in content:
        if char == chr(96):
            inside_code = not inside_code
            current.append(char)
        elif char == "$" and not inside_code:
            inside_math = not inside_math
            current.append(char)
        elif char == "|" and not inside_code and not inside_math:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def is_separator_row(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def validate_markdown_tables(markdown_text: str) -> None:
    """Reject math pipes that GitHub-style Markdown treats as cell separators."""
    for line_number, line in enumerate(markdown_text.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            continue
        for match in re.finditer(r"(?<!\$)\$([^$\n]+)\$(?!\$)", line):
            if "|" in match.group(1):
                raise ValueError(
                    "Raw '|' inside table math breaks Markdown preview "
                    f"(line {line_number}); use \\lvert or \\rvert."
                )


def make_table(rows: list[list[str]]) -> KeepTogether:
    column_count = max(len(row) for row in rows)
    normalized = [row + [""] * (column_count - len(row)) for row in rows]
    data = []
    for row_index, row in enumerate(normalized):
        is_header = row_index == 0
        style_name = "PocketTableHead" if is_header else "PocketTable"
        header_color = "#FFFFFF" if is_header else None
        data.append(
            [
                Paragraph(
                    inline_markup(
                        cell,
                        color_override=header_color,
                        math_size=6.8 if is_header else 6.7,
                    ),
                    STYLES[style_name],
                )
                for cell in row
            ]
        )

    if column_count == 2:
        widths = [CONTENT_WIDTH * 0.34, CONTENT_WIDTH * 0.66]
    elif column_count == 3:
        widths = [CONTENT_WIDTH * 0.24, CONTENT_WIDTH * 0.38, CONTENT_WIDTH * 0.38]
    elif column_count == 4:
        widths = [CONTENT_WIDTH * 0.27] + [CONTENT_WIDTH * 0.2433] * 3
    else:
        widths = [CONTENT_WIDTH / column_count] * column_count

    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE_BLUE]),
                ("GRID", (0, 0), (-1, -1), 0.35, GRID),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    table.spaceAfter = 4
    return KeepTogether([table])


def parse_markdown(markdown_text: str):
    story = []
    lines = markdown_text.splitlines()
    index = 0
    paragraph_lines: list[str] = []

    def flush_paragraph(*, keep_with_next: bool = False):
        if paragraph_lines:
            text = " ".join(item.strip() for item in paragraph_lines)
            style = STYLES["PocketBodyKeep"] if keep_with_next else STYLES["PocketBody"]
            story.append(Paragraph(inline_markup(text), style))
            paragraph_lines.clear()

    while index < len(lines):
        stripped = lines[index].strip()

        if stripped == "<!-- pagebreak -->":
            flush_paragraph()
            story.append(PageBreak())
            story.append(Spacer(1, 8 * mm))
            index += 1
            continue

        if stripped == "$$":
            flush_paragraph()
            index += 1
            formula_lines = []
            while index < len(lines) and lines[index].strip() != "$$":
                formula_lines.append(lines[index])
                index += 1
            if index >= len(lines):
                raise ValueError("Unclosed display-math block in Markdown source.")
            story.append(make_formula_block("\n".join(formula_lines)))
            index += 1
            continue

        if stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 4:
            flush_paragraph()
            story.append(make_formula_block(stripped[2:-2]))
            index += 1
            continue

        if stripped.startswith("```"):
            flush_paragraph(keep_with_next=True)
            index += 1
            code_lines = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.extend(wrap_code_line(lines[index]))
                index += 1
            story.append(make_code_block("\n".join(code_lines)))
            index += 1
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            raw_rows = []
            while index < len(lines):
                candidate = lines[index].strip()
                if not (candidate.startswith("|") and candidate.endswith("|")):
                    break
                raw_rows.append(split_table_row(candidate))
                index += 1
            rows = [row for row in raw_rows if not is_separator_row(row)]
            if rows:
                story.append(make_table(rows))
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            heading = stripped[2:].strip()
            if not story:
                story.append(Spacer(1, 15 * mm))
                story.append(
                    Paragraph(inline_markup(heading, math_size=22), STYLES["PocketTitle"])
                )
            else:
                story.append(PageBreak())
                story.append(
                    Paragraph(
                        inline_markup(
                            heading,
                            color_override="#FFFFFF",
                            math_size=14,
                        ),
                        STYLES["PocketH1"],
                    )
                )
            index += 1
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            story.append(
                Paragraph(
                    inline_markup(stripped[3:].strip(), math_size=11.3),
                    STYLES["PocketH2"],
                )
            )
            index += 1
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            story.append(
                Paragraph(
                    inline_markup(stripped[4:].strip(), math_size=9.3),
                    STYLES["PocketH3"],
                )
            )
            index += 1
            continue

        if stripped == "---":
            flush_paragraph()
            story.append(Spacer(1, 3))
            index += 1
            continue

        bullet = re.match(r"^-\s+(.*)$", stripped)
        if bullet:
            flush_paragraph()
            story.append(
                Paragraph(
                    inline_markup(bullet.group(1)),
                    STYLES["PocketBullet"],
                    bulletText="•",
                )
            )
            index += 1
            continue

        numbered = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if numbered:
            flush_paragraph()
            story.append(
                Paragraph(
                    f"{numbered.group(1)}. {inline_markup(numbered.group(2))}",
                    STYLES["PocketNumber"],
                )
            )
            index += 1
            continue

        if not stripped:
            next_index = index + 1
            while next_index < len(lines) and not lines[next_index].strip():
                next_index += 1
            next_is_code = (
                next_index < len(lines)
                and lines[next_index].strip().startswith("```")
            )
            flush_paragraph(keep_with_next=next_is_code)
            index += 1
            continue

        paragraph_lines.append(stripped)
        index += 1

    flush_paragraph()
    return story


def draw_page(canvas, doc):
    canvas.saveState()
    page_number = canvas.getPageNumber()
    if page_number > 1:
        canvas.setFillColor(BLUE)
        canvas.rect(0, PAGE_HEIGHT - 5 * mm, PAGE_WIDTH, 5 * mm, stroke=0, fill=1)
        canvas.setFont(FONT_BOLD, 6.5)
        canvas.setFillColor(WHITE)
        canvas.drawString(MARGIN_X, PAGE_HEIGHT - 3.7 * mm, "Qiskit v2.x ポケットリファレンス")

    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.35)
    canvas.line(MARGIN_X, 8 * mm, PAGE_WIDTH - MARGIN_X, 8 * mm)
    canvas.setFont(FONT, 6.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN_X, 4.8 * mm, "Qiskit 2.5.2 / Runtime 0.49.0")
    canvas.drawRightString(PAGE_WIDTH - MARGIN_X, 4.8 * mm, str(page_number))
    canvas.restoreState()


class PocketDocTemplate(BaseDocTemplate):
    """Isolate page content before drawing headers and footers."""

    def beforePage(self):
        self.canv.saveState()

    def afterPage(self):
        self.canv.restoreState()
        draw_page(self.canv, self)


def build_pdf():
    markdown_text = SOURCE.read_text(encoding="utf-8")
    validate_markdown_tables(markdown_text)
    if FORMULA_DIR.exists():
        shutil.rmtree(FORMULA_DIR)
    doc = PocketDocTemplate(
        str(OUTPUT),
        pagesize=A5,
        leftMargin=MARGIN_X - 6,
        rightMargin=MARGIN_X - 6,
        topMargin=MARGIN_TOP - 6,
        bottomMargin=MARGIN_BOTTOM - 6,
        title="Qiskit v2.x ポケットリファレンス",
        author="qiskit-cert-guide-jp",
        subject="Qiskit certification portable reference",
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="pocket-reference",
    )
    doc.addPageTemplates(
        [
            PageTemplate(
                id="pocket-reference",
                frames=[frame],
                pagesize=A5,
            )
        ]
    )
    doc.build(parse_markdown(markdown_text))
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
