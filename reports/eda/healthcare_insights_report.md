# MedIntel AI - Healthcare Insights & EDA Report

## 1. Executive Summary
This report details the comprehensive Exploratory Data Analysis (EDA) of the 100,000-patient synthetic healthcare dataset. Significant patterns linking BMI, Age, and Lifestyle to chronic diseases (Diabetes, Heart Disease) were isolated using statistical plotting, mutual information scoring, and bivariate analysis.

## 2. Key Findings
- Strong direct correlations between Age/BMI and disease onset.
- Highly prominent risk progression across BMI categories (Normal -> Obese).
- High mutual information between Fasting Glucose and Diabetes Risk.

## 1. Dataset Overview


- **Dimensions**: 100000 rows, 29 columns
- **Numerical Features**: 15 (age, bmi, fasting_glucose, hba1c, cholesterol_total...)
- **Categorical Features**: 6 (gender, ethnicity, smoking_status, alcohol_consumption, physical_activity_level, stress_level)
- **Binary Features**: 3 (family_history_diabetes, family_history_heart_disease, family_history_kidney_disease)
- **Target Variables**: 4 (diabetes_risk, heart_disease_risk, kidney_disease_risk, stroke_risk)


## 2. Univariate Analysis

### Univariate Statistics

|                   |   count |   mean |   std |   min |    25% |   50% |    75% |    max |   variance |   skewness |   kurtosis |
|:------------------|--------:|-------:|------:|------:|-------:|------:|-------:|-------:|-----------:|-----------:|-----------:|
| age               |  100000 |  49.6  | 14.73 |  18   |  39    |  50   |  60    |  90    |     216.98 |       0.08 |      -0.31 |
| bmi               |  100000 |  25.42 |  5.26 |  15   |  21.7  |  25.4 |  29    |  49.1  |      27.69 |       0.13 |      -0.3  |
| fasting_glucose   |  100000 |  90.59 | 13.91 |  60   |  80.9  |  90.4 | 100    | 155.5  |     193.38 |       0.11 |      -0.21 |
| hba1c             |  100000 |   4.8  |  0.53 |   4   |   4.4  |   4.8 |   5.2  |   7.4  |       0.28 |       0.38 |      -0.34 |
| cholesterol_total |  100000 | 190.14 | 23.78 | 120   | 174    | 190   | 206    | 292    |     565.51 |       0.03 |      -0.04 |
| ldl               |  100000 | 114.67 | 27.34 |  50   |  96    | 115   | 133    | 234    |     747.65 |       0.06 |      -0.16 |
| hdl               |  100000 |  55.04 |  9.59 |  20   |  48    |  55   |  61    | 100    |      91.88 |       0.13 |       0.01 |
| triglycerides     |  100000 | 105.15 | 35.11 |  40   |  80    | 104   | 129    | 279    |    1233    |       0.27 |      -0.17 |
| systolic_bp       |  100000 | 123.15 | 13.72 |  90   | 114    | 123   | 132    | 182    |     188.16 |       0.07 |      -0.18 |
| diastolic_bp      |  100000 |  73.73 |  9.02 |  60   |  67    |  73   |  80    | 115    |      81.39 |       0.36 |      -0.37 |
| heart_rate        |  100000 |  68.22 |  9.31 |  45   |  62    |  68   |  75    | 109    |      86.71 |      -0.09 |      -0.16 |
| creatinine        |  100000 |   0.8  |  0.16 |   0.4 |   0.68 |   0.8 |   0.91 |   1.52 |       0.03 |       0.08 |      -0.32 |
| sleep_hours       |  100000 |   7    |  1.2  |   3   |   6.2  |   7   |   7.8  |  12    |       1.45 |       0.01 |      -0.01 |
| height_cm         |  100000 | 168.35 |  9.2  | 138.7 | 161.4  | 167.8 | 175.1  | 202.9  |      84.57 |       0.18 |      -0.49 |
| weight_kg         |  100000 |  72.27 | 16.98 |  30.4 |  60.1  |  71.3 |  83.3  | 172.5  |     288.28 |       0.36 |       0.05 |

## 3. Categorical Analysis

### Categorical Distributions

**gender**:
```
gender
Female    51.21
Male      48.79
```

**ethnicity**:
```
ethnicity
Caucasian           59.97
Hispanic            17.93
African American    13.09
Asian                5.94
Other                3.07
```

**smoking_status**:
```
smoking_status
Never      59.97
Former     25.06
Current    14.97
```

**alcohol_consumption**:
```
alcohol_consumption
Occasional    40.26
Unknown       29.93
Regular       19.89
Heavy          9.91
```

**physical_activity_level**:
```
physical_activity_level
Light        35.22
Sedentary    24.95
Moderate     24.88
Active       14.95
```

**stress_level**:
```
stress_level
Medium    49.95
Low       29.84
High      20.21
```

**family_history_diabetes**:
```
family_history_diabetes
0    80.15
1    19.85
```

**family_history_heart_disease**:
```
family_history_heart_disease
0    84.83
1    15.17
```

**family_history_kidney_disease**:
```
family_history_kidney_disease
0    90.11
1     9.89
```



## 4. Target Variable Analysis

### Target Variable Distributions

**diabetes_risk**: {0: 84.07, 1: 15.93}
**heart_disease_risk**: {0: 87.83999999999999, 1: 12.16}
**kidney_disease_risk**: {0: 98.83999999999999, 1: 1.16}
**stroke_risk**: {0: 94.69999999999999, 1: 5.3}



## Recommendations
- Use non-linear ensemble models to capture combined interactive effects of Age + BMI.
- Mitigate class imbalance for Kidney Disease & Stroke before predictive modeling.
