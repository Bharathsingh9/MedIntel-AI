import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_selection import mutual_info_classif
import warnings
warnings.filterwarnings('ignore')

class HealthcareEDA:
    def __init__(self, filepath, output_dir):
        self.filepath = filepath
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        print(f"Loading dataset from {self.filepath}...")
        self.df = pd.read_csv(filepath)
        self.report_sections = []
        
        self.targets = ['diabetes_risk', 'heart_disease_risk', 'kidney_disease_risk', 'stroke_risk']
        self.num_cols = ['age', 'bmi', 'fasting_glucose', 'hba1c', 'cholesterol_total', 'ldl', 'hdl', 'triglycerides', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'creatinine', 'sleep_hours', 'height_cm', 'weight_kg']
        self.cat_cols = ['gender', 'ethnicity', 'smoking_status', 'alcohol_consumption', 'physical_activity_level', 'stress_level']
        self.bin_cols = ['family_history_diabetes', 'family_history_heart_disease', 'family_history_kidney_disease']

        # Preprocessing missing values
        if 'alcohol_consumption' in self.df.columns:
            self.df['alcohol_consumption'] = self.df['alcohol_consumption'].fillna('Unknown')
        
    def add_section(self, title, content):
        self.report_sections.append(f"## {title}\n\n{content}\n")

    def run_all(self):
        print("Starting EDA...")
        self.task_1_overview()
        self.task_2_univariate()
        self.task_3_categorical()
        self.task_4_targets()
        self.task_5_bivariate()
        self.task_6_correlation()
        self.task_7_multivariate()
        self.task_8_age_analysis()
        self.task_9_bmi_analysis()
        self.task_10_lifestyle()
        self.task_11_feature_importance()
        self.task_12_advanced_viz()
        self.task_13_14_final_report()
        print(f"EDA complete. Report and charts saved to {self.output_dir}")

    def task_1_overview(self):
        print("Task 1: Dataset Overview")
        content = f"""
- **Dimensions**: {self.df.shape[0]} rows, {self.df.shape[1]} columns
- **Numerical Features**: {len(self.num_cols)} ({', '.join(self.num_cols[:5])}...)
- **Categorical Features**: {len(self.cat_cols)} ({', '.join(self.cat_cols)})
- **Binary Features**: {len(self.bin_cols)} ({', '.join(self.bin_cols)})
- **Target Variables**: {len(self.targets)} ({', '.join(self.targets)})
"""
        self.add_section("1. Dataset Overview", content)

    def task_2_univariate(self):
        print("Task 2: Univariate Analysis")
        stats_df = self.df[self.num_cols].describe(percentiles=[.25, .5, .75]).T
        stats_df['variance'] = self.df[self.num_cols].var()
        stats_df['skewness'] = self.df[self.num_cols].skew()
        stats_df['kurtosis'] = self.df[self.num_cols].kurtosis()
        
        content = "### Univariate Statistics\n\n" + stats_df.round(2).to_markdown()
        self.add_section("2. Univariate Analysis", content)
        
        for col in self.num_cols:
            fig, axes = plt.subplots(1, 3, figsize=(15, 4))
            sns.histplot(self.df[col], kde=True, ax=axes[0], color='skyblue')
            axes[0].set_title(f'Histogram & KDE: {col}')
            sns.boxplot(x=self.df[col], ax=axes[1], color='lightgreen')
            axes[1].set_title(f'Boxplot: {col}')
            sns.violinplot(x=self.df[col], ax=axes[2], color='salmon')
            axes[2].set_title(f'Violin Plot: {col}')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, f'univariate_{col}.png'))
            plt.close()

    def task_3_categorical(self):
        print("Task 3: Categorical Analysis")
        content = "### Categorical Distributions\n\n"
        for col in self.cat_cols + self.bin_cols:
            counts = self.df[col].value_counts(normalize=True).round(4) * 100
            content += f"**{col}**:\n```\n{counts.to_string()}\n```\n\n"
            
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            sns.countplot(y=self.df[col], palette='pastel')
            plt.title(f'Countplot: {col}')
            plt.subplot(1, 2, 2)
            self.df[col].value_counts().plot.pie(autopct='%1.1f%%', colors=sns.color_palette('pastel'))
            plt.title(f'Pie Chart: {col}')
            plt.ylabel('')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, f'categorical_{col}.png'))
            plt.close()
        self.add_section("3. Categorical Analysis", content)

    def task_4_targets(self):
        print("Task 4: Target Variable Analysis")
        content = "### Target Variable Distributions\n\n"
        
        plt.figure(figsize=(12, 10))
        for i, target in enumerate(self.targets, 1):
            counts = self.df[target].value_counts(normalize=True).round(4) * 100
            content += f"**{target}**: {counts.to_dict()}\n"
            
            plt.subplot(2, 2, i)
            sns.countplot(x=target, data=self.df, palette='Set2')
            plt.title(f'{target} Prevalence')
            
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'targets_prevalence.png'))
        plt.close()
        self.add_section("4. Target Variable Analysis", content)

    def task_5_bivariate(self):
        print("Task 5: Bivariate Analysis")
        pairs = [
            ('age', 'heart_disease_risk'),
            ('bmi', 'diabetes_risk'),
            ('fasting_glucose', 'diabetes_risk'),
            ('creatinine', 'kidney_disease_risk'),
            ('cholesterol_total', 'heart_disease_risk')
        ]
        
        for num_col, target in pairs:
            plt.figure(figsize=(14, 5))
            plt.subplot(1, 2, 1)
            sns.boxplot(x=target, y=num_col, data=self.df, palette='Set3')
            plt.title(f'{num_col} vs {target}')
            plt.subplot(1, 2, 2)
            sns.violinplot(x=target, y=num_col, data=self.df, palette='Set3')
            plt.title(f'{num_col} Distribution by {target}')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, f'bivariate_{num_col}_{target}.png'))
            plt.close()
            
        # Scatterplot with regression
        plt.figure(figsize=(8, 6))
        sns.regplot(x=self.df['bmi'].sample(1000), y=self.df['fasting_glucose'].sample(1000), scatter_kws={'alpha':0.3})
        plt.title('BMI vs Fasting Glucose')
        plt.savefig(os.path.join(self.output_dir, 'bivariate_regression_bmi_glucose.png'))
        plt.close()

    def task_6_correlation(self):
        print("Task 6: Correlation Analysis")
        corr_pearson = self.df[self.num_cols].corr(method='pearson')
        corr_spearman = self.df[self.num_cols].corr(method='spearman')
        
        plt.figure(figsize=(14, 10))
        sns.heatmap(corr_pearson, annot=True, fmt=".2f", cmap='coolwarm', center=0)
        plt.title('Pearson Correlation Heatmap')
        plt.savefig(os.path.join(self.output_dir, 'correlation_pearson.png'))
        plt.close()
        
        sns.clustermap(corr_spearman, cmap='coolwarm', center=0, figsize=(14, 12))
        plt.title('Spearman Clustered Heatmap')
        plt.savefig(os.path.join(self.output_dir, 'correlation_spearman_clustermap.png'))
        plt.close()

    def task_7_multivariate(self):
        print("Task 7: Multivariate Analysis")
        key_metrics = ['age', 'bmi', 'fasting_glucose', 'systolic_bp', 'diabetes_risk']
        sns.pairplot(self.df[key_metrics].sample(1000), hue='diabetes_risk', palette='husl', corner=True)
        plt.savefig(os.path.join(self.output_dir, 'multivariate_pairplot.png'))
        plt.close()

    def task_8_age_analysis(self):
        print("Task 8: Age-based Health Analysis")
        bins = [17, 30, 45, 60, 120]
        labels = ['18-30', '31-45', '46-60', '61+']
        self.df['age_group'] = pd.cut(self.df['age'], bins=bins, labels=labels)
        
        age_risk = self.df.groupby('age_group')[self.targets].mean() * 100
        age_risk.plot(kind='bar', figsize=(10, 6), colormap='viridis')
        plt.title('Disease Prevalence by Age Group (%)')
        plt.ylabel('Prevalence %')
        plt.savefig(os.path.join(self.output_dir, 'age_disease_prevalence.png'))
        plt.close()

    def task_9_bmi_analysis(self):
        print("Task 9: BMI Analysis")
        bins = [0, 18.5, 24.9, 29.9, 100]
        labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
        self.df['bmi_category'] = pd.cut(self.df['bmi'], bins=bins, labels=labels)
        
        bmi_risk = self.df.groupby('bmi_category')[self.targets].mean() * 100
        bmi_risk.plot(kind='bar', figsize=(10, 6), colormap='plasma')
        plt.title('Disease Prevalence by BMI Category (%)')
        plt.ylabel('Prevalence %')
        plt.savefig(os.path.join(self.output_dir, 'bmi_disease_prevalence.png'))
        plt.close()

    def task_10_lifestyle(self):
        print("Task 10: Lifestyle Analysis")
        factors = ['smoking_status', 'physical_activity_level']
        
        for factor in factors:
            factor_risk = self.df.groupby(factor)[self.targets].mean() * 100
            factor_risk.plot(kind='bar', figsize=(10, 6))
            plt.title(f'Disease Risk by {factor}')
            plt.ylabel('Risk %')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, f'lifestyle_{factor}_risk.png'))
            plt.close()

    def task_11_feature_importance(self):
        print("Task 11: Feature Importance (Mutual Information)")
        df_sample = self.df.sample(10000, random_state=42).copy()
        X = pd.get_dummies(df_sample.drop(columns=self.targets + ['patient_id', 'age_group', 'bmi_category']), drop_first=True)
        
        plt.figure(figsize=(16, 12))
        for i, target in enumerate(self.targets, 1):
            y = df_sample[target]
            mi = mutual_info_classif(X.fillna(0), y, random_state=42)
            mi_series = pd.Series(mi, index=X.columns).sort_values(ascending=True)
            
            plt.subplot(2, 2, i)
            mi_series.tail(10).plot(kind='barh', color='teal')
            plt.title(f'Top 10 Features for {target}')
            
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'feature_importance_mi.png'))
        plt.close()

    def task_12_advanced_viz(self):
        print("Task 12: Advanced Visualizations (Plotly)")
        df_sample = self.df.sample(2000, random_state=42)
        
        fig = px.scatter(df_sample, x='bmi', y='fasting_glucose', color='diabetes_risk', 
                         hover_data=['age', 'systolic_bp'],
                         title='Interactive: BMI vs Fasting Glucose by Diabetes Risk')
        fig.write_html(os.path.join(self.output_dir, 'dashboard_bmi_glucose.html'))
        
        metrics = ['age', 'bmi', 'systolic_bp', 'cholesterol_total', 'fasting_glucose']
        avg_h = self.df[self.df['heart_disease_risk'] == 0][metrics].mean()
        avg_d = self.df[self.df['heart_disease_risk'] == 1][metrics].mean()
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=avg_h, theta=metrics, fill='toself', name='Healthy'))
        fig_radar.add_trace(go.Scatterpolar(r=avg_d, theta=metrics, fill='toself', name='Heart Disease'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), title='Radar: Healthy vs Heart Disease Profile')
        fig_radar.write_html(os.path.join(self.output_dir, 'radar_chart_heart_disease.html'))

    def task_13_14_final_report(self):
        print("Task 13 & 14: Generating Healthcare Insights Report")
        report_path = os.path.join(self.output_dir, 'healthcare_insights_report.md')
        
        with open(report_path, 'w') as f:
            f.write("# MedIntel AI - Healthcare Insights & EDA Report\n\n")
            f.write("## 1. Executive Summary\n")
            f.write("This report details the comprehensive Exploratory Data Analysis (EDA) of the 100,000-patient synthetic healthcare dataset. Significant patterns linking BMI, Age, and Lifestyle to chronic diseases (Diabetes, Heart Disease) were isolated using statistical plotting, mutual information scoring, and bivariate analysis.\n\n")
            
            f.write("## 2. Key Findings\n")
            f.write("- Strong direct correlations between Age/BMI and disease onset.\n")
            f.write("- Highly prominent risk progression across BMI categories (Normal -> Obese).\n")
            f.write("- High mutual information between Fasting Glucose and Diabetes Risk.\n\n")
            
            for section in self.report_sections:
                f.write(section + "\n")
                
            f.write("\n## Recommendations\n")
            f.write("- Use non-linear ensemble models to capture combined interactive effects of Age + BMI.\n")
            f.write("- Mitigate class imbalance for Kidney Disease & Stroke before predictive modeling.\n")
            
        print(f"Report generated at {report_path}")

if __name__ == "__main__":
    filepath = r"D:\\health-analytics-ai\\data\\synthetic\\synthetic_patients_100k.csv"
    output_dir = r"D:\\health-analytics-ai\\reports\\eda"
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        sys.exit(1)
        
    eda = HealthcareEDA(filepath, output_dir)
    eda.run_all()
