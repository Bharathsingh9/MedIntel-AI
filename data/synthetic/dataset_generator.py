import pandas as pd
import numpy as np
import uuid
import os

def generate_synthetic_data(num_patients=100000):
    np.random.seed(42)
    
    # 1. Demographics
    patient_id = [str(uuid.uuid4()) for _ in range(num_patients)]
    age = np.random.normal(loc=50, scale=15, size=num_patients)
    age = np.clip(age, 18, 90).astype(int)
    
    gender_choices = ['Male', 'Female']
    gender = np.random.choice(gender_choices, num_patients, p=[0.49, 0.51])
    
    ethnicity_choices = ['Caucasian', 'African American', 'Asian', 'Hispanic', 'Other']
    ethnicity = np.random.choice(ethnicity_choices, num_patients, p=[0.6, 0.13, 0.06, 0.18, 0.03])

    # 2. Lifestyle
    smoking_choices = ['Never', 'Former', 'Current']
    smoking_status = np.random.choice(smoking_choices, num_patients, p=[0.6, 0.25, 0.15])
    
    alcohol_choices = ['None', 'Occasional', 'Regular', 'Heavy']
    alcohol_consumption = np.random.choice(alcohol_choices, num_patients, p=[0.3, 0.4, 0.2, 0.1])
    
    activity_choices = ['Sedentary', 'Light', 'Moderate', 'Active']
    physical_activity_level = np.random.choice(activity_choices, num_patients, p=[0.25, 0.35, 0.25, 0.15])
    
    sleep_hours = np.random.normal(loc=7, scale=1.2, size=num_patients)
    sleep_hours = np.clip(sleep_hours, 3, 12).round(1)
    
    stress_choices = ['Low', 'Medium', 'High']
    stress_level = np.random.choice(stress_choices, num_patients, p=[0.3, 0.5, 0.2])

    # 3. Vitals
    height_cm = np.where(gender == 'Male', 
                         np.random.normal(175, 7, num_patients),
                         np.random.normal(162, 6, num_patients))
    
    # Base BMI with effects from activity
    base_bmi = np.random.normal(26, 5, num_patients)
    activity_effect_bmi = {'Sedentary': 2, 'Light': 0, 'Moderate': -2, 'Active': -4}
    activity_bmi_adj = np.array([activity_effect_bmi[a] for a in physical_activity_level])
    bmi = base_bmi + activity_bmi_adj
    bmi = np.clip(bmi, 15, 50)
    
    weight_kg = bmi * ((height_cm / 100) ** 2)
    
    # Blood pressure influenced by age, bmi, stress, smoking
    bp_base = 110 + (age - 30) * 0.4 + (bmi - 25) * 1.2
    stress_effect_bp = {'Low': 0, 'Medium': 5, 'High': 10}
    stress_bp_adj = np.array([stress_effect_bp[s] for s in stress_level])
    smoking_bp_adj = np.where(smoking_status == 'Current', 5, 0)
    
    systolic_bp = bp_base + stress_bp_adj + smoking_bp_adj + np.random.normal(0, 10, num_patients)
    systolic_bp = np.clip(systolic_bp, 90, 200).astype(int)
    
    diastolic_bp = systolic_bp * 0.6 + np.random.normal(0, 5, num_patients)
    diastolic_bp = np.clip(diastolic_bp, 60, 120).astype(int)
    
    heart_rate = 70 + (bmi - 25) * 0.5 - np.where(physical_activity_level == 'Active', 10, 0) + np.random.normal(0, 8, num_patients)
    heart_rate = np.clip(heart_rate, 45, 120).astype(int)

    # 4. Family History
    family_history_diabetes = np.random.choice([0, 1], num_patients, p=[0.8, 0.2])
    family_history_heart_disease = np.random.choice([0, 1], num_patients, p=[0.85, 0.15])
    family_history_kidney_disease = np.random.choice([0, 1], num_patients, p=[0.9, 0.1])

    # 5. Lab Results
    # Glucose and HbA1c driven heavily by BMI, age, and family history
    glucose_base = 85 + (bmi - 25) * 1.5 + (age - 40) * 0.3 + family_history_diabetes * 10
    fasting_glucose = glucose_base + np.random.normal(0, 10, num_patients)
    fasting_glucose = np.clip(fasting_glucose, 60, 300)
    
    hba1c = (fasting_glucose + 46.7) / 28.7 + np.random.normal(0, 0.3, num_patients)
    hba1c = np.clip(hba1c, 4.0, 15.0).round(1)
    
    # Cholesterol driven by BMI, activity, alcohol
    cholesterol_total = 180 + (bmi - 25) * 2 + (age - 30) * 0.5 + np.random.normal(0, 20, num_patients)
    cholesterol_total = np.clip(cholesterol_total, 120, 350).astype(int)
    
    hdl = 55 - (bmi - 25) * 0.5 + np.where(physical_activity_level == 'Active', 10, 0) - np.where(smoking_status == 'Current', 5, 0) + np.random.normal(0, 8, num_patients)
    hdl = np.clip(hdl, 20, 100).astype(int)
    
    ldl = cholesterol_total - hdl - (np.random.normal(20, 5, num_patients)) # simplified Friedewald approx
    ldl = np.clip(ldl, 50, 250).astype(int)
    
    triglycerides = 100 + (bmi - 25) * 3 + np.where(alcohol_consumption == 'Heavy', 40, 0) + np.random.normal(0, 30, num_patients)
    triglycerides = np.clip(triglycerides, 40, 500).astype(int)
    
    # Creatinine driven by age, glucose (diabetes effect)
    creatinine_base = np.where(gender == 'Male', 0.9, 0.7)
    creatinine = creatinine_base + (age - 50) * 0.005 + np.where(fasting_glucose > 125, 0.2, 0) + np.random.normal(0, 0.1, num_patients)
    creatinine = np.clip(creatinine, 0.4, 5.0).round(2)

    # 6. Target Variables (Risk Probabilities calculated logically)
    
    # Diabetes Risk (Logistic function approximation)
    diab_logit = -5.0 + 0.05*age + 0.1*(bmi-25) + 0.05*(fasting_glucose-90) + 0.8*family_history_diabetes
    diabetes_prob = 1 / (1 + np.exp(-diab_logit))
    
    # Heart Disease Risk
    heart_logit = -6.0 + 0.06*age + 0.02*(systolic_bp-120) + 0.01*(ldl-100) - 0.02*(hdl-50) + 0.5*smoking_bp_adj/5 + 0.6*family_history_heart_disease + 1.0*diabetes_prob
    heart_disease_prob = 1 / (1 + np.exp(-heart_logit))
    
    # Kidney Disease Risk
    kidney_logit = -7.0 + 0.04*age + 0.02*(systolic_bp-120) + 1.5*(creatinine-1.0) + 1.2*diabetes_prob + 0.8*family_history_kidney_disease
    kidney_disease_prob = 1 / (1 + np.exp(-kidney_logit))
    
    # Stroke Risk
    stroke_logit = -7.5 + 0.07*age + 0.03*(systolic_bp-120) + 0.5*smoking_bp_adj/5 + 0.5*diabetes_prob + 0.6*heart_disease_prob
    stroke_prob = 1 / (1 + np.exp(-stroke_logit))
    
    diabetes_risk = (np.random.rand(num_patients) < diabetes_prob).astype(int)
    heart_disease_risk = (np.random.rand(num_patients) < heart_disease_prob).astype(int)
    kidney_disease_risk = (np.random.rand(num_patients) < kidney_disease_prob).astype(int)
    stroke_risk = (np.random.rand(num_patients) < stroke_prob).astype(int)

    df = pd.DataFrame({
        'patient_id': patient_id,
        'age': age,
        'gender': gender,
        'ethnicity': ethnicity,
        'smoking_status': smoking_status,
        'alcohol_consumption': alcohol_consumption,
        'physical_activity_level': physical_activity_level,
        'sleep_hours': sleep_hours,
        'stress_level': stress_level,
        'height_cm': np.round(height_cm, 1),
        'weight_kg': np.round(weight_kg, 1),
        'bmi': np.round(bmi, 1),
        'systolic_bp': systolic_bp,
        'diastolic_bp': diastolic_bp,
        'heart_rate': heart_rate,
        'fasting_glucose': np.round(fasting_glucose, 1),
        'hba1c': hba1c,
        'cholesterol_total': cholesterol_total,
        'ldl': ldl,
        'hdl': hdl,
        'triglycerides': triglycerides,
        'creatinine': creatinine,
        'family_history_diabetes': family_history_diabetes,
        'family_history_heart_disease': family_history_heart_disease,
        'family_history_kidney_disease': family_history_kidney_disease,
        'diabetes_risk': diabetes_risk,
        'heart_disease_risk': heart_disease_risk,
        'kidney_disease_risk': kidney_disease_risk,
        'stroke_risk': stroke_risk
    })
    
    return df

if __name__ == "__main__":
    print("Generating synthetic healthcare data with realistic dependencies...")
    df = generate_synthetic_data(100000)
    
    # Save in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "synthetic_patients_100k.csv")
    
    print(f"Exporting data to {output_path}...")
    df.to_csv(output_path, index=False)
    
    print("Data generation complete!")
    print(df.head())
    print("\nDataset Info:")
    print(df.info())
    print("\nTarget Variables Distribution:")
    for col in ['diabetes_risk', 'heart_disease_risk', 'kidney_disease_risk', 'stroke_risk']:
        print(f"{col}:\n{df[col].value_counts(normalize=True)}\n")
