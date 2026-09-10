"""Structural QA for practice-bank markdown files.

This script uses only the Python standard library. It checks invariants that
should remain true as future mock exams and topic questions are edited.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TOPIC_DIR = ROOT / "topic-tests"
MOCK = ROOT / "mock-exams" / "mock-01.md"
MOCK_ANSWERS = ROOT / "answers" / "mock-exams" / "mock-01-answers.md"
OBJECTIVE_MAP = ROOT / "exam-objectives-map.md"

TOPIC_FILES = [
    "01-quantum-operations.md",
    "02-visualization-measurement-states.md",
    "03-circuit-construction.md",
    "04-running-circuits.md",
    "05-sampler.md",
    "06-estimator.md",
    "07-results-analysis.md",
    "08-openqasm3.md",
]

EXPECTED_MOCK_DOMAIN_RANGES = [
    (1, 11),
    (12, 19),
    (20, 31),
    (32, 41),
    (42, 49),
    (50, 57),
    (58, 64),
    (65, 68),
]
EXPECTED_MOCK_DOMAIN_COUNTS = [11, 8, 12, 10, 8, 8, 7, 4]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def blocks(text: str, heading: str) -> list[tuple[int, str]]:
    """Return numbered question blocks for headings like '### Q' or '## Q'."""
    pattern = re.compile(
        rf"(?ms)^{re.escape(heading)}(\d+)\n(.*?)(?=^{re.escape(heading)}\d+\n|\Z)"
    )
    return [(int(number), body) for number, body in pattern.findall(text)]


def option_labels(body: str) -> list[str]:
    return re.findall(r"(?m)^([ABCD])\.\s", body)


def explanation_blocks(text: str, prefix: str) -> list[tuple[int, str, str]]:
    pattern = re.compile(
        rf"(?ms)^### {re.escape(prefix)}(\d+) — ([ABCD])\n(.*?)"
        rf"(?=^### {re.escape(prefix)}\d+ — [ABCD]\n|^## |^---\n|\Z)"
    )
    return [(int(number), answer, body) for number, answer, body in pattern.findall(text)]


def covered_choice_labels(body: str) -> set[str]:
    """Accept bullets such as '- A:' and grouped bullets such as '- A/C/D:'."""
    covered: set[str] = set()
    for line in body.splitlines():
        if not line.startswith("- ") or ":" not in line:
            continue
        prefix = line[2:].split(":", 1)[0]
        for item in prefix.split("/"):
            item = item.strip()
            if item in {"A", "B", "C", "D"}:
                covered.add(item)
    return covered


def check_topic_file(path: Path) -> Counter[str]:
    text = read(path)
    question_part = text.split("# Answers & Explanations", 1)[0]
    questions = blocks(question_part, "### Q")
    assert len(questions) == 10, f"{path.name}: expected 10 questions, got {len(questions)}"
    assert [n for n, _ in questions] == list(range(1, 11)), f"{path.name}: question numbering"

    for number, body in questions:
        labels = option_labels(body)
        assert labels == ["A", "B", "C", "D"], (
            f"{path.name} Q{number}: expected exactly A-D choices, got {labels}"
        )

    explanations = explanation_blocks(text, "A")
    assert len(explanations) == 10, f"{path.name}: expected 10 explanations"
    assert [n for n, _, _ in explanations] == list(range(1, 11)), (
        f"{path.name}: explanation numbering"
    )

    answers = Counter(answer for _, answer, _ in explanations)
    assert set(answers) == {"A", "B", "C", "D"}, (
        f"{path.name}: every answer position should appear at least once; {answers}"
    )
    assert max(answers.values()) <= 6, f"{path.name}: answer-position concentration {answers}"

    for number, _, body in explanations:
        covered = covered_choice_labels(body)
        assert covered == {"A", "B", "C", "D"}, (
            f"{path.name} A{number}: distractor coverage is {sorted(covered)}"
        )

    return answers


def parse_mock_answer_key(text: str) -> dict[int, str]:
    key_section = text.split("---", 1)[0]
    pairs = re.findall(r"\b(\d+)\s+([ABCD])\b", key_section)
    return {int(number): answer for number, answer in pairs}


def check_mock() -> None:
    mock_text = read(MOCK)
    questions = blocks(mock_text, "## Q")
    assert len(questions) == 68, f"Mock: expected 68 questions, got {len(questions)}"
    assert [n for n, _ in questions] == list(range(1, 69)), "Mock question numbering"

    for number, body in questions:
        labels = option_labels(body)
        assert labels == ["A", "B", "C", "D"], (
            f"Mock Q{number}: expected exactly A-D choices, got {labels}"
        )

    answer_text = read(MOCK_ANSWERS)
    key = parse_mock_answer_key(answer_text)
    assert list(sorted(key)) == list(range(1, 69)), "Mock answer key must cover Q1-Q68"

    distribution = Counter(key.values())
    assert distribution == Counter({"A": 17, "B": 17, "C": 17, "D": 17}), (
        f"Mock answer-position distribution: {distribution}"
    )

    explanations = explanation_blocks(answer_text, "Q")
    assert len(explanations) == 68, f"Mock: expected 68 detailed explanations, got {len(explanations)}"
    exp_map = {number: (answer, body) for number, answer, body in explanations}
    assert set(exp_map) == set(range(1, 69)), "Mock explanation numbering"

    for number in range(1, 69):
        answer, body = exp_map[number]
        assert answer == key[number], (
            f"Mock Q{number}: key={key[number]} but explanation heading={answer}"
        )
        covered = covered_choice_labels(body)
        assert covered == {"A", "B", "C", "D"}, (
            f"Mock Q{number}: distractor coverage is {sorted(covered)}"
        )

    actual_counts = [end - start + 1 for start, end in EXPECTED_MOCK_DOMAIN_RANGES]
    assert actual_counts == EXPECTED_MOCK_DOMAIN_COUNTS
    assert sum(actual_counts) == 68

    objective_map = read(OBJECTIVE_MAP)
    for start, end in EXPECTED_MOCK_DOMAIN_RANGES:
        marker = f"Q{start}–Q{end}"
        assert marker in objective_map, f"Objective map missing mock range {marker}"

    print(f"Mock 01: 68 questions; answer positions {dict(sorted(distribution.items()))}")
    print(f"Mock 01 domain counts: {actual_counts}")


def main() -> None:
    aggregate: Counter[str] = Counter()
    for filename in TOPIC_FILES:
        answers = check_topic_file(TOPIC_DIR / filename)
        aggregate.update(answers)
        print(f"{filename}: OK; answers {dict(sorted(answers.items()))}")

    assert sum(aggregate.values()) == 80
    assert max(aggregate.values()) - min(aggregate.values()) <= 5, (
        f"Topic-bank aggregate answer positions too uneven: {aggregate}"
    )
    print(f"Topic tests aggregate: {dict(sorted(aggregate.items()))}")

    check_mock()
    print("practice-bank structural validation: OK")


if __name__ == "__main__":
    main()
