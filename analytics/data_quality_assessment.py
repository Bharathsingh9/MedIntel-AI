import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class DataQualityAssessor:
    """
    Enterprise-level Data Quality Assessment module for Healthcare Datasets.
    """
    def __init__(self, filepath, output_dir):
        self.filepath = filepath
        self.output_dir = output_dir
        print(f"Loading dataset from {self.filepath}...")
        self.df = pd.read_csv(filepath)
        os.makedirs(output_dir, exist_ok=True)
        self.report_sections = []
        
        # Initialize Quality Score components
        self.score_metrics = {
            'Completeness': 100,
            'Accuracy': 100,
            'Consistency': 100,
            'Validity': 100,
            'Uniqueness': 100
        }
        
    def add_section(self, title, content):
        self.report_sections.append(f"## {title}\n\n{content}\n")

    def run_all(self):
        print("Starting Data Quality Assessment...")
        self.task_1_overview()
        self.task_2_missing()
        self.task_3_duplicates()
        self.task_4_datatypes()
        self.task_5_range()
        self.task_6_outliers()
        self.task_7_class_balance()
        self.task_8_correlation()
        self.task_9_leakage()
        self.task_10_consistency()
        self.task_11_quality_score()
        self.task_12_final_report()
        print(f"Assessment complete. Report saved to {self.output_dir}")

    def task_1_overview(self):
        print("Task 1: Dataset Overview...")
        shape = self.df.shape
        mem_usage = self.df.memory_usage(deep=True).sum() / 1024**2
        dtypes = {str(k): v for k, v in self.df.dtypes.value_counts().to_dict().items()}
        
        overview = f"""
- **Number of Rows**: {shape[0]}
- **Number of Columns**: {shape[1]}
- **Memory Usage**: {mem_usage:.2f} MB
- **Data Types Summary**: {dtypes}
"""
        self.add_section("1. Dataset Overview", overview)

    def task_2_missing(self):
        print("Task 2: Missing Value Analysis...")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        missing_df = pd.DataFrame({'Missing_Count': missing, 'Missing_Pct': missing_pct})
        missing_df = missing_df[missing_df['Missing_Count'] > 0]
        
        if len(missing_df) > 0:
            self.score_metrics['Completeness'] -= len(missing_df) * 5
            content = missing_df.to_markdown()
        else:
            content = "No missing values found in the dataset."
            
        plt.figure(figsize=(10, 6))
        sns.heatmap(self.df.isnull(), cbar=False, cmap='viridis')
        plt.title('Missing Values Heatmap')
        plt.savefig(os.path.join(self.output_dir, 'missing_heatmap.png'))
        plt.close()
        
        content += "\n\n![Missing Values Heatmap](missing_heatmap.png)"
        self.add_section("2. Missing Value Analysis", content)

    def task_3_duplicates(self):
        print("Task 3: Duplicate Analysis...")
        full_dupes = self.df.duplicated().sum()
        id_dupes = self.df['patient_id'].duplicated().sum() if 'patient_id' in self.df.columns else 0
        
        if full_dupes > 0: self.score_metrics['Uniqueness'] -= 10
        if id_dupes > 0: self.score_metrics['Uniqueness'] -= 20
        
        content = f"""
- **Full-Row Duplicates**: {full_dupes} ({full_dupes/len(self.df)*100:.2f}%)
- **Duplicate Patient IDs**: {id_dupes}

**Recommended Handling Strategy**: 
- Exact full-row duplicates should be dropped immediately.
- Duplicate Patient IDs require further investigation to determine if they represent legitimate separate visits or data entry errors.
"""
        self.add_section("3. Duplicate Analysis", content)

    def task_4_datatypes(self):
        print("Task 4: Data Type Validation...")
        num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        content = f"- **Numerical Columns**: {len(num_cols)}\n"
        content += f"- **Categorical Columns**: {len(cat_cols)}\n\n"
        
        mixed_types = []
        for col in cat_cols:
            types = self.df[col].apply(type).nunique()
            if types > 1:
                mixed_types.append(col)
                
        if mixed_types:
            content += f"**Warning**: Mixed Datatypes detected in: {mixed_types}\n"
            self.score_metrics['Validity'] -= 10
        else:
            content += "All categorical columns have consistent string types.\n"
            
        self.add_section("4. Data Type Validation", content)

    def task_5_range(self):
        print("Task 5: Range Validation...")
        ranges = {
            'age': (0, 120),
            'bmi': (10, 60),
            'systolic_bp': (70, 250),
            'diastolic_bp': (40, 150),
            'heart_rate': (30, 220),
            'fasting_glucose': (40, 500),
            'hba1c': (3, 20),
            'creatinine': (0.1, 20)
        }
        
        anomalies = {}
        for col, (min_val, max_val) in ranges.items():
            if col in self.df.columns:
                invalid = self.df[(self.df[col] < min_val) | (self.df[col] > max_val)]
                if len(invalid) > 0:
                    anomalies[col] = len(invalid)
                    self.score_metrics['Validity'] -= 5
                    
        content = "### Out-of-Range Medical Anomalies\n"
        if anomalies:
            for k, v in anomalies.items():
                content += f"- **{k}**: {v} anomalous records outside expected range {ranges[k]}.\n"
        else:
            content += "All medical metrics fall within plausible bounds.\n"
            
        self.add_section("5. Range Validation", content)

    def task_6_outliers(self):
        print("Task 6: Outlier Detection...")
        num_cols = self.df.select_dtypes(include=[np.number]).columns
        
        outliers_info = []
        for col in num_cols:
            if self.df[col].nunique() > 5: 
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                outliers = self.df[(self.df[col] < lower) | (self.df[col] > upper)]
                if len(outliers) > 0:
                    outliers_info.append(f"- **{col}**: {len(outliers)} outliers ({len(outliers)/len(self.df)*100:.2f}%)")
                    
        content = "### IQR Outlier Detection\n" + "\n".join(outliers_info)
        content += "\n\n**Strategy Recommendation**: For healthcare datasets, statistical outliers are often valid pathological conditions (e.g., extremely high fasting glucose is indicative of severe diabetes, not a measurement error). Do not remove them blindly. Consider transformation or robust scaling instead of capping."
        
        plt.figure(figsize=(15, 6))
        cols_to_plot = [c for c in ['age', 'bmi', 'systolic_bp', 'cholesterol_total'] if c in self.df.columns]
        for i, col in enumerate(cols_to_plot, 1):
            plt.subplot(1, len(cols_to_plot), i)
            sns.boxplot(y=self.df[col], color='skyblue')
            plt.title(f'Boxplot: {col}')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'outliers_boxplot.png'))
        plt.close()
        
        content += "\n\n![Outlier Boxplots](outliers_boxplot.png)"
        self.add_section("6. Outlier Detection", content)

    def task_7_class_balance(self):
        print("Task 7: Class Balance Analysis...")
        targets = ['diabetes_risk', 'heart_disease_risk', 'kidney_disease_risk', 'stroke_risk']
        
        content = "### Target Distributions\n"
        plt.figure(figsize=(14, 10))
        for i, target in enumerate(targets, 1):
            if target in self.df.columns:
                counts = self.df[target].value_counts(normalize=True) * 100
                content += f"- **{target}**: Class 0 ({counts.get(0, 0):.1f}%), Class 1 ({counts.get(1, 0):.1f}%)\n"
                
                plt.subplot(2, 2, i)
                sns.countplot(x=target, data=self.df, palette='viridis')
                plt.title(f'{target} Class Balance')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'class_balance.png'))
        plt.close()
        
        content += "\n**Recommendation**: If the minority class is < 10%, consider applying SMOTE or class-weight adjustment during model training.\n"
        content += "\n![Class Balance](class_balance.png)"
        self.add_section("7. Class Balance Analysis", content)

    def task_8_correlation(self):
        print("Task 8: Correlation Analysis...")
        num_cols = self.df.select_dtypes(include=[np.number])
        corr_matrix = num_cols.corr(method='pearson')
        
        plt.figure(figsize=(16, 12))
        sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0)
        plt.title('Pearson Correlation Heatmap')
        plt.savefig(os.path.join(self.output_dir, 'correlation_heatmap.png'))
        plt.close()
        
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i):
                if abs(corr_matrix.iloc[i, j]) > 0.8:
                    high_corr.append(f"{corr_matrix.columns[i]} & {corr_matrix.columns[j]}: {corr_matrix.iloc[i, j]:.2f}")
                    
        content = "### Highly Correlated Features (>0.80)\n"
        if high_corr:
            content += "\n".join([f"- {pair}" for pair in high_corr])
            content += "\n\n**Warning**: Multicollinearity detected. Consider removing one of the highly correlated features before training linear models."
        else:
            content += "No highly correlated feature pairs found."
            
        content += "\n\n![Correlation Heatmap](correlation_heatmap.png)"
        self.add_section("8. Correlation Analysis", content)

    def task_9_leakage(self):
        print("Task 9: Target Leakage Detection...")
        targets = ['diabetes_risk', 'heart_disease_risk', 'kidney_disease_risk', 'stroke_risk']
        num_cols = self.df.select_dtypes(include=[np.number])
        corr_matrix = num_cols.corr()
        
        content = "### Potential Target Leakage\n"
        content += "Checking for non-target features that have >0.8 correlation with a target variable.\n\n"
        
        leakage_found = False
        for target in targets:
            if target in corr_matrix.columns:
                corrs = corr_matrix[target].abs().sort_values(ascending=False)
                # Exclude correlation with itself and other target variables
                leaks = corrs[(corrs > 0.8) & (corrs < 1.0)]
                for feature, corr_val in leaks.items():
                    if feature not in targets:
                        leakage_found = True
                        content += f"- **{target}** with **{feature}** (Corr: {corr_val:.2f})\n"
                        
        if not leakage_found:
            content += "No obvious target leakage detected through simple correlation.\n"
            
        self.add_section("9. Target Leakage Detection", content)

    def task_10_consistency(self):
        print("Task 10: Data Consistency Checks...")
        inconsistencies = []
        
        if all(x in self.df.columns for x in ['bmi', 'weight_kg', 'height_cm']):
            calc_bmi = self.df['weight_kg'] / ((self.df['height_cm']/100)**2)
            bmi_diff = (self.df['bmi'] - calc_bmi).abs()
            bad_bmi = len(bmi_diff[bmi_diff > 1.0])
            if bad_bmi > 0:
                inconsistencies.append(f"{bad_bmi} records have a calculated BMI significantly different from the provided BMI.")
                self.score_metrics['Consistency'] -= (bad_bmi / len(self.df)) * 100

        if 'age' in self.df.columns:
            neg_age = len(self.df[self.df['age'] < 0])
            if neg_age > 0:
                inconsistencies.append(f"{neg_age} records have negative age.")
                self.score_metrics['Accuracy'] -= 10
                
        content = "### Logical Inconsistencies\n"
        if inconsistencies:
            content += "\n".join([f"- {i}" for i in inconsistencies])
        else:
            content += "All logical consistency checks passed."
            
        self.add_section("10. Data Consistency Checks", content)

    def task_11_quality_score(self):
        print("Task 11: Quality Score Calculation...")
        for k in self.score_metrics:
            self.score_metrics[k] = max(0, min(100, self.score_metrics[k]))
            
        final_score = np.mean(list(self.score_metrics.values()))
        
        content = f"### Overall Data Quality Score: **{final_score:.1f} / 100**\n\n"
        for k, v in self.score_metrics.items():
            content += f"- **{k}**: {v:.1f}/100\n"
            
        self.add_section("11. Quality Score", content)

    def task_12_final_report(self):
        print("Task 12: Generating Final Report...")
        report_path = os.path.join(self.output_dir, 'data_quality_report.md')
        
        with open(report_path, 'w') as f:
            f.write("# Enterprise Data Quality Assessment Report\n\n")
            f.write("## Executive Summary\n")
            f.write("This report provides a comprehensive overview of the MedIntel AI synthetic dataset quality, covering completeness, uniqueness, consistency, and statistical validity.\n\n")
            for section in self.report_sections:
                f.write(section + "\n")
                
        print(f"Report successfully generated at {report_path}")

if __name__ == "__main__":
    # Point to the synthetic dataset generated earlier
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'synthetic', 'synthetic_patients_100k.csv'))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data_quality_report'))
    
    if not os.path.exists(filepath):
        print(f"Error: Dataset not found at {filepath}")
        sys.exit(1)
        
    assessor = DataQualityAssessor(filepath, output_dir)
    assessor.run_all()
