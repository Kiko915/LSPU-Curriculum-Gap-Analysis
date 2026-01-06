import pickle
import os
import numpy as np
import pandas as pd

def load_artifact(filename):
    path = os.path.join("backend", "ml_engine", filename)
    with open(path, 'rb') as f:
        return pickle.load(f)

def main():
    print("Loading artifacts...")
    try:
        model = load_artifact("model.pkl")
        vectorizer = load_artifact("vectorizer.pkl")
        label_encoder = load_artifact("label_encoder.pkl")
        print("Artifacts loaded.")
    except Exception as e:
        print(f"Error loading artifacts: {e}")
        return

    # 1. Check Vocabulary
    vocab = vectorizer.vocabulary_
    terms = ['arduino', 'esp32', 'microcontroller', 'robotics']
    print("\n--- Vocabulary Check ---")
    for term in terms:
        if term in vocab:
            print(f"'{term}': index {vocab[term]}")
        else:
            print(f"'{term}': NOT IN VOCABULARY")

    # 2. Check Input Transformation
    input_text = "arduino esp32 microcontroller"
    vec_input = vectorizer.transform([input_text])
    print(f"\nInput: '{input_text}'")
    print(f"Vector shape: {vec_input.shape}")
    print(f"Non-zero elements: {vec_input.nnz}")
    print(f"Vector data: {vec_input.data}")
    print(f"Vector indices: {vec_input.indices}")

    # 3. Check Individual Estimators
    print("\n--- Ensemble Breakdown ---")
    if hasattr(model, 'estimators_'):
        estimators = model.estimators_
        print(f"Number of estimators: {len(estimators)}")
        
        for name, clf in model.named_estimators_.items():
            print(f"\nEstimator: {name} ({type(clf).__name__})")
            try:
                # Predict
                pred = clf.predict(vec_input)[0]
                pred_label = label_encoder.inverse_transform([pred])[0]
                
                # Proba
                if hasattr(clf, 'predict_proba'):
                    proba = clf.predict_proba(vec_input)[0]
                    max_prob = np.max(proba)
                    print(f"  Prediction: {pred_label} (Confidence: {max_prob:.4f})")
                    
                    # Top 3 classes
                    top3_idx = np.argsort(proba)[-3:][::-1]
                    for idx in top3_idx:
                        class_name = label_encoder.inverse_transform([idx])[0]
                        print(f"    - {class_name}: {proba[idx]:.4f}")
                else:
                    print(f"  Prediction: {pred_label}")
            except Exception as e:
                print(f"  Error inspecting {name}: {e}")

    # 4. Check Final Prediction
    print("\n--- Final Ensemble Prediction ---")
    final_pred_idx = model.predict(vec_input)[0]
    final_role = label_encoder.inverse_transform([final_pred_idx])[0]
    final_proba = model.predict_proba(vec_input)[0] if hasattr(model, 'predict_proba') else []
    
    print(f"Final Role: {final_role}")
    
    # Check specifically for Robotics Engineer
    if "Robotics Engineer" in label_encoder.classes_:
        robo_idx = list(label_encoder.classes_).index("Robotics Engineer")
        if hasattr(model, 'predict_proba'):
            robo_prob = model.predict_proba(vec_input)[0][robo_idx]
            print(f"Robotics Engineer Probability: {robo_prob:.6f}")
    else:
        print("CRITICAL: 'Robotics Engineer' is NOT in the label encoder classes!")

    if len(final_proba) > 0:

        print(f"Final Confidence: {np.max(final_proba):.4f}")
        # Top 5
        top5 = np.argsort(final_proba)[-5:][::-1]
        for idx in top5:
            print(f"  {label_encoder.inverse_transform([idx])[0]}: {final_proba[idx]:.4f}")

if __name__ == "__main__":
    main()
