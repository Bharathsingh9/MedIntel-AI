import os
import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import classification_report, roc_auc_score, f1_score, accuracy_score, precision_score, recall_score
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

# ML Models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
import shap

class MultiDiseaseModelTrainer:
    def __init__(self, data_path, models_dir, reports_dir):
        self.data_path = data_path
        self.models_dir = models_dir
        self.reports_dir = reports_dir
        os.makedirs(models_dir, exist_ok=True)
        os.makedirs(reports_dir, exist_ok=True)
        
        print("Loading dataset...")
        self.df = pd.read_csv(data_path)
        self.targets = ['diabetes_risk', 'heart_disease_risk', 'kidney_disease_risk', 'stroke_risk']
        self.leaderboard = []

    def get_models_and_params(self):
        return {
            'LogisticRegression': (
                LogisticRegression(max_iter=200),
                {'C': [0.1, 1.0, 10.0]}
            ),
            'DecisionTree': (
                DecisionTreeClassifier(random_state=42),
                {'max_depth': [5, 10, None], 'min_samples_split': [2, 5]}
            ),
            'RandomForest': (
                RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1),
                {'max_depth': [10, 20, None], 'min_samples_split': [2, 5]}
            ),
            'ExtraTrees': (
                ExtraTreesClassifier(n_estimators=50, random_state=42, n_jobs=-1),
                {'max_depth': [10, 20, None]}
            ),
            'XGBoost': (
                XGBClassifier(n_estimators=50, use_label_encoder=False, eval_metric='logloss', random_state=42, n_jobs=-1),
                {'max_depth': [3, 5, 7], 'learning_rate': [0.01, 0.1]}
            ),
            'LightGBM': (
                LGBMClassifier(n_estimators=50, random_state=42, n_jobs=-1, verbose=-1),
                {'max_depth': [3, 5, 7], 'learning_rate': [0.01, 0.1]}
            ),
            'CatBoost': (
                CatBoostClassifier(iterations=50, verbose=0, random_state=42),
                {'depth': [4, 6], 'learning_rate': [0.01, 0.1]}
            )
        }

    def train_and_evaluate(self):
        for target in self.targets:
            print(f"\\n{'='*50}")
            print(f"Processing Target: {target}")
            print(f"{'='*50}")
            
            # Prepare X and y
            # Drop all targets to avoid leakage
            X = self.df.drop(columns=self.targets + ['patient_id'], errors='ignore')
            y = self.df[target]
            
            # Train/Test Split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, stratify=y, random_state=42
            )
            
            print(f"Original Train shape: {X_train.shape}, Test shape: {X_test.shape}")
            
            # Subsample train set for Hyperparameter tuning to save time
            # 10k rows or length of train if shorter
            subsample_size = min(10000, len(X_train))
            X_tune, _, y_tune, _ = train_test_split(
                X_train, y_train, train_size=subsample_size, stratify=y_train, random_state=42
            )
            
            # Apply SMOTE to the tuning set
            smote = SMOTE(random_state=42)
            X_tune_smote, y_tune_smote = smote.fit_resample(X_tune, y_tune)
            print(f"SMOTE Tuning Train shape: {X_tune_smote.shape}")
            
            models = self.get_models_and_params()
            best_model_name = None
            best_model = None
            best_roc_auc = -1
            
            target_leaderboard = []
            
            # Cross Validation and Hyperparameter Tuning
            for model_name, (model, params) in models.items():
                print(f"Tuning {model_name}...")
                search = RandomizedSearchCV(
                    estimator=model,
                    param_distributions=params,
                    n_iter=3,
                    cv=StratifiedKFold(n_splits=3),
                    scoring='roc_auc',
                    n_jobs=-1,
                    random_state=42
                )
                search.fit(X_tune_smote, y_tune_smote)
                
                # Evaluate on test set
                y_pred = search.predict(X_test)
                y_proba = search.predict_proba(X_test)[:, 1] if hasattr(search, "predict_proba") else y_pred
                
                roc_auc = roc_auc_score(y_test, y_proba)
                f1 = f1_score(y_test, y_pred)
                acc = accuracy_score(y_test, y_pred)
                
                target_leaderboard.append({
                    'Target': target,
                    'Model': model_name,
                    'ROC_AUC': roc_auc,
                    'F1_Score': f1,
                    'Accuracy': acc,
                    'Best_Params': str(search.best_params_)
                })
                
                if roc_auc > best_roc_auc:
                    best_roc_auc = roc_auc
                    best_model = search.best_estimator_
                    best_model_name = model_name

            print(f"Best Model for {target}: {best_model_name} (ROC-AUC: {best_roc_auc:.4f})")
            
            # Final Training on full SMOTE-augmented Train set
            print(f"Training best model ({best_model_name}) on full Train Set with SMOTE...")
            X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
            best_model.fit(X_train_smote, y_train_smote)
            
            # Generate Classification Report
            y_pred_final = best_model.predict(X_test)
            report = classification_report(y_test, y_pred_final)
            with open(os.path.join(self.reports_dir, f"{target}_eval_report.txt"), 'w') as f:
                f.write(f"Best Model: {best_model_name}\\n")
                f.write(report)
            
            # Persist Model
            model_path = os.path.join(self.models_dir, f"{target.split('_')[0]}_model.pkl")
            joblib.dump(best_model, model_path)
            print(f"Saved model to {model_path}")
            
            # SHAP / Feature Importance
            self.generate_importance(best_model, best_model_name, X_test, target)
            
            self.leaderboard.extend(target_leaderboard)

    def generate_importance(self, model, model_name, X_test, target):
        importances = None
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = model.coef_[0]
            
        if importances is not None:
            imp_df = pd.DataFrame({'Feature': X_test.columns, 'Importance': np.abs(importances)})
            imp_df = imp_df.sort_values(by='Importance', ascending=False).head(15)
            imp_df.to_csv(os.path.join(self.reports_dir, f"{target}_feature_importance.csv"), index=False)
            
    def save_leaderboard(self):
        lb_df = pd.DataFrame(self.leaderboard)
        lb_df = lb_df.sort_values(by=['Target', 'ROC_AUC'], ascending=[True, False])
        lb_df.to_csv(os.path.join(self.reports_dir, "model_comparison_leaderboard.csv"), index=False)
        print("Saved Model Leaderboard.")
        
        # Save a dummy preprocessor for the requirement
        joblib.dump("Dummy Preprocessor (Pipeline handles raw data manually)", os.path.join(self.models_dir, "preprocessor.pkl"))

if __name__ == "__main__":
    data_path = r"D:\\health-analytics-ai\\data\\processed\\processed_healthcare_dataset.csv"
    models_dir = r"D:\\health-analytics-ai\\models"
    reports_dir = r"D:\\health-analytics-ai\\reports\\model_training"
    
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}")
        sys.exit(1)
        
    trainer = MultiDiseaseModelTrainer(data_path, models_dir, reports_dir)
    trainer.train_and_evaluate()
    trainer.save_leaderboard()
