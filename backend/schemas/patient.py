from pydantic import BaseModel
from typing import List, Dict, Any

class PatientCreate(BaseModel):
    """Schema for creating a new patient record and requesting a health prediction."""
    age: int
    gender: str = "Male"
    bmi: float
    systolic_bp: int
    fasting_glucose: float
    cholesterol_total: float
    ldl: float
    hdl: float
    hba1c: float
    triglycerides: float
    smoking_status: str
    alcohol_consumption: str
    physical_activity_level: str
    sleep_hours: float
    stress_level: str

class PredictionResponse(BaseModel):
    """Schema for the prediction response payload containing health scores and recommendations."""
    overall_health_score: int
    health_category: str
    diabetes_risk: int
    heart_risk: int
    kidney_risk: int
    stroke_risk: int
    cardiovascular_score: int
    metabolic_score: int
    lifestyle_score: int
    biological_age: int
    alerts: List[str]
    recommendations: List[str]
    shap_explanations: Dict[str, Any]
