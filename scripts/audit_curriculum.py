"""
Curriculum Audit Script (Deterministic Best-Fit Algorithm)
==========================================================

This script uses a mathematical "Battle Royale" approach to match
each subject's skills against ALL job roles and find the best fit.

NO AI/ML predictor is used - this is a pure graph-based comparison.
"""

import os
import sys

# Setup path to import backend modules
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from backend.ml_engine.graph_logic import KnowledgeEngine

# --- CONFIGURATION ---
# Subjects to exclude (Gen Ed / Non-Technical)
SKIP_KEYWORDS = ["PATHFIT", "KOMFIL", "SOSLIT", "GEC", "PI 100", "PE_", "MATH", "FILDIS"]

# Minimum score to display (filters out low-relevance matches)
DISPLAY_THRESHOLD = 15.0


def should_skip_subject(subject_code: str) -> bool:
    """Check if subject should be skipped (Gen Ed/Minor)."""
    code_upper = subject_code.upper()
    for keyword in SKIP_KEYWORDS:
        if keyword.upper() in code_upper:
            return True
    return False


def calculate_match_score(subject_skills: list, role_skills: set) -> float:
    """
    Calculate the match score between subject skills and role requirements.
    
    Formula: (overlapping skills / total required skills) * 100
    """
    if not role_skills:
        return 0.0
    
    # Normalize to lowercase sets
    subject_set = set(s.lower() for s in subject_skills)
    role_set = set(s.lower() for s in role_skills)
    
    # Calculate overlap
    overlap = subject_set.intersection(role_set)
    
    # Score = overlap / required * 100
    return (len(overlap) / len(role_set)) * 100


def find_best_role(subject_skills: list, role_requirements: dict) -> tuple:
    """
    Battle Royale: Compare subject skills against ALL roles.
    Returns: (best_role_name, best_score)
    """
    best_role = None
    best_score = 0.0
    
    for role_name, required_skills in role_requirements.items():
        score = calculate_match_score(subject_skills, required_skills)
        if score > best_score:
            best_score = score
            best_role = role_name
    
    return best_role, best_score


def main():
    print("=" * 80)
    print("📚 CURRICULUM AUDIT REPORT (Deterministic Best-Fit Algorithm)")
    print("   Graph-Based Role Matching - No AI Prediction")
    print("=" * 80)
    
    # 1. Initialize Knowledge Engine
    print("\n🔧 Initializing Knowledge Engine...")
    try:
        ke = KnowledgeEngine()
        print(f"   ✅ Loaded {len(ke.course_map)} subjects from course_map")
        print(f"   ✅ Loaded {len(ke.role_requirements)} roles from role_requirements")
    except Exception as e:
        print(f"   ❌ Error initializing engine: {e}")
        return

    # 2. Audit Loop - Battle Royale
    print("\n" + "-" * 80)
    print(f"{'SUBJECT CODE':<15} | {'BEST MATCHING ROLE':<25} | {'SCORE':>10}")
    print("-" * 80)
    
    # Tracking variables
    total_subjects = 0
    skipped_gened = 0
    below_threshold = 0
    displayed = 0
    high_relevance = 0  # >50%
    
    results = []  # Store valid results
    
    for subject_code, subject_skills in ke.course_map.items():
        total_subjects += 1
        
        # Filter: Skip Gen Ed subjects
        if should_skip_subject(subject_code):
            skipped_gened += 1
            continue
        
        # Skip empty skill lists
        if not subject_skills:
            continue
        
        # Battle Royale: Find best matching role
        best_role, best_score = find_best_role(subject_skills, ke.role_requirements)
        
        if best_role is None:
            continue
        
        # Track high relevance
        if best_score > 50:
            high_relevance += 1
        
        # Apply display threshold
        if best_score > DISPLAY_THRESHOLD:
            results.append({
                'code': subject_code,
                'role': best_role,
                'score': best_score
            })
            displayed += 1
        else:
            below_threshold += 1
    
    # Sort by score (descending)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Print results
    for r in results:
        print(f"{r['code']:<15} | {r['role']:<25} | {r['score']:>8.1f}%")
    
    print("-" * 80)
    
    # 3. Summary Section
    print("\n" + "=" * 80)
    print("📊 AUDIT SUMMARY")
    print("=" * 80)
    print(f"   Total Subjects in Course Map:    {total_subjects}")
    print(f"   Gen Ed/Minor Skipped:            {skipped_gened}")
    print(f"   Below {DISPLAY_THRESHOLD}% Threshold (Hidden):   {below_threshold}")
    print(f"   Displayed in Report:             {displayed}")
    print(f"   High Relevance Matches (>50%):   {high_relevance}")
    print("=" * 80)
    print("\n✅ Audit Complete.")


if __name__ == "__main__":
    main()
