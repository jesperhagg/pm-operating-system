"""
/prd-writer — Draft a PRD from a one-liner feature idea.

Usage:
    python skills/prd_writer.py "AI-powered smart search across all projects"
    python skills/prd_writer.py --persona persona-002 "AI-powered smart search"
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from skills._claude import ask
from integrations import analytics

DATA_DIR = Path(__file__).parent.parent / "data"


def load_personas() -> list:
    with open(DATA_DIR / "users" / "personas.json") as f:
        return json.load(f)["personas"]


def load_product(product_id: str = "prod-001") -> dict:
    with open(DATA_DIR / "products" / "products.json") as f:
        products = json.load(f)["products"]
    return next(p for p in products if p["id"] == product_id)


def write_prd(feature: str, persona_id: str | None = None, product_id: str = "prod-001") -> str:
    product = load_product(product_id)
    personas = load_personas()
    metrics = analytics.get_snapshot(product_id)

    if persona_id:
        primary_persona = next((p for p in personas if p["id"] == persona_id), personas[0])
    else:
        primary_persona = personas[0]

    system = """You are a senior Product Manager writing a concise, high-quality PRD.
Your PRDs are clear, outcome-focused, and skip corporate fluff.
Format in clean markdown. Be specific — use numbers and metrics where relevant."""

    user = f"""Write a PRD for the following feature idea:

**Feature:** {feature}

**Product context:**
- Product: {product['name']} — {product['description']}
- Stage: {product['stage']}
- Current OKRs: {json.dumps(product['okrs'], indent=2)}

**Primary user persona:**
{json.dumps(primary_persona, indent=2)}

**Current metrics (for context):**
- DAU/MAU: {metrics['engagement']['dau_mau_ratio']:.1%}
- Day-7 activation: {metrics['activation']['day_7_activation_rate']:.1%}
- NPS: {metrics['satisfaction']['nps_score']}
- Monthly churn: {metrics['retention']['monthly_churn_rate']:.1%}
- Top complaints: {metrics['satisfaction']['top_complaints']}

Write a PRD with these sections:
1. **Problem** (2-3 sentences max — what pain, for whom, how often)
2. **Why now** (opportunity, metrics signal, or strategic moment)
3. **Goal** (single measurable outcome this feature drives)
4. **Non-goals** (2-3 explicit things out of scope)
5. **User stories** (3-5 "As a [user], I want to [action] so that [outcome]")
6. **Acceptance criteria** (5-8 specific, testable criteria)
7. **Success metrics** (2-3 metrics + targets + measurement approach)
8. **Open questions** (2-4 unknowns to resolve before building)
9. **Rough effort estimate** (S/M/L/XL with brief rationale)
"""

    return ask(system, user)


def main():
    parser = argparse.ArgumentParser(description="Draft a PRD from a feature idea")
    parser.add_argument("feature", help="Feature idea (one sentence)")
    parser.add_argument("--persona", default=None, help="Persona ID (e.g. persona-002)")
    parser.add_argument("--product", default="prod-001", help="Product ID")
    args = parser.parse_args()

    print(f"\nDrafting PRD for: {args.feature}\n")
    prd = write_prd(args.feature, args.persona, args.product)
    print(prd)


if __name__ == "__main__":
    main()
