from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from reasoning import run_reasoning

app = FastAPI()

class QueryRequest(BaseModel):
    case_name: str
    data: List[Dict]

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.post("/reasoning-query")
def reasoning_query(request: QueryRequest):
    result = run_reasoning(request.case_name, request.data)
    return {
        "process": result["process"],
        "kg": result["kg"],
        "causal": result["causal"]
    }
