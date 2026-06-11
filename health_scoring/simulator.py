from health_scoring.scoring_engine import ScoringEngine
from health_scoring.biological_age import BiologicalAgeEstimator

class HealthTrendSimulator:
    @staticmethod
    def simulate(patient_data, disease_probs, delta_weight_kg=0, quit_smoking=False, glucose_reduction_pct=0):
        # Create a deep copy for simulation
        sim_data = patient_data.copy()
        sim_probs = disease_probs.copy()
        
        # Apply deltas
        if delta_weight_kg != 0:
            height_m = sim_data.get('height_cm', 170) / 100.0
            current_weight = sim_data.get('weight_kg', 70)
            new_weight = current_weight + delta_weight_kg
            sim_data['weight_kg'] = new_weight
            sim_data['bmi'] = new_weight / (height_m ** 2)
            
        if quit_smoking:
            sim_data['smoking_status'] = 'Former'
            
        if glucose_reduction_pct > 0:
            sim_data['fasting_glucose'] = sim_data.get('fasting_glucose', 100) * (1 - glucose_reduction_pct/100.0)
            
        # Recalculate Bio Age
        new_bio_age = BiologicalAgeEstimator.estimate(
            sim_data.get('age', 40), 
            sim_data['bmi'], 
            sim_data.get('systolic_bp', 120),
            sim_data['smoking_status'], 
            sim_data.get('physical_activity_level', 'Active'), 
            sim_data.get('sleep_hours', 8)
        )
        
        # Heuristic probability adjustments (API optimized, rather than full ML re-inference)
        if delta_weight_kg < 0:
            sim_probs['diabetes'] = max(0.01, sim_probs['diabetes'] - 0.15)
            sim_probs['heart'] = max(0.01, sim_probs['heart'] - 0.10)
        if quit_smoking:
            sim_probs['heart'] = max(0.01, sim_probs['heart'] - 0.20)
            sim_probs['stroke'] = max(0.01, sim_probs['stroke'] - 0.15)
        if glucose_reduction_pct > 0:
            sim_probs['diabetes'] = max(0.01, sim_probs['diabetes'] - 0.20)
            
        # Recalculate Overall Health Score
        new_health_score = ScoringEngine.calculate_health_score(
            sim_probs.get('diabetes', 0.1), 
            sim_probs.get('heart', 0.1), 
            sim_probs.get('kidney', 0.1), 
            sim_probs.get('stroke', 0.1)
        )
        
        return {
            "simulated_health_score": round(new_health_score),
            "simulated_biological_age": new_bio_age,
            "simulated_disease_probs": {k: round(v, 2) for k, v in sim_probs.items()}
        }
