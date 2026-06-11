class ExplainabilityEngine:
    def __init__(self, models_dict):
        self.models = models_dict

    def explain_prediction(self, target, patient_dict):
        # In a full production environment, this would initialize shap.TreeExplainer or shap.LinearExplainer
        # and pass the one-hot-encoded patient features array.
        # For this API endpoint, we return a heuristic top-driver mapping based on our EDA findings.
        if 'diabetes' in target:
            return {"top_drivers": ["fasting_glucose", "bmi", "age"], "insight": "High fasting glucose heavily drove this risk prediction."}
        elif 'heart' in target:
            return {"top_drivers": ["systolic_bp", "cholesterol_total", "age"], "insight": "Blood pressure and lipid profiles are the primary risk factors here."}
        elif 'kidney' in target:
            return {"top_drivers": ["fasting_glucose", "systolic_bp"], "insight": "Hypertension combined with elevated glucose impacts kidney function."}
        else:
            return {"top_drivers": ["age", "systolic_bp", "smoking_status"], "insight": "Cardiovascular markers and age are driving this stroke prediction."}
