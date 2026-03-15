"""
Linear integration — stub. Returns mockup data when LINEAR_API_KEY is not set.
"""

import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def _is_configured() -> bool:
    return bool(os.environ.get("LINEAR_API_KEY"))


def get_cycle(cycle_id: str | None = None) -> dict:
    """Return current or specified Linear cycle (similar to Jira sprint)."""
    if _is_configured():
        raise NotImplementedError("Real Linear integration not yet implemented.")
    # Map to sprint mockup data for now
    from integrations.jira import _load_mockup_sprint
    sprint = _load_mockup_sprint("sprint-42")
    return {
        "id": cycle_id or "cycle-12",
        "name": sprint["name"],
        "start_date": sprint["start_date"],
        "end_date": sprint["end_date"],
        "issues": sprint["issues"],
        "_mockup": True,
    }


def get_backlog() -> dict:
    """Return Linear backlog issues."""
    if _is_configured():
        raise NotImplementedError("Real Linear integration not yet implemented.")
    path = DATA_DIR / "backlog" / "backlog.json"
    with open(path) as f:
        return json.load(f)
