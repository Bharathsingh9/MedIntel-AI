from health_scoring.scoring_engine import ScoringEngine

class HealthIntelligenceIndex:
    @staticmethod
    def calculate_index(disease_probs, patient_data):
        overall_health = ScoringEngine.calculate_health_score(
            disease_probs.get('diabetes', 0),
            disease_probs.get('heart', 0),
            disease_probs.get('kidney', 0),
            disease_probs.get('stroke', 0)
        )
        ls_score = ScoringEngine.lifestyle_score(
            patient_data.get('smoking_status'),
            patient_data.get('alcohol_consumption'),
            patient_data.get('physical_activity_level'),
            patient_data.get('sleep_hours'),
            patient_data.get('stress_level')
        )
        
        # Methodology:
        # 60% driven by exact ML probability predictions (disease risks)
        # 40% driven by current lifestyle/behaviors to promote preventative changes
        index = (overall_health * 0.6) + (ls_score * 0.4)
        return round(index)
