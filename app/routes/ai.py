from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.ai_model import generate_plan

# ✅ Better: add prefix and tags for organization
router = APIRouter(
    prefix="/ai",
    tags=["AI Plan Generator"]
)

@router.get("/generate")
def generate_plan_endpoint(
    age: int = Query(..., description="User age in years", ge=10, le=100),
    height_cm: float = Query(..., description="Height in cm", gt=50, lt=250),
    weight_kg: float = Query(..., description="Weight in kg", gt=20, lt=300),
    gender: str = Query(..., description="Gender: male/female/other"),
    activity_level: str = Query(..., description="Activity level: sedentary/light/moderate/active/very_active"),
    goal: str = Query(..., description="Goal: lose/maintain/gain"),
    user_id: Optional[int] = Query(None, description="Optional user ID for DB logging")
):
    """
    ✅ Generates a personalized diet + workout plan based on user details.
    - Validates all inputs
    - Calls LLaMA model through generate_plan()
    - Returns JSON with macros, meals, and workout plan
    """

    # --- Input validation ---
    gender = gender.lower()
    if gender not in ["male", "female", "other"]:
        raise HTTPException(status_code=400, detail="Invalid gender. Must be: male, female, or other.")
    
    activity_level = activity_level.lower()
    if activity_level not in ["sedentary", "light", "moderate", "active", "very_active"]:
        raise HTTPException(status_code=400, detail="Invalid activity level. Must be: sedentary, light, moderate, active, or very_active.")
    
    goal = goal.lower()
    if goal not in ["lose", "maintain", "gain"]:
        raise HTTPException(status_code=400, detail="Invalid goal. Must be: lose, maintain, or gain.")

    # --- Call the model safely ---
    try:
        plan_result = generate_plan(age, height_cm, weight_kg, gender, activity_level, goal, user_id)
    except Exception as e:
        # Catch any runtime/model errors so the frontend doesn't crash
        raise HTTPException(status_code=500, detail=f"AI plan generation failed: {str(e)}")

    return {
        "status": "success",
        "message": "AI-generated plan created successfully",
        "data": plan_result
    }
