import pandas as pd

def load_policy_data_from_csv():
    cases_df = pd.read_csv("Policy_Analysis_Cases.csv")
    events_df = pd.read_csv("Policy_Analysis_Events.csv")

    # Join metadata if needed later — for now, use events only
    merged = events_df.sort_values(by=["case_id", "timestamp"])

    # Convert to list of dicts for FastAPI
    data_records = merged.to_dict(orient="records")

    return data_records
