from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_reasoning_to_supabase(case_name: str, process: str, kg: str, causal: str, source: str = "lovable"):
    try:
        response = supabase.table("reasoning_logs").insert({
            "case_name": case_name,
            "process": process,
            "kg": kg,
            "causal": causal,
            "source": source
        }).execute()

        print("✅ Logged reasoning to Supabase:", response)
    except Exception as e:
        print("⚠️ Supabase logging failed:", e)
