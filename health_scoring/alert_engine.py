class EarlyWarningSystem:
    @staticmethod
    def generate_alerts(health_score, disease_probs, patient_data):
        alerts = []
        highest_prob = max(disease_probs.values()) if disease_probs else 0
        
        # Core Triage
        if health_score <= 30 or highest_prob > 0.7:
            alerts.append("Red Alert: Critical Risk - Immediate medical intervention recommended.")
        elif health_score <= 60 or highest_prob > 0.4:
            alerts.append("Orange Alert: High Risk - Schedule a comprehensive clinical evaluation.")
        elif health_score <= 80:
            alerts.append("Yellow Alert: Moderate Risk - Monitor lifestyle factors and specific biomarkers.")
        else:
            alerts.append("Green Alert: Healthy - Maintain current lifestyle habits.")
            
        # Specific Biomarker Alerts
        if patient_data.get('fasting_glucose', 0) > 126:
            alerts.append("Biomarker Alert: Elevated Fasting Glucose indicative of active Diabetes Risk.")
        if patient_data.get('systolic_bp', 0) > 140:
            alerts.append("Biomarker Alert: Stage 2 Hypertension detected (High Cardiovascular Risk).")
            
        return alerts
