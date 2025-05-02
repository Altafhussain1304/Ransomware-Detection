import json
from collections import Counter
import os

# Load classified results
results_path = os.path.abspath('../../data/logs/simulated/classified_simulated_events.json')
with open(results_path, 'r') as f:
    data = json.load(f)

# Count predictions
predictions = [entry['prediction'] for entry in data]
summary = Counter(predictions)

print("[📊] Prediction Summary:")
for label, count in summary.items():
    print(f"  {label}: {count} events")
