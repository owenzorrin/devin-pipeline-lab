# devin-pipeline-lab

Sandbox repo for running Devin through a real team pipeline:
issue → branch → PR → CI → code-owner review → merge.

- `src/ledger/` holds a tiny money library with a real bug, tracked in issue #1.
- `.github/` holds the CI workflow, CODEOWNERS and the PR template.
- `scripts/ruleset-main.json` is the baseline protection for `main`.
- `scripts/fault.sh` injects common "Devin is broken" faults for practice.
- `scripts/timeline.py` builds the ticket timeline for `02-team-pipeline.md`.
- `docs/DEVIN-RUNBOOK.md` is the step-by-step walkthrough and troubleshooting map.

Local checks, the same ones CI runs:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
ruff check . && ruff format --check . && pytest -q
```
