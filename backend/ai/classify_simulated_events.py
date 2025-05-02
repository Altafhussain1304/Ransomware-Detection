import json
import os
from predictor import predict

# Load simulated events
simulated_path = os.path.abspath('../../data/logs/simulated/simulated_events.json')
with open(simulated_path, 'r') as f:
    events = json.load(f)

classified_events = []

for event in events:
    event_for_prediction = {k: v for k, v in event.items() if k != "timestamp"}
    prediction = predict(event_for_prediction)
    event['prediction'] = prediction
    classified_events.append(event)

# Save the classified results
output_path = os.path.abspath('../../data/logs/simulated/classified_simulated_events.json')
with open(output_path, 'w') as f:
    json.dump(classified_events, f, indent=4)

print(f"[✔] Classified {len(classified_events)} events saved to {output_path}")

