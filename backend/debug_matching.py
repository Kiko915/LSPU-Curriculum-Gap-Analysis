
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_engine'))

from ml_engine.graph_logic import KnowledgeEngine

def debug_match():
    ke = KnowledgeEngine()
    
    # Test Case: User enters "API Testing" (should match "api")
    req_role = "Web Developer"  # Requires 'api'
    
    user_skills = ["API Testing", "HTML, CSS", "JavaScript Basics"]
    
    print(f"Role: {req_role}")
    print(f"Requirements: {ke.role_requirements[req_role]}")
    print(f"User Skills: {user_skills}")
    
    result = ke.analyze_gap(req_role, user_skills)
    
    print("\n--- Results ---")
    print(f"Present Skills: {result['present_skills']}")
    print(f"Missing Skills: {result['missing_skills']}")
    
    # Check if 'api' is in present skills
    if 'api' in result['present_skills']:
        print("\nSUCCESS: 'api' found in present skills!")
    else:
        print("\nFAILURE: 'api' NOT found.")

if __name__ == "__main__":
    debug_match()
