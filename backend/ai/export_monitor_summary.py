import json
import os

# FIXED PATHS — go up two levels from 'ai' folder
classified_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'logs', 'simulated', 'classified_simulated_events.json'))
export_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'logs', 'simulated', 'summary_for_ui.json'))

print(f"[📂] Reading from: {classified_path}")
print(f"[💾] Will export to: {export_path}")

# Check if input file exists
if not os.path.exists(classified_path):
    print("[❌] ERROR: Input file does not exist.")
    exit(1)

# Load classified data
with open(classified_path, 'r') as f:
    data = json.load(f)
    print(f"[📊] Loaded {len(data)} entries.")

# Prepare summary
summary_data = []
for entry in data:
    summary_data.append({
        "name": entry.get("name"),
        "event_type": entry.get("event_type"),
        "yara_match": entry.get("yara_match"),
        "prediction": entry.get("prediction"),
        "timestamp": entry.get("timestamp")
    })

# Ensure output directory exists
os.makedirs(os.path.dirname(export_path), exist_ok=True)

# Export for frontend
with open(export_path, 'w') as f:
    json.dump(summary_data, f, indent=4)

print(f"[✔] Successfully exported {len(summary_data)} entries to: {export_path}")
