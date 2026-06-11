import json
import os
import sys

# Ensure module is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from health_scoring.scoring_engine import ScoringEngine
from health_scoring.health_index import HealthIntelligenceIndex
from health_scoring.biological_age import BiologicalAgeEstimator
from health_scoring.alert_engine import EarlyWarningSystem
from health_scoring.recommendation_engine import RecommendationEngine
from health_scoring.simulator import HealthTrendSimulator
from health_scoring.dashboard import DashboardGenerator

def generate_health_payload(patient_data, disease_probs):
    # 1. Scoring
    overall_health = ScoringEngine.calculate_health_score(
        disease_probs.get('diabetes',0), disease_probs.get('heart',0),
        disease_probs.get('kidney',0), disease_probs.get('stroke',0)
    )
    health_category = ScoringEngine.get_risk_category(overall_health)
    
    cardio_score = ScoringEngine.cardiovascular_score(
        patient_data.get('cholesterol_total', 150), patient_data.get('ldl', 100),
        patient_data.get('hdl', 50), patient_data.get('systolic_bp', 120),
        patient_data.get('smoking_status', 'Never'), patient_data.get('age', 40)
    )
    
    metabolic_score = ScoringEngine.metabolic_score(
        patient_data.get('bmi', 22), patient_data.get('fasting_glucose', 90),
        patient_data.get('hba1c', 5.0), patient_data.get('triglycerides', 100)
    )
    
    lifestyle_score = ScoringEngine.lifestyle_score(
        patient_data.get('smoking_status', 'Never'), patient_data.get('alcohol_consumption', 'None'),
        patient_data.get('physical_activity_level', 'Active'), patient_data.get('sleep_hours', 8),
        patient_data.get('stress_level', 'Low')
    )
    
    # 2. Bio Age
    bio_age = BiologicalAgeEstimator.estimate(
        patient_data.get('age', 40), patient_data.get('bmi', 22),
        patient_data.get('systolic_bp', 120), patient_data.get('smoking_status', 'Never'),
        patient_data.get('physical_activity_level', 'Active'), patient_data.get('sleep_hours', 8)
    )
    
    # 3. Alerts & Recs
    alerts = EarlyWarningSystem.generate_alerts(overall_health, disease_probs, patient_data)
    recs = RecommendationEngine.generate_recommendations(patient_data, disease_probs)
    
    # Payload Construction
    payload = {
        "overall_health_score": round(overall_health),
        "health_category": health_category,
        "diabetes_risk": round(disease_probs.get('diabetes', 0) * 100),
        "heart_risk": round(disease_probs.get('heart', 0) * 100),
        "kidney_risk": round(disease_probs.get('kidney', 0) * 100),
        "stroke_risk": round(disease_probs.get('stroke', 0) * 100),
        "cardiovascular_score": round(cardio_score),
        "metabolic_score": round(metabolic_score),
        "lifestyle_score": round(lifestyle_score),
        "biological_age": bio_age,
        "alerts": alerts,
        "recommendations": recs
    }
    return payload

if __name__ == "__main__":
    # Dummy high-risk patient for testing
    patient_data = {
        'age': 55, 'bmi': 31.5, 'systolic_bp': 145, 'fasting_glucose': 130,
        'cholesterol_total': 220, 'ldl': 150, 'hdl': 35, 'hba1c': 6.2,
        'triglycerides': 180, 'smoking_status': 'Current', 'alcohol_consumption': 'Regular',
        'physical_activity_level': 'Sedentary', 'sleep_hours': 5, 'stress_level': 'High'
    }
    # These would normally come from the inference_pipeline.py Output
    disease_probs = {
        'diabetes': 0.65,
        'heart': 0.58,
        'kidney': 0.22,
        'stroke': 0.35
    }
    
    reports_dir = r"D:\\health-analytics-ai\\reports\\health_scoring"
    os.makedirs(reports_dir, exist_ok=True)
    
    print("Generating Health Payload...")
    payload = generate_health_payload(patient_data, disease_probs)
    
    # Save API JSON
    with open(os.path.join(reports_dir, "api_response_payload.json"), "w") as f:
        json.dump(payload, f, indent=4)
        
    print("Generating Dashboards...")
    dash_gen = DashboardGenerator(reports_dir)
    dash_gen.generate_health_gauge(payload['overall_health_score'])
    dash_gen.generate_risk_radar({
        "Cardiovascular Health": payload['cardiovascular_score'],
        "Metabolic Health": payload['metabolic_score'],
        "Lifestyle Wellness": payload['lifestyle_score']
    })
    
    print("Running Health Trend Simulation...")
    sim_result = HealthTrendSimulator.simulate(patient_data, disease_probs, delta_weight_kg=-10, quit_smoking=True)
    with open(os.path.join(reports_dir, "simulation_result.json"), "w") as f:
        json.dump(sim_result, f, indent=4)
        
    print(f"Health Risk Scoring Engine Execution Complete. Reports saved to {reports_dir}")
