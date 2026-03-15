"""
/user-story-gen — Generate user stories with acceptance criteria from a feature idea.

Usage:
    python skills/user_story_gen.py "Jira two-way sync"
    python skills/user_story_gen.py --personas all "Notification preferences center"
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from skills._claude import ask

DATA_DIR = Path(__file__).parent.parent / "data"


def load_personas(persona_ids: list[str] | None = None) -> list:
    with open(DATA_DIR / "users" / "personas.json") as f:
        all_personas = json.load(f)["personas"]
    if not persona_ids or persona_ids == ["all"]:
        return all_personas
    return [p for p in all_personas if p["id"] in persona_ids]


def generate_stories(feature: str, persona_ids: list[str] | None = None) -> str:
    personas = load_personas(persona_ids)

    system = """You are a PM who writes crystal-clear user stories.
Your stories follow the standard format and always include:
- A clear "so that" clause (the outcome/value, not just the action)
- Specific, testable acceptance criteria (Given/When/Then or bullet list)
- Edge cases and error states
You write for engineers who need to build the feature, not marketing."""

    user = f"""Generate user stories for the following feature:

**Feature:** {feature}

**User personas to consider:**
{json.dumps(personas, indent=2)}

For each persona that would use this feature, write:
- 2-3 user stories in format: "As a [persona], I want to [action] so that [outcome]"
- 4-6 acceptance criteria per story (specific and testable)
- 1-2 edge cases / error states per story

Also include:
- **Epic summary** (one sentence tying all stories together)
- **Out of scope** (2-3 explicit non-goals for this feature)
- **Dependencies / blockers** (what needs to be true before building)
"""

    return ask(system, user)


def main():
    parser = argparse.ArgumentParser(description="Generate user stories from a feature idea")
    parser.add_argument("feature", help="Feature idea (one sentence)")
    parser.add_argument(
        "--personas",
        nargs="+",
        default=["all"],
        help="Persona IDs to consider (default: all)",
    )
    args = parser.parse_args()

    print(f"\nGenerating user stories for: {args.feature}\n")
    stories = generate_stories(args.feature, args.personas)
    print(stories)


if __name__ == "__main__":
    main()
