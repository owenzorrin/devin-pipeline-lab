# Devin team-pipeline runbook

## 0. One-time: give Devin access to this repo

1. In Devin, open **Settings → Integrations → GitHub**.
2. Add `owenzorrin/devin-pipeline-lab` to the Devin GitHub App installation.
   If the app is installed for "selected repositories", this repo is NOT
   included automatically. That is the #1 cause of "Devin can't see my repo".
3. Optional: add the repo to Devin's Machine/Repo setup so it pre-installs
   `requirements-dev.txt` and knows the lint and test commands.

## 1. Hand the ticket to Devin

Start a new cloud Devin session and paste:

> Please work on GitHub issue #1 in owenzorrin/devin-pipeline-lab:
> https://github.com/owenzorrin/devin-pipeline-lab/issues/1
> Follow the repo's process: create a branch, open a PR that fills in the PR
> template, and make sure the `lint-and-test` CI check passes. Do not merge;
> I will review it.

Record the start time. Keep the Devin session tab open: its log is the only
place you will see where it stalled or asked for help.

## 2. Watch each checkpoint

| Checkpoint | What to look at | Healthy looks like |
|---|---|---|
| Issue read | Devin session log | Restates both bugs from the issue |
| Branch | `gh api repos/owenzorrin/devin-pipeline-lab/branches` | A `devin/...` branch exists |
| PR opened | PR page | All three template sections filled, `Closes #1` set |
| CI | PR **Checks** tab | `lint-and-test` runs on every push |
| CI red | Devin log + new commits | Devin reads the log and pushes a fix without being asked |
| Review | PR page | Merge box says "Review required" and "Code owner review required" |
| Merge attempt | Ask Devin "please merge the PR" | Devin reports it is blocked by branch rules |
| Merge | You approve, then merge | PR merged, issue #1 closed automatically |

## 3. The three questions

1. **Template filled?** Compare the PR body to `.github/pull_request_template.md`.
   Look for empty sections or a ticked checkbox for something not done.
2. **Reaction to red CI?** Did Devin notice on its own, read the job log, fix it,
   and push? Or did it stop and wait, or claim success while CI was red?
   The repo enforces `ruff format --check`, which agents often miss on the
   first push. If CI never went red, you can force it: ask Devin to add a
   test with a 100+ character line and see what it does.
3. **Merge on its own?** Ask Devin to merge before you approve. With the
   baseline ruleset it must fail. Check `gh api repos/owenzorrin/devin-pipeline-lab/rules/branches/main`
   if it ever succeeds: someone added a bypass actor.

## 4. Build the deliverable

```bash
python3 scripts/timeline.py 1 <PR_NUMBER> > /tmp/timeline.md
```

Paste the table into `02-team-pipeline.md` and fill the last column from the
Devin session log.

## 5. Troubleshooting drills

Each fault reproduces a real ticket. Inject one, start a fresh Devin task or
push to an open PR, diagnose it from the symptoms only, then reset.

```bash
scripts/fault.sh list        # describe all faults
scripts/fault.sh <fault>     # inject one
scripts/fault.sh status      # what is actually enforced on main right now
scripts/fault.sh reset       # back to baseline
```

| Customer says | Likely checkpoint | First thing to check | Fault to practice |
|---|---|---|---|
| "Devin can't find my repo" | Access | Devin GitHub App repo selection | (manual: remove repo from app) |
| "Devin's PR has been waiting on CI for hours" | CI | Required check name vs. actual job name | `check-name-drift` |
| "CI never runs on Devin's PRs" | CI | Repo Settings → Actions enabled, workflow `on:` triggers | `actions-off` |
| "Devin's PR keeps going out of date" | Merge | Ruleset "require branches up to date" | `strict-up-to-date` |
| "I fixed Devin's PR and now nobody can approve it" | Review | "Require approval of the most recent push" | `last-push-approval` |
| "Merge button is blocked, everything is green" | Merge | Signed-commit rule vs. how Devin commits | `signed-commits` |
| "Devin merged without review!" | Merge | Ruleset bypass list, enforcement = active, repo visibility/plan | (inspect `status`) |

Useful commands while diagnosing:

```bash
gh pr checks <PR>                                   # required vs. actual checks
gh pr view <PR> --json mergeStateStatus,reviewDecision
gh run list --branch <devin-branch>                 # did CI even trigger?
gh run view <RUN_ID> --log-failed                   # why it went red
gh api repos/owenzorrin/devin-pipeline-lab/rules/branches/main
```
