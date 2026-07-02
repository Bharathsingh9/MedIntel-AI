from typing import Union

class ScoringEngine:
    @staticmethod
    def calculate_health_score(diabetes_prob: float, heart_prob: float, kidney_prob: float, stroke_prob: float) -> float:
        """
        Calculate an overall health score based on disease probabilities.

        Args:
            diabetes_prob (float): Probability of diabetes.
            heart_prob (float): Probability of heart disease.
            kidney_prob (float): Probability of kidney disease.
            stroke_prob (float): Probability of stroke.

        Returns:
            float: The calculated health score (0-100).
        """
        # 100 - weighted sum of probabilities (scaled 0-100)
        risk = (0.3 * diabetes_prob + 0.4 * heart_prob + 0.1 * kidney_prob + 0.2 * stroke_prob) * 100
        score = 100 - risk
        return max(0.0, min(100.0, score))

    @staticmethod
    def get_risk_category(score: Union[int, float]) -> str:
        """
        Get the risk category corresponding to a health score.

        Args:
            score (Union[int, float]): The health score.

        Returns:
            str: The risk category ('Critical', 'High Risk', 'Moderate Risk', 'Healthy', 'Excellent').
        """
        if score <= 30: return "Critical"
        elif score <= 60: return "High Risk"
        elif score <= 80: return "Moderate Risk"
        elif score <= 90: return "Healthy"
        else: return "Excellent"

    @staticmethod
    def cardiovascular_score(cholesterol: float, ldl: float, hdl: float, sbp: float, smoking: str, age: int) -> int:
        """
        Calculate cardiovascular health score.

        Args:
            cholesterol (float): Total cholesterol level.
            ldl (float): LDL cholesterol level.
            hdl (float): HDL cholesterol level.
            sbp (float): Systolic blood pressure.
            smoking (str): Smoking status ('Current', 'Former', 'Never').
            age (int): Patient's age in years.

        Returns:
            int: The cardiovascular health score (0-100).
        """
        score = 100
        if cholesterol > 200: score -= 10
        if ldl > 130: score -= 10
        if hdl < 40: score -= 10
        if sbp > 130: score -= 15
        if smoking == 'Current': score -= 20
        elif smoking == 'Former': score -= 5
        if age > 60: score -= 10
        return max(0, min(100, score))

    @staticmethod
    def metabolic_score(bmi: float, glucose: float, hba1c: float, triglycerides: float) -> int:
        """
        Calculate metabolic health score.

        Args:
            bmi (float): Body Mass Index.
            glucose (float): Fasting blood glucose level.
            hba1c (float): HbA1c percentage.
            triglycerides (float): Triglycerides level.

        Returns:
            int: The metabolic health score (0-100).
        """
        score = 100
        if bmi > 25: score -= 10
        if bmi > 30: score -= 15
        if glucose > 100: score -= 15
        if hba1c > 5.7: score -= 15
        if triglycerides > 150: score -= 10
        return max(0, min(100, score))

    @staticmethod
    def lifestyle_score(smoking, alcohol, activity, sleep, stress):
        score = 100
        if smoking == 'Current': score -= 20
        elif smoking == 'Former': score -= 10
        
        if alcohol in ['Regular', 'Heavy']: score -= 15
        
        if activity == 'Sedentary': score -= 20
        elif activity == 'Light': score -= 10
        
        if sleep < 6 or sleep > 9: score -= 15
        
        if stress == 'High': score -= 20
        elif stress == 'Medium': score -= 10
        return max(0, min(100, score))
