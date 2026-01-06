import pickle
import os
import numpy as np
import pandas as pd

def main():
    print("--- AI Brain Inspection ---")
    
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, "backend", "ml_engine")
    model_path = os.path.join(model_dir, "model.pkl")
    vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")

    # Load Artifacts
    try:
        with open(model_path, 'rb') as f:
            clf_calibrated = pickle.load(f) # This is CalibratedClassifierCV
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
            
        print("Model and Vectorizer Loaded.")
        
        # Extract the actual LinearSVC from the CalibratedClassifierCV
        # CalibratedClassifierCV.calibrated_classifiers_[0].base_estimator
        # But commonly we can just access the base_estimator if it was fit on all data, 
        # OR we pull it from the first fold.
        
        # Since we want to see what it "learned", looking at the base estimator inside is valid for inspection.
        base_model = clf_calibrated.calibrated_classifiers_[0].estimator
        
        feature_names = vectorizer.get_feature_names_out()
        classes = clf_calibrated.classes_
        
        print(f"Total Vocabulary Size: {len(feature_names)} words")
        print(f"Number of Classes: {len(classes)}")
        print("="*60)

        # Helper to print top keywords
        def print_top_features(role_name, n=10):
            try:
                # Find index of the role
                class_idx = np.where(classes == role_name)[0][0]
                
                # Get coefficients for this class
                # Mobile App Developer vs Rest (One-vs-Rest)
                coefs = base_model.coef_[class_idx]
                
                # Sort indices by coefficient value
                top_indices = np.argsort(coefs)[-n:][::-1]
                
                print(f"\nRole: {role_name.upper()}")
                print(f"{'KEYWORD':<20} | {'WEIGHT (The Math)':<15}")
                print("-" * 40)
                for idx in top_indices:
                    word = feature_names[idx]
                    weight = coefs[idx]
                    print(f"{word:<20} | {weight:.4f}")
                    
            except IndexError:
                print(f"Role '{role_name}' not found.")

        # Inspect specific roles
        print_top_features("Mobile App Developer")
        print_top_features("Network Engineer")
        print_top_features("Project Manager")
        print_top_features("AI Engineer")
        
        print("\n" + "="*60)
        print("INTERPRETATION:")
        print("These numbers are the 'Brain Weights'.")
        print("A positive number means the word PULLS the prediction towards that role.")
        print("This proves it is doing MATH (Dot Product), not matching IF statements.")

    except Exception as e:
        print(f"Error inspecting model: {e}")

if __name__ == "__main__":
    main()
