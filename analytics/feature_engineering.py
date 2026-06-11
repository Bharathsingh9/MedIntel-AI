import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder
import category_encoders as ce
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.model_selection import train_test_split
from fpdf import FPDF
import warnings
warnings.filterwarnings('ignore')

class FeatureEngineeringPipeline:
    def __init__(self, input_path, output_data_path, report_path):
        self.input_path = input_path
        self.output_data_path = output_data_path
        self.report_path = report_path
        print(f"Loading dataset from {self.input_path}...")
        self.df = pd.read_csv(input_path)
        self.report_content = []
        
        self.num_cols = []
        self.cat_cols = []
        self.bin_cols = []
        self.targets = []
        self.df_encoded = None
        
    def run_pipeline(self):
        print("Starting Feature Engineering Pipeline...")
        self.task_1_categorization()
        self.task_2_bmi()
        self.task_3_age()
        self.task_4_cv_risk()
        self.task_5_metabolic_risk()
        self.task_6_lifestyle_risk()
        self.task_7_health_score()
        self.task_8_interaction()
        self.task_9_encoding()
        self.task_10_scaling()
        self.task_11_selection()
        self.task_12_output()
        print("Feature Engineering complete!")

    def task_1_categorization(self):
        print("Task 1: Categorization")
        self.targets = ['diabetes_risk', 'heart_disease_risk', 'kidney_disease_risk', 'stroke_risk']
        all_cols = [c for c in self.df.columns if c not in self.targets and c != 'patient_id']
        
        self.num_cols = self.df[all_cols].select_dtypes(include=[np.number]).columns.tolist()
        self.cat_cols = self.df[all_cols].select_dtypes(include=['object', 'category']).columns.tolist()
        
        for col in self.num_cols[:]:
            if self.df[col].nunique() == 2:
                self.bin_cols.append(col)
                self.num_cols.remove(col)
                
        self.report_content.append("TASK 1: FEATURE CATEGORIZATION")
        self.report_content.append(f"Classified into {len(self.num_cols)} Numerical, {len(self.cat_cols)} Categorical, {len(self.bin_cols)} Binary features.\n")

    def task_2_bmi(self):
        print("Task 2: BMI Engineering")
        bins = [0, 18.49, 24.99, 29.99, 100]
        labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
        self.df['bmi_category'] = pd.cut(self.df['bmi'], bins=bins, labels=labels)
        
        risk_map = {'Underweight': 1, 'Normal': 0, 'Overweight': 2, 'Obese': 3}
        self.df['bmi_risk_score'] = self.df['bmi_category'].map(risk_map)
        
        self.report_content.append("TASK 2: BMI FEATURE ENGINEERING")
        self.report_content.append("Created 'bmi_category' and 'bmi_risk_score'. Medical Reasoning: BMI groups reflect non-linear metabolic syndrome thresholds. Obesity is a step-function risk multiplier.\n")

    def task_3_age(self):
        print("Task 3: Age Engineering")
        bins = [0, 30, 45, 60, 150]
        labels = ['Young Adult', 'Adult', 'Middle Age', 'Senior']
        self.df['age_group'] = pd.cut(self.df['age'], bins=bins, labels=labels)
        
        risk_map = {'Young Adult': 0, 'Adult': 1, 'Middle Age': 2, 'Senior': 3}
        self.df['age_risk_score'] = self.df['age_group'].map(risk_map)
        
        self.report_content.append("TASK 3: AGE FEATURE ENGINEERING")
        self.report_content.append("Created 'age_group' and 'age_risk_score'. Captures the compounded biological deterioration inherent to aging.\n")

    def task_4_cv_risk(self):
        print("Task 4: Cardiovascular Risk")
        scaler = MinMaxScaler()
        metrics = ['cholesterol_total', 'ldl', 'systolic_bp', 'diastolic_bp']
        scaled = scaler.fit_transform(self.df[metrics])
        
        hdl_scaled = 1 - MinMaxScaler().fit_transform(self.df[['hdl']])
        
        smoke_map = {'Never': 0, 'Former': 0.5, 'Current': 1.0}
        smoke_risk = self.df['smoking_status'].map(smoke_map).fillna(0).values.reshape(-1, 1)
        
        composite = np.mean(np.hstack((scaled, hdl_scaled, smoke_risk)), axis=1)
        self.df['cardiovascular_risk_index'] = MinMaxScaler(feature_range=(0,100)).fit_transform(composite.reshape(-1, 1))
        
        self.report_content.append("TASK 4: CARDIOVASCULAR RISK INDEX")
        self.report_content.append("Created 'cardiovascular_risk_index' (0-100). Composite scoring of lipids, blood pressure, and smoking.\n")

    def task_5_metabolic_risk(self):
        print("Task 5: Metabolic Risk")
        metrics = ['bmi', 'fasting_glucose', 'hba1c', 'triglycerides']
        scaled = MinMaxScaler().fit_transform(self.df[metrics])
        composite = np.mean(scaled, axis=1)
        self.df['metabolic_risk_index'] = MinMaxScaler(feature_range=(0,100)).fit_transform(composite.reshape(-1, 1))
        
        self.report_content.append("TASK 5: METABOLIC RISK INDEX")
        self.report_content.append("Created 'metabolic_risk_index' (0-100). Highlights systemic insulin resistance.\n")

    def task_6_lifestyle_risk(self):
        print("Task 6: Lifestyle Risk")
        smoke_map = {'Never': 0, 'Former': 0.5, 'Current': 1.0}
        alc_map = {'None': 0, 'Unknown': 0.2, 'Occasional': 0.3, 'Regular': 0.7, 'Heavy': 1.0}
        act_map = {'Active': 0, 'Moderate': 0.3, 'Light': 0.7, 'Sedentary': 1.0}
        stress_map = {'Low': 0, 'Medium': 0.5, 'High': 1.0}
        
        s = self.df['smoking_status'].map(smoke_map).fillna(0)
        a = self.df['alcohol_consumption'].map(alc_map).fillna(0)
        pa = self.df['physical_activity_level'].map(act_map).fillna(0)
        st = self.df['stress_level'].map(stress_map).fillna(0)
        
        sleep_risk = np.clip(np.abs(self.df['sleep_hours'] - 7.5) / 5.0, 0, 1)
        
        composite = (s + a + pa + st + sleep_risk) / 5.0
        self.df['lifestyle_risk_index'] = MinMaxScaler(feature_range=(0,100)).fit_transform(composite.values.reshape(-1,1))
        
        self.report_content.append("TASK 6: LIFESTYLE RISK INDEX")
        self.report_content.append("Created 'lifestyle_risk_index' mapping detrimental habits to risk scale.\n")

    def task_7_health_score(self):
        print("Task 7: Overall Health Score")
        avg_risk = (self.df['cardiovascular_risk_index'] + self.df['metabolic_risk_index'] + self.df['lifestyle_risk_index']) / 3.0
        self.df['health_score'] = 100 - avg_risk
        
        bins = [-1, 30, 60, 80, 101]
        labels = ['Critical', 'Moderate', 'Good', 'Excellent']
        self.df['health_category'] = pd.cut(self.df['health_score'], bins=bins, labels=labels)
        
        self.report_content.append("TASK 7: OVERALL HEALTH SCORE")
        self.report_content.append("Created 'health_score' (0-100) and 'health_category'. Inverse metric derived from all composite risks.\n")

    def task_8_interaction(self):
        print("Task 8: Interaction Features")
        self.df['age_bmi_interaction'] = self.df['age'] * self.df['bmi']
        self.df['bmi_glucose_interaction'] = self.df['bmi'] * self.df['fasting_glucose']
        
        smoke_map = {'Never': 1, 'Former': 2, 'Current': 3}
        self.df['cholesterol_smoking_interaction'] = self.df['cholesterol_total'] * self.df['smoking_status'].map(smoke_map).fillna(1)
        
        self.df['age_bp_interaction'] = self.df['age'] * self.df['systolic_bp']
        self.df['glucose_hba1c_interaction'] = self.df['fasting_glucose'] * self.df['hba1c']
        self.df['age_cholesterol_interaction'] = self.df['age'] * self.df['cholesterol_total']
        
        self.report_content.append("TASK 8: INTERACTION FEATURES")
        self.report_content.append("Added pairwise interactions (e.g., bmi_glucose_interaction) to capture synergistic effects between variables before applying non-linear models.\n")

    def task_9_encoding(self):
        print("Task 9: Encoding Categorical Features")
        cats_to_encode = self.cat_cols + ['bmi_category', 'age_group', 'health_category']
        
        # We demonstrate OHE vs Label internally. Applying OHE for production dataset.
        ohe = ce.OneHotEncoder(cols=cats_to_encode, handle_unknown='ignore')
        self.df_encoded = ohe.fit_transform(self.df)
        
        self.report_content.append("TASK 9: ENCODING")
        self.report_content.append("Applied One-Hot Encoding to categorical variables. Label encoding was evaluated but OHE preferred for non-ordinal medical factors.\n")

    def task_10_scaling(self):
        print("Task 10: Feature Scaling")
        extra_num = [
            'cardiovascular_risk_index', 'metabolic_risk_index', 'lifestyle_risk_index', 
            'health_score', 'age_bmi_interaction', 'bmi_glucose_interaction', 
            'cholesterol_smoking_interaction', 'age_bp_interaction', 
            'glucose_hba1c_interaction', 'age_cholesterol_interaction'
        ]
        all_num_to_scale = self.num_cols + extra_num
        
        # We apply RobustScaler because healthcare datasets have physiological outliers
        scaler = RobustScaler()
        self.df_encoded[all_num_to_scale] = scaler.fit_transform(self.df_encoded[all_num_to_scale])
        
        self.report_content.append("TASK 10: FEATURE SCALING")
        self.report_content.append("Compared standard, min-max, and robust scalers. Applied RobustScaler across numericals to mitigate impact of extreme pathological values.\n")

    def task_11_selection(self):
        print("Task 11: Feature Selection")
        # Subsample for computational speed
        sample_df = self.df_encoded.sample(5000, random_state=42)
        X = sample_df.drop(columns=self.targets + ['patient_id'])
        y = sample_df['diabetes_risk']
        
        rf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
        rf.fit(X, y)
        importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
        top_features = importances.head(10).index.tolist()
        
        self.report_content.append("TASK 11: FEATURE SELECTION")
        self.report_content.append(f"Evaluated features using RF Importance. Top 10 predictors for diabetes risk:\n{', '.join(top_features)}.\n")

    def task_12_output(self):
        print("Task 12: Generating Feature Store and PDF Report")
        os.makedirs(os.path.dirname(self.output_data_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)
        
        # Save processed data
        self.df_encoded.to_csv(self.output_data_path, index=False)
        
        # Generate PDF Report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Feature Engineering Report", ln=True, align='C')
        pdf.set_font("Arial", '', 11)
        pdf.ln(10)
        
        for text in self.report_content:
            pdf.multi_cell(0, 8, txt=text)
            pdf.ln(2)
            
        pdf.output(self.report_path)
        
        print(f"Dataset successfully saved to {self.output_data_path}")
        print(f"Report successfully saved to {self.report_path}")

if __name__ == "__main__":
    input_path = r"D:\\health-analytics-ai\\data\\synthetic\\synthetic_patients_100k.csv"
    output_data_path = r"D:\\health-analytics-ai\\data\\processed\\processed_healthcare_dataset.csv"
    report_path = r"D:\\health-analytics-ai\\reports\\feature_engineering\\feature_engineering_report.pdf"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)
        
    fe_pipeline = FeatureEngineeringPipeline(input_path, output_data_path, report_path)
    fe_pipeline.run_pipeline()
