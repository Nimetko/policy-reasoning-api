from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from reasoning import run_reasoning

app = FastAPI()

# ✅ Enable CORS for frontend integrations (e.g., Lovable.dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can change this to ["https://lovable.dev"] for stricter access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request schema using Pydantic
class ReasoningRequest(BaseModel):
    case_name: str
    data: List[Dict]

# ✅ Root route (optional health check)
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# ✅ Main reasoning endpoint with logging and dropdown-safe case_name support
@app.post("/reasoning-query")
def analyze(request: ReasoningRequest):
    print("📎 case_name:", request.case_name)
    print("📎 data:", request.data)

    # 🔄 Accepts both display names and kebab-case variants
    case_map = {
        "Policy Analysis": "Policy Analysis",
        "Clause Rejections": "Clause Rejections",
        "Department Delays": "Department Delays",
        "Multi-Department Impact": "Multi-Department Impact",
        "AI Regulation Bottlenecks": "AI Regulation Bottlenecks",
        "policy-analysis": "Policy Analysis",
        "clause-rejections": "Clause Rejections",
        "department-delays": "Department Delays",
        "multi-department-impact": "Multi-Department Impact",
        "ai-regulation-bottlenecks": "AI Regulation Bottlenecks"
    }

    # 🧠 Normalize and match case name
    raw = request.case_name.strip()
    mapped = case_map.get(raw, case_map.get(raw.lower().replace(" ", "-")))

    if not mapped:
        raise ValueError(f"Unknown case_name: {request.case_name}")

    return run_reasoning(mapped, request.data)
