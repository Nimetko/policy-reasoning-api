import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_reasoning(case_name, structured_data):
    # Define reasoning prompts for each query type
    reasoning_sets = {
        "Policy Analysis": {
            "process": "Analyze the process flow. Identify any delays, inefficiencies, or bottlenecks based on the data.",
            "kg": "Extract important relationships between actors, clauses, and outcomes from the dataset. What patterns do you notice?",
            "causal": "Determine the most likely causes of policy rejection. What factors contribute to failure?"
        },
        "Department Delays": {
            "process": "Analyze delays between stages. Which actors or departments are most often involved in delayed cases?",
            "kg": "Map relationships between departments and delay frequency. Are delays isolated or systemic across reviewers?",
            "causal": "Does department involvement directly increase rejection or review time? Are there causal patterns?"
        },
        "Clause Rejections": {
            "process": "Identify stages where rejections happen most often due to clause issues.",
            "kg": "Find repeated relationships between specific clauses and negative outcomes. Are certain clauses riskier?",
            "causal": "What clause features most strongly contribute to policy rejection? Are there root causes related to language or scope?"
        },
        "Multi-Department Impact": {
            "process": "Do policies reviewed by more than two departments have longer timelines? Identify any correlation between number of departments involved and review duration.",
            "kg": "Visualise how department count connects to outcome. Are multi-department chains more common in failed cases?",
            "causal": "Does increasing the number of reviewers or departments lead to more rejections? What causal patterns are evident in the data?"
        },
        "AI Regulation Bottlenecks": {
            "process": "Compare review timelines for AI-related policies versus other categories. Are AI policies slower? Highlight any delays linked to specific stages.",
            "kg": "Which actors and clauses are frequently associated with AI policy delays or rejections? Are there recurring patterns?",
            "causal": "Do ethical, legal, or clause-specific concerns in AI-related policies lead to higher rejection rates? Identify possible root causes."
        }
    }

    if case_name not in reasoning_sets:
        raise ValueError(f"Unknown case_name: {case_name}")

    # Get prompts for the selected query
    reasoning_prompts = reasoning_sets[case_name]

    # Shared context message with structured input
    base_message = [
        {"role": "system", "content": "You are an expert in process mining and policy optimisation."},
        {"role": "user", "content": f"The following dataset is from a policy review process:\n\n{structured_data}"}
    ]

    # Build structured response with process, kg, causal perspectives
    result = {}
    for key, follow_up in reasoning_prompts.items():
        full_prompt = base_message + [{"role": "user", "content": follow_up}]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=full_prompt
        )
        result[key] = response.choices[0].message.content

    return result
