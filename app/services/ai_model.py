import json
import re
from app.db import get_db_connection
from llama_cpp import Llama

# ✅ Use your new Llama 3 model here
llm = Llama(
    model_path="data/llama-3.2-1b-instruct-q4_k_m.gguf",
    n_ctx=2048,
    n_threads=6
)

# --- Helpers ---
def calculate_bmr(age, height_cm, weight_kg, gender):
    """Mifflin-St Jeor Equation"""
    if gender.lower() == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

def get_activity_multiplier(level):
    mapping = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }
    return mapping.get(level.lower(), 1.2)


def generate_plan(age, height_cm, weight_kg, gender, activity_level, goal, user_id=None):
    # 1️⃣ Compute macros dynamically
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
        "carbs_g": round(carbs_g, 1)
    }

    # 2️⃣ Build smarter structured prompt
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
Generate a **7-day meal plan** and **7-day workout plan** tailored to the user’s GOAL.

Rules:
- Each day must be different.
- Meals: 3/day if lose or maintain, 4/day if gain.
- Workouts: 3-5 exercises/day.
- Focus on the goal (hypertrophy, fat loss, or balance).

📤 Respond ONLY with valid JSON between BEGIN_JSON and END_JSON.
Do not include any explanations, comments, or extra text.

FORMAT:
BEGIN_JSON
{{
  "meal_plan": [
    {{
      "day": 1,
      "meals": [
        {{"meal_time": "breakfast", "food": "Oats with berries"}},
        {{"meal_time": "lunch", "food": "Grilled chicken with rice"}},
        {{"meal_time": "dinner", "food": "Salmon with broccoli"}}
      ]
    }}
  ],
  "workout_plan": [
    {{
      "day": 1,
      "exercises": [
        {{"name": "Squats", "sets": 3, "reps": "8-12"}},
        {{"name": "Push-ups", "sets": 3, "reps": "15"}}
      ]
    }}
  ]
}}
END_JSON
"""

    def ask_model(prompt_text):
        """Call model and try to parse JSON."""
        output = llm(prompt_text, max_tokens=1400, temperature=0.4, stop=["</s>"])
        raw_text = output["choices"][0]["text"].strip()
        print("🔎 RAW MODEL OUTPUT:\n", raw_text)


        match = re.search(r'BEGIN_JSON(.*?)END_JSON', raw_text, re.S)
        if not match:
            return None

        candidate = match.group(1).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # Cleanup common JSON mistakes
            candidate = candidate.replace("```", "").replace("\n", "").strip().rstrip(",")
            try:
                return json.loads(candidate)
            except:
                return None

    # 3️⃣ Try twice: if first fails, retry with stricter instructions
    ideas = ask_model(prompt)
    if ideas is None:
        retry_prompt = prompt + "\n⚠️ STRICT: DO NOT OUTPUT ANYTHING EXCEPT VALID JSON."
        ideas = ask_model(retry_prompt)

    # 4️⃣ Fallback if still fails
    if ideas is None:
        ideas = {"meal_plan": [], "workout_plan": [], "error": "Fallback used (model returned invalid JSON)"}

    # 5️⃣ Final response
    response_json = {
        "macros": macros,
        "meal_plan": ideas.get("meal_plan", []),
        "workout_plan": ideas.get("workout_plan", []),
        "duration_weeks": 8
    }

    # 6️⃣ Save to MySQL
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
            "Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"
        )
    )
    conn.commit()
    cursor.close()
    conn.close()

    return response_json
