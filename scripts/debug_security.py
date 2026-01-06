import pickle
import os
import numpy as np

def main():
    base_dir = os.path.join("backend", "ml_engine")
    with open(os.path.join(base_dir, "vectorizer.pkl"), 'rb') as f:
        vectorizer = pickle.load(f)
    with open(os.path.join(base_dir, "model.pkl"), 'rb') as f:
        model = pickle.load(f)
    with open(os.path.join(base_dir, "label_encoder.pkl"), 'rb') as f:
        le = pickle.load(f)

    vocab = vectorizer.vocabulary_
    terms = ['kali', 'linux', 'hacking', 'penetration', 'pen', 'security']
    
    print("--- Vocabulary Check ---")
    for term in terms:
        if term in vocab:
            print(f"'{term}': index {vocab[term]}")
        else:
            print(f"'{term}': NOT IN VOCABULARY")
            
    input_text = "kali linux hacking penetration"
    vec = vectorizer.transform([input_text])
    
    print("\n--- Prediction Breakdown ---")
    probs = model.predict_proba(vec)[0]
    
    # Get Top 5
    top5_idx = np.argsort(probs)[-5:][::-1]
    for idx in top5_idx:
        role = le.inverse_transform([idx])[0]
        print(f"{role}: {probs[idx]:.4f}")

if __name__ == "__main__":
    main()
