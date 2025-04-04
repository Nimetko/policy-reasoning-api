from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from reasoning import run_reasoning

app = FastAPI()

# ✅ CORS: allow Lovable.dev or any frontend to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For security, later you can restrict to ["https://lovable.dev"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define request schema
class ReasoningRequest(BaseModel):
    case_name: str
    data: List[Dict]

# ✅ Basic root check (optional)
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# ✅ Main reasoning endpoint with debugging and format-safe lookup
@app.post("/reasoning-query")
def analyze(request: ReasoningRequest):
    print("📎 case_name:", request.case_name)
    print("📎 data:", request.data)

    # 🔄 Normalization for case_name input from Lovable.dev
    case_lookup = {
        "policy-analysis": "Policy Analysis",
        "clause-rejections": "Clause Rejections",
        "department-delays": "Department Delays",
        "multi-department-impact": "Multi-Department Impact",
        "ai-regulation-bottlenecks": "AI Regulation Bottlenecks"
    }

    # Convert input like "department-delays" → "Department Delays"
    case = request.case_name.lower().strip().replace(" ", "-")
    if case not in case_lookup:
        raise ValueError(f"Unknown case_name: {request.case_name}")

    # Run reasoning with safe value
    mapped_case = case_lookup[case]
    return run_reasoning(mapped_case, request.data)
