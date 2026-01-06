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

    # Check Terms
    vocab = vectorizer.vocabulary_
    terms = ['arduino', 'esp32', 'microcontroller', 'robotics', 'design', 'ui', 'ux']
    print("--- Vocabulary Check ---")
    for term in terms:
        if term in vocab:
            print(f"'{term}': index {vocab[term]}")
        else:
            print(f"'{term}': NOT IN VOCABULARY")

    # Check Individual Predictions
    inputs = [
        "arduino",
        "esp32",
        "microcontroller",
        "arduino esp32 microcontroller"
    ]
    
    print("\n--- Feature Contributions ---")
    # This is rough, just checking raw probas
    for text in inputs:
        vec = vectorizer.transform([text])
        probs = model.predict_proba(vec)[0]
        top5_idx = np.argsort(probs)[-5:][::-1]
        
        print(f"\nInput: '{text}'")
        for idx in top5_idx:
            role = le.inverse_transform([idx])[0]
            print(f"  {role}: {probs[idx]:.4f}")

if __name__ == "__main__":
    main()
