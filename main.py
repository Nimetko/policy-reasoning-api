from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from reasoning import run_reasoning
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# ✅ Enable CORS to allow requests from Lovable.dev (or anywhere during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with ["https://lovable.dev"] for stricter access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔧 Request schema
class ReasoningRequest(BaseModel):
    case_name: str
    data: List[Dict]

# 🔄 Basic root route
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# 🧠 Main reasoning endpoint
@app.post("/reasoning-query")
def analyze(request: ReasoningRequest):
    result = run_reasoning(request.case_name, request.data)
    return result
