import pickle
import os
import re
import numpy as np

class MLPredictor:
    def __init__(self, model_filename="model.pkl", vectorizer_filename="vectorizer.pkl", encoder_filename="label_encoder.pkl"):
        """
        Initializes the ML Predictor by loading the model, vectorizer, and label encoder.
        """
        # Determine absolute paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_dir, model_filename)
        self.vectorizer_path = os.path.join(base_dir, vectorizer_filename)
        self.encoder_path = os.path.join(base_dir, encoder_filename)
        
        self.model = self._load_artifact(self.model_path)
        self.vectorizer = self._load_artifact(self.vectorizer_path)
        self.label_encoder = self._load_artifact(self.encoder_path)

    def _load_artifact(self, path):
        """Helper to load pickles with error handling."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"ML Artifact not found at: {path}")
        
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            raise RuntimeError(f"Error loading artifact {path}: {e}")

    def clean_text(self, text):
        """
        Cleans input text: Lowercase, remove special chars, strip whitespace.
        MUST match the logic used in training.
        """
        if not isinstance(text, str):
            return ""
        text = text.lower()
        # Regex to keep only alphanumeric and spaces
        text = re.sub(r'[^a-zA-Z0-9\s\+\#]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def predict_role(self, skills_list):
        """
        Predicts the Job Role based on a list of skills.
        
        Args:
            skills_list (list): List of skill strings (e.g., ['Python', 'SQL']).
            
        Returns:
            tuple: (Predicted Role Name, Confidence Score 0.0-1.0)
        """
        if not skills_list:
            return None, 0.0
            
        # 1. Join list into a single string
        combined_text = " ".join([str(s) for s in skills_list])
        
        # 2. Clean
        cleaned_text = self.clean_text(combined_text)
        
        if not cleaned_text:
            return None, 0.0
            
        # 3. Vectorize (Transform only)
        try:
            vectorized_input = self.vectorizer.transform([cleaned_text])
        except Exception as e:
            print(f"Error during vectorization: {e}")
            return None, 0.0

        # 4. Predict
        try:
            # Get class prediction (Integer)
            predicted_index = self.model.predict(vectorized_input)[0]
            
            # Decode Integer -> String (Human Readable Role)
            predicted_role = self.label_encoder.inverse_transform([predicted_index])[0]
            
            # Get confidence probabilities
            probabilities = self.model.predict_proba(vectorized_input)[0]
            
            # Max probability is the confidence
            confidence = float(np.max(probabilities))
            
            return predicted_role, confidence
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None, 0.0

if __name__ == "__main__":
    print("--- Testing ML Predictor ---")
    
    try:
        predictor = MLPredictor()
        print("Predictor initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize: {e}")
        exit(1)
    
    # Dummy Data
    test_skills = ['Python', 'Data Analysis', 'Statistics', 'Machine Learning']
    print(f"\nInput: {test_skills}")
    
    role, conf = predictor.predict_role(test_skills)
    
    print(f"Predicted Role: {role}")
    print(f"Confidence: {conf * 100:.2f}%")
    
    # Another test
    test_skills_2 = ['Canva', 'Photoshop', 'Illustrator', 'UX Design']
    print(f"\nInput: {test_skills_2}")
    role2, conf2 = predictor.predict_role(test_skills_2)
    print(f"Predicted Role: {role2}")
    print(f"Confidence: {conf2 * 100:.2f}%")

    test_skills_3 = ['HTML', 'CSS', 'Javascript']
    print(f"\nInput: {test_skills_3}")
    role3, conf3 = predictor.predict_role(test_skills_3)
    print(f"Predicted Role: {role3}")
    print(f"Confidence: {conf3 * 100:.2f}%")

    test_skills_4 = ['Project Management', 'Leadership', 'Communication']
    print(f"\nInput: {test_skills_4}")
    role4, conf4 = predictor.predict_role(test_skills_4)
    print(f"Predicted Role: {role4}")
    print(f"Confidence: {conf4 * 100:.2f}%")

    test_skills_5 = ['cisco', 'rj45', 'fiber', 'switch', 'router']
    print(f"\nInput: {test_skills_5}")
    role5, conf5 = predictor.predict_role(test_skills_5)
    print(f"Predicted Role: {role5}")
    print(f"Confidence: {conf5 * 100:.2f}%")

    test_skills_6 = ['React Native', 'Flutter', 'Dart']
    print(f"\nInput: {test_skills_6}")
    role6, conf6 = predictor.predict_role(test_skills_6)
    print(f"Predicted Role: {role6}")
    print(f"Confidence: {conf6 * 100:.2f}%")

    test_skills_se = ['java', 'c++', 'oop', 'software engineering', 'sysadmin']
    print(f"\nInput: {test_skills_se}")
    role_se, conf_se = predictor.predict_role(test_skills_se)
    print(f"Predicted Role: {role_se}")
    print(f"Confidence: {conf_se * 100:.2f}%")
    
    test_skills_7 = ['Unity', 'Pygame', 'Unreal Engine']
    print(f"\nInput: {test_skills_7}")
    role7, conf7 = predictor.predict_role(test_skills_7)
    print(f"Predicted Role: {role7}")
    print(f"Confidence: {conf7 * 100:.2f}%")
    
    test_skills_8 = ['Arduino', 'ESP32', 'microcontroller']
    print(f"\nInput: {test_skills_8}")
    role8, conf8 = predictor.predict_role(test_skills_8)
    print(f"Predicted Role: {role8}")
    print(f"Confidence: {conf8 * 100:.2f}%")

    test_skills_9 = ['editor', 'content writing', 'copywriting']
    print(f"\nInput: {test_skills_9}")
    role9, conf9 = predictor.predict_role(test_skills_9)
    print(f"Predicted Role: {role9}")
    print(f"Confidence: {conf9 * 100:.2f}%")

    test_skills_10 = ['kali linux', 'hacking', 'penetration']
    print(f"\nInput: {test_skills_10}")
    role10, conf10 = predictor.predict_role(test_skills_10)
    print(f"Predicted Role: {role10}")
    print(f"Confidence: {conf10 * 100:.2f}%")

    test_skills_11 = ['cursor', 'vibe coding', 'ai-assisted programming']
    print(f"\nInput: {test_skills_11}")
    role11, conf11 = predictor.predict_role(test_skills_11)
    print(f"Predicted Role: {role11}")
    print(f"Confidence: {conf11 * 100:.2f}%")