import os
import sys

# Ensure we can import from the backend module
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)

from backend.ml_engine.predictor import MLPredictor

def main():
    print("--- Initializing MLPredictor for Stress Test ---")
    try:
        predictor = MLPredictor()
    except Exception as e:
        print(f"Failed to initialize predictor: {e}")
        return

    test_scenarios = [
        {
            "name": "The Hybrid (Design + Code)",
            "skills": ['React', 'CSS', 'Figma', 'Photoshop']
        },
        {
            "name": "The Ambiguous (Generic)",
            "skills": ['Python', 'SQL', 'Git']
        },
        {
            "name": "The Niche (QA/Testing)",
            "skills": ['Selenium', 'Junit', 'Bug Tracking', 'Jira']
        },
        {
            "name": "The Minimalist (One Keyword)",
            "skills": ['Excel']
        },
        {
            "name": "The Noisy (Relevant + Irrelevant)",
            "skills": ['Python', 'Cooking', 'Swimming', 'Django']
        },
        {
            "name": "The Managerial",
            "skills": ['Leadership', 'Agile', 'Scrum', 'Budgeting']
        }
    ]

    print("\n--- Starting Stress Test ---\n")

    for test in test_scenarios:
        skills = test["skills"]
        try:
            role, confidence = predictor.predict_role(skills)
            print(f"[TEST: {test['name']}]")
            print(f"Input: {skills}")
            print(f"=> Prediction: {role} ({confidence * 100:.1f}%)")
            print("-" * 40)
        except Exception as e:
            print(f"[TEST: {test['name']}] FAILED: {e}")
            print("-" * 40)

if __name__ == "__main__":
    main()
