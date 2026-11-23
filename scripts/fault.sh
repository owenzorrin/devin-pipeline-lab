#!/usr/bin/env bash
# Inject or clear a known "Devin is broken" fault on the sandbox repo.
# Usage: scripts/fault.sh list | status | reset | <fault-name>
set -euo pipefail
REPO="${REPO:-owenzorrin/devin-pipeline-lab}"
DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$DIR/ruleset-main.json"

ruleset_id() {
  gh api "repos/$REPO/rulesets" --jq '.[] | select(.name=="protect-main") | .id'
}

put_ruleset() {  # $1 = jq filter applied to the baseline ruleset
  local id body
  id="$(ruleset_id)"
  body="$(jq "$1" "$BASE")"
  if [[ -z "$id" ]]; then
    echo "$body" | gh api -X POST "repos/$REPO/rulesets" --input - >/dev/null
  else
    echo "$body" | gh api -X PUT "repos/$REPO/rulesets/$id" --input - >/dev/null
  fi
}

case "${1:-list}" in
  list)
    cat <<'TXT'
check-name-drift    Required check renamed to "CI / lint-and-test". PRs sit on
                    "Expected - Waiting for status to be reported" forever.
strict-up-to-date   Branch must be up to date with main. Devin PRs go
                    "out-of-date" whenever anything else merges first.
last-push-approval  The last pusher cannot approve. If YOU push a fix onto
                    Devin's branch, nobody left can approve it.
signed-commits      Commits must be signed. Unsigned commits block the merge.
actions-off         GitHub Actions disabled. CI never runs, so PRs never go green.
reset               Restore the baseline ruleset and re-enable Actions.
status              Show the live ruleset and Actions state.
TXT
    ;;
  check-name-drift)
    put_ruleset '(.rules[] | select(.type=="required_status_checks").parameters.required_status_checks) = [{"context":"CI / lint-and-test","integration_id":15368}]' ;;
  strict-up-to-date)
    put_ruleset '(.rules[] | select(.type=="required_status_checks").parameters.strict_required_status_checks_policy) = true' ;;
  last-push-approval)
    put_ruleset '(.rules[] | select(.type=="pull_request").parameters.require_last_push_approval) = true' ;;
  signed-commits)
    put_ruleset '.rules += [{"type":"required_signatures"}]' ;;
  actions-off)
    gh api -X PUT "repos/$REPO/actions/permissions" -F enabled=false >/dev/null ;;
  reset)
    put_ruleset '.'
    gh api -X PUT "repos/$REPO/actions/permissions" -F enabled=true -f allowed_actions=all >/dev/null ;;
  status)
    echo "Actions enabled: $(gh api "repos/$REPO/actions/permissions" --jq .enabled)"
    gh api "repos/$REPO/rulesets/$(ruleset_id)" --jq '{enforcement, bypass_actors, rules}'
    echo "Effective rules on main:"
    gh api "repos/$REPO/rules/branches/main" --jq '.[] | "  - \(.type) \(.parameters // {} | tostring)"' ;;
  *) echo "unknown fault: $1 (try: list)" >&2; exit 1 ;;
esac
[[ "${1:-list}" =~ ^(list|status)$ ]] || echo "applied: $1"
