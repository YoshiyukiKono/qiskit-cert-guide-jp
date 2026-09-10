"""Run a check without hiding failures; retain environment, output and exit code."""
from __future__ import annotations
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 4 or sys.argv[2] != "--":
        raise SystemExit("usage: run_check.py NAME -- COMMAND [ARGS...]")
    name = sys.argv[1]
    if not re.fullmatch(r"[a-z0-9-]+", name):
        raise SystemExit("NAME must contain only lowercase letters, digits or hyphens")
    command = sys.argv[3:]
    output_dir = Path("validation-output")
    output_dir.mkdir(exist_ok=True)
    versions = {}
    for package in ("qiskit", "qiskit-ibm-runtime", "qiskit-qasm3-import", "numpy"):
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = "not installed"
    sha_run = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    sha = sha_run.stdout.strip() if sha_run.returncode == 0 else "not a git checkout"
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, encoding="utf-8", errors="replace", timeout=600)
        code, output = result.returncode, result.stdout
    except (OSError, subprocess.TimeoutExpired) as exc:
        code, output = 1, f"Check could not complete: {exc}"
    record = {"name": name, "commit": sha, "python": sys.version,
              "versions": versions, "command": command, "exit_code": code,
              "status": "passed" if code == 0 else "failed", "output": output}
    payload = json.dumps(record, ensure_ascii=False, indent=2)
    (output_dir / f"{name}.json").write_text(payload + "\n", encoding="utf-8")
    # Prefix ordinary output so child output cannot issue Actions workflow commands.
    for line in payload.splitlines():
        print("| " + line)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        escaped = payload[-40000:].replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        kind = "notice" if code == 0 else "error"
        print(f"::{kind} title=practice-bank {name}::{escaped}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
