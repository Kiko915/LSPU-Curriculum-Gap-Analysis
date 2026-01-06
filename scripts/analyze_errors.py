import pandas as pd
import pickle
import os
import re
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# --- ALLOWED CLASSES (Must Match Training) ---
ALLOWED_CLASSES = {
    "AI Engineer", "Content Specialist", "Cybersecurity Engineer", "Data Analyst", 
    "Data Engineer", "DevOps Engineer", "Digital Marketer", "Mobile App Developer", 
    "Project Manager", "QA Engineer", "Robotics Engineer", "Sales Executive", 
    "Software Engineer", "UI/UX Designer", "Web Developer", 
    "Game Developer", "Network Engineer", "Cloud Architect", "Business Analyst", "Vibe Coder"
}

def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s\+\#]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    print("Analyzing Misclassifications...")
    
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Load raw data again to see what's happening
    hybrid_csv = os.path.join(base_dir, "data", "raw", "job_dataset_hybrid.csv")
    raw_csv = os.path.join(base_dir, "data", "raw", "job_dataset.csv")
    input_csv = hybrid_csv if os.path.exists(hybrid_csv) else raw_csv
    
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

    # Load and Prep Data (Simplified for analysis - focusing on the Problematic Classes)
    df = pd.read_csv(input_csv)
    df = df.dropna(subset=['Title', 'Skills'])
    df['cleaned_skills'] = df['Skills'].apply(clean_text)
    
    # Only keep relevant columns
    df = df[['Title', 'Skills', 'cleaned_skills']]
    
    # --- SIMULATE PREDICTING ON THE RAW DATA (To see where it fails naturally) ---
    # We want to see how the model handles the *original* labels vs what it predicts
    # Note: We can't strictly trust original labels, but let's look at specific classes.
    
    target_classes = ['Sales Executive', 'Software Engineer']
    
    # Filter for rows that likely belong to these classes based on string match in Title
    # This is a heuristic to finding "ground truth" errors
    
    print("\n--- Detailed Error Analysis ---")
    
    for target_role in target_classes:
        print(f"\nAnalyzing '{target_role}' rows (from original Title)...")
        # Find rows where Title contains the role name
        mask = df['Title'].str.contains(target_role, case=False, na=False)
        subset = df[mask].sample(n=min(100, mask.sum()), random_state=42) # Take 100 samples
        
        if len(subset) == 0:
            print("  No samples found.")
            continue
            
        X_sub = vectorizer.transform(subset['cleaned_skills'])
        y_pred_idx = model.predict(X_sub)
        y_pred_label = le.inverse_transform(y_pred_idx)
        
        subset['Predicted'] = y_pred_label
        
        # Calculate accuracy for this subset
        # We assume the Title IS the truth for this analysis
        correct = subset[subset['Predicted'] == target_role]
        accuracy = len(correct) / len(subset)
        print(f"  Heuristic Accuracy: {accuracy*100:.2f}%")
        
        # Show top confusions
        confusions = subset[subset['Predicted'] != target_role]['Predicted'].value_counts().head(5)
        print("  Top Confusions:")
        print(confusions)

if __name__ == "__main__":
    main()
