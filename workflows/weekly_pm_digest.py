"""
Weekly PM Digest workflow — end-to-end agentic workflow.

Pulls sprint data + metrics, generates a digest via Claude, and optionally posts to Slack.

Usage:
    python workflows/weekly_pm_digest.py
    python workflows/weekly_pm_digest.py --post-to-slack
    python workflows/weekly_pm_digest.py --sprint sprint-42 --product prod-001
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent))

from skills._claude import ask
from integrations.jira import get_sprint, get_backlog
from integrations.analytics import get_snapshot, get_funnel
from integrations.slack import post_message


def run_digest(sprint_id: str = "sprint-42", product_id: str = "prod-001") -> str:
    print("  [1/4] Fetching sprint data...")
    sprint = get_sprint(sprint_id)

    print("  [2/4] Fetching metrics snapshot...")
    metrics = get_snapshot(product_id)

    print("  [3/4] Fetching backlog...")
    backlog = get_backlog(product_id)

    print("  [4/4] Generating digest with Claude...")

    activation_funnel = get_funnel("activation", product_id)

    done_issues = [i for i in sprint["issues"] if i["status"] == "done"]
    blocked_issues = [i for i in sprint["issues"] if i.get("blocker")]
    next_up = [i for i in backlog["items"] if i["status"] in ("ready", "groomed")][:5]

    system = """You are a PM's AI assistant writing the weekly PM digest.
The digest goes to the full team (engineering, design, leadership).
It should be informative, honest, and motivating — not a boring status report.
Write in a clear, direct tone. Use emoji sparingly and only where it adds clarity.
Format in markdown, optimized for Slack rendering."""

    user = f"""Write the weekly PM digest for the week ending {date.today().strftime('%B %d, %Y')}.

**Sprint:** {sprint['name']}
**Sprint goal:** {sprint['goal']}
**Sprint completion:** {sprint['summary']['completion_rate']:.0%} ({sprint['summary']['done_points']}/{sprint['summary']['committed_points']} pts)

**What shipped this week:**
{json.dumps([{{'id': i['id'], 'title': i['title']}} for i in done_issues], indent=2)}

**Active blockers:**
{json.dumps([{{'issue': i['id'], 'title': i['title'], 'blocker': i['blocker']}} for i in blocked_issues], indent=2)}

**Metrics this week:**
- MRR: ${metrics['revenue']['mrr_usd']:,} (+{metrics['revenue']['mrr_mom_growth_pct']}% MoM)
- New signups: {metrics['acquisition']['new_signups']} (+{metrics['acquisition']['signups_mom_pct']}% MoM)
- Day-7 activation: {metrics['activation']['day_7_activation_rate']:.1%} (target: 60%)
- Monthly churn: {metrics['retention']['monthly_churn_rate']:.1%} (target: 2%)
- NPS: {metrics['satisfaction']['nps_score']} (target: 45)
- DAU/MAU: {metrics['engagement']['dau_mau_ratio']:.1%}

**Activation funnel:**
{json.dumps(activation_funnel, indent=2)}

**Coming up next sprint:**
{json.dumps([{{'id': i['id'], 'title': i['title'], 'priority': i['priority']}} for i in next_up], indent=2)}

Write the digest with these sections:
1. **This week in one line** (the headline — what was the most important thing?)
2. **Shipped** (brief, energizing bullets on what went out)
3. **Metrics pulse** (3-4 sentences — are we moving toward our goals? What stands out?)
4. **Blockers** (honest, solution-oriented — what are we doing about them?)
5. **Up next** (what the team is focused on in the coming sprint)
6. **Ask / FYI** (any decision needed from leadership, or important heads-up)

Keep total length to ~400 words.
"""

    return ask(system, user)


def main():
    parser = argparse.ArgumentParser(description="Run the weekly PM digest workflow")
    parser.add_argument("--sprint", default="sprint-42", help="Sprint ID")
    parser.add_argument("--product", default="prod-001", help="Product ID")
    parser.add_argument("--post-to-slack", action="store_true", help="Post digest to Slack")
    args = parser.parse_args()

    print(f"\nRunning Weekly PM Digest for {args.sprint}...\n")

    digest = run_digest(args.sprint, args.product)

    print("\n" + "="*60)
    print("WEEKLY PM DIGEST")
    print("="*60)
    print(digest)

    if args.post_to_slack:
        print("\nPosting to Slack...")
        result = post_message(digest)
        if result.get("ok"):
            print(f"Posted to {result['channel']}")

    return digest


if __name__ == "__main__":
    main()
