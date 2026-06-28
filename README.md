# code-setup

A central library of **reusable Claude Code configuration** — agents, workflow
rules, and GitHub Actions — shared across my repositories. Instead of recreating
the same `.claude` setup in every project, I keep the canonical versions here and
copy or symlink what each repo needs.

## Contents

### Agents — `.claude/agents/`

| Agent | Purpose |
| --- | --- |
| [`requirement-implementer`](.claude/agents/requirement-implementer.md) | Takes one scoped requirement and drives it to a review-ready state: branch, implement, test, document, PR. |
| [`code-reviewer`](.claude/agents/code-reviewer.md) | Read-only reviewer of a diff/branch/PR — flags correctness, security, test, and maintainability issues with a clear verdict. |

### Rules — `.claude/rules/`

| Rule | What it enforces |
| --- | --- |
| [`git-branching`](.claude/rules/git-branching.md) | Branch off `develop` for every requirement — one requirement, one branch, one PR. |
| [`git-commit-push-pr`](.claude/rules/git-commit-push-pr.md) | Hands-off delivery: stage intentionally, commit, push, open a PR against `develop`, with guardrails. |
| [`run-tests`](.claude/rules/run-tests.md) | Add/update and run tests once development is finished — green before done. |
| [`update-docs`](.claude/rules/update-docs.md) | Check and update `/docs`, `README.md`, and `CLAUDE.md` when development is finished. |

### GitHub Actions — `.github/workflows/`

Both workflows run on the [`JaimeMartinSoler/github-actions`](https://github.com/JaimeMartinSoler/github-actions)
custom actions and authenticate with a `CLAUDE_CODE_OAUTH_TOKEN` (or
`ANTHROPIC_API_KEY`) repository secret.

| Workflow | Trigger | What it does |
| --- | --- | --- |
| [`claude.yml`](.github/workflows/claude.yml) | `@claude` mention in an issue, PR, or review comment | Runs Claude Code against the repo to answer or implement, branching from `develop`. |
| [`claude-code-review.yml`](.github/workflows/claude-code-review.yml) | PR opened or updated | Posts an automated Claude review of the diff. |

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
2. Copy the `.github/workflows/` you want and add a `CLAUDE_CODE_OAUTH_TOKEN`
   (or `ANTHROPIC_API_KEY`) secret to the target repo.
3. If the target repo's integration branch isn't `develop`, adjust the branch
   names in the rules and the `base_branch` input in `claude.yml`.

See [`CLAUDE.md`](CLAUDE.md) for conventions when editing this repo itself.
