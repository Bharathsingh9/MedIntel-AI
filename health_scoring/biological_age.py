class BiologicalAgeEstimator:
    @staticmethod
    def estimate(chronological_age, bmi, sbp, smoking, activity, sleep):
        bio_age = chronological_age
        
        # Penalties for negative health markers
        if bmi > 25: bio_age += (bmi - 25) * 0.5
        if sbp > 120: bio_age += (sbp - 120) * 0.1
        if smoking == 'Current': bio_age += 5
        elif smoking == 'Former': bio_age += 2
        
        # Deductions for healthy habits
        if activity == 'Active': bio_age -= 3
        if 7 <= sleep <= 8: bio_age -= 1
        
        return int(round(bio_age))
