import json
import re
from typing import Optional
from llama_cpp import Llama
from app.db import get_db_connection

# ✅ Safely load the LLaMA model
try:
    llm = Llama(
        model_path="data/llama-3.2-1b-instruct-q4_k_m.gguf",
        n_ctx=2048,
        n_threads=4  # better default for most CPUs
    )
    print("✅ LLaMA model loaded successfully.")
except Exception as e:
    print("❌ Failed to load LLaMA model:", e)
    llm = None

# --- Helper functions ---
def calculate_bmr(age: int, height_cm: float, weight_kg: float, gender: str) -> float:
    """Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation."""
    if gender.lower() == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

def get_activity_multiplier(level: str) -> float:
    mapping = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }
    return mapping.get(level.lower(), 1.2)

# --- Core AI Plan Generator ---
def generate_plan(
    age: int,
    height_cm: float,
    weight_kg: float,
    gender: str,
    activity_level: str,
    goal: str,
    user_id: Optional[int] = None
) -> dict:
    """Generate meal + workout plan with macros based on user details."""

    # 1️⃣ Calculate macros
    bmr = calculate_bmr(age, height_cm, weight_kg, gender)
    tdee = bmr * get_activity_multiplier(activity_level)

    if goal == "lose":
        calories = tdee - 500
    elif goal == "gain":
        calories = tdee + 500
    else:
        calories = tdee

    protein_g = weight_kg * 1.8
    fat_g = weight_kg * 0.9
    carbs_g = (calories - (protein_g * 4 + fat_g * 9)) / 4

    macros = {
        "calories": round(calories),
        "protein_g": round(protein_g, 1),
        "fat_g": round(fat_g, 1),
        "carbs_g": round(carbs_g, 1),
    }

    # 2️⃣ Create prompt for LLaMA
    prompt = f"""
You are a professional AI fitness assistant.

USER PROFILE:
- Age: {age}
- Gender: {gender}
- Height: {height_cm} cm
- Weight: {weight_kg} kg
- Activity: {activity_level}
- Goal: {goal}

TASK:
Generate a **7-day meal plan** and **7-day workout plan** tailored to the user's goal.

Rules:
- Each day must be different.
- Meals: 3/day if lose or maintain, 4/day if gain.
- Workouts: 3-5 exercises/day.
- Focus on the goal (hypertrophy, fat loss, or balance).

📤 Respond ONLY with valid JSON between BEGIN_JSON and END_JSON.
Do not include explanations or comments.

FORMAT:
BEGIN_JSON
{{
  "meal_plan": [
    {{
      "day": 1,
      "meals": [
        {{"meal_time": "breakfast", "food": "Oats with berries"}}
      ]
    }}
  ],
  "workout_plan": [
    {{
      "day": 1,
      "exercises": [
        {{"name": "Squats", "sets": 3, "reps": "8-12"}}
      ]
    }}
  ]
}}
END_JSON
"""

    # 3️⃣ Ask the model & parse JSON
    def ask_model(prompt_text: str) -> Optional[dict]:
        if llm is None:
            return None
        try:
            output = llm(prompt_text, max_tokens=1400, temperature=0.4, stop=["</s>"])
            raw_text = output["choices"][0]["text"].strip()
            print("🔎 RAW MODEL OUTPUT:\n", raw_text)

            # Extract JSON between markers
            match = re.search(r'BEGIN_JSON(.*?)END_JSON', raw_text, re.S)
            if not match:
                return None

            candidate = match.group(1).strip()
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                candidate = candidate.replace("```", "").replace("\n", "").strip().rstrip(",")
                return json.loads(candidate)
        except Exception as e:
            print("❌ LLaMA call failed:", e)
            return None

    ideas = ask_model(prompt)
    if ideas is None:
        retry_prompt = prompt + "\n⚠️ STRICT: Output must be valid JSON only."
        ideas = ask_model(retry_prompt)

    if ideas is None:
        ideas = {"meal_plan": [], "workout_plan": [], "error": "Model output invalid – fallback used."}

    # 4️⃣ Build final response
    response_json = {
        "macros": macros,
        "meal_plan": ideas.get("meal_plan", []),
        "workout_plan": ideas.get("workout_plan", []),
        "duration_weeks": 8
    }

    # 5️⃣ Save result to database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO model_requests (user_id, request_json, response_json, model_name)
            VALUES (%s, %s, %s, %s)
            """,
            (
                user_id,
                json.dumps({
                    "age": age, "height_cm": height_cm, "weight_kg": weight_kg,
                    "gender": gender, "activity_level": activity_level, "goal": goal
                }),
                json.dumps(response_json),
                "Meta-Llama-3.2-1B-Instruct-Q4_K_M.gguf"
            )
        )
        conn.commit()
    except Exception as db_error:
        print("⚠️ Failed to log model request to database:", db_error)
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

    return response_json
