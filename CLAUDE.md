# CLAUDE.md

Guidance for Claude Code (and any agent) working in this repository.

## What this repo is

`code-setup` is a **central library of reusable Claude Code configuration** —
agents, rules, and GitHub Actions — that get copied or symlinked into other
repositories so every project shares the same conventions. It contains
configuration and documentation, not application code.

## Layout

```
.claude/
  agents/        Subagent definitions (Markdown + frontmatter)
    requirement-implementer.md   Implements a scoped requirement end-to-end
    code-reviewer.md             Read-only reviewer of a diff/branch/PR
  rules/         Workflow rules referenced by agents and by CLAUDE.md
    git-branching.md         Branch off `develop` for every requirement
    git-commit-push-pr.md    Hands-off commit + push + open PR
    run-tests.md         Run tests once development is finished
    update-docs.md       Update /docs, README.md, CLAUDE.md when finished
.github/
  workflows/
    claude.yml               Claude Code on @claude mentions (issues/PRs)
    claude-code-review.yml   Automated Claude review on every PR
scripts/
  validate.py    Validates agent frontmatter and internal links (the "tests")
```

The workflows use the [`JaimeMartinSoler/github-actions`](https://github.com/JaimeMartinSoler/github-actions)
custom actions and need a `CLAUDE_CODE_OAUTH_TOKEN` (or `ANTHROPIC_API_KEY`)
repository secret.

## Working rules (apply to every change here and are meant to be reused)

These rules are the substance of this repo. Read the file before acting:

1. **Branch per requirement** — `.claude/rules/git-branching.md`
2. **Run tests when done** — `.claude/rules/run-tests.md`
3. **Update docs when done** — `.claude/rules/update-docs.md`
4. **Commit, push, open PR** — `.claude/rules/git-commit-push-pr.md`

The intended flow for any requirement: branch off `develop` → implement →
add/run tests (green) → update docs → commit, push, and open a PR against
`develop`.

## Conventions for editing this repo

- **Agents** are Markdown files with YAML frontmatter (`name`, `description`,
  optional `tools`, `model`). Keep the body a focused system prompt. `name` must
  match the filename slug.
- **Rules** are plain Markdown. Keep each one single-purpose, imperative, and
  copy-paste portable across repos — avoid hardcoding any one project's stack.
- When you add a new agent or rule, **add it to the layout above** and to
  `README.md`.
- This repo has no build step. "Tests" here means: frontmatter is valid, internal
  links between files resolve, and the docs match the files on disk. Run them with
  `python3 scripts/validate.py` (standard library only — no dependencies). This is
  the suite `.claude/rules/run-tests.md` refers to; keep it green before opening a PR.

## Reusing this in another repo

Copy the `.claude/agents`, `.claude/rules`, and `.github/workflows` you need into
the target repo, add the `CLAUDE_CODE_OAUTH_TOKEN` (or `ANTHROPIC_API_KEY`)
secret, and adjust the integration branch name (rules + `base_branch` in
`claude.yml`) if it isn't `develop`.
