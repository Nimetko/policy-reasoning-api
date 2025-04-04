from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from reasoning import run_reasoning
from load_data import load_policy_data_from_csv
from supabase_logger import log_reasoning_to_supabase
import os
from openai import OpenAI

app = FastAPI()

# ✅ Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Lovable URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ POST /reasoning-query (structured query)
class ReasoningRequest(BaseModel):
    case_name: str
    data: List[Dict]

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

    log_reasoning_to_supabase(
        case_name=mapped_case,
        process=result.get("process", ""),
        kg=result.get("kg", ""),
        causal=result.get("causal", ""),
        source="lovable"
    )

    return result

# ✅ GET /test-batch-reasoning (batch analysis on CSV)
@app.get("/test-batch-reasoning")
def test_reasoning():
    data = load_policy_data_from_csv()
    case_name = "Policy Analysis"
    result = run_reasoning(case_name, data)

    log_reasoning_to_supabase(
        case_name=case_name,
        process=result.get("process", ""),
        kg=result.get("kg", ""),
        causal=result.get("causal", ""),
        source="test"
    )

    return result

# ✅ POST /free-question (exploratory natural language query)
class FreeQuestionRequest(BaseModel):
    question: str

@app.post("/free-question")
def free_question(request: FreeQuestionRequest):
    question = request.question
    data = load_policy_data_from_csv()

    prompt = f"""
    You are a senior policy analyst. Based on the following policy review events, please answer the user's question below in clear, evidence-informed terms.

    Question: {question}

    Event Logs:
    {data}
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful policy reasoning assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "response": response.choices[0].message.content
    }

# ✅ Health check route
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}
