from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from reasoning import run_reasoning
from load_data import load_policy_data_from_csv  # ✅ CSV loader

app = FastAPI()

# ✅ Enable CORS for Lovable.dev or any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["https://lovable.dev"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request body structure
class ReasoningRequest(BaseModel):
    case_name: str
    data: List[Dict]

# ✅ Health check root
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# ✅ Main reasoning route used by Lovable (POST)
@app.post("/reasoning-query")
def analyze(request: ReasoningRequest):
    print("📎 case_name:", request.case_name)
    print("📎 data:", request.data)

    # Normalize and map dropdown label to internal reasoning prompt name
    key = request.case_name.strip().lower().replace(" ", "-")

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

# ✅ NEW: Route to test full CSV batch reasoning
@app.get("/test-batch-reasoning")
def test_reasoning():
    data = load_policy_data_from_csv()
    case_name = "Policy Analysis"  # You can test other mappings too
    return run_reasoning(case_name, data)
