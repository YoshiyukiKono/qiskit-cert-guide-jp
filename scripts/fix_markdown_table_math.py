"""Conservatively repair literal math pipes in top-level Markdown tables.

Python 3.10+, standard library only. Default: print a diff, never write.
"""

import argparse
import difflib
import re
import sys
from pathlib import Path


class UnsafeTable(ValueError):
    """The row cannot be interpreted without guessing."""


def escaped(text: str, pos: int) -> bool:
    start = pos
    while start > 0 and text[start - 1] == "\\":
        start -= 1
    return (pos - start) % 2 == 1


def repair_row(line: str, columns: int) -> str:
    """Replace unescaped pipes only inside paired single-dollar math spans."""
    pieces = []
    in_math = False
    separators = 0
    i = 0
    while i < len(line):
        char = line[i]
        if char == "`" and not escaped(line, i):
            run = re.match(r"`+", line[i:])[0]
            end = re.search(r"(?<!`)" + re.escape(run) + r"(?!`)", line[i + len(run):])
            if in_math or end is None:
                raise UnsafeTable("ambiguous code span")
            stop = i + len(run) + end.end()
            code = line[i:stop]
            # Markdown table parsers also split unescaped pipes in code spans.
            if any(c == "|" and not escaped(code, n) for n, c in enumerate(code)):
                raise UnsafeTable("unescaped pipe in code span")
            pieces.append(code)
            i = stop
            continue
        if char == "$" and not escaped(line, i):
            if line[i:i + 2] == "$$":
                raise UnsafeTable("display math in table row")
            in_math = not in_math
        if char == "|" and not escaped(line, i):
            if in_math:
                # Space terminates the TeX command, including before letters.
                pieces.append(r"\vert ")
            else:
                separators += 1
                pieces.append(char)
        else:
            pieces.append(char)
        i += 1
    if in_math:
        raise UnsafeTable("unpaired dollar delimiter")
    if separators != columns + 1:
        raise UnsafeTable("column count does not match delimiter row")
    return "".join(pieces)


def table_row(line: str) -> bool:
    return bool(re.match(r"^ {0,3}\|.*\|[ \t]*(?:\r?\n)?$", line))


def delimiter_columns(line: str) -> int:
    if not table_row(line):
        return 0
    cells = line.strip()[1:-1].split("|")
    return len(cells) if all(re.fullmatch(r"\s*:?-{3,}:?\s*", c) for c in cells) else 0


def repair(text: str) -> str:
    """Return new text; retain BOM, line endings and all non-target content."""
    bom = "\ufeff" if text.startswith("\ufeff") else ""
    lines = text[len(bom):].splitlines(keepends=True)
    result = list(lines)
    fence = None
    html_block = False
    html_end = None
    display_math = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if html_end:
            if html_end.search(line):
                html_end = None
            i += 1
            continue
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}[ \t]*\r?\n?", line):
                fence = None
            i += 1
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if opening:
            fence = opening[1]
            i += 1
            continue
        # Comments/raw HTML may contain blank lines and table-looking text.
        raw_html = re.match(r"^ {0,3}<(script|pre|style|textarea)(?:\s|>)", line, re.I)
        if line.lstrip().startswith("<!--") or raw_html:
            end_pattern = r"-->" if not raw_html else r"</" + raw_html[1] + r"\s*>"
            html_end = re.compile(end_pattern, re.I)
            if html_end.search(line):
                html_end = None
            i += 1
            continue
        # Conservatively ignore other HTML blocks through the next blank line.
        if line.lstrip().startswith("<"):
            html_block = True
        if html_block:
            if not line.strip():
                html_block = False
            i += 1
            continue
        if line.strip() == "$$":
            display_math = not display_math
        if display_math:
            i += 1
            continue
        columns = delimiter_columns(lines[i + 1]) if i + 1 < len(lines) else 0
        if table_row(line) and columns:
            end = i + 2
            while end < len(lines) and table_row(lines[end]):
                end += 1
            for row in [i, *range(i + 2, end)]:
                try:
                    result[row] = repair_row(lines[row], columns)
                except UnsafeTable as exc:
                    raise UnsafeTable(f"line {row + 1}: {exc}") from exc
            i = end
        else:
            i += 1
    return bom + "".join(result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, help="write a NEW file; existing files are refused")
    args = parser.parse_args()
    try:
        original = args.input.read_bytes().decode("utf-8")
        fixed = repair(original)
        if args.output:
            # Exclusive creation prevents overwriting source, aliases or other files.
            with args.output.open("xb") as stream:
                stream.write(fixed.encode("utf-8"))
            print(f"Saved: {args.output}")
        else:
            diff = difflib.unified_diff(original.splitlines(keepends=True), fixed.splitlines(keepends=True), fromfile=str(args.input), tofile=str(args.input) + " (preview)")
            sys.stdout.writelines(diff)
    except (OSError, UnicodeError, UnsafeTable) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
