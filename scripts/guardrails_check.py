#!/usr/bin/env python3
import os, re, sys
from pathlib import Path

CODE_DIRS = ["backend", "frontend", "tests-e2e", "docs"]
ALLOW_HYPHEN = {"frontend/next-env.d.ts"}

EMOJI_RE = re.compile(r"[\u2600-\u27BF\U0001F300-\U0001FAFF]")
violations = []

repo = Path(__file__).resolve().parents[1]

# filenames
for root, _dirs, files in os.walk(repo):
    rel_dir = os.path.relpath(root, repo)
    if rel_dir.split(os.sep)[0] not in CODE_DIRS:
        continue
    for f in files:
        rel_path = os.path.join(rel_dir, f).replace("\\", "/")
        if rel_path in ALLOW_HYPHEN: 
            continue
        if "-" in f:
            violations.append(f"hyphen-in-filename: {rel_path}")

# emojis + console/print minimal checks
for code_dir in CODE_DIRS:
    base = repo / code_dir
    if not base.exists():
        continue
    for p in base.rglob("*"):
        if not p.is_file():
            continue
        try:
            txt = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if EMOJI_RE.search(txt):
            violations.append(f"emoji-found: {p.as_posix()}")
        if p.suffix == ".py" and "/tests/" not in p.as_posix() and "print(" in txt:
            violations.append(f"print-outside-tests: {p.as_posix()}")
        if p.suffix in (".ts", ".tsx") and "/tests/" not in p.as_posix() and "console.log(" in txt:
            violations.append(f"console-log-outside-tests: {p.as_posix()}")

if not (repo / "docs" / "GUARDRAILS.md").exists():
    violations.append("missing-docs: docs/GUARDRAILS.md not found")

if violations:
    print("Guardrails violations:")
    for v in violations:
        print(" -", v)
    sys.exit(1)

print("Guardrails check passed.")
