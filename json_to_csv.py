import json
import pandas as pd
from tqdm import tqdm  # 1. import tqdm

# # Step 1: Load your exported JSON
# with open('input/perm_krai_only.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)  # expects a list of docs

# output_path = 'output/perm_krai.csv'



with open('input/job_forecast.hh_ru_jobs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)  # expects a list of docs

output_path = 'output/all_data.csv'


# Step 2: Flatten each document safely, with a progress bar
processed_data = []
for doc in tqdm(data, desc="Processing jobs"):         # 2. wrap data in tqdm
    processed_doc = {
        "name": doc.get("name"),
        "city": (doc.get("area") or {}).get("name"),
        "area_name": doc.get("area_name"),
        "salary_from": (doc.get("salary") or {}).get("from"),
        "salary_to":   (doc.get("salary") or {}).get("to"),
        "url": doc.get("url"),
        "employer_name": (doc.get("employer") or {}).get("name"),
        "schedule_id":   (doc.get("schedule") or {}).get("id"),
        "working_days_id": (
            (doc.get("working_days") or [{}])[0].get("id")
            if doc.get("working_days") is not None else None
        ),
        "working_time_intervals_id": (
            (doc.get("working_time_intervals") or [{}])[0].get("id")
            if doc.get("working_time_intervals") is not None else None
        ),
        "working_time_modes_id": (
            (doc.get("working_time_modes") or [{}])[0].get("id")
            if doc.get("working_time_modes") is not None else None
        ),
        "professional_roles_name": (
            (doc.get("professional_roles") or [{}])[0].get("name")
            if doc.get("professional_roles") is not None else None
        ),
        "experience_id": (doc.get("experience") or {}).get("id"),
        "employment_id": (doc.get("employment") or {}).get("id"),
        "entry_date": doc.get("entry_date")
    }
    processed_data.append(processed_doc)

# Step 3: Build DataFrame and write to CSV
df = pd.DataFrame(processed_data)

# If you want a specific column order:
cols = [
    "name", "city", "area_name",
    "salary_from", "salary_to",
    "employer_name", "schedule_id",
    "working_days_id", "working_time_intervals_id", "working_time_modes_id",
    "professional_roles_name", "experience_id", "employment_id",
    "entry_date", "url"
]
df = df[[c for c in cols if c in df.columns]]


df.to_csv(output_path, index=False)

print(f"Wrote {len(df)} jobs to {output_path}")
