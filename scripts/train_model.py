import pandas as pd
import pickle
import os
import re
import numpy as np

# ML Imports (The Committee)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import RandomOverSampler

# --- ALLOWED CLASSES (The "Bouncer") ---
ALLOWED_CLASSES = {
    "AI Engineer", "Cybersecurity Engineer", "Data Analyst", 
    "Data Engineer", "DevOps Engineer", "Mobile App Developer", 
    "Project Manager", "QA Engineer", "Robotics Engineer", 
    "Software Engineer", "UI/UX Designer", "Web Developer", 
    "Game Developer", "Network Engineer", "Cloud Architect", "Business Analyst", "Vibe Coder", "Content Specialist"
}

def clean_text(text):
    """
    Cleans the input text by:
    1. Lowercasing.
    2. Removing special characters (keeping alphanumeric and spaces).
    3. Stripping extra whitespace.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s\+\#]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def purify_role(row):
    """
    Forces the role label based on specific skills found in the 'Skills' column.
    """
    skills = str(row['Skills']).lower()
    title = str(row['Title'])
    
    # Priority 1: Highly Specialized / Hardware
    if re.search(r'\brobotics\b|\bros\b|\barduino\b|\braspberry pi\b|\bembedded\b', skills):
        return "Robotics Engineer"
        
    # Priority 1.1: Game Development
    if re.search(r'unity|unreal|godot|game design|3d model|blender', skills):
        return "Game Developer"

    # Priority 1.2: Vibe Coder (The Chill Developer)
    if re.search(r'cursor|antigravity|windsurf|copilot', skills):
        return "Vibe Coder"

    # Priority 2: Security
    if re.search(r'\bsecurity\b|\bhack|\bpen\w*(\s)?test|\bcissp\b|\bcyber|\bkali\b', skills):
        return "Cybersecurity Engineer"
        
    # Priority 2.1: Network Engineering
    if re.search(r'cisco|ccna|tcp/ip|networking|network admin|troubleshooting|dumb switch', skills):
        return "Network Engineer"

    # Priority 3: AI / Data
    if re.search(r'machine learning|tensorflow|pytorch|deep learning|neural network|computer vision|nlp', skills):
        return "AI Engineer"
        
    # Priority 3.1: Mobile App Development
    if re.search(r'react native|flutter|android|ios|swift|kotlin|dart|mobile app', skills):
        return "Mobile App Developer"

    # Priority 4: Design
    if re.search(r'\bfigma\b|\bphotoshop\b|\billustrator\b|\bindesign\b|\bui/ux\b|\buser experience\b', skills):
        return "UI/UX Designer" 
        
    # Priority 5: Web
    if re.search(r'\b(react|angular|vue|node|django|laravel|php)\b', skills): 
        return "Web Developer"
    if re.search(r'\b(html|css)\b', skills) and "design" not in title.lower():
         return "Web Developer"

    # Priority 6: QA / Testing
    if re.search(r'\btesting\b|\bselenium\b|\bjunit\b|\bcypress\b|\bqa\b', skills):
        return "QA Engineer"

    # Priority 7: Data Analyst vs Scientist
    if re.search(r'data analysis|statistics|visualization|tableau', skills):
         return "Data Analyst"
         
    # Priority 7.1: Business Analyst
    if re.search(r'business analysis|requirements gathering|use case|visio|uml', skills):
        return "Business Analyst"

    # Priority 8: Management
    if re.search(r'project management|product management|scrum|agile|kanban|jira|roadmap|stakeholder', skills):
        return "Project Manager"

    return title

def normalize_role(role):
    """
    Standardizes job titles into a Comprehensive Role Taxonomy.
    """
    if not isinstance(role, str):
        return "Unknown"
    
    role = role.lower().strip()
    
    # --- 1. Specialized Tech Roles ---
    if re.search(r'robot|embedded', role): return "Robotics Engineer" # Captured embedded
    if re.search(r'security|cyber|hacker', role): return "Cybersecurity Engineer"
    if re.search(r'cloud|devops|sre|reliability', role): return "DevOps Engineer"
    if re.search(r'network|cisco|system admin|sysadmin', role): return "Network Engineer"
    if re.search(r'game developer|unity|unreal|game design', role): return "Game Developer"
    if re.search(r'gemini|cursor|antigravity|windsurf|copilot', role): return "Vibe Coder"

    # --- 2. AI & Data ---
    if re.search(r'data scientist', role): return "Data Scientist"
    if re.search(r'machine learning|ml engineer|ai engineer|deep learning|nlp', role): return "AI Engineer"
    if re.search(r'data engineer|big data|spark|hadoop', role): return "Data Engineer"
    if re.search(r'business analyst|bi analyst', role): return "Business Analyst"
    if re.search(r'data analyst', role): return "Data Analyst" # Only map pure Data Analyst here
    if re.search(r'architect', role): return "Cloud Architect"

    # --- 3. Software Development ---
    if re.search(r'web developer|frontend|front end|backend|back end|full stack|react|angular|node|php|wordpress', role): return "Web Developer"
    if re.search(r'mobile|android|ios|flutter|native', role): return "Mobile App Developer"
    if re.search(r'qa|quality assurance|tester|testing|sdet', role): return "QA Engineer"

    # --- 4. Design & Creative ---
    if re.search(r'ui|ux|interaction|product design', role): return "UI/UX Designer"
    if re.search(r'graphic|visual|art|illustrator', role): return "UI/UX Designer"

    # --- 5. Content & Marketing ---
    if re.search(r'content|copywriter|writer|editor', role): return "Content Specialist" 
    if re.search(r'marketing|seo|social media|digital', role): return "Digital Marketer"

    # --- 6. Management ---
    if re.search(r'project manager|program manager|scrum', role): return "Project Manager"
    if re.search(r'product manager|product owner', role): return "Product Manager"
    
    # Precise Software Engineer Capture
    # Differentiate from Web Developer
    if re.search(r'software engineer|software developer|application developer', role): 
        return "Software Engineer"
    
    # --- 7. Generic Fallback ---
    # --- 7. Generic Fallback ---
    # Catch-all for generic "Software Engineer" valid titles
    if re.search(r'software|java|python|c\+\+|developer|engineer|programmer', role):
        return "Software Engineer"
        
    return role.title()

def main():
    print("\n--- Starting Advanced Model Training (Ensemble Mode) ---")

    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Use Hybrid Dataset if available, otherwise fallback to raw
    hybrid_csv = os.path.join(base_dir, "data", "raw", "job_dataset_hybrid.csv")
    raw_csv = os.path.join(base_dir, "data", "raw", "job_dataset.csv")
    input_csv = hybrid_csv if os.path.exists(hybrid_csv) else raw_csv
    
    output_dir = os.path.join(base_dir, "backend", "ml_engine")
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, "model.pkl")
    vectorizer_path = os.path.join(output_dir, "vectorizer.pkl")
    label_encoder_path = os.path.join(output_dir, "label_encoder.pkl")

    print(f"Loading data from {input_csv}...")
    try:
        df = pd.read_csv(input_csv)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # 1. Preprocessing
    print("Cleaning data...")
    df = df.dropna(subset=['Title', 'Skills'])
    df['cleaned_skills'] = df['Skills'].apply(clean_text)
    df = df[df['cleaned_skills'].str.len() > 0]
    
    # 2. Purification & Normalization
    print("Standardizing Roles...")
    df['purified_role'] = df.apply(purify_role, axis=1)
    df['normalized_role'] = df['purified_role'].apply(normalize_role)
    
    # 2.5 Aggressive Cleaning: Remove Tech keywords from Non-Tech Roles
    # Prevents "Digital Marketer" or "Content Specialist" from absorbing tech keywords
    print("Purging Tech Keywords from Non-Tech Roles...")
    tech_keywords = ['arduino', 'esp32', 'ros ', 'robotics', 'microcontroller', 'embedded', 'c++', 'python', 'kali', 'hacking']
    non_tech_roles = ['Digital Marketer', 'Content Specialist', 'Business Analyst', 'Project Manager', 'Product Manager', 'UI/UX Designer']
    
    def is_contaminated(row):
        if row['normalized_role'] in non_tech_roles:
            for keyword in tech_keywords:
                if keyword in str(row['cleaned_skills']):
                    return True
        return False

    contaminated_mask = df.apply(is_contaminated, axis=1)
    n_contaminated = contaminated_mask.sum()
    df = df[~contaminated_mask]
    print(f"Removed {n_contaminated} contaminated rows from {non_tech_roles}.")
    
    # 3. Whitelist Filtering (The Bouncer)
    print("Applying Strict Whitelist...")
    initial_count = len(df)
    df = df[df['normalized_role'].isin(ALLOWED_CLASSES)].copy()
    dropped_count = initial_count - len(df)
    print(f"Dropped {dropped_count} rows (Irrelevant Roles).")
    print(f"Retained {len(df)} rows (Allowed Tech Roles).")

    # --- 3.1 Downsample Majority Classes (Anti-Bias & Memory Fix) ---
    MAX_SAMPLES = 3000
    print(f"Downsampling majority classes to {MAX_SAMPLES}...")
    df = df.groupby('normalized_role').apply(lambda x: x.sample(n=min(len(x), MAX_SAMPLES), random_state=42)).reset_index(drop=True)
    print(f"Dataset size after downsampling: {len(df)}")

    # 3.5.1 synthetic Injection (Robotics Engineer) - Fix for Arduino/ESP32
    # The hybrid dataset might have the role, but lacks specific hardware keywords in the skills column.
    robot_count = len(df[df['normalized_role'] == 'Robotics Engineer'])
    print(f"Existing Robotics Engineer samples: {robot_count}")
    
    # Always inject some high-quality hardware samples to ensure signal
    print(f"Injecting Synthetic 'Hardware/Robotics' Data...")
    synthetic_robot = []
    # Inject 2000 strong samples (Enough if Sales Exec is capped at 3000)
    for _ in range(2000):
        synthetic_robot.append({
            'Title': 'Robotics Engineer',
            'Skills': 'arduino esp32 raspberry pi ros embedded systems microcontroller robotics pcb sensors actuators',
            'cleaned_skills': 'arduino esp32 raspberry pi ros embedded systems microcontroller robotics pcb sensors actuators',
            'purified_role': 'Robotics Engineer',
            'normalized_role': 'Robotics Engineer'
        })
    df = pd.concat([df, pd.DataFrame(synthetic_robot)], ignore_index=True)
    print(f"Added {len(synthetic_robot)} synthetic Robotics Engineer samples.")

    # 3.5.3 Synthetic Injection (Software Engineer) - The Empire Strikes Back
    print(f"Injecting Synthetic 'Software Engineer' Data...")
    synthetic_se = []
    # Inject 2000 strong samples
    for _ in range(2000):
        synthetic_se.append({
            'Title': 'Software Engineer',
            'Skills': 'java c++ python software engineering oop object oriented programming algorithms data structures system design backend',
            'cleaned_skills': 'java c++ python software engineering oop object oriented programming algorithms data structures system design backend',
            'purified_role': 'Software Engineer',
            'normalized_role': 'Software Engineer'
        })
    df = pd.concat([df, pd.DataFrame(synthetic_se)], ignore_index=True)
    print(f"Added {len(synthetic_se)} synthetic Software Engineer samples.")

    # 3.5.2 Synthetic Injection (Cybersecurity) - Fix for 'hacking', 'kali'
    print(f"Injecting Synthetic 'Cybersecurity' Data...")
    synthetic_cyber = []
    # Inject 2000 strong samples
    for _ in range(2000):
        synthetic_cyber.append({
            'Title': 'Cybersecurity Engineer',
            'Skills': 'kali linux hacking penetration testing wireshark metasploit nmap ethical hacking security cyber defense network security',
            'cleaned_skills': 'kali linux hacking penetration testing wireshark metasploit nmap ethical hacking security cyber defense network security',
            'purified_role': 'Cybersecurity Engineer',
            'normalized_role': 'Cybersecurity Engineer'
        })
    df = pd.concat([df, pd.DataFrame(synthetic_cyber)], ignore_index=True)
    print(f"Added {len(synthetic_cyber)} synthetic Cybersecurity Engineer samples.")

    # 3.5.4 Synthetic Injection (Project Manager) - Fix for management skill confusion
    print(f"Injecting Synthetic 'Project Manager' Data...")
    synthetic_pm = []
    for _ in range(1500):
        synthetic_pm.append({
            'Title': 'Project Manager',
            'Skills': 'project management leadership communication stakeholder agile scrum kanban roadmap planning coordination team management',
            'cleaned_skills': 'project management leadership communication stakeholder agile scrum kanban roadmap planning coordination team management',
            'purified_role': 'Project Manager',
            'normalized_role': 'Project Manager'
        })
    df = pd.concat([df, pd.DataFrame(synthetic_pm)], ignore_index=True)
    print(f"Added {len(synthetic_pm)} synthetic Project Manager samples.")

    # 3.5.5 Synthetic Injection (Vibe Coder) - AI-assisted coding
    print(f"Injecting Synthetic 'Vibe Coder' Data...")
    synthetic_vc = []
    for _ in range(1500):
        synthetic_vc.append({
            'Title': 'Vibe Coder',
            'Skills': 'cursor vibe coding ai-assisted programming copilot windsurf antigravity gemini claude chatgpt prompt engineering ai tools',
            'cleaned_skills': 'cursor vibe coding ai assisted programming copilot windsurf antigravity gemini claude chatgpt prompt engineering ai tools',
            'purified_role': 'Vibe Coder',
            'normalized_role': 'Vibe Coder'
        })
    df = pd.concat([df, pd.DataFrame(synthetic_vc)], ignore_index=True)
    print(f"Added {len(synthetic_vc)} synthetic Vibe Coder samples.")

    # 3.5.6 Synthetic Injection (Content Specialist) - Writers
    print(f"Injecting Synthetic 'Content Specialist' Data...")
    synthetic_cs = []
    for _ in range(1500):
        synthetic_cs.append({
            'Title': 'Content Specialist',
            'Skills': 'content writing copywriting editor blog writing seo content marketing technical writing creative writing proofreading',
            'cleaned_skills': 'content writing copywriting editor blog writing seo content marketing technical writing creative writing proofreading',
            'purified_role': 'Content Specialist',
            'normalized_role': 'Content Specialist'
        })
    df = pd.concat([df, pd.DataFrame(synthetic_cs)], ignore_index=True)
    print(f"Added {len(synthetic_cs)} synthetic Content Specialist samples.")

    # Validation: Check Robotics Engineer Count
    final_robot_count = len(df[df['normalized_role'] == 'Robotics Engineer'])
    print(f"FINAL ROBOTICS ENGINEER COUNT: {final_robot_count}")
    
    # Validation: Check Sales Executive Count
    sales_count = len(df[df['normalized_role'] == 'Sales Executive'])
    print(f"FINAL SALES EXECUTIVE COUNT: {sales_count}")

    # Debug: Print Class Distribution
    print("\n--- Class Distribution (Top 20) ---")
    print(df['normalized_role'].value_counts().head(20))
    print("-----------------------------------\n")

    # 3.6 Label Encoding (String -> Int) - CRITICAL FOR XGBOOST
    print("Encoding Labels (String -> Int)...")
    le = LabelEncoder()
    df['label_encoded'] = le.fit_transform(df['normalized_role'])
    
    # 4. Vectorization (N-Grams 1,2)
    # Increased max_features to 12000 to capture more vocabulary in the larger dataset
    print("Vectorizing skills (N-Grams 1-2, Max Features=12000)...")
    # Custom token pattern to keep c++, c#
    vectorizer = TfidfVectorizer(
        max_features=12000, 
        stop_words='english', 
        ngram_range=(1, 2),
        token_pattern=r'(?u)\b\w[\w\+\#]*\b' 
    )
    X = vectorizer.fit_transform(df['cleaned_skills'])
    y = df['label_encoded'] # Use encoded labels

    # Debug: Check if C++ and Arduino are in vocab
    print(f"Vocab check 'c++': {'c++' in vectorizer.vocabulary_}")
    print(f"Vocab check 'c#': {'c#' in vectorizer.vocabulary_}")
    print(f"Vocab check 'arduino': {'arduino' in vectorizer.vocabulary_}")
    print(f"Vocab check 'esp32': {'esp32' in vectorizer.vocabulary_}")

    # 5. Split (CRITICAL: Split BEFORE balancing to create valid test set)
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )

    # 6. Balancing (RandomOverSampler)
    print("Applying RandomOverSampler (Balancing Training Data)...")
    sampler = RandomOverSampler(random_state=42)
    X_train_resampled, y_train_resampled = sampler.fit_resample(X_train, y_train)

    # 6.5 Sample Weighting (Crucial allow Robotics to overpower Sales Exec noise)
    print("Computing Sample Weights...")
    
    # Get the integer labels for interest classes
    robotics_label = le.transform(['Robotics Engineer'])[0]
    cyber_label = le.transform(['Cybersecurity Engineer'])[0]
    
    sample_weights = np.ones(len(y_train_resampled))
    for i, label in enumerate(y_train_resampled):
        if label == robotics_label:
            sample_weights[i] = 25.0 # Force Robotics (25) - Balanced
        elif label == cyber_label:
            sample_weights[i] = 5.0 # Reduce Cyber weight (was 8)
            
    print("Weights computed.")

    # 7. Training The Committee (Ensemble)
    print("Training Enhanced Ensemble Model (SVM + LR + XGBoost)...")

    # Estimator 1: Linear SVC (Calibrated) - The Margin Master
    svc = LinearSVC(class_weight='balanced', random_state=42, max_iter=10000, dual=False)
    clf_svc = CalibratedClassifierCV(svc) 

    # Estimator 2: Logistic Regression - The Probability Pro
    clf_lr = LogisticRegression(solver='liblinear', random_state=42, max_iter=1000, C=1.5)

    # Estimator 3: XGBoost - The Gradient Boosting Champion
    clf_xgb = XGBClassifier(
        n_estimators=200, 
        learning_rate=0.1,
        max_depth=6,
        random_state=42, 
        n_jobs=-1,
        use_label_encoder=False,
        eval_metric='mlogloss'
    )
    
    # The Ensemble
    ensemble = VotingClassifier(
        estimators=[
            ('svc', clf_svc), 
            ('lr', clf_lr),
            ('xgb', clf_xgb)
        ],
        voting='soft',
        weights=[1, 2, 2] # Adjusted weights: LR proved more sensitive to Robotics
    )
    
    # All inputs to fit are now properly prepared (X is float, y is int)
    ensemble.fit(X_train_resampled, y_train_resampled, sample_weight=sample_weights)

    # 8. Evaluate
    y_pred = ensemble.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n***************************************")
    print(f"XGBoost Ensemble Accuracy: {accuracy * 100:.2f}%")
    print(f"***************************************\n")
    
    print("Classes in model (Encoded):", ensemble.classes_)
    print("Mapping:", dict(zip(le.transform(le.classes_), le.classes_)))

    # Save Everything
    print("Saving artifacts...")
    with open(model_path, 'wb') as f:
        pickle.dump(ensemble, f)
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    with open(label_encoder_path, 'wb') as f:
        pickle.dump(le, f)
        
    print("Model Saved.")

if __name__ == "__main__":
    main()
