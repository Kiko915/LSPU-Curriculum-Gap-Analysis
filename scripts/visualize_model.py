import pandas as pd
import pickle
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils import resample

# --- COPIED LOGIC FROM TRAIN_MODEL.PY STARTS ---
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def purify_role(row):
    skills = str(row['Skills']).lower()
    title = str(row['Title'])
    if re.search(r'\brobotics\b|\bros\b|\barduino\b|\braspberry pi\b', skills):
        return "Robotics Engineer"
    if re.search(r'\bsecurity\b|\bethical hack|\bpen\w*test|\bcissp\b|\bcyber', skills):
        return "Cybersecurity Engineer"
    if re.search(r'machine learning|tensorflow|pytorch|deep learning|neural network|computer vision|nlp', skills):
        return "AI Engineer"
    if re.search(r'\bfigma\b|\bphotoshop\b|\billustrator\b|\bindesign\b|\bui/ux\b|\buser experience\b', skills):
        return "UI/UX Designer" 
    if re.search(r'\b(react|angular|vue|node|django|laravel|php)\b', skills): 
        return "Web Developer"
    if re.search(r'\b(html|css)\b', skills) and "design" not in title.lower():
         return "Web Developer"
    if re.search(r'\btesting\b|\bselenium\b|\bjunit\b|\bcypress\b|\bqa\b', skills):
        return "QA Engineer"
    if re.search(r'data analysis|statistics|visualization|tableau|power bi', skills):
         return "Data Analyst"
    if re.search(r'project management|product management|scrum|agile|kanban|jira|roadmap|stakeholder', skills):
        return "Project Manager"
    return title

def normalize_role(role):
    if not isinstance(role, str):
        return "Unknown"
    role = role.lower().strip()
    if re.search(r'robot', role):
        return "Robotics Engineer"
    if re.search(r'security|cyber|hacker', role):
        return "Cybersecurity Engineer"
    if re.search(r'cloud|devops|sre|reliability', role):
        return "DevOps Engineer"
    if re.search(r'data scientist', role):
        return "Data Scientist"
    if re.search(r'machine learning|ml engineer|ai engineer|deep learning|nlp', role):
        return "AI Engineer"
    if re.search(r'data engineer|big data|spark|hadoop', role):
        return "Data Engineer"
    if re.search(r'data analyst|business analyst|bi analyst', role):
        return "Data Analyst"
    if re.search(r'web developer|frontend|front end|backend|back end|full stack|react|angular|node|php|wordpress', role):
        return "Web Developer"
    if re.search(r'mobile|android|ios|flutter|native', role):
        return "Mobile App Developer"
    if re.search(r'game developer|unity|unreal', role):
        return "Game Developer"
    if re.search(r'qa|quality assurance|tester|testing|sdet', role):
        return "QA Engineer"
    if re.search(r'ui|ux|interaction|product design', role):
        return "UI/UX Designer"
    if re.search(r'graphic|visual|art|illustrator', role):
        return "UI/UX Designer" 
    if re.search(r'animator|video|multimedia', role):
        return "Multimedia Artist"
    if re.search(r'technical writer', role):
        return "Technical Writer"
    if re.search(r'content|copywriter|writer|editor', role):
        return "Content Specialist" 
    if re.search(r'marketing|seo|social media|digital', role):
        return "Digital Marketer"
    if re.search(r'sales|business dev|account manager', role):
        return "Sales Executive"
    if re.search(r'project manager|program manager|scrum', role):
        return "Project Manager"
    if re.search(r'product manager|product owner', role):
        return "Product Manager"
    if re.search(r'operations|admin|hr|human resources', role):
        return "Operations Manager"
    if re.search(r'software|java|python|c\+\+|developer|engineer|programmer|architect', role):
        return "Software Engineer"
    return role.title()
# --- COPIED LOGIC ENDS ---

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_csv = os.path.join(base_dir, "data", "raw", "job_dataset.csv")
    model_dir = os.path.join(base_dir, "backend", "ml_engine")
    model_path = os.path.join(model_dir, "model.pkl")
    vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")

    # 1. Load Data
    print("Loading data...")
    df = pd.read_csv(input_csv)
    df = df.dropna(subset=['Title', 'Skills'])
    df['cleaned_skills'] = df['Skills'].apply(clean_text)
    df = df[df['cleaned_skills'].str.len() > 0]
    
    # 2. Process
    df['purified_role'] = df.apply(purify_role, axis=1)
    df['normalized_role'] = df['purified_role'].apply(normalize_role)
    
    # 3. Filter Rare
    min_samples = 15
    class_counts = df['normalized_role'].value_counts()
    valid_classes = class_counts[class_counts >= min_samples].index
    df = df[df['normalized_role'].isin(valid_classes)].copy()
    
    # 4. Perfect Balance (To match training distribution)
    TARGET_SIZE = 50
    balanced_df = pd.DataFrame()
    for role, group in df.groupby('normalized_role'):
        if len(group) == TARGET_SIZE:
             balanced_df = pd.concat([balanced_df, group])
        elif len(group) > TARGET_SIZE:
            sampled_group = resample(group, replace=False, n_samples=TARGET_SIZE, random_state=42)
            balanced_df = pd.concat([balanced_df, sampled_group])
        else:
            sampled_group = resample(group, replace=True, n_samples=TARGET_SIZE, random_state=42)
            balanced_df = pd.concat([balanced_df, sampled_group])
    df = balanced_df.reset_index(drop=True)
    
    # 5. Load Model
    print("Loading model...")
    with open(model_path, 'rb') as f:
        clf = pickle.load(f)
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
        
    # 6. Transform & Predict
    print("Predicting...")
    X = vectorizer.transform(df['cleaned_skills'])
    y_true = df['normalized_role']
    y_pred = clf.predict(X)
    
    # 7. Generate Metrics
    print("\nClassification Report:\n")
    report = classification_report(y_true, y_pred)
    print(report)
    
    with open(os.path.join(model_dir, "classification_report.txt"), "w") as f:
        f.write(report)
        
    print("Generating Confusion Matrix...")
    cm = confusion_matrix(y_true, y_pred, labels=clf.classes_)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=clf.classes_, yticklabels=clf.classes_)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(model_dir, "confusion_matrix.png"))
    print(f"Confusion Matrix saved to {os.path.join(model_dir, 'confusion_matrix.png')}")

if __name__ == "__main__":
    main()
