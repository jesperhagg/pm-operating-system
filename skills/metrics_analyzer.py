"""
/metrics-analyzer — Analyze a metrics snapshot and surface key insights.

Usage:
    python skills/metrics_analyzer.py
    python skills/metrics_analyzer.py --focus retention
    python skills/metrics_analyzer.py --focus acquisition
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from skills._claude import ask
from integrations.analytics import get_snapshot


FOCUS_AREAS = ["all", "acquisition", "activation", "engagement", "retention", "revenue", "satisfaction"]


def analyze_metrics(product_id: str = "prod-001", focus: str = "all") -> str:
    snapshot = get_snapshot(product_id)

    system = """You are a sharp, data-driven PM who turns metrics into clear narratives and action items.
You think in terms of the growth funnel (AARRR). You don't just describe numbers — you interpret them,
spot anomalies, identify the biggest levers, and recommend concrete next steps.
Format your response in clean markdown."""

    focus_instruction = (
        f"Focus your analysis specifically on the **{focus}** section of the funnel."
        if focus != "all"
        else "Analyze the full funnel — acquisition, activation, engagement, retention, and revenue."
    )

    user = f"""Analyze the following product metrics snapshot and surface the most important insights.

{focus_instruction}

**Metrics snapshot:**
{json.dumps(snapshot, indent=2)}

Structure your response as:
1. **TL;DR** (2-3 sentence executive summary — what's the headline?)
2. **What's working** (2-3 green flags with evidence)
3. **What needs attention** (top 2-3 concerns, ranked by impact)
4. **Biggest lever right now** (the single metric that, if improved, would have the most downstream impact — and why)
5. **Recommended actions** (3-5 specific, owner-assignable action items)
6. **Watch list** (1-2 metrics to keep an eye on next period)
"""

    return ask(system, user)


def main():
    parser = argparse.ArgumentParser(description="Analyze product metrics and surface insights")
    parser.add_argument("--product", default="prod-001", help="Product ID")
    parser.add_argument(
        "--focus",
        default="all",
        choices=FOCUS_AREAS,
        help="Focus area of the analysis",
    )
    args = parser.parse_args()

    print(f"\nAnalyzing metrics for {args.product} (focus: {args.focus})...\n")
    analysis = analyze_metrics(args.product, args.focus)
    print(analysis)


if __name__ == "__main__":
    main()
