from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
import os

# Import DB
from backend.database import database, models
from backend.schemas import patient as schemas

# Import ML and Scoring
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ml.prediction.inference_pipeline import PatientRiskPredictor
from health_scoring.main import generate_health_payload
from explainability.shap_engine import ExplainabilityEngine

router = APIRouter()

MODELS_DIR = "D:\\health-analytics-ai\\models"
try:
    ml_predictor = PatientRiskPredictor(MODELS_DIR)
    explainer = ExplainabilityEngine(ml_predictor.models)
except Exception as e:
    print(f"Error loading models: {e}")
    ml_predictor = None
    explainer = None

@router.post("/predict", response_model=schemas.PredictionResponse)
def create_prediction(patient: schemas.PatientCreate, db: Session = Depends(database.get_db)):
    if not ml_predictor:
        raise HTTPException(status_code=500, detail="ML Models not loaded.")
        
    patient_dict = patient.dict()
    
    # 1. Save Patient
    db_patient = models.Patient(**patient_dict)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    # 2. ML Inference
    probs = ml_predictor.predict(patient_dict)
    clean_probs = {}
    for k, v in probs.items():
        clean_key = k.replace('_risk', '')
        clean_probs[clean_key] = v if isinstance(v, float) else 0.1
        
    # 3. Health Scoring
    health_payload = generate_health_payload(patient_dict, clean_probs)
    
    # 4. Explainability
    shap_exps = {
        "diabetes": explainer.explain_prediction("diabetes", patient_dict),
        "heart": explainer.explain_prediction("heart", patient_dict)
    }
    health_payload['shap_explanations'] = shap_exps
    
    # 5. Save Prediction
    db_prediction = models.Prediction(
        patient_id=db_patient.id,
        overall_health_score=health_payload['overall_health_score'],
        health_category=health_payload['health_category'],
        disease_risks=clean_probs,
        composite_scores={
            "cardio": health_payload['cardiovascular_score'],
            "metabolic": health_payload['metabolic_score'],
            "lifestyle": health_payload['lifestyle_score']
        },
        biological_age=health_payload['biological_age'],
        alerts=health_payload['alerts'],
        recommendations=health_payload['recommendations'],
        shap_explanations=shap_exps
    )
    db.add(db_prediction)
    db.commit()
    
    return health_payload
