"""
Workout Plan Service
--------------------
This module provides workout plan generation based on user goals
even if the AI model is unavailable. It can be used as a fallback
or a standalone plan generator.

Usage:
    from app.services.workout import generate_workout_plan

    plan = generate_workout_plan(goal="gain", weeks=8)
"""

def generate_workout_plan(goal: str, weeks: int = 8):
    """
    Generate a default workout plan for the given goal.
    
    Args:
        goal (str): "lose", "maintain", or "gain"
        weeks (int): Duration in weeks (default: 8)

    Returns:
        list[dict]: A 7-day workout plan template.
    """
    goal = goal.lower()

    # Define exercises by category
    strength_exercises = [
        {"name": "Squats", "sets": 4, "reps": "8-12"},
        {"name": "Deadlifts", "sets": 4, "reps": "6-10"},
        {"name": "Bench Press", "sets": 4, "reps": "8-12"},
        {"name": "Overhead Press", "sets": 3, "reps": "10-12"},
        {"name": "Barbell Row", "sets": 4, "reps": "8-12"},
    ]

    fat_loss_exercises = [
        {"name": "Jump Rope", "sets": 4, "duration": "2 min"},
        {"name": "Burpees", "sets": 3, "reps": "20"},
        {"name": "Mountain Climbers", "sets": 3, "reps": "30"},
        {"name": "Bodyweight Squats", "sets": 4, "reps": "20"},
        {"name": "Push-ups", "sets": 4, "reps": "15"},
    ]

    balanced_exercises = [
        {"name": "Lunges", "sets": 3, "reps": "12-15"},
        {"name": "Incline Push-ups", "sets": 3, "reps": "15"},
        {"name": "Lat Pulldown", "sets": 3, "reps": "10-12"},
        {"name": "Plank", "sets": 3, "duration": "1 min"},
        {"name": "Dumbbell Curls", "sets": 3, "reps": "12"},
    ]

    # Pick based on goal
    if goal == "gain":
        chosen = strength_exercises
    elif goal == "lose":
        chosen = fat_loss_exercises
    else:
        chosen = balanced_exercises

    # Build a 7-day plan
    workout_plan = []
    for day in range(1, 8):
        workout_plan.append({
            "day": day,
            "exercises": chosen[:5]  # pick first 5 (or customize)
        })

    return {
        "duration_weeks": weeks,
        "workout_plan": workout_plan
    }

# ✅ Optional: if run directly, show a preview
if __name__ == "__main__":
    import json
    print(json.dumps(generate_workout_plan("gain"), indent=2))
