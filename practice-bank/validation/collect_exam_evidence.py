"""Collect relevant public exam fields; do not persist contact data or signed URLs.

This network-dependent provenance aid is not a semantic coverage test and does
not fetch or certify a separate Study Guide PDF. Unavailable sources fail openly.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

URL = "https://www.ibm.com/training/credentials/getExam/C1000-179"
EXAM_FIELDS = ("EXAM_SERIES_CODE", "EXAM_TITLE", "EXAM_STATUS", "EXAM_TIME_LIMIT",
               "EXAM_NUMBER_OF_QUESTIONS", "EXAM_NUMBER_OF_QUESTIONS_TO_PASS", "LANGUAGES")
OBJECTIVE_FIELDS = ("EXAM_OBJECTIVE_ORDER", "EXAM_OBJECTIVE_TITLE",
                    "PERCENTAGE_OF_OBJECTIVE_QUESTIONS", "EXAM_OBJECTIVE_DESCRIPTION")


def main() -> int:
    record = {"requested_url": URL, "checked_at": datetime.now(timezone.utc).isoformat(),
              "verification": "unverified", "study_guide_pdf_reviewed": False}
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
        if data.get("EXAM_SERIES_CODE") != "C1000-179":
            raise ValueError("record does not identify C1000-179")
        objectives = data.get("OBJECTIVES")
        if not isinstance(objectives, list) or not objectives:
            raise ValueError("record contains no objective list")
        selected = {field: data.get(field) for field in EXAM_FIELDS}
        selected["OBJECTIVES"] = [{field: item.get(field) for field in OBJECTIVE_FIELDS}
                                  for item in objectives]
        record.update(final_url=final_url, sha256=hashlib.sha256(raw).hexdigest(),
                      verification="record_retrieved_requires_comparison", data=selected,
                      has_study_guide_reference=bool(data.get("STUDY_GUIDE_URL")))
        code = 0
    except Exception as exc:
        # Do not log response bodies or signed URLs in an exception message.
        record["error"] = f"{type(exc).__name__}: public exam record could not be verified"
        code = 1
    destination = Path("validation-output")
    destination.mkdir(exist_ok=True)
    (destination / "exam-record.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
