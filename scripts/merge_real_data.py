import pandas as pd
import os
import re

def main():
    print("--- 🧬 Hybrid Dataset Factory ---")
    
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_data_path = os.path.join(base_dir, "data", "raw", "linkedin_job_listings.csv")
    synthetic_data_path = os.path.join(base_dir, "data", "raw", "job_dataset.csv")
    output_path = os.path.join(base_dir, "data", "raw", "job_dataset_hybrid.csv")
    
    # 1. Load Data
    if not os.path.exists(real_data_path):
        print(f"❌ Error: Real data not found at {real_data_path}")
        return
        
    print("Loading data...")
    try:
        # Optimization: Read only necessary columns
        # First read just the header to see what columns we have
        header = pd.read_csv(real_data_path, nrows=0)
        use_cols = ['title', 'description']
        if 'skills_desc' in header.columns:
            use_cols.append('skills_desc')
            
        print(f"Reading columns: {use_cols}")
        real_df = pd.read_csv(real_data_path, usecols=use_cols)
        syn_df = pd.read_csv(synthetic_data_path)
    except Exception as e:
        print(f"❌ Error loading csv: {e}")
        return
        
    print(f"Total Real Rows Loaded: {len(real_df)}")
    print(f"Total Synthetic Rows Loaded: {len(syn_df)}")
    
    # 2. Tech Keywords List
    # A comprehensive list to identify tech jobs and extract skills
    tech_keywords = [
        # Languages
        "python", "java", "c++", "c#", "javascript", "typescript", "ruby", "swift", "kotlin", "go", "rust", "php", "html", "css", "sql", "r", "matlab", "bash", "shell"
        # Frameworks/Libs
        "react", "angular", "vue", "node", "django", "flask", "spring", "laravel", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "spark", "hadoop", "flutter", "react native",
        # Tools/Infra
        "git", "docker", "kubernetes", "aws", "azure", "gcp", "linux", "jenkins", "jira", "tableau", "power bi", "excel", "figma", "photoshop", "illustrator",
        # Concepts
        "machine learning", "deep learning", "ai", "data analysis", "web development", "devops", "agile", "scrum", "cybersecurity", "networking", "database", "api", "rest", "graphql", "ui/ux", "robotics"
    ]
    
    # 3. Filter Real Data (Tech Jobs Only)
    # Filter titles containing keywords like Developer, Engineer, etc.
    job_titles_regex = r'developer|engineer|data|cloud|ai|cyber|analyst|system|admin|architect|programmer|technician|specialist|consultant|manager|robotics|embedded|networking|security|database|api|rest|graphql|ui/ux|android|ios|mobile|web|application'
    
    print("Filtering unrelated jobs...")
    
    # Ensure columns exist
    if 'title' not in real_df.columns:
        print("❌ Error: 'title' column missing in real data.")
        return
        
    # Standardize columns to lower for checking
    real_df['title_lower'] = real_df['title'].str.lower().fillna('')
    
    # Filter
    tech_df = real_df[real_df['title_lower'].str.contains(job_titles_regex, na=False)].copy()
    print(f"Tech Jobs Retained: {len(tech_df)}")
    
    # 4. Feature Engineering: Extract Skills from Description
    print("Extracting skills from descriptions...")
    
    # Combine description and skills_desc if available
    cols_to_combine = ['description']
    if 'skills_desc' in tech_df.columns:
        cols_to_combine.append('skills_desc')
        
    def extract_skills(row):
        text = ""
        for col in cols_to_combine:
            val = str(row.get(col, ""))
            text += " " + val
        
        text = text.lower()
        found_skills = []
        for keyword in tech_keywords:
            # Simple word matching, robust enough for this purpose
            # Use regex boundaries to avoid partial matches (e.g. 'c' in 'cat')
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text):
                found_skills.append(keyword) # Keep lowercase
        
        return ", ".join(found_skills)

    tech_df['Skills'] = tech_df.apply(extract_skills, axis=1)
    
    # 5. Drop empty skills
    tech_df = tech_df[tech_df['Skills'].str.len() > 0].copy()
    print(f"rows with detected skills: {len(tech_df)}")
    
    # 6. Standardize and Merge
    print("Merging datasets...")
    
    # Prepare real data
    tech_df['Title'] = tech_df['title'] # Capitalize T
    final_real_df = tech_df[['Title', 'Skills']].copy()
    
    # Prepare synthetic data
    final_syn_df = syn_df[['Title', 'Skills']].copy()
    
    # Concatenate
    hybrid_df = pd.concat([final_real_df, final_syn_df], ignore_index=True)
    
    # 7. Save
    hybrid_df.to_csv(output_path, index=False)
    
    print("-" * 30)
    print(f"Total Real Rows Loaded: {len(real_df)}")
    print(f"Tech Jobs Retained: {len(tech_df)}")
    print(f"Synthetic Rows Added: {len(syn_df)}")
    print(f"Final Hybrid Dataset Size: {len(hybrid_df)}")
    print(f"Saved to: {output_path}")
    print("-" * 30)

if __name__ == "__main__":
    main()
