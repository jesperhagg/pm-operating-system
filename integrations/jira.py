"""
Jira integration — stub that returns mockup data when no credentials are set.
Set JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN env vars for real integration.
"""

import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def _is_configured() -> bool:
    return all(
        os.environ.get(k) for k in ["JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN"]
    )


def get_sprint(sprint_id: str) -> dict:
    """Return sprint data by ID."""
    if _is_configured():
        return _fetch_sprint_real(sprint_id)
    return _load_mockup_sprint(sprint_id)


def get_backlog(product_id: str = "prod-001") -> dict:
    """Return backlog items for a product."""
    if _is_configured():
        return _fetch_backlog_real(product_id)
    return _load_mockup_backlog(product_id)


def create_issue(title: str, description: str, issue_type: str = "Story", priority: str = "Medium") -> dict:
    """Create a Jira issue. Returns the created issue dict."""
    if _is_configured():
        return _create_issue_real(title, description, issue_type, priority)
    # Mockup: just echo back a fake created issue
    return {
        "id": "CORE-999",
        "title": title,
        "description": description,
        "type": issue_type,
        "priority": priority,
        "status": "To Do",
        "url": "https://example.atlassian.net/browse/CORE-999",
        "_mockup": True,
    }


# --- Mockup loaders ---

def _load_mockup_sprint(sprint_id: str) -> dict:
    path = DATA_DIR / "sprints" / f"{sprint_id}.json"
    if not path.exists():
        # Return latest sprint as fallback
        sprints = list((DATA_DIR / "sprints").glob("*.json"))
        if not sprints:
            raise FileNotFoundError("No sprint data found in data/sprints/")
        path = sorted(sprints)[-1]
    with open(path) as f:
        return json.load(f)


def _load_mockup_backlog(product_id: str) -> dict:
    path = DATA_DIR / "backlog" / "backlog.json"
    with open(path) as f:
        data = json.load(f)
    if product_id and data.get("product_id") != product_id:
        return {"product_id": product_id, "items": []}
    return data


# --- Real API stubs (implement when credentials are set) ---

def _fetch_sprint_real(sprint_id: str) -> dict:
    raise NotImplementedError("Real Jira integration not yet implemented. Set JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN.")


def _fetch_backlog_real(product_id: str) -> dict:
    raise NotImplementedError("Real Jira integration not yet implemented.")


def _create_issue_real(title: str, description: str, issue_type: str, priority: str) -> dict:
    raise NotImplementedError("Real Jira integration not yet implemented.")
