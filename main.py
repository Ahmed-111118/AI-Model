from fastapi import FastAPI
from app.routes import users, plans, ai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Add this middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(plans.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "Gym AI Backend running"}
