from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.nutrition import calculate_macros

router = APIRouter(prefix="/plans", tags=["Plans"])


class PlanRequest(BaseModel):
    age: int = Field(..., gt=0)
    height_cm: float = Field(..., gt=0)
    weight_kg: float = Field(..., gt=0)
    gender: str
    activity_level: str
    goal: str


class PlanResponse(BaseModel):
    bmr: float
    tdee: float
    calories: float
    protein_g: float
    fat_g: float
    carbs_g: float
    meal_plan: list[str]
    workout_plan: list[str]


@router.post("/calculate", response_model=PlanResponse)
def calculate_plan(data: PlanRequest):
    macros = calculate_macros(
        age=data.age,
        height_cm=data.height_cm,
        weight_kg=data.weight_kg,
        gender=data.gender,
        activity_level=data.activity_level,
        goal=data.goal
    )

    # 🧮 Split daily macros into meals
    breakfast_cal = macros["calories"] * 0.25
    lunch_cal = macros["calories"] * 0.35
    dinner_cal = macros["calories"] * 0.30
    snack_cal = macros["calories"] * 0.10

    # 🍳 Estimate food portions using calorie density
    # (approx values: chicken ~ 165 kcal per 100g, oats ~ 380 kcal per 100g, etc.)
    breakfast_oats_g = round((breakfast_cal * 0.4) / 3.8)  # ~40% oats
    breakfast_eggs_g = round((breakfast_cal * 0.3) / 1.55) # ~30% eggs
    breakfast_fruit_g = round((breakfast_cal * 0.3) / 0.52) # ~30% fruits

    lunch_chicken_g = round((lunch_cal * 0.5) / 1.65)
    lunch_rice_g = round((lunch_cal * 0.35) / 3.6)
    lunch_veggies_g = round((lunch_cal * 0.15) / 0.5)

    dinner_fish_g = round((dinner_cal * 0.5) / 2.0)
    dinner_pasta_g = round((dinner_cal * 0.35) / 3.5)
    dinner_salad_g = round((dinner_cal * 0.15) / 0.4)

    snack_nuts_g = round((snack_cal * 0.6) / 6.0)
    snack_fruit_g = round((snack_cal * 0.4) / 0.52)

    # 🍱 Build personalized meal plan
    meal_plan = [
        f"🍳 Breakfast: {breakfast_oats_g}g oats + {breakfast_eggs_g}g eggs + {breakfast_fruit_g}g fruits",
        f"🥗 Lunch: {lunch_chicken_g}g grilled chicken + {lunch_rice_g}g brown rice + {lunch_veggies_g}g veggies",
        f"🍝 Dinner: {dinner_fish_g}g baked fish + {dinner_pasta_g}g whole grain pasta + {dinner_salad_g}g salad",
        f"🍏 Snack: {snack_nuts_g}g mixed nuts + {snack_fruit_g}g fruit"
    ]

    # 🏋️‍♂️ Workout plan (still goal-based, but can be dynamic too)
    if data.goal.lower() == "lose":
        workout_plan = [
            "🏃‍♂️ 40 mins cardio + 15 mins HIIT",
            "💪 Full-body resistance training (3x sets)",
            "🧘‍♂️ Mobility + core strengthening"
        ]
    elif data.goal.lower() == "gain":
        workout_plan = [
            "🏋️‍♂️ Heavy push day (Bench, OHP, Dips)",
            "🦵 Leg hypertrophy (Squats, Deadlifts)",
            "💪 Pull workout (Rows, Pullups, Curls)"
        ]
    else:
        workout_plan = [
            "🏋️‍♂️ Full-body strength (3x per week)",
            "🚶‍♂️ Cardio 30 mins",
            "🧘‍♂️ Core + stretching"
        ]

    return {
        **macros,
        "meal_plan": meal_plan,
        "workout_plan": workout_plan
    }
