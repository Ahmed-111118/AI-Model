from fastapi import APIRouter
from app.services.nutrition import calculate_macros

router = APIRouter(prefix="/plans", tags=["Plans"])

@router.post("/calculate")
def calculate_plan(age: int, height_cm: float, weight_kg: float, gender: str, activity_level: str, goal: str):
    return calculate_macros(age, height_cm, weight_kg, gender, activity_level, goal)
