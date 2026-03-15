"""
/stakeholder-update — Write a stakeholder update from sprint and metrics data.

Usage:
    python skills/stakeholder_update.py
    python skills/stakeholder_update.py --sprint sprint-42 --post-to-slack
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from skills._claude import ask
from integrations.jira import get_sprint
from integrations.analytics import get_snapshot
from integrations.slack import post_message


def write_update(sprint_id: str = "sprint-42", product_id: str = "prod-001") -> str:
    sprint = get_sprint(sprint_id)
    metrics = get_snapshot(product_id)

    done_issues = [i for i in sprint["issues"] if i["status"] == "done"]
    blocked_issues = [i for i in sprint["issues"] if i.get("blocker")]

    system = """You are a PM writing a crisp, honest stakeholder update.
Your updates are:
- Concise (2-3 min read max)
- Honest about blockers — you don't hide problems
- Forward-looking — you always end with what's next
- Written in plain English, no jargon
Format in markdown."""

    user = f"""Write a stakeholder update for the following sprint.

**Sprint:** {sprint['name']}
**Goal:** {sprint['goal']}
**Period:** {sprint['start_date']} → {sprint['end_date']}

**Completion:** {sprint['summary']['completion_rate']:.0%} ({sprint['summary']['done_points']}/{sprint['summary']['committed_points']} pts)

**Completed this sprint:**
{json.dumps([{{'id': i['id'], 'title': i['title']}} for i in done_issues], indent=2)}

**In progress / carried over:**
{json.dumps([{{'id': i['id'], 'title': i['title'], 'status': i['status'], 'blocker': i.get('blocker')}} for i in sprint['issues'] if i['status'] != 'done'], indent=2)}

**Blockers:**
{json.dumps([{{'id': i['id'], 'title': i['title'], 'blocker': i['blocker']}} for i in blocked_issues], indent=2)}

**Key metrics this period:**
- Day-7 activation: {metrics['activation']['day_7_activation_rate']:.1%} (target: 60%)
- Monthly churn: {metrics['retention']['monthly_churn_rate']:.1%} (target: 2%)
- NPS: {metrics['satisfaction']['nps_score']} (target: 45)
- MRR: ${metrics['revenue']['mrr_usd']:,} (+{metrics['revenue']['mrr_mom_growth_pct']}% MoM)

Write the update with:
1. **Sprint summary** (2-3 sentences: what we shipped, completion rate, headline)
2. **Shipped** (bullet list of notable completions)
3. **Blockers & risks** (honest assessment, with mitigation plan)
4. **Metrics pulse** (2-3 sentences on key numbers — is the sprint moving the needle?)
5. **Next sprint focus** (what we're prioritizing and why)
"""

    return ask(system, user)


def main():
    parser = argparse.ArgumentParser(description="Write a stakeholder update from sprint data")
    parser.add_argument("--sprint", default="sprint-42", help="Sprint ID")
    parser.add_argument("--product", default="prod-001", help="Product ID")
    parser.add_argument("--post-to-slack", action="store_true", help="Post update to Slack")
    args = parser.parse_args()

    print(f"\nWriting stakeholder update for {args.sprint}...\n")
    update = write_update(args.sprint, args.product)
    print(update)

    if args.post_to_slack:
        print("\nPosting to Slack...")
        post_message(update)


if __name__ == "__main__":
    main()
