# 02 · Team pipeline: Devin through issue → PR → CI → review → merge

## Links

- Issue: https://github.com/owenzorrin/devin-pipeline-lab/issues/1
- Merged PR: <!-- https://github.com/owenzorrin/devin-pipeline-lab/pull/N -->
- Devin session: <!-- link -->

## Guardrails turned on

| Guardrail | Where | Setting |
|---|---|---|
| CI on every PR | `.github/workflows/ci.yml` | `ruff check`, `ruff format --check`, `pytest` on `pull_request` and pushes to `main` |
| Require a PR to change `main` | Ruleset `protect-main` | Pull request required |
| 1 approval | Ruleset `protect-main` | `required_approving_review_count: 1` |
| Code owner review | Ruleset + `.github/CODEOWNERS` | `* @owenzorrin`, `require_code_owner_review: true` |
| Stale approvals dismissed | Ruleset `protect-main` | `dismiss_stale_reviews_on_push: true` |
| Passing CI required | Ruleset `protect-main` | Required check `lint-and-test` from GitHub Actions |
| No force-push, no deletion | Ruleset `protect-main` | `non_fast_forward`, `deletion` |
| No bypass | Ruleset `protect-main` | Bypass list empty, enforcement active |
| PR template | `.github/pull_request_template.md` | What changed / How it was tested / Risk |

## Ticket timeline

Generated with `python3 scripts/timeline.py 1 <PR>`, then annotated.
Mark rows with **STOPPED**, **FAILED** or **NEEDED ME**.

| Time (UTC) | Stage | Actor | Event | Devin stopped/failed/needed me? |
|---|---|---|---|---|
| | issue | | | |
| | branch | | | |
| | PR | | | |
| | CI | | | |
| | review | | | |
| | merge | | | |

## Answers

1. **Did Devin fill in the template?**
2. **What did Devin do when CI failed?**
3. **Could Devin merge on its own?**

## Notes for future "Devin is broken" tickets
