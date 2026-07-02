from typing import Dict, List, Any

class RecommendationEngine:
    @staticmethod
    def generate_recommendations(patient_data: Dict[str, Any], disease_probs: Dict[str, float]) -> List[str]:
        """
        Generate personalized health recommendations based on patient data and disease probabilities.

        Args:
            patient_data (Dict[str, Any]): Dictionary containing patient health metrics and lifestyle data.
            disease_probs (Dict[str, float]): Dictionary containing predicted probabilities for various diseases.

        Returns:
            List[str]: A list of unique recommendation strings.
        """
        recs = []
        
        # Metabolic & Diabetes
        if patient_data.get('fasting_glucose', 0) > 100 or disease_probs.get('diabetes', 0) > 0.3:
            recs.extend([
                "Reduce dietary intake of refined carbohydrates and simple sugars.",
                "Incorporate at least 150 minutes of moderate aerobic exercise weekly.",
                "Schedule a follow-up test to monitor HbA1c levels."
            ])
        
        # Cardiovascular
        if patient_data.get('cholesterol_total', 0) > 200 or patient_data.get('ldl', 0) > 130 or disease_probs.get('heart', 0) > 0.3:
            recs.extend([
                "Adopt a heart-healthy diet (e.g., Mediterranean or DASH diet).",
                "Increase daily physical activity to improve HDL and lower LDL."
            ])
            
        # Physical / BMI
        if patient_data.get('bmi', 0) > 25:
            recs.append("Target a 5-10% weight reduction to significantly lower your combined metabolic risk score.")
            
        # Lifestyle
        if patient_data.get('smoking_status') == 'Current':
            recs.append("Enroll in a smoking cessation program immediately; this single action drastically reduces CVD risk.")
            
        if patient_data.get('sleep_hours', 7) < 6:
            recs.append("Improve sleep hygiene to consistently reach 7-8 hours of restful sleep per night.")
            
        if patient_data.get('stress_level') == 'High':
            recs.append("Incorporate daily stress-reduction techniques such as mindfulness, meditation, or yoga.")
            
        # Fallback if extremely healthy
        if not recs:
            recs.append("Continue current exceptional health habits; maintain routine annual checkups.")
            
        # Return unique list
        return list(set(recs))
