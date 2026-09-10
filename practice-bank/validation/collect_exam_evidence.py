"""Retrieve IBM's public exam record, not a third-party transcription.

This is a network-dependent provenance aid, not a semantic coverage test. An
unavailable endpoint is reported as unverified and exits nonzero. No credentials
or copyrighted PDF bytes are stored in the repository.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

URL = "https://www.ibm.com/training/credentials/getExam/C1000-179"


def main() -> int:
    record = {"requested_url": URL, "checked_at": datetime.now(timezone.utc).isoformat(),
              "verification": "unverified"}
    try:
        request = Request(URL, headers={"User-Agent": "practice-bank-source-check/1.0",
                                        "Accept": "application/json"})
        with urlopen(request, timeout=45) as response:
            final_url = response.geturl()
            host = urlsplit(final_url).hostname or ""
            if not (host == "ibm.com" or host.endswith(".ibm.com")):
                raise ValueError("IBM record redirected outside ibm.com")
            raw = response.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError("exam record exceeds size limit")
        data = json.loads(raw)
        if "C1000-179" not in json.dumps(data):
            raise ValueError("record does not identify C1000-179")
        record.update(final_url=final_url, sha256=hashlib.sha256(raw).hexdigest(),
                      verification="record_retrieved_not_yet_manually_reviewed", data=data)
        code = 0
    except Exception as exc:
        record["error"] = f"{type(exc).__name__}: {exc}"
        code = 1
    destination = Path("validation-output")
    destination.mkdir(exist_ok=True)
    (destination / "exam-record.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
