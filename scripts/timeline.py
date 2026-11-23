#!/usr/bin/env python3
"""Print the issue -> branch -> PR -> CI -> review -> merge timeline as Markdown.

Usage: python3 scripts/timeline.py ISSUE_NUMBER PR_NUMBER [owner/repo]
Paste the output into 02-team-pipeline.md, then add the "Devin stopped / failed /
needed me" notes from the Devin session log by hand.
"""

import json
import subprocess
import sys


def gh(path: str):
    out = subprocess.run(
        ["gh", "api", "--paginate", "--slurp", path],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    pages = json.loads(out)
    if isinstance(pages[0], list):
        return [item for page in pages for item in page]
    return pages[0]


def main() -> None:
    issue_no, pr_no = sys.argv[1], sys.argv[2]
    repo = sys.argv[3] if len(sys.argv) > 3 else "owenzorrin/devin-pipeline-lab"
    rows = []

    def add(ts, stage, actor, what):
        rows.append((ts, stage, actor or "-", what))

    issue = gh(f"repos/{repo}/issues/{issue_no}")
    add(
        issue["created_at"],
        "issue",
        issue["user"]["login"],
        f"Issue #{issue_no} opened",
    )
    for ev in gh(f"repos/{repo}/issues/{issue_no}/timeline"):
        kind = ev.get("event")
        actor = (ev.get("actor") or ev.get("user") or {}).get("login")
        ts = ev.get("created_at")
        if kind == "commented":
            add(ts, "issue", actor, "Comment: " + ev["body"].splitlines()[0][:80])
        elif kind in ("assigned", "labeled", "cross-referenced", "closed", "reopened"):
            add(ts, "issue", actor, kind)

    pr = gh(f"repos/{repo}/pulls/{pr_no}")
    add(
        pr["created_at"],
        "PR",
        pr["user"]["login"],
        f"PR #{pr_no} opened from `{pr['head']['ref']}` (draft={pr['draft']})",
    )

    commits = gh(f"repos/{repo}/pulls/{pr_no}/commits")
    for i, c in enumerate(commits):
        who = (c.get("author") or {}).get("login") or c["commit"]["author"]["name"]
        stage = "branch" if i == 0 else "fix-up"
        msg = c["commit"]["message"].splitlines()[0][:70]
        add(c["commit"]["author"]["date"], stage, who, f"Commit {c['sha'][:7]}: {msg}")
        for run in gh(f"repos/{repo}/commits/{c['sha']}/check-runs").get(
            "check_runs", []
        ):
            add(
                run["started_at"],
                "CI",
                "github-actions",
                f"{run['name']} started on {c['sha'][:7]}",
            )
            if run["completed_at"]:
                mark = "GREEN" if run["conclusion"] == "success" else "**RED**"
                add(
                    run["completed_at"],
                    "CI",
                    "github-actions",
                    f"{run['name']} {run['conclusion']} {mark} on {c['sha'][:7]}",
                )

    for c in gh(f"repos/{repo}/issues/{pr_no}/comments"):
        add(
            c["created_at"],
            "PR",
            c["user"]["login"],
            "Comment: " + c["body"].splitlines()[0][:80],
        )
    for r in gh(f"repos/{repo}/pulls/{pr_no}/reviews"):
        add(r["submitted_at"], "review", r["user"]["login"], f"Review: {r['state']}")
    for c in gh(f"repos/{repo}/pulls/{pr_no}/comments"):
        add(
            c["created_at"],
            "review",
            c["user"]["login"],
            f"Inline on {c['path']}: " + c["body"].splitlines()[0][:60],
        )

    if pr["merged_at"]:
        add(
            pr["merged_at"],
            "merge",
            (pr.get("merged_by") or {}).get("login"),
            f"Merged into {pr['base']['ref']}",
        )

    print(
        "| Time (UTC) | Stage | Actor | Event | Devin stopped / failed / needed me? |"
    )
    print("|---|---|---|---|---|")
    for ts, stage, actor, what in sorted(rows):
        print(f"| {ts.replace('T', ' ').rstrip('Z')} | {stage} | {actor} | {what} | |")


if __name__ == "__main__":
    main()
