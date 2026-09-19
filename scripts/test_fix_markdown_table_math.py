import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from fix_markdown_table_math import UnsafeTable, repair


class RepairTests(unittest.TestCase):
    def test_scope_and_idempotence(self):
        table = '| state | value |\n|---|---|\n| $|x\\rangle$ | $a|b$ |\n'
        outside = '$|x\\rangle$\n\n```md\n' + table + '```\n\n'
        expected = table.replace('$|x', '$\\vert x').replace('$a|b$', '$a\\vert b$')
        result = repair(outside + table)
        self.assertEqual(result, outside + expected)
        self.assertEqual(repair(result), result)

    def test_escaped_pipes_code_and_dollars(self):
        source = '| a | b |\n|---|---|\n| `$x$` | $\\|x\\|$ and \\$5 |\n'
        self.assertEqual(repair(source), source)

    def test_bom_crlf_and_final_newline(self):
        source = '\ufeff| a |\r\n|---|\r\n| $|0\\rangle$ |'
        self.assertEqual(repair(source), source.replace('$|0', '$\\vert 0'))

    def test_html_and_display_blocks(self):
        table = '| a |\n|---|\n| $|0$ |\n'
        for start, end in [('<!--', '-->'), ('<pre>', '</pre>'), ('$$', '$$'), ('~~~~', '~~~~')]:
            source = start + '\n\n' + table + '\n' + end + '\n'
            self.assertEqual(repair(source), source)

    def test_ambiguous_rows_fail(self):
        for row in ['| $x |', '| $$x$$ |', '| x | y |', '| `x|y` |']:
            with self.subTest(row=row), self.assertRaises(UnsafeTable):
                repair('| a |\n|---|\n' + row + '\n')

    def test_cli_never_overwrites(self):
        script = Path(__file__).with_name('fix_markdown_table_math.py')
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source.md'
            output = Path(directory) / 'fixed.md'
            original = b'| a |\r\n|---|\r\n| $|0$ |\r\n'
            source.write_bytes(original)
            command = [sys.executable, str(script), str(source)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(list(Path(directory).iterdir()), [source])
            self.assertEqual(subprocess.run(command + ['--output', str(output)], capture_output=True).returncode, 0)
            fixed = output.read_bytes()
            self.assertEqual(subprocess.run(command + ['--output', str(output)], capture_output=True).returncode, 2)
            self.assertEqual(subprocess.run(command + ['--output', str(source)], capture_output=True).returncode, 2)
            self.assertEqual(output.read_bytes(), fixed)
            self.assertEqual(source.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
