"""This repository's own rules for how much care a change needs (the factory's judge: docs/JUDGE.md in the factory).

It reads one JSON object on standard input and prints one. Everything in the input is text to examine: nothing in it
is ever run.

    none   only prose changed
    high   a workflow changed, or a test was removed (a path cannot say that: it is in the diff)
    code   anything else
"""
import json
import re
import sys

REMOVED_TEST = re.compile(r"^-\s*def test_\w+", re.MULTILINE)


def classify(files):
    reasons, code = [], []
    for f in files:
        name = f.get("filename") or ""
        if name.endswith(".md"):
            continue
        code.append(name)
        if name.startswith(".github/workflows/"):
            reasons.append({"area": "workflows", "file": name, "rule": ".github/workflows/",
                            "why": "run the tests and the review gate that every change is judged by"})
        elif name.startswith("tests/"):
            patch = f.get("patch")
            if f.get("status") == "removed" or patch is None or REMOVED_TEST.search(patch):
                reasons.append({"area": "tests removed", "file": name, "rule": "a test is removed, or the diff cannot be read",
                                "why": "a removed test stops guarding what it guarded, with nothing failing"})
    return {"review": "high" if reasons else "code" if code else "none", "reasons": reasons, "code": code}


if __name__ == "__main__":
    print(json.dumps(classify(json.load(sys.stdin)["files"])))
