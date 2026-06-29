#!/usr/bin/env python3
"""Validate this repo's Claude Code configuration.

This is the "test suite" referenced by CLAUDE.md and .claude/rules/run-tests.md.
The repo ships configuration and docs, not application code, so the checks are:

1. Agent frontmatter is well-formed: every file in .claude/agents/ has YAML
   frontmatter with `name` and `description`, and `name` matches the filename
   slug (a convention CLAUDE.md requires).
2. Internal references resolve: every relative Markdown link and every
   repo-internal path (.claude/..., .github/..., scripts/...) written in
   backticks across the docs points at a file that actually exists.

No third-party dependencies — standard library only. Exit code 0 on success,
1 on any failure, so it can gate CI or a pre-commit hook.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"

# Files whose links/paths we validate.
DOC_GLOBS = ["*.md", ".claude/**/*.md"]

# Backtick paths are only treated as repo references when they start with one of
# these prefixes, so generic examples (`package.json`, `git diff`, `<branch>`)
# are not flagged as missing files.
REPO_PATH_PREFIXES = (".claude/", ".github/", "scripts/")

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BACKTICK_PATH = re.compile(r"`([^`]+)`")


def split_frontmatter(text: str) -> dict[str, str] | None:
    """Return top-level scalar keys from a leading `---` YAML block, or None."""
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return None
    keys: dict[str, str] = {}
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z_][\w-]*):(.*)$", line)
        if m:  # top-level key (no leading indentation)
            keys[m.group(1)] = m.group(2).strip()
    return keys


def check_agents(errors: list[str]) -> None:
    if not AGENTS_DIR.is_dir():
        errors.append(f"missing agents directory: {AGENTS_DIR}")
        return
    for path in sorted(AGENTS_DIR.glob("*.md")):
        rel = path.relative_to(REPO_ROOT)
        fm = split_frontmatter(path.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{rel}: missing or unterminated YAML frontmatter")
            continue
        for required in ("name", "description"):
            if not fm.get(required):
                errors.append(f"{rel}: frontmatter missing `{required}`")
        slug = path.stem
        if fm.get("name") and fm["name"] != slug:
            errors.append(
                f"{rel}: frontmatter `name: {fm['name']}` must match filename slug `{slug}`"
            )


def check_links(errors: list[str]) -> None:
    doc_paths: list[Path] = []
    for pattern in DOC_GLOBS:
        doc_paths.extend(REPO_ROOT.glob(pattern))
    for path in sorted(set(doc_paths)):
        rel = path.relative_to(REPO_ROOT)
        text = path.read_text(encoding="utf-8")

        for target in MD_LINK.findall(text):
            target = target.split()[0]  # drop any "title" after the URL
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            ref = (path.parent / target.split("#", 1)[0]).resolve()
            if not ref.exists():
                errors.append(f"{rel}: broken link -> {target}")

        for token in BACKTICK_PATH.findall(text):
            if token.startswith(REPO_PATH_PREFIXES):
                if not (REPO_ROOT / token.split("#", 1)[0]).exists():
                    errors.append(f"{rel}: broken path reference -> `{token}`")


def main() -> int:
    errors: list[str] = []
    check_agents(errors)
    check_links(errors)

    if errors:
        print("FAIL — configuration validation found problems:\n")
        for err in errors:
            print(f"  - {err}")
        print(f"\n{len(errors)} problem(s).")
        return 1

    print("PASS — agent frontmatter and internal references are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
