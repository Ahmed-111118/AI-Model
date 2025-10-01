from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List
from app.db import get_db_connection

router = APIRouter(prefix="/users", tags=["Users"])


# --- Pydantic Models ---
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    age: int = Field(..., gt=0, description="Age of the user")
    height_cm: float = Field(..., gt=0, description="Height in centimeters")
    weight_kg: float = Field(..., gt=0, description="Weight in kilograms")
    gender: str = Field(..., description="Gender: male or female")
    activity_level: str = Field(..., description="Activity level: sedentary, light, moderate, active, very_active")
    goal: str = Field(..., description="Goal: lose, gain, or maintain")


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    age: int
    height_cm: float
    weight_kg: float
    gender: str
    activity_level: str
    goal: str


# --- Routes ---

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    """
    👤 Create a new user in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if email already exists
    cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    # Insert new user
    cursor.execute(
        """
        INSERT INTO users (email, age, height_cm, weight_kg, gender, activity_level, goal)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            user.email,
            user.age,
            user.height_cm,
            user.weight_kg,
            user.gender,
            user.activity_level,
            user.goal,
        ),
    )
    conn.commit()
    new_id = cursor.lastrowid

    # Retrieve the created user
    cursor.execute(
        "SELECT id, email, age, height_cm, weight_kg, gender, activity_level, goal FROM users WHERE id = %s",
        (new_id,),
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=500, detail="Failed to create user")

    return row


@router.get("/", response_model=List[UserResponse])
def list_users():
    """
    📋 Get a list of all users in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, email, age, height_cm, weight_kg, gender, activity_level, goal FROM users")
    users = cursor.fetchall()
    conn.close()

    return users
