class BiologicalAgeEstimator:
    @staticmethod
    def estimate(
        chronological_age: int,
        bmi: float,
        sbp: float,
        smoking: str,
        activity: str,
        sleep: float,
    ) -> int:
        """
        Estimate biological age based on chronological age and health markers.

        Args:
            chronological_age (int): The person's actual age in years.
            bmi (float): Body Mass Index.
            sbp (float): Systolic blood pressure.
            smoking (str): Smoking status ('Current', 'Former', 'Never').
            activity (str): Physical activity level (e.g., 'Active', 'Sedentary').
            sleep (float): Average hours of sleep per night.

        Returns:
            int: The estimated biological age.
        """
        bio_age = float(chronological_age)
        
        # Penalties for negative health markers
        if bmi > 25: bio_age += (bmi - 25) * 0.5
        if sbp > 120: bio_age += (sbp - 120) * 0.1
        if smoking == 'Current': bio_age += 5
        elif smoking == 'Former': bio_age += 2
        
        # Deductions for healthy habits
        if activity == 'Active': bio_age -= 3
        if 7 <= sleep <= 8: bio_age -= 1
        
        return int(round(bio_age))
