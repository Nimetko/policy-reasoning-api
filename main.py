from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from reasoning import run_reasoning

app = FastAPI()

# ✅ Allow frontend access (e.g., Lovable.dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["https://lovable.dev"] later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Expected request structure
class ReasoningRequest(BaseModel):
    case_name: str
    data: List[Dict]

# ✅ Root route
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# ✅ Reasoning endpoint with case_name normalization
@app.post("/reasoning-query")
def analyze(request: ReasoningRequest):
    print("📎 case_name:", request.case_name)
    print("📎 data:", request.data)

    # 🔄 Normalize to lowercase-hyphen format
    key = request.case_name.strip().lower().replace(" ", "-")

    # 🧠 Map all formats to internal GPT-ready names
    case_map = {
        "policy-analysis": "Policy Analysis",
        "clause-rejections": "Clause Rejections",
        "department-delays": "Department Delays",
        "multi-department-impact": "Multi-Department Impact",
        "ai-regulation-bottlenecks": "AI Regulation Bottlenecks"
    }

    if key not in case_map:
        raise ValueError(f"Unknown case_name: {request.case_name}")

    mapped_case = case_map[key]
    return run_reasoning(mapped_case, request.data)
