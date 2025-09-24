def calculate_macros(age, height_cm, weight_kg, gender, activity_level, goal):
    # 1. Calculate BMR
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    # 2. Apply activity multiplier
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    tdee = bmr * multipliers.get(activity_level.lower(), 1.2)

    # 3. Adjust for goal
    if goal == "lose":
        calories = tdee - 500
    elif goal == "gain":
        calories = tdee + 500
    else:
        calories = tdee

    # 4. Macros
    protein_g = weight_kg * 2
    fat_g = (0.25 * calories) / 9
    carbs_g = (calories - (protein_g * 4 + fat_g * 9)) / 4

    return {
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
        "calories": round(calories, 2),
        "protein_g": round(protein_g, 2),
        "fat_g": round(fat_g, 2),
        "carbs_g": round(carbs_g, 2)
    }
