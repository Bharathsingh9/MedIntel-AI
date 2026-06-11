from sqlalchemy import Column, Integer, Float, String, JSON, ForeignKey
from .database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    bmi = Column(Float)
    systolic_bp = Column(Integer)
    fasting_glucose = Column(Float)
    cholesterol_total = Column(Float)
    ldl = Column(Float)
    hdl = Column(Float)
    hba1c = Column(Float)
    triglycerides = Column(Float)
    smoking_status = Column(String)
    alcohol_consumption = Column(String)
    physical_activity_level = Column(String)
    sleep_hours = Column(Float)
    stress_level = Column(String)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    overall_health_score = Column(Float)
    health_category = Column(String)
    disease_risks = Column(JSON)
    composite_scores = Column(JSON)
    biological_age = Column(Integer)
    alerts = Column(JSON)
    recommendations = Column(JSON)
    shap_explanations = Column(JSON)
