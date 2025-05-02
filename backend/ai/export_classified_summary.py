import json
import os

# Paths
classified_path = os.path.abspath('../../data/logs/simulated/classified_simulated_events.json')
export_path = os.path.abspath('../../data/logs/simulated/summary_for_ui.json')

# Load classified data
with open(classified_path, 'r') as f:
    data = json.load(f)

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

# Export for frontend
with open(export_path, 'w') as f:
    json.dump(summary_data, f, indent=4)

print(f"[✔] Exported summarized data for UI: {export_path}")

