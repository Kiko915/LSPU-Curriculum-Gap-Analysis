import pandas as pd
import networkx as nx
import json
import pickle
import os
import sys

def normalize_skill(skill):
    """Normalizes skill text to Title Case for consistency."""
    if not isinstance(skill, str):
        return ""
    # Strip whitespace and convert to Title Case
    return skill.strip().title()

def main():
    # Paths
    job_data_path = os.path.join("data", "raw", "job_dataset.csv")
    curriculum_data_path = os.path.join("data", "processed", "curriculum_data.json")
    output_dir = os.path.join("backend", "ml_engine")
    output_path = os.path.join(output_dir, "graph.gpickle")

    print("Initializing Knowledge Graph Construction...")

    # 1. Initialize Directed Graph
    G = nx.DiGraph()

    # 2. Add Industry Nodes (Job -> Skill)
    print(f"Loading Industry Data from {job_data_path}...")
    if not os.path.exists(job_data_path):
        print(f"Error: {job_data_path} not found.")
        sys.exit(1)

    try:
        df = pd.read_csv(job_data_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    job_count = 0
    industry_skill_count = 0

    # Ensure 'Title' and 'Skills' columns exist (using 'Title' as 'Role' per verification)
    if 'Title' not in df.columns or 'Skills' not in df.columns:
         print("Error: CSV must contain 'Title' and 'Skills' columns.")
         sys.exit(1)

    for _, row in df.iterrows():
        job_role = row['Title']
        if pd.isna(job_role):
            continue
            
        job_role = str(job_role).strip()
        
        # Add Job Node
        if job_role not in G:
            G.add_node(job_role, type="job_role")
            job_count += 1

        skills_entry = row['Skills']
        if pd.isna(skills_entry):
            continue

        # Simple splitting by both ; and , to be robust
        # The previous analysis showed mostly semicolon separation but sometimes mix
        raw_skills = str(skills_entry).replace(";", ",").split(",")
        
        for s in raw_skills:
            clean_s = normalize_skill(s)
            if not clean_s:
                continue

            # Add Skill Node
            if clean_s not in G:
                G.add_node(clean_s, type="skill")
                industry_skill_count += 1 # Count unique *new* skills added here is tough in loop, just tracking interactions might be easier or total unique nodes later.

            # Add Edge: Job -> requires -> Skill
            G.add_edge(job_role, clean_s, relation="requires")

    print(f"Processed Industry Data: Added {job_count} Job nodes.")

    # 3. Add Curriculum Nodes (Subject -> Skill)
    print(f"Loading Curriculum Data from {curriculum_data_path}...")
    if not os.path.exists(curriculum_data_path):
        print(f"Error: {curriculum_data_path} not found.")
        sys.exit(1)

    with open(curriculum_data_path, 'r') as f:
        curriculum_data = json.load(f)

    subject_count = 0
    
    for subject_file, skills_list in curriculum_data.items():
        # Clean subject name (remove .pdf extension or keep as is? User said "Subject_Name.pdf" is key)
        # We can treat the filename as the subject ID.
        subject_name = subject_file
        
        # Add Subject Node
        if subject_name not in G:
            G.add_node(subject_name, type="subject")
            subject_count += 1
            
        for s in skills_list:
            clean_s = normalize_skill(s)
            if not clean_s:
                continue
                
            # Add Skill Node (if not already from industry)
            if clean_s not in G:
                G.add_node(clean_s, type="skill")
            
            # Add Edge: Subject -> teaches -> Skill
            G.add_edge(subject_name, clean_s, relation="teaches")

    print(f"Processed Curriculum Data: Added {subject_count} Subject nodes.")

    # 4. Save the Graph
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Saving graph to {output_path}...")
    try:
        with open(output_path, 'wb') as f:
            pickle.dump(G, f)
    except Exception as e:
        print(f"Error saving graph: {e}")
        sys.exit(1)

    # 5. Print Statistics
    print("\n--- Knowledge Graph Statistics ---")
    print(f"Total Nodes: {G.number_of_nodes()}")
    print(f"Total Edges: {G.number_of_edges()}")
    
    # Count by type
    jobs = len([n for n, d in G.nodes(data=True) if d.get('type') == 'job_role'])
    subjects = len([n for n, d in G.nodes(data=True) if d.get('type') == 'subject'])
    skills = len([n for n, d in G.nodes(data=True) if d.get('type') == 'skill'])
    
    print(f"Job Role Nodes: {jobs}")
    print(f"Subject Nodes: {subjects}")
    print(f"Skill Nodes: {skills}")
    print("----------------------------------")

if __name__ == "__main__":
    main()
