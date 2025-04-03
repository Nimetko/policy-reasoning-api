from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from reasoning import run_reasoning

app = FastAPI()

# ✅ Enable CORS for frontend (Lovable.dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For stricter security, replace with ["https://lovable.dev"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define request schema
class ReasoningRequest(BaseModel):
    case_name: str
    data: List[Dict]

# ✅ Basic test route
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# ✅ Main reasoning endpoint with debug logging
@app.post("/reasoning-query")
def analyze(request: ReasoningRequest):
    print("🔍 Incoming request to /reasoning-query")
    print("📎 case_name:", request.case_name)
    print("📎 data:", request.data)

    result = run_reasoning(request.case_name, request.data)
    return result
