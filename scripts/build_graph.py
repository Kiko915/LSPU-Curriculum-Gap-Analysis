import pandas as pd
import json
import ast
import os
import sys

def parse_skills(skill_entry):
    """
    Parses a skill entry which could be a list string, a semicolon-separated string,
    or a comma-separated string. Returns a list of strings.
    """
    if pd.isna(skill_entry) or skill_entry == "":
        return []

    # Try interpreting as a python list literal (e.g. "['Python', 'SQL']")
    try:
        # If it looks like a list
        if str(skill_entry).strip().startswith("["):
            parsed = ast.literal_eval(skill_entry)
            if isinstance(parsed, list):
                return [str(s).strip() for s in parsed]
    except (ValueError, SyntaxError):
        pass

    # Handle string delimiters
    # Some entries might use semicolons, others commas.
    # We'll replace semicolons with commas and then split, 
    # but we must be careful if there are valid commas in skill names (unlikely in this context but possible).
    # Given the examples: "Python; Java" and "React, Node.js"
    
    # Priority 1: Semicolon separation (common in the provided sample)
    if ";" in str(skill_entry):
        return [s.strip() for s in str(skill_entry).split(";") if s.strip()]
    
    # Priority 2: Comma separation
    if "," in str(skill_entry):
        return [s.strip() for s in str(skill_entry).split(",") if s.strip()]

    # Priority 3: Single item
    return [str(skill_entry).strip()]

def main():
    input_path = os.path.join("data", "raw", "job_dataset.csv")
    output_dir = os.path.join("data", "processed")
    output_path = os.path.join(output_dir, "skills_taxonomy.json")

    print(f"Loading data from {input_path}...")
    
    if not os.path.exists(input_path):
        print(f"Error: Input file ( {input_path} ) not found.")
        sys.exit(1)

    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    if 'Skills' not in df.columns:
        print("Error: 'Skills' column not found in the dataset.")
        sys.exit(1)

    print("Parsing skills...")
    all_skills = set()
    
    # Process each row
    for raw_skills in df['Skills']:
        parsed_list = parse_skills(raw_skills)
        for skill in parsed_list:
            all_skills.add(skill)

    # Sort alphabetically
    sorted_skills = sorted(list(all_skills))

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save to JSON
    with open(output_path, 'w') as f:
        json.dump(sorted_skills, f, indent=4)

    print(f"Success! Processed {len(sorted_skills)} unique skills.")
    print(f"Saved taxonomy to {output_path}")

if __name__ == "__main__":
    main()
