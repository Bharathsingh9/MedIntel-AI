import { create } from 'zustand';

interface PatientData {
  age: number;
  gender: string;
  bmi: number;
  systolic_bp: number;
  fasting_glucose: number;
  cholesterol_total: number;
  ldl: number;
  hdl: number;
  hba1c: number;
  triglycerides: number;
  smoking_status: string;
  alcohol_consumption: string;
  physical_activity_level: string;
  sleep_hours: number;
  stress_level: string;
}

interface PredictionResult {
  overall_health_score: number;
  health_category: string;
  diabetes_risk: number;
  heart_risk: number;
  kidney_risk: number;
  stroke_risk: number;
  cardiovascular_score: number;
  metabolic_score: number;
  lifestyle_score: number;
  biological_age: number;
  alerts: string[];
  recommendations: string[];
  shap_explanations: Record<string, { insight: string; top_drivers?: string[] }>;
}

interface PatientStore {
  patientData: PatientData;
  setPatientData: (data: Partial<PatientData>) => void;
  clearPatientData: () => void;
  predictionResult: PredictionResult | null;
  setPredictionResult: (result: PredictionResult | null) => void;
}

const defaultPatientData: PatientData = {
  age: 55, gender: 'Male', bmi: 31.5, systolic_bp: 145, fasting_glucose: 130,
  cholesterol_total: 220, ldl: 150, hdl: 35, hba1c: 6.2, triglycerides: 180,
  smoking_status: 'Current', alcohol_consumption: 'Regular', physical_activity_level: 'Sedentary',
  sleep_hours: 5, stress_level: 'High'
};

export const usePatientStore = create<PatientStore>((set) => ({
  patientData: defaultPatientData,
  setPatientData: (data) => set((state) => ({ patientData: { ...state.patientData, ...data } })),
  clearPatientData: () => set({ patientData: defaultPatientData, predictionResult: null }),
  predictionResult: null,
  setPredictionResult: (result) => set({ predictionResult: result }),
}));
