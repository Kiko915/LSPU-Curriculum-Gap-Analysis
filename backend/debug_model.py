
import sys
import os
import numpy as np

# Add ml_engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_engine'))

from ml_engine.predictor import MLPredictor

def inspect_model():
    print("Loading Predictor...")
    try:
        p = MLPredictor()
    except Exception as e:
        print(f"Error loading predictor: {e}")
        return

    # Check Vocabulary
    vocab = p.vectorizer.vocabulary_
    print(f"\nVocabulary Size: {len(vocab)}")
    
    keywords = ['tensorflow', 'pytorch', 'keras', 'scikit', 'learn', 'sklearn', 'python', 'ai', 'cybersecurity']
    print("\nKeyword Check in Vocabulary:")
    for k in keywords:
        print(f"  '{k}': {'FOUND (' + str(vocab[k]) + ')' if k in vocab else 'MISSING'}")

    # Inspect features for a prediction
    test_input = ['Python', 'Frameworks: TensorFlow, PyTorch, Keras, Scikit-learn (advanced)', 'React']
    print(f"\nAnalyzing prediction for: {test_input}")
    
    # Manually reproduce steps
    combined_text = " ".join([str(s) for s in test_input])
    cleaned_text = p.clean_text(combined_text)
    print(f"Cleaned Text: '{cleaned_text}'")
    
    vec = p.vectorizer.transform([cleaned_text])
    print(f"Vector Non-Zero Count: {vec.nnz}")
    
    # Get prediction
    pred_idx = p.model.predict(vec)[0]
    pred_role = p.label_encoder.inverse_transform([pred_idx])[0]
    probs = p.model.predict_proba(vec)[0]
    
    print(f"Predicted Role: {pred_role}")
    print(f"Confidence: {np.max(probs):.4f}")
    
    # Top 3 predictions
    top_3_idx = np.argsort(probs)[-3:][::-1]
    print("\nTop 3 Probabilities:")
    classes = p.label_encoder.classes_
    for idx in top_3_idx:
        print(f"  {classes[idx]}: {probs[idx]:.4f}")

if __name__ == "__main__":
    inspect_model()
