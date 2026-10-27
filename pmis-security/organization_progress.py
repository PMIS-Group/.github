#!/usr/bin/env python3
"""Create a small, read-only organization contribution report from the GitHub API."""
from __future__ import annotations
import argparse, json, os
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def api(url: str, token: str):
    req = Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "PMIS-Security",
    })
    with urlopen(req, timeout=30) as response:
        return json.load(response)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--org", required=True)
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--output", default="weekly-progress.md")
    args = p.parse_args()
    token = os.environ.get("GH_TOKEN", "")
    if not token:
        raise SystemExit("GH_TOKEN is required to create the organization progress report.")

    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    since_iso = since.strftime("%Y-%m-%dT%H:%M:%SZ")
    repos = api(f"https://api.github.com/orgs/{args.org}/repos?per_page=100&type=all", token)
    active, people = [], Counter()
    for repo in repos:
        if repo.get("archived") or repo.get("fork"):
            continue
        name = repo["full_name"]
        commits = api(f"https://api.github.com/repos/{name}/commits?" + urlencode({"since": since_iso, "per_page": 100}), token)
        pulls = api(f"https://api.github.com/repos/{name}/pulls?" + urlencode({"state": "all", "sort": "updated", "direction": "desc", "per_page": 100}), token)
        recent_pulls = [x for x in pulls if x.get("updated_at", "") >= since_iso]
        authors = Counter()
        for commit in commits:
            login = (commit.get("author") or {}).get("login") or "unlinked Git author"
            authors[login] += 1; people[login] += 1
        for pr in recent_pulls:
            login = (pr.get("user") or {}).get("login")
            if login: people[login] += 1
        if commits or recent_pulls:
            merged = sum(1 for x in recent_pulls if x.get("merged_at"))
            active.append((name, len(commits), len(recent_pulls), merged, repo.get("updated_at", ""), authors))

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# PMIS Security — Organization progress ({args.days} days)", "",
        f"**Checked:** {now}  ",
        f"**Organization:** `{args.org}`  ",
        f"**Coverage:** {len(repos)} visible repositories; archived and forked repositories excluded.", "",
        "## Project activity", "",
        "| Repository | Commits | Updated PRs | Merged PRs | Last repository update |",
        "|---|---:|---:|---:|---|",
    ]
    if active:
        for name, commits, pulls, merged, updated, _ in sorted(active, key=lambda x: (-x[1]-x[2], x[0].lower())):
            lines.append(f"| `{name}` | {commits} | {pulls} | {merged} | {updated[:10] or 'unknown'} |")
    else:
        lines.append("| — | 0 | 0 | 0 | No activity visible in this period |");
    lines += ["", "## Contributor activity", "", "| Contributor | Activity items |", "|---|---:|"]
    if people:
        for login, count in people.most_common(30):
            mention = f"@{login}" if login != "unlinked Git author" else login
            lines.append(f"| {mention} | {count} |")
    else:
        lines.append("| No activity visible | 0 |")
    lines += ["", "## Review notes", "", "- Counts show GitHub activity, not hours worked or quality of work.", "- Use the linked project reports and pull requests to review the actual code and findings.", "- A repository missing from this report may be inaccessible to the configured GitHub token.", ""]
    Path(args.output).write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
