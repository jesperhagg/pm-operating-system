"""
/sprint-planner — Generate a sprint plan from the current backlog.

Usage:
    python skills/sprint_planner.py
    python skills/sprint_planner.py --capacity 40 --sprint-goal "Ship Jira integration"
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from skills._claude import ask
from integrations.jira import get_backlog, get_sprint


def plan_sprint(capacity: int = 40, sprint_goal: str | None = None, product_id: str = "prod-001") -> str:
    backlog = get_backlog(product_id)
    last_sprint = get_sprint("sprint-42")

    velocity = last_sprint["velocity_last_3_sprints"]
    avg_velocity = sum(velocity) / len(velocity)

    system = """You are a seasoned Agile PM and Scrum Master.
You create sprint plans that are ambitious but achievable, always include a clear goal,
and explicitly call out risks and dependencies."""

    user = f"""Create a sprint plan for the next sprint (Sprint 43).

**Team capacity:** {capacity} story points
**Average velocity (last 3 sprints):** {avg_velocity:.0f} points
**Team:** {', '.join(last_sprint['team'])}

**Sprint goal (if specified):** {sprint_goal or "Infer the best goal from the backlog priority"}

**Last sprint summary:**
- Goal: {last_sprint['goal']}
- Completion rate: {last_sprint['summary']['completion_rate']:.0%}
- Blockers encountered: {last_sprint['summary']['blockers_count']}
- Bugs resolved: {last_sprint['summary']['bugs_resolved']}, open: {last_sprint['summary']['bugs_open']}

**Carry-over items (incomplete from sprint 42):**
{json.dumps([i for i in last_sprint['issues'] if i['status'] not in ('done',)], indent=2)}

**Backlog (prioritized, ready items):**
{json.dumps([i for i in backlog['items'] if i['status'] in ('ready', 'groomed')], indent=2)}

Produce:
1. **Sprint goal** (one crisp sentence)
2. **Committed items** — table with: Issue ID | Title | Points | Assignee | Why this sprint
3. **Total committed points** and buffer remaining
4. **Risks & dependencies** (2-4 bullets)
5. **Definition of done for the sprint goal**
6. **What's NOT in this sprint** (explicitly cut items with brief rationale)
"""

    return ask(system, user)


def main():
    parser = argparse.ArgumentParser(description="Generate a sprint plan from the backlog")
    parser.add_argument("--capacity", type=int, default=40, help="Team capacity in story points")
    parser.add_argument("--sprint-goal", default=None, help="Desired sprint goal (optional)")
    parser.add_argument("--product", default="prod-001", help="Product ID")
    args = parser.parse_args()

    print(f"\nGenerating sprint plan (capacity: {args.capacity} pts)...\n")
    plan = plan_sprint(args.capacity, args.sprint_goal, args.product)
    print(plan)


if __name__ == "__main__":
    main()
