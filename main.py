from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from reasoning import run_reasoning

app = FastAPI()

# ✅ Enable CORS to allow frontend access (e.g., Lovable.dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later: restrict to ["https://lovable.dev"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define expected structure of incoming request
class ReasoningRequest(BaseModel):
    case_name: str
    data: List[Dict]

# ✅ Root test endpoint (optional)
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# ✅ Reasoning endpoint with robust case_name mapping
@app.post("/reasoning-query")
def analyze(request: ReasoningRequest):
    print("📎 case_name:", request.case_name)
    print("📎 data:", request.data)

    # Normalize input to lowercase-hyphenated form
    key = request.case_name.strip().lower().replace(" ", "-")

    # Supported mappings from UI → GPT prompt label
    case_map = {
        "policy-analysis": "Policy Analysis",
        "clause-rejections": "Clause Rejections",
        "department-delays": "Department Delays",
        "multi-department-impact": "Multi-Department Impact",
        "ai-regulation-bottlenecks": "AI Regulation Bottlenecks"
    }

    # Validate and map to GPT prompt label
    if key not in case_map:
        raise ValueError(f"Unknown case_name: {request.case_name}")

    mapped_case = case_map[key]
    return run_reasoning(mapped_case, request.data)
