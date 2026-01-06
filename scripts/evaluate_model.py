import pandas as pd
import pickle
import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# --- ALLOWED CLASSES ---
ALLOWED_CLASSES = {
    "AI Engineer", "Cybersecurity Engineer", "Data Analyst", 
    "Data Engineer", "DevOps Engineer", "Mobile App Developer", 
    "Project Manager", "QA Engineer", "Robotics Engineer", 
    "Software Engineer", "UI/UX Designer", "Web Developer", 
    "Game Developer", "Network Engineer", "Cloud Architect", "Business Analyst", "Vibe Coder"
}

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s\+\#]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def purify_role(row):
    skills = str(row['Skills']).lower()
    title = str(row['Title'])
    if re.search(r'\brobotics\b|\bros\b|\barduino\b|\braspberry pi\b|\bembedded\b', skills): return "Robotics Engineer"
    if re.search(r'unity|unreal|godot|game design|3d model|blender', skills): return "Game Developer"
    if re.search(r'cursor|antigravity|windsurf|copilot', skills): return "Vibe Coder"
    if re.search(r'\bsecurity\b|\bhack|\bpen\w*(\s)?test|\bcissp\b|\bcyber|\bkali\b', skills): return "Cybersecurity Engineer"
    if re.search(r'cisco|ccna|tcp/ip|networking|network admin|troubleshooting|dumb switch', skills): return "Network Engineer"
    if re.search(r'machine learning|tensorflow|pytorch|deep learning|neural network|computer vision|nlp', skills): return "AI Engineer"
    if re.search(r'react native|flutter|android|ios|swift|kotlin|dart|mobile app', skills): return "Mobile App Developer"
    if re.search(r'\bfigma\b|\bphotoshop\b|\billustrator\b|\bindesign\b|\bui/ux\b|\buser experience\b', skills): return "UI/UX Designer" 
    if re.search(r'\b(react|angular|vue|node|django|laravel|php)\b', skills): return "Web Developer"
    if re.search(r'\b(html|css)\b', skills) and "design" not in title.lower(): return "Web Developer"
    if re.search(r'\btesting\b|\bselenium\b|\bjunit\b|\bcypress\b|\bqa\b', skills): return "QA Engineer"
    if re.search(r'data analysis|statistics|visualization|tableau', skills): return "Data Analyst"
    if re.search(r'business analysis|requirements gathering|use case|visio|uml', skills): return "Business Analyst"
    if re.search(r'project management|product management|scrum|agile|kanban|jira|roadmap|stakeholder', skills): return "Project Manager"
    return title

def normalize_role(role):
    if not isinstance(role, str): return "Unknown"
    role = role.lower().strip()
    if re.search(r'robot|embedded', role): return "Robotics Engineer"
    if re.search(r'security|cyber|hacker', role): return "Cybersecurity Engineer"
    if re.search(r'cloud|devops|sre|reliability', role): return "DevOps Engineer"
    if re.search(r'network|cisco|system admin|sysadmin', role): return "Network Engineer"
    if re.search(r'game developer|unity|unreal|game design', role): return "Game Developer"
    if re.search(r'gemini|cursor|antigravity|windsurf|copilot', role): return "Vibe Coder"
    if re.search(r'data scientist', role): return "Data Scientist"
    if re.search(r'machine learning|ml engineer|ai engineer|deep learning|nlp', role): return "AI Engineer"
    if re.search(r'data engineer|big data|spark|hadoop', role): return "Data Engineer"
    if re.search(r'business analyst|bi analyst', role): return "Business Analyst"
    if re.search(r'data analyst', role): return "Data Analyst"
    if re.search(r'architect', role): return "Cloud Architect"
    if re.search(r'web developer|frontend|front end|backend|back end|full stack|react|angular|node|php|wordpress', role): return "Web Developer"
    if re.search(r'mobile|android|ios|flutter|native', role): return "Mobile App Developer"
    if re.search(r'qa|quality assurance|tester|testing|sdet', role): return "QA Engineer"
    if re.search(r'ui|ux|interaction|product design', role): return "UI/UX Designer"
    if re.search(r'graphic|visual|art|illustrator', role): return "UI/UX Designer"
    if re.search(r'content|copywriter|writer|editor', role): return "Content Specialist" 
    if re.search(r'marketing|seo|social media|digital', role): return "Digital Marketer"
    if re.search(r'project manager|program manager|scrum', role): return "Project Manager"
    if re.search(r'product manager|product owner', role): return "Product Manager"
    
    # Precise Software Engineer Capture
    # Differentiate from Web Developer
    if re.search(r'software engineer|software developer|application developer', role): 
        return "Software Engineer"
        
    if re.search(r'software|java|python|c\+\+|developer|engineer|programmer', role): return "Software Engineer"
    return role.title()

def main():
    print("Evaluating Model Accuracy...")
    
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hybrid_csv = os.path.join(base_dir, "data", "raw", "job_dataset_hybrid.csv")
    raw_csv = os.path.join(base_dir, "data", "raw", "job_dataset.csv")
    input_csv = hybrid_csv if os.path.exists(hybrid_csv) else raw_csv
    
    # Load Data
    try:
        df = pd.read_csv(input_csv)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    df = df.dropna(subset=['Title', 'Skills'])
    df['cleaned_skills'] = df['Skills'].apply(clean_text)
    df = df[df['cleaned_skills'].str.len() > 0]
    
    # Purify & Normalize
    df['purified_role'] = df.apply(purify_role, axis=1)
    df['normalized_role'] = df['purified_role'].apply(normalize_role)
    
    # Aggressive Cleaning (Non-Tech)
    tech_keywords = ['arduino', 'esp32', 'ros ', 'robotics', 'microcontroller', 'embedded', 'c++', 'python', 'kali', 'hacking']
    non_tech_roles = ['Digital Marketer', 'Content Specialist', 'Business Analyst', 'Project Manager', 'Product Manager', 'UI/UX Designer']
    
    def is_contaminated(row):
        if row['normalized_role'] in non_tech_roles:
            for keyword in tech_keywords:
                if keyword in str(row['cleaned_skills']):
                    return True
        return False
    df = df[~df.apply(is_contaminated, axis=1)]
    
    # Whitelist
    df = df[df['normalized_role'].isin(ALLOWED_CLASSES)].copy()
    
    # Downsample
    MAX_SAMPLES = 3000
    df = df.groupby('normalized_role').apply(lambda x: x.sample(n=min(len(x), MAX_SAMPLES), random_state=42)).reset_index(drop=True)
    
    # Inject Synthetic (MUST MATCH TRAINING)
    synthetic_robot = []
    for _ in range(2000):
        synthetic_robot.append({
            'Title': 'Robotics Engineer',
            'Skills': 'arduino esp32 raspberry pi ros embedded systems microcontroller robotics pcb sensors actuators',
            'cleaned_skills': 'arduino esp32 raspberry pi ros embedded systems microcontroller robotics pcb sensors actuators',
            'purified_role': 'Robotics Engineer',
            'normalized_role': 'Robotics Engineer'
        })
    df = pd.concat([df, pd.DataFrame(synthetic_robot)], ignore_index=True)

    # Synthetic SE
    synthetic_se = []
    for _ in range(2000):
        synthetic_se.append({
            'Title': 'Software Engineer',
            'Skills': 'java c++ python software engineering oop object oriented programming algorithms data structures system design backend',
            'cleaned_skills': 'java c++ python software engineering oop object oriented programming algorithms data structures system design backend',
            'purified_role': 'Software Engineer',
            'normalized_role': 'Software Engineer'
        })
    df = pd.concat([df, pd.DataFrame(synthetic_se)], ignore_index=True)
    
    # Load Model Artifacts
    model_path = os.path.join(base_dir, "backend", "ml_engine", "model.pkl")
    vectorizer_path = os.path.join(base_dir, "backend", "ml_engine", "vectorizer.pkl")
    encoder_path = os.path.join(base_dir, "backend", "ml_engine", "label_encoder.pkl")
    
    try:
        with open(model_path, 'rb') as f: model = pickle.load(f)
        with open(vectorizer_path, 'rb') as f: vectorizer = pickle.load(f)
        with open(encoder_path, 'rb') as f: le = pickle.load(f)
    except Exception as e:
        print(f"Error loading artifacts: {e}")
        return
    
    # Prepare X, y
    X = vectorizer.transform(df['cleaned_skills']) # Transform only, don't fit
    y = le.transform(df['normalized_role'])
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )
    
    # Predict
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    # Save report
    report_path = os.path.join(base_dir, "backend", "ml_engine", "classification_report.txt")
    with open(report_path, "w") as f:
        f.write(f"Accuracy: {accuracy * 100:.2f}%\n\n")
        f.write(classification_report(y_test, y_pred, target_names=le.classes_))
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    main()
