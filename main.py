from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from reasoning import run_reasoning
from load_data import load_policy_data_from_csv
from supabase_logger import log_reasoning_to_supabase  # ✅ Supabase logger

app = FastAPI()

# ✅ Enable CORS for Lovable.dev or other frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["https://lovable.dev"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Pydantic schema for POST input
class ReasoningRequest(BaseModel):
    case_name: str
    data: List[Dict]

# ✅ Root health check
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# ✅ Reasoning route used by Lovable
@app.post("/reasoning-query")
def analyze(request: ReasoningRequest):
    print("📎 case_name:", request.case_name)
    print("📎 data:", request.data)

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
    result = run_reasoning(mapped_case, request.data)

    # ✅ Log result to Supabase
    log_reasoning_to_supabase(
        case_name=mapped_case,
        process=result.get("process", ""),
        kg=result.get("kg", ""),
        causal=result.get("causal", ""),
        source="lovable"
    )

    return result

# ✅ Route to test CSV data via batch reasoning
@app.get("/test-batch-reasoning")
def test_reasoning():
    data = load_policy_data_from_csv()
    case_name = "Policy Analysis"
    result = run_reasoning(case_name, data)

    # ✅ Log batch result to Supabase
    log_reasoning_to_supabase(
        case_name=case_name,
        process=result.get("process", ""),
        kg=result.get("kg", ""),
        causal=result.get("causal", ""),
        source="test"
    )

    return result
