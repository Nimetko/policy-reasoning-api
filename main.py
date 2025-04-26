from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from reasoning import run_reasoning
from load_data import load_policy_data_from_csv
from supabase_logger import log_reasoning_to_supabase
import os
from openai import OpenAI

# Load OpenAI API key once at startup
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize FastAPI application
app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing) to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin; change to specific origin in production
    allow_credentials=True,
    allow_methods=["*"],   # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],   # Allow all HTTP headers
)

# Define data model for structured reasoning requests
class ReasoningRequest(BaseModel):
    case_name: str        # The name of the case study or analysis type
    data: List[Dict]      # A list of event data in dictionary form

# Endpoint for running structured reasoning analysis
@app.post("/reasoning-query")
def analyze(request: ReasoningRequest):
    print("📎 case_name:", request.case_name)
    print("📎 data:", request.data)

    # Normalize input to match internal mapping keys
    key = request.case_name.strip().lower().replace(" ", "-")

    # Predefined map linking case keys to full case names
    case_map = {
        "policy-analysis": "Policy Analysis",
        "clause-rejections": "Clause Rejections",
        "department-delays": "Department Delays",
        "multi-department-impact": "Multi-Department Impact",
        "ai-regulation-bottlenecks": "AI Regulation Bottlenecks"
    }

    # Check if the provided case name is recognized
    if key not in case_map:
        raise ValueError(f"Unknown case_name: {request.case_name}")

    # Get the mapped full case name
    mapped_case = case_map[key]

    # Run reasoning function using provided data and mapped case name
    result = run_reasoning(mapped_case, request.data)

    # Log the reasoning result to Supabase for later retrieval and analysis
    log_reasoning_to_supabase(
        case_name=mapped_case,
        process=result.get("process", ""),
        kg=result.get("kg", ""),
        causal=result.get("causal", ""),
        source="lovable"  # Tag the source for this request
    )

    # Return the result of reasoning
    return result

# Endpoint for running a test batch reasoning on predefined CSV data
@app.get("/test-batch-reasoning")
def test_reasoning():
    # Load event data from a local CSV file
    data = load_policy_data_from_csv()
    case_name = "Policy Analysis"

    # Run reasoning using the test case name and loaded data
    result = run_reasoning(case_name, data)

    # Log the result tagged as a test
    log_reasoning_to_supabase(
        case_name=case_name,
        process=result.get("process", ""),
        kg=result.get("kg", ""),
        causal=result.get("causal", ""),
        source="test"
    )

    # Return the test reasoning result
    return result

# Define data model for free-form natural language questions
class FreeQuestionRequest(BaseModel):
    question: str  # User's natural language question

# Endpoint for handling exploratory free-form questions
@app.post("/free-question")
def free_question(request: FreeQuestionRequest):
    question = request.question

    # Load policy event data from CSV for context
    data = load_policy_data_from_csv()

    # Format a detailed prompt combining the user's question and policy event logs
    prompt = f"""
    You are a senior policy analyst. Based on the following policy review events, please answer the user's question below in clear, evidence-informed terms.

    Question: {question}

    Event Logs:
    {data}
    """

    # Create a chat completion request to the LLM (Language Model)
    response = openai_client.chat.completions.create(
        model="gpt-4o",  # Use GPT-4o model for better reasoning
        messages=[
            {"role": "system", "content": "You are a helpful policy reasoning assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and return the assistant's response
    return {
        "response": response.choices[0].message.content
    }

# Basic health check endpoint to confirm server is running
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

