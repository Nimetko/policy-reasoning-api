import pandas as pd
import random
from datetime import datetime, timedelta

# Possible values for various fields
policy_names = [
    "AI Accountability Bill",
    "Digital Privacy Framework",
    "Cybersecurity Oversight Act",
    "Health Data Sharing Reform",
    "Public Infrastructure Review",
    "Education Funding Amendment",
    "Climate Impact Disclosure Law",
    "Workforce Reskilling Policy",
    "Automated Decision-Making Bill",
    "AI Regulation for Public Use"
]

policy_categories = [
    "AI Regulation",
    "Health",
    "Cybersecurity",
    "Environment",
    "Education",
    "Public Safety"
]

compliance_statuses = ["Compliant", "Non-Compliant", "Needs Review", "Rejected"]

# Create 10 synthetic case entries
cases = []

for i in range(1, 11):
    case_id = i
    policy_id = 300 + i
    name = random.choice(policy_names)
    category = random.choice(policy_categories)
    last_review_date = datetime.today() - timedelta(days=random.randint(1, 365))
    compliance_status = random.choice(compliance_statuses)

    cases.append({
        "case_id": case_id,
        "policy_id": policy_id,
        "policy_name": name,
        "policy_category": category,
        "last_review_date": last_review_date.strftime("%Y-%m-%d"),
        "compliance_status": compliance_status
    })

# Convert to DataFrame and save as CSV
df = pd.DataFrame(cases)
df.to_csv("Policy_Analysis_Cases.csv", index=False)

print("✅ Generated Policy_Analysis_Cases.csv with 10 records.")
