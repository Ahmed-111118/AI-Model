from fastapi import APIRouter, Query, HTTPException
from app.services.ai_model import generate_plan

router = APIRouter()

@router.get("/generate")
def generate(
    age: int = Query(..., description="User age in years", ge=10, le=100),
    height_cm: float = Query(..., description="Height in cm", gt=50, lt=250),
    weight_kg: float = Query(..., description="Weight in kg", gt=20, lt=300),
    gender: str = Query(..., description="Gender: male/female/other"),
    activity_level: str = Query(..., description="Activity level: sedentary/light/moderate/active/very_active"),
    goal: str = Query(..., description="Goal: lose/maintain/gain"),
    user_id: int = Query(None, description="Optional user ID for DB logging")
):
    # Basic validation
    gender = gender.lower()
    if gender not in ["male", "female", "other"]:
        raise HTTPException(status_code=400, detail="Invalid gender. Use male, female, or other.")
    
    activity_level = activity_level.lower()
    if activity_level not in ["sedentary", "light", "moderate", "active", "very_active"]:
        raise HTTPException(status_code=400, detail="Invalid activity_level. Use sedentary, light, moderate, active, very_active.")
    
    goal = goal.lower()
    if goal not in ["lose", "maintain", "gain"]:
        raise HTTPException(status_code=400, detail="Invalid goal. Use lose, maintain, or gain.")

    # Generate plan
    result = generate_plan(age, height_cm, weight_kg, gender, activity_level, goal, user_id)
    
    return {"plan": result}
