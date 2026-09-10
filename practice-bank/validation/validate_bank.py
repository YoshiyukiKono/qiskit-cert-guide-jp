"""Strict structural validation of the bank's documented Markdown format.

This checks structure, not scientific truth, distractor plausibility, or whether
an author's domain/task assignment is semantically justified. No check depends
on Python assert statements, so python -O does not disable validation.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TOPIC_FILES = (
    "01-quantum-operations.md", "02-visualization-measurement-states.md",
    "03-circuit-construction.md", "04-running-circuits.md", "05-sampler.md",
    "06-estimator.md", "07-results-analysis.md", "08-openqasm3.md",
)
DOMAIN_RANGES = ((1, 11), (12, 19), (20, 31), (32, 41),
                 (42, 49), (50, 57), (58, 64), (65, 68))
DOMAIN_COUNTS = (11, 8, 12, 10, 8, 8, 7, 4)
LETTERS = tuple("ABCD")


class ValidationError(ValueError):
    """A documented structural invariant is violated."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def outside_code(text: str) -> str:
    """Mask fenced-code lines, preserving line count and all other characters."""
    result: list[str] = []
    fence: str | None = None
    width = 0
    for line in text.splitlines():
        if fence is not None:
            if re.fullmatch(r" {0,3}" + re.escape(fence) + "{" + str(width) + r",}[ \t]*", line):
                fence = None
            result.append("")
            continue
        match = re.match(r" {0,3}(`{3,}|~{3,})", line)
        if match:
            fence, width = match[1][0], len(match[1])
            result.append("")
        else:
            result.append(line)
    require(fence is None, "unclosed fenced code block")
    return "\n".join(result)


def section(text: str, heading: str) -> str:
    lines = text.splitlines()
    masked = outside_code(text).splitlines()
    starts = [i for i, line in enumerate(masked) if line.strip() == heading]
    require(len(starts) == 1, f"expected one {heading!r} section")
    start = starts[0] + 1
    level = len(heading) - len(heading.lstrip("#"))
    end = next((i for i in range(start, len(masked))
                if re.match(r"^#{1," + str(level) + r"} ", masked[i])), len(lines))
    return "\n".join(lines[start:end])


def numbered_blocks(text: str, prefix: str, explanations: bool = False) -> list[tuple[int, str, str]]:
    """Parse numbered headings; return (number, answer-or-empty, original body)."""
    original = text.splitlines()
    masked = outside_code(text).splitlines()
    pattern = re.compile(re.escape(prefix) + r"([1-9]\d*)" +
                         (r" — ([A-D])" if explanations else "") + r"[ \t]*")
    starts = []
    for i, line in enumerate(masked):
        if line.startswith(prefix):
            match = pattern.fullmatch(line)
            require(match is not None, f"malformed heading: {line}")
            starts.append((i, int(match[1]), match[2] if explanations else ""))
    blocks = []
    for i, number, answer in starts:
        end = next((j for j in range(i + 1, len(masked))
                    if re.match(r"^#{1,3} ", masked[j]) or masked[j] == "---"), len(original))
        blocks.append((number, answer, "\n".join(original[i + 1:end])))
    return blocks


def check_numbering(blocks: list[tuple[int, str, str]], count: int, label: str) -> None:
    numbers = [number for number, _, _ in blocks]
    require(numbers == list(range(1, count + 1)), f"{label}: expected Q1-Q{count} once in order; got {numbers}")


def check_choices(body: str, label: str) -> None:
    masked = outside_code(body)
    # Capture every letter, not just A-D; reject E and malformed/empty choices.
    choices = re.findall(r"(?m)^([A-Za-z])\.[ \t]*(.*)$", masked)
    require([letter for letter, _ in choices] == list(LETTERS), f"{label}: expected exactly A-D choices")
    require(all(value.strip() for _, value in choices), f"{label}: empty choice")
    require(len({value.strip() for _, value in choices}) == 4, f"{label}: duplicate choice text")
    first = re.search(r"(?m)^[A-Za-z]\.", masked)
    require(first is not None and bool(re.sub(r"<!--.*?-->", "", masked[:first.start()], flags=re.S).strip()),
            f"{label}: missing question stem")


def check_explanation(body: str, label: str) -> None:
    coverage: Counter[str] = Counter()
    for line in outside_code(body).splitlines():
        if not re.match(r"^- [A-Za-z](?:/|:)", line):
            continue
        match = re.fullmatch(r"- ([A-Za-z](?:/[A-Za-z])*):[ \t]*(.*)", line)
        require(match is not None, f"{label}: malformed explanation bullet")
        require(bool(match[2].strip()), f"{label}: empty explanation bullet")
        coverage.update(match[1].split("/"))
    require(coverage == Counter(LETTERS), f"{label}: explain A-D exactly once; got {dict(coverage)}")


def check_period(answers: list[str], label: str) -> None:
    for period in range(1, min(4, len(answers) // 2) + 1):
        repeated = all(answer == answers[i % period] for i, answer in enumerate(answers))
        require(not repeated, f"{label}: whole answer sequence repeats with period {period}")


def parse_answer_key(text: str, count: int = 68) -> dict[int, str]:
    key_text = section(text, "## Answer Key").split("---", 1)[0]
    # Limit parsing to key lines; the position-summary paragraph is not a key.
    lines = [line.strip() for line in key_text.splitlines() if re.match(r"^\s*\d", line)]
    pairs: list[tuple[int, str]] = []
    for line in lines:
        for token in line.split("/"):
            match = re.fullmatch(r"([1-9]\d*)\s+([A-D])", token.strip())
            require(match is not None, f"malformed answer-key entry: {token!r}")
            pairs.append((int(match[1]), match[2]))
    ids = [number for number, _ in pairs]
    require(len(ids) == len(set(ids)), "duplicate answer-key number")
    require(ids == list(range(1, count + 1)), f"answer key must cover Q1-Q{count} once in order")
    return dict(pairs)


def check_topic_text(text: str, label: str) -> Counter[str]:
    question_text = section(text, "## Questions")
    questions = numbered_blocks(question_text, "### Q")
    check_numbering(questions, 10, label)
    for number, _, body in questions:
        check_choices(body, f"{label} Q{number}")
    explanations = numbered_blocks(section(text, "# Answers & Explanations"), "### A", True)
    check_numbering(explanations, 10, f"{label} explanations")
    for number, _, body in explanations:
        check_explanation(body, f"{label} A{number}")
    sequence = [answer for _, answer, _ in explanations]
    counts = Counter(sequence)
    require(set(counts) == set(LETTERS) and max(counts.values()) <= 6,
            f"{label}: answer-position concentration {dict(counts)}")
    check_period(sequence, label)
    return counts


def check_mock_text(mock: str, answer_text: str, objective_map: str) -> Counter[str]:
    questions = numbered_blocks(mock, "## Q")
    check_numbering(questions, 68, "Mock")
    domains: Counter[int] = Counter()
    for number, _, body in questions:
        check_choices(body, f"Mock Q{number}")
        markers = re.findall(r"(?m)^<!-- domain: ([1-8]) -->$", outside_code(body))
        require(len(markers) == 1, f"Mock Q{number}: expected one domain marker")
        expected = next(i for i, (start, end) in enumerate(DOMAIN_RANGES, 1) if start <= number <= end)
        domain = int(markers[0])
        require(domain == expected, f"Mock Q{number}: domain {domain}, expected {expected}")
        domains[domain] += 1
    require(tuple(domains[i] for i in range(1, 9)) == DOMAIN_COUNTS, "Mock domain-count mismatch")
    key = parse_answer_key(answer_text)
    counts = Counter(key.values())
    require(counts == Counter(dict.fromkeys(LETTERS, 17)), f"Mock answer distribution: {dict(counts)}")
    explanations = numbered_blocks(section(answer_text, "## Detailed Explanations"), "### Q", True)
    check_numbering(explanations, 68, "Mock explanations")
    for number, answer, body in explanations:
        require(answer == key[number], f"Mock Q{number}: key / explanation mismatch")
        check_explanation(body, f"Mock Q{number}")
    check_period(list(key.values()), "Mock")
    # Compare actual author-assigned marker counts with the rendered map table.
    map_table = section(objective_map, "## Domain coverage")
    rows = re.findall(r"(?m)^\|\s*([1-8])\s*\|.*?Q(\d+)–Q(\d+).*?\|\s*(\d+)\s*\|$", map_table)
    expected_rows = [(str(i), str(start), str(end), str(DOMAIN_COUNTS[i-1]))
                     for i, (start, end) in enumerate(DOMAIN_RANGES, 1)]
    require(rows == expected_rows, "Objective map domain table disagrees with question markers")
    return counts


def validate(root: Path = ROOT) -> None:
    aggregate: Counter[str] = Counter()
    for filename in TOPIC_FILES:
        counts = check_topic_text((root / "topic-tests" / filename).read_text(encoding="utf-8"), filename)
        aggregate.update(counts)
        print(f"{filename}: 10 questions; {dict(sorted(counts.items()))}")
    require(sum(aggregate.values()) == 80, "Topic bank must contain 80 questions")
    require(max(aggregate.values()) - min(aggregate.values()) <= 5,
            f"Topic aggregate answer positions too uneven: {dict(aggregate)}")
    counts = check_mock_text((root / "mock-exams/mock-01.md").read_text(encoding="utf-8"),
                            (root / "answers/mock-exams/mock-01-answers.md").read_text(encoding="utf-8"),
                            (root / "exam-objectives-map.md").read_text(encoding="utf-8"))
    print(f"Topic total: 80; {dict(sorted(aggregate.items()))}")
    print(f"Mock total: 68; {dict(sorted(counts.items()))}; author-assigned domains: {list(DOMAIN_COUNTS)}")
    print("Structural validation: OK (not a proof of technical accuracy or objective coverage)")


if __name__ == "__main__":
    try:
        validate(Path(sys.argv[1]) if len(sys.argv) == 2 else ROOT)
    except (ValidationError, OSError) as exc:
        print(f"Structural validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
