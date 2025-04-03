from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from reasoning import run_reasoning

app = FastAPI()

# ✅ Add CORS immediately after app is created
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use ["https://lovable.dev"] for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema for the incoming request
class ReasoningRequest(BaseModel):
    case_name: str
    data: List[Dict]

# Root route (optional test)
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# Reasoning API
@app.post("/reasoning-query")
def analyze(request: ReasoningRequest):
    return run_reasoning(request.case_name, request.data)
