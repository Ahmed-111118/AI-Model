from fastapi import APIRouter
from app.db import get_db_connection
from app.models import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        INSERT INTO users (email, age, height_cm, weight_kg, gender, activity_level, goal)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user.email, user.age, user.height_cm, user.weight_kg,
          user.gender, user.activity_level, user.goal))
    conn.commit()
    new_id = cursor.lastrowid

    cursor.execute("SELECT id, email, age, height_cm, weight_kg, gender, activity_level, goal FROM users WHERE id=%s", (new_id,))
    row = cursor.fetchone()
    conn.close()
    return row

@router.get("/", response_model=list[UserResponse])
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, email, age, height_cm, weight_kg, gender, activity_level, goal FROM users")
    users = cursor.fetchall()
    conn.close()
    return users
