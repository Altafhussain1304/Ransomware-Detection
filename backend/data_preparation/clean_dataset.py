import os
import json
import csv
from datetime import datetime
import pandas as pd

# ✅ Set up paths
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
log_folder = os.path.join(base_dir, "data", "logs")
output_csv = os.path.join(base_dir, "data", "clean_dataset.csv")

# ✅ Rule-based labeling
def label_event(event):
    if event.get("type") == "process_events":
        if "ransom" in event.get("extra", "").lower():
            return "suspicious"
    if event.get("type") == "file_events":
        if event.get("event_type") == "modified" and event.get("name", "").endswith(".exe"):
            return "suspicious"
    if isinstance(event.get("yara_match", []), list):
        if any("encrypt" in match.lower() or "ransom" in match.lower() for match in event["yara_match"]):
            return "suspicious"
    return "benign"

# ✅ Collect all events
all_events = []

if not os.path.exists(log_folder):
    print(f"[ERROR] Log folder does not exist: {log_folder}")
    exit()

for file_name in os.listdir(log_folder):
    if file_name.endswith(".json"):
        file_path = os.path.join(log_folder, file_name)
        if os.path.getsize(file_path) == 0:
            print(f"[WARNING] Skipping empty file: {file_name}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for entry in data:
                    print(f"[DEBUG] Processing: {file_name} -> {entry}")
                    event = {
                        "type": entry.get("type", file_name.replace("_log.json", "")),
                        "name": entry.get("name") or os.path.basename(entry.get("src_path", "unknown")),
                        "event_type": entry.get("event_type", entry.get("status", "unknown")),
                        "yara_match": ",".join(entry.get("yara_match", [])) if isinstance(entry.get("yara_match", []), list) else "",
                        "extra": entry.get("extra", ""),
                        "timestamp": entry.get("timestamp", datetime.now().isoformat())
                    }
                    event["label"] = label_event(event)
                    all_events.append(event)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Failed to parse {file_name}: {e}")

# ✅ Write to CSV
with open(output_csv, "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["type", "name", "event_type", "yara_match", "extra", "timestamp", "label"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for entry in all_events:
        writer.writerow(entry)

print(f"[INFO] Clean dataset written to: {output_csv}")

# Load the dataset
df = pd.read_csv(output_csv)

# Preprocess 'yara_match' column to standardize its values
if 'yara_match' in df.columns:
    df['yara_match'] = df['yara_match'].apply(lambda x: set(x.split(',')) if isinstance(x, str) else set())
    if not df['yara_match'].empty and all(isinstance(x, set) for x in df['yara_match']):
        unique_yara_matches = set.union(*df['yara_match']) - {''}
        for match in unique_yara_matches:
            df[f'yara_match_{match.strip()}'] = df['yara_match'].apply(lambda x: 1 if match.strip() in x else 0)
    df.drop(columns=['yara_match'], inplace=True)

# One-hot encode other categorical columns
categorical_columns = ['type', 'event_type']
df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

# Save the updated dataset
df.to_csv(output_csv, index=False)
