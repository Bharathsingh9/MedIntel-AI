import os
import joblib
import pandas as pd
import numpy as np

class PatientRiskPredictor:
    """
    Reusable prediction pipeline for MedIntel AI.
    Loads pickled models and preprocessors to provide risk predictions.
    Suitable for FastAPI deployment.
    """
    def __init__(self, models_dir):
        self.models_dir = models_dir
        self.models = {}
        
        # Load models
        targets = ['diabetes', 'heart', 'kidney', 'stroke']
        for t in targets:
            model_path = os.path.join(models_dir, f"{t}_model.pkl")
            if os.path.exists(model_path):
                self.models[f"{t}_risk"] = joblib.load(model_path)
            else:
                print(f"Warning: {model_path} not found.")
                
        # Load preprocessor
        prep_path = os.path.join(models_dir, "preprocessor.pkl")
        if os.path.exists(prep_path):
            self.preprocessor = joblib.load(prep_path)

    def predict(self, patient_features: dict) -> dict:
        """
        Takes raw patient features, preprocesses them, and returns risk probabilities.
        For demonstration, assuming `patient_features` is already preprocessed (or 
        this method would call the custom preprocessor logic).
        """
        df = pd.DataFrame([patient_features])
        
        results = {}
        for target, model in self.models.items():
            try:
                # Ensure correct columns (drop targets if present)
                features = df.drop(columns=['diabetes_risk', 'heart_disease_risk', 'kidney_disease_risk', 'stroke_risk', 'patient_id'], errors='ignore')
                
                # Predict probability of class 1 (High Risk)
                if hasattr(model, 'predict_proba'):
                    prob = model.predict_proba(features)[0][1]
                else:
                    prob = float(model.predict(features)[0])
                results[target] = round(float(prob), 4)
            except Exception as e:
                results[target] = f"Error: {str(e)}"
                
        return results

# Example Usage for testing
if __name__ == "__main__":
    predictor = PatientRiskPredictor("D:\\health-analytics-ai\\models")
    print("Inference Pipeline Loaded Successfully.")
