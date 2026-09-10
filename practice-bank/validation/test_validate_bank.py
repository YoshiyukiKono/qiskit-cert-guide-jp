"""Positive and mutation tests for the structural validator (stdlib only)."""
from __future__ import annotations
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest

import validate_bank as bank

# Fixed structural fixture: semantic correctness is not tested by this key.
KEY = "CDCBDBCDDCCADCBADAACBBAADDDBBDCABCABDAABCDCDBDBBCCCBADDAAADACBCCBABA"


def fixture():
    if len(KEY) != 68:
        raise RuntimeError(f"fixture key length {len(KEY)}")
    questions = []
    explanations = []
    table = ["## Domain coverage", "", "| # | Name | Weight | Topic | Mock | Target mock count |",
             "|---|---|---:|---|---|---:|"]
    for domain, (start, end) in enumerate(bank.DOMAIN_RANGES, 1):
        table.append(f"| {domain} | Domain {domain} | 1% | topic | Q{start}–Q{end} | {end-start+1} |")
        for number in range(start, end + 1):
            questions.append(f"## Q{number}\n<!-- domain: {domain} -->\nQuestion {number}?\n\n"
                             "A. first\nB. second\nC. third\nD. fourth\n")
            explanations.append(f"### Q{number} — {KEY[number-1]}\n"
                                "- A: explanation one\n- B/C: explanation two\n- D: explanation three\n")
    answers = "## Answer Key\n\n" + " / ".join(f"{i} {a}" for i, a in enumerate(KEY, 1))
    answers += "\n\n---\n\n## Detailed Explanations\n\n" + "\n".join(explanations)
    return "\n".join(questions), answers, "\n".join(table)


class ParserTests(unittest.TestCase):
    def setUp(self):
        self.mock, self.answers, self.table = fixture()

    def reject(self, *, mock=None, answers=None, table=None):
        with self.assertRaises(bank.ValidationError):
            bank.check_mock_text(mock if mock is not None else self.mock,
                                 answers if answers is not None else self.answers,
                                 table if table is not None else self.table)

    def test_valid_fixture(self):
        self.assertEqual(bank.check_mock_text(self.mock, self.answers, self.table),
                         bank.Counter(dict.fromkeys("ABCD", 17)))

    def test_extra_option(self):
        self.reject(mock=self.mock.replace("D. fourth", "D. fourth\nE. fifth", 1))

    def test_empty_option(self):
        self.reject(mock=self.mock.replace("B. second", "B.   ", 1))

    def test_duplicate_option(self):
        self.reject(mock=self.mock.replace("B. second", "B. first", 1))

    def test_missing_option(self):
        self.reject(mock=self.mock.replace("B. second\n", "", 1))

    def test_duplicate_key_same_value(self):
        self.reject(answers=self.answers.replace("1 C /", "1 C / 1 C /", 1))

    def test_conflicting_duplicate_key(self):
        self.reject(answers=self.answers.replace("1 C /", "1 A / 1 C /", 1))

    def test_missing_key(self):
        self.reject(answers=self.answers.replace("1 C / ", "", 1))

    def test_unknown_key_letter(self):
        self.reject(answers=self.answers.replace("1 C /", "1 E /", 1))

    def test_key_heading_disagreement(self):
        self.reject(answers=self.answers.replace("### Q1 — C", "### Q1 — A", 1))

    def test_empty_grouped_explanation(self):
        self.reject(answers=self.answers.replace("- B/C: explanation two", "- B/C: ", 1))

    def test_missing_explanation_label(self):
        self.reject(answers=self.answers.replace("- B/C: explanation two", "- B: explanation two", 1))

    def test_duplicate_explanation_label(self):
        self.reject(answers=self.answers.replace("- B/C: explanation two", "- B/B/C: explanation two", 1))

    def test_unknown_explanation_label(self):
        self.reject(answers=self.answers.replace("- B/C: explanation two", "- B/C/E: explanation two", 1))

    def test_missing_domain_marker(self):
        self.reject(mock=self.mock.replace("<!-- domain: 1 -->", "", 1))

    def test_duplicate_domain_marker(self):
        self.reject(mock=self.mock.replace("<!-- domain: 1 -->", "<!-- domain: 1 -->\n<!-- domain: 1 -->", 1))

    def test_wrong_domain_assignment(self):
        self.reject(mock=self.mock.replace("<!-- domain: 1 -->", "<!-- domain: 8 -->", 1))

    def test_wrong_map_count(self):
        self.reject(table=self.table.replace("| 11 |", "| 12 |", 1))

    def test_duplicate_question(self):
        self.reject(mock=self.mock.replace("## Q2\n", "## Q1\n", 1))

    def test_malformed_question_heading(self):
        self.reject(mock=self.mock.replace("## Q2\n", "## Q2 bad\n", 1))

    def test_empty_stem(self):
        self.reject(mock=self.mock.replace("Question 1?", "", 1))

    def test_code_fences_do_not_create_options_or_headings(self):
        mock = self.mock.replace("Question 1?", "Question 1?\n```text\n## Q99\nE. example\n```", 1)
        self.assertEqual(bank.check_mock_text(mock, self.answers, self.table)["A"], 17)

    def test_unclosed_code_fence(self):
        self.reject(mock=self.mock + "\n```python\n")

    def test_period_four_detected(self):
        with self.assertRaises(bank.ValidationError):
            bank.check_period(list("BDACBDACBD"), "periodic topic")
        bank.check_period(list("BDCABDACBD"), "reordered topic")

    def test_optimized_python_still_rejects_empty_options(self):
        command = [sys.executable, "-O", "-c",
                   "import validate_bank as v; v.check_choices('Question?\\nA. one\\nB. \\nC. three\\nD. four', 'bad')"]
        result = subprocess.run(command, cwd=Path(__file__).parent, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("empty choice", result.stderr)


class RepositoryTests(unittest.TestCase):
    def test_actual_bank(self):
        with contextlib.redirect_stdout(io.StringIO()):
            bank.validate()


if __name__ == "__main__":
    unittest.main(verbosity=2)
