import json
import pandas as pd

# Step 1: Load the JSON file
# Replace 'exported_jobs.json' with your filename
with open('exported_jobs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)  # expects a top‐level list of documents

# Step 2: Process and flatten each document
processed_data = []
for doc in data:
    processed_doc = {
        "name": doc.get("name"),
        "city": doc.get("area", {}).get("name"),
        "area_name": doc.get("area_name"),
        "salary_from": doc.get("salary", {}).get("from"),
        "salary_to": doc.get("salary", {}).get("to"),
        "url": doc.get("url"),
        "employer_name": doc.get("employer", {}).get("name"),
        "schedule_id": doc.get("schedule", {}).get("id"),
        "working_days_id": (
            doc.get("working_days", [{}])[0].get("id")
            if doc.get("working_days") else None
        ),
        "working_time_intervals_id": (
            doc.get("working_time_intervals", [{}])[0].get("id")
            if doc.get("working_time_intervals") else None
        ),
        "working_time_modes_id": (
            doc.get("working_time_modes", [{}])[0].get("id")
            if doc.get("working_time_modes") else None
        ),
        "professional_roles_name": (
            doc.get("professional_roles", [{}])[0].get("name")
            if doc.get("professional_roles") else None
        ),
        "experience_id": doc.get("experience", {}).get("id"),
        "employment_id": doc.get("employment", {}).get("id"),
        "entry_date": doc.get("entry_date")
    }
    processed_data.append(processed_doc)

# Step 3: Create DataFrame and export
df = pd.DataFrame(processed_data)

# Optional: reorder columns if you like
column_order = [
    "name", "city", "area_name",
    "salary_from", "salary_to",
    "employer_name", "schedule_id",
    "working_days_id", "working_time_intervals_id", "working_time_modes_id",
    "professional_roles_name", "experience_id", "employment_id",
    "entry_date", "url"
]
df = df[column_order]

# Step 4: Write to Excel
output_path = 'jobs.xlsx'
df.to_excel(output_path, index=False)
print(f"Written {len(df)} records to {output_path}")
