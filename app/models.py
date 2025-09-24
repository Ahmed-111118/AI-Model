from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    age: int
    height_cm: float
    weight_kg: float
    gender: str
    activity_level: str
    goal: str

class UserResponse(BaseModel):
    id: int
    email: str
    age: int
    height_cm: float
    weight_kg: float
    gender: str
    activity_level: str
    goal: str
