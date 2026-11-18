"""
SupportPilot - Rule-Based Severity & Priority Module
----------------------------------------------------
Determines ticket severity using keyword-based rules (NOT machine learning)
and maps severity levels to standard IT support priority codes.

Severity Levels:
- Critical -> P1
- High     -> P2
- Medium   -> P3 (default when no Critical/High/Low keywords match)
- Low      -> P4
"""

# Rule-based keyword lists (ordered by precedence: Critical -> High -> Low -> Medium default)
SEVERITY_KEYWORDS = {
    "Critical": [
        "entire office",
        "all employees",
        "all users",
        "server down",
        "server is down",
        "complete outage",
        "critical outage",
        "major outage",
        "company-wide outage",
        "business stopped",
    ],
    "High": [
        "multiple users",
        "many employees",
        "production down",
        "cannot work",
        "unable to work",
        "entire team",
        "department down",
    ],
    "Low": [
        "minor issue",
        "small issue",
        "occasionally",
        "cosmetic",
        "low priority",
        "not urgent",
    ],
}

# Standard severity-to-priority mapping
PRIORITY_MAP = {
    "Critical": "P1",
    "High": "P2",
    "Medium": "P3",
    "Low": "P4",
}


def calculate_severity(description, title=""):
    """
    Calculate ticket severity using keyword-based rules.
    Evaluates both ticket title and description together.

    Note: This is strictly rule-based keyword matching, not an ML model.
    """
    combined_text = f"{title or ''} {description or ''}".lower().strip()

    if not combined_text:
        return "Medium"

    # Check in strict precedence order: Critical -> High -> Low -> default Medium
    if any(keyword in combined_text for keyword in SEVERITY_KEYWORDS["Critical"]):
        return "Critical"

    if any(keyword in combined_text for keyword in SEVERITY_KEYWORDS["High"]):
        return "High"

    if any(keyword in combined_text for keyword in SEVERITY_KEYWORDS["Low"]):
        return "Low"

    return "Medium"


def calculate_priority(severity):
    """Map severity level to priority code (Critical->P1, High->P2, Medium->P3, Low->P4)."""
    return PRIORITY_MAP.get(severity, "P3")
