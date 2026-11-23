#!/usr/bin/env bash
# One-time GitHub setup for the lab. Run from the repo root.
# Creates the PUBLIC repo, pushes main, waits for the first CI run so the
# required check exists, turns on the protect-main ruleset, and opens issue #1.
set -euo pipefail
REPO="owenzorrin/devin-pipeline-lab"

# Public, because rulesets on private repos need a paid plan on personal accounts.
gh repo create "$REPO" --public \
  --description "Sandbox: Devin through issue -> PR -> CI -> review -> merge" \
  --source . --push

echo "Waiting for the first CI run on main..."
sleep 10
RUN_ID="$(gh run list -R "$REPO" --branch main --limit 1 --json databaseId --jq '.[0].databaseId')"
gh run watch -R "$REPO" "$RUN_ID" --exit-status

scripts/fault.sh reset          # creates protect-main from scripts/ruleset-main.json
gh api -X PATCH "repos/$REPO" -F delete_branch_on_merge=true -F allow_auto_merge=false >/dev/null

gh issue create -R "$REPO" \
  --title "Money parsing and formatting break on negatives and thousands separators" \
  --body-file docs/issue-1.md

scripts/fault.sh status
