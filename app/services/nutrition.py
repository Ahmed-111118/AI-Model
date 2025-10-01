"""
Nutrition Service
-----------------
This module calculates daily calorie and macronutrient needs,
and can optionally generate a simple 7-day meal plan fallback.

Usage:
    from app.services.nutrition import calculate_macros, generate_meal_plan
"""

def calculate_macros(age: int, height_cm: float, weight_kg: float, gender: str, activity_level: str, goal: str):
    """
    Calculate daily calorie and macronutrient requirements.

    Args:
        age (int): Age of the user in years
        height_cm (float): Height in centimeters
        weight_kg (float): Weight in kilograms
        gender (str): "male", "female", or "other"
        activity_level (str): sedentary, light, moderate, active, very_active
        goal (str): "lose", "maintain", or "gain"

    Returns:
        dict: Calculated BMR, TDEE, calories, protein, fat, carbs
    """

    gender = gender.lower()
    if gender not in ["male", "female", "other"]:
        raise ValueError("Invalid gender. Must be 'male', 'female', or 'other'.")

    activity_level = activity_level.lower()
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    if activity_level not in multipliers:
        raise ValueError("Invalid activity_level. Must be sedentary, light, moderate, active, or very_active.")

    goal = goal.lower()
    if goal not in ["lose", "maintain", "gain"]:
        raise ValueError("Invalid goal. Must be lose, maintain, or gain.")

    # 1️⃣ BMR (Mifflin-St Jeor)
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    # 2️⃣ TDEE
    tdee = bmr * multipliers[activity_level]

    # 3️⃣ Goal adjustment
    if goal == "lose":
        calories = tdee - 500
    elif goal == "gain":
        calories = tdee + 500
    else:
        calories = tdee

    # 4️⃣ Macronutrients
    # Adjust protein needs by goal
    if goal == "gain":
        protein_g = weight_kg * 2.0
    elif goal == "lose":
        protein_g = weight_kg * 2.2  # more protein to preserve muscle
    else:
        protein_g = weight_kg * 1.8

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


def generate_meal_plan(goal: str):
    """
    Fallback: Generate a simple 7-day meal plan if the AI model fails.

    Args:
        goal (str): "lose", "maintain", or "gain"

    Returns:
        list[dict]: Meal plan for 7 days.
    """
    goal = goal.lower()
    meals_per_day = 4 if goal == "gain" else 3

    base_meals = [
        "Oatmeal with berries",
        "Grilled chicken with rice and vegetables",
        "Salmon with quinoa and broccoli",
        "Greek yogurt with honey and almonds",
        "Vegetable omelette with toast",
        "Tuna salad with olive oil",
        "Protein smoothie with banana"
    ]

    meal_plan = []
    for day in range(1, 8):
        meals = [{"meal_time": f"Meal {i+1}", "food": base_meals[i % len(base_meals)]} for i in range(meals_per_day)]
        meal_plan.append({"day": day, "meals": meals})

    return meal_plan


# ✅ Quick test when run directly
if __name__ == "__main__":
    print(calculate_macros(25, 175, 70, "male", "moderate", "gain"))
    print(generate_meal_plan("gain"))
