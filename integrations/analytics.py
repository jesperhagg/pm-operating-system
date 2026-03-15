"""
Analytics integration — stub returning mockup metric snapshots.
Mimics a Mixpanel/Amplitude-style data layer.
"""

import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "metrics"


def get_snapshot(product_id: str = "prod-001", period: str | None = None) -> dict:
    """Return the latest (or specified) metrics snapshot for a product."""
    snapshots = sorted(DATA_DIR.glob("snapshot_*.json"), reverse=True)
    if not snapshots:
        raise FileNotFoundError("No metric snapshots found in data/metrics/")
    with open(snapshots[0]) as f:
        return json.load(f)


def get_funnel(funnel_name: str, product_id: str = "prod-001") -> dict:
    """Return a named funnel from the snapshot."""
    snapshot = get_snapshot(product_id)
    funnels = {
        "activation": {
            "name": "Activation Funnel",
            "steps": [
                {"name": "Signup", "users": 1240, "rate": 1.0},
                {"name": "Day 1 Active", "users": 757, "rate": snapshot["activation"]["day_1_activation_rate"]},
                {"name": "Day 7 Active", "users": 583, "rate": snapshot["activation"]["day_7_activation_rate"]},
                {"name": "Completed Onboarding", "users": 471, "rate": snapshot["activation"]["onboarding_completion_rate"]},
            ],
        },
        "conversion": {
            "name": "Trial → Paid Conversion",
            "steps": [
                {"name": "Trial Start", "users": snapshot["acquisition"]["trial_starts"], "rate": 1.0},
                {"name": "Paid Conversion", "users": snapshot["acquisition"]["paid_conversions"], "rate": snapshot["acquisition"]["trial_to_paid_rate"]},
            ],
        },
    }
    if funnel_name not in funnels:
        raise ValueError(f"Unknown funnel: {funnel_name}. Available: {list(funnels.keys())}")
    return funnels[funnel_name]


def get_feature_adoption(product_id: str = "prod-001") -> dict:
    """Return feature adoption rates."""
    snapshot = get_snapshot(product_id)
    return snapshot["engagement"]["feature_adoption"]


def get_retention_curve(product_id: str = "prod-001") -> dict:
    """Return retention curve data."""
    snapshot = get_snapshot(product_id)
    return snapshot["retention"]
