import pandas as pd
import random
from datetime import datetime, timedelta

# Load cases
cases_df = pd.read_csv("Policy_Analysis_Cases.csv")

activities = ["Draft Created", "Committee Review", "Ethics Review", "Legal Review", "Final Approval"]
actors = ["Department A", "Department B", "AI Ethics Committee", "Legal Team", "Regulatory Board"]
outcomes = ["Needs Revision", "In Progress", "Rejected", "Approved"]

# Optional clause snippets for comments (especially for AI Regulation)
clauses = [
    "Clause 12: Algorithm Transparency is vague",
    "Clause 19: Bias Mitigation needs clarification",
    "Clause 5: Accountability framework not defined",
    "Clause 17: Risk assessment unclear"
]

# Create event logs
event_logs = []
event_id = 1

for _, row in cases_df.iterrows():
    case_id = row["case_id"]
    category = row["policy_category"]

    # Choose how many events to simulate (3–5)
    num_events = random.randint(3, 5)
    base_time = datetime.today() - timedelta(days=random.randint(30, 365))

    for i in range(num_events):
        timestamp = base_time + timedelta(days=i, hours=random.randint(1, 6))
        activity = activities[i % len(activities)]
        actor = random.choice(actors)
        review_outcome = random.choice(outcomes)

        if "AI Regulation" in category:
            comment = random.choice(clauses)
        else:
            comment = random.choice([
                "Policy requires clarification.",
                "Missing compliance with standard X.",
                "Well-structured draft.",
                "Needs legal alignment."
            ])

        event_logs.append({
            "event_id": event_id,
            "case_id": case_id,
            "activity": activity,
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
            "actor": actor,
            "review_outcome": review_outcome,
            "comments": comment
        })

        event_id += 1

# Save to CSV
events_df = pd.DataFrame(event_logs)
events_df.to_csv("Policy_Analysis_Events.csv", index=False)

print("✅ Generated Policy_Analysis_Events.csv with synthetic event logs.")
