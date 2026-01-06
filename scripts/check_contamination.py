import pandas as pd
import os
import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s\+\#]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    print("Checking Digital Marketer Contamination...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hybrid_csv = os.path.join(base_dir, "data", "raw", "job_dataset_hybrid.csv")
    raw_csv = os.path.join(base_dir, "data", "raw", "job_dataset.csv")
    input_csv = hybrid_csv if os.path.exists(hybrid_csv) else raw_csv
    
    df = pd.read_csv(input_csv)
    df = df.dropna(subset=['Title', 'Skills'])
    df['cleaned_skills'] = df['Skills'].apply(clean_text)
    
    # Filter for UI/UX titles
    dm_mask = df['Title'].str.contains('UI|UX|Designer', case=False, na=False)
    dm_df = df[dm_mask]
    
    tech_keywords = ['arduino', 'esp32', 'ros', 'robotics', 'microcontroller', 'embedded', 'c++', 'python']
    
    count = 0
    print(f"\nScanning {len(dm_df)} UI/UX rows for tech keywords...")
    for _, row in dm_df.iterrows():
        found_keywords = [k for k in tech_keywords if k in row['cleaned_skills']]
        if found_keywords:
            count += 1
            if count <= 5: # Print first 5
                print(f"  [Contaminated] {row['Title']}")
                print(f"    Keywords found: {found_keywords}")
                
    print(f"\nTotal Contaminated Rows Found: {count}")

if __name__ == "__main__":
    main()
