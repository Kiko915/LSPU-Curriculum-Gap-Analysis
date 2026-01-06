"""
Analytics Database Module
=========================

JSON-based logging for student requests and curriculum analytics.
Used for Macro-Gap Analysis to identify curriculum improvement opportunities.
"""

import json
import os
from collections import Counter
from datetime import datetime
from typing import Dict, List, Any

# Path to the student logs JSON file
LOGS_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_FILE = os.path.join(LOGS_DIR, "student_logs.json")


def _load_logs() -> List[Dict]:
    """Load existing logs from JSON file."""
    if not os.path.exists(LOGS_FILE):
        return []
    try:
        with open(LOGS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save_logs(logs: List[Dict]) -> None:
    """Save logs to JSON file."""
    with open(LOGS_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def log_student_request(role: str, missing_skills: List[str], student_name: str = None) -> None:
    """
    Log a student's analysis request.
    
    Args:
        role: The predicted job role
        missing_skills: List of skills the student is missing for that role
        student_name: Optional name of the student
    """
    logs = _load_logs()
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "student_name": student_name,
        "predicted_role": role,
        "missing_skills": missing_skills
    }
    
    logs.append(log_entry)
    _save_logs(logs)


def get_analytics() -> Dict[str, Any]:
    """
    Analyze logged student data to identify trends.
    
    Returns:
        Dictionary containing:
        - top_5_roles: Most predicted roles with counts
        - top_10_missing_skills: Most commonly missing skills with counts
        - total_requests: Total number of logged requests
    """
    logs = _load_logs()
    
    if not logs:
        return {
            "top_5_roles": [],
            "top_10_missing_skills": [],
            "total_requests": 0
        }
    
    # Count roles
    role_counter = Counter(log["predicted_role"] for log in logs)
    top_5_roles = [
        {"role": role, "count": count}
        for role, count in role_counter.most_common(5)
    ]
    
    # Count missing skills (flatten all missing skills)
    all_missing_skills = []
    for log in logs:
        all_missing_skills.extend(log.get("missing_skills", []))
    
    skill_counter = Counter(all_missing_skills)
    top_10_missing_skills = [
        {"skill": skill, "count": count}
        for skill, count in skill_counter.most_common(10)
    ]
    
    return {
        "top_5_roles": top_5_roles,
        "top_10_missing_skills": top_10_missing_skills,
        "total_requests": len(logs)
    }


def clear_logs() -> None:
    """Clear all student logs (for testing/admin purposes)."""
    _save_logs([])
