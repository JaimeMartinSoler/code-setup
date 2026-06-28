# code-setup

A central library of **reusable Claude Code configuration** — agents, workflow
rules, and CI templates — shared across my repositories. Instead of recreating the
same `.claude` setup in every project, I keep the canonical versions here and copy
or symlink what each repo needs.

## Contents

### Agents — `.claude/agents/`

| Agent | Purpose |
| --- | --- |
| [`requirement-implementer`](.claude/agents/requirement-implementer.md) | Takes one scoped requirement and drives it to a review-ready state: branch, implement, test, document, PR. |
| [`code-reviewer`](.claude/agents/code-reviewer.md) | Read-only reviewer of a diff/branch/PR — flags correctness, security, test, and maintainability issues with a clear verdict. |

### Rules — `.claude/rules/`

| Rule | What it enforces |
| --- | --- |
| [`branching`](.claude/rules/branching.md) | Branch off `develop` for every requirement — one requirement, one branch, one PR. |
| [`commit-push-pr`](.claude/rules/commit-push-pr.md) | Hands-off delivery: stage intentionally, commit, push, open a PR against `develop`, with guardrails. |
| [`run-tests`](.claude/rules/run-tests.md) | Add/update and run tests once development is finished — green before done. |
| [`update-docs`](.claude/rules/update-docs.md) | Check and update `/docs`, `README.md`, and `CLAUDE.md` when development is finished. |

### CI — `.github/workflows/`

- [`ci.yml`](.github/workflows/ci.yml) — a **sample** workflow with placeholder
  build/test steps. Copy it into a repo and fill in the real toolchain.

## The workflow these encode

For any requirement:

1. **Branch** off an up-to-date `develop`.
2. **Implement** the smallest change that fully satisfies the requirement.
3. **Test** — add/update tests and run the suite until green.
4. **Document** — update `/docs`, `README.md`, and `CLAUDE.md` as needed.
5. **Ship** — commit, push, and open a PR against `develop`.

## Using it in another repo

1. Copy the agents and rules you want from `.claude/` into the target repo's
   `.claude/` directory.
2. Copy `.github/workflows/ci.yml` and replace the placeholder steps with the
   project's real setup, lint, and test commands.
3. If the target repo's integration branch isn't `develop`, adjust the branch
   names in the rules and workflow.

See [`CLAUDE.md`](CLAUDE.md) for conventions when editing this repo itself.
