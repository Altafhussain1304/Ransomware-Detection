import os
import json
import random
from datetime import datetime, timezone

output_dir = os.path.abspath('../../data/logs/simulated')
os.makedirs(output_dir, exist_ok=True)

# List of simulated suspicious process names
suspicious_names = ["wannacry.exe", "locky.exe", "teslacrypt.exe", "abc.exe"]

# YARA rule types we pretend to trigger
yara_matches = ["SuspiciousFileNames", "SuspiciousAPI", "SuspiciousName"]

# Event types
event_types = ["created", "deleted", "renamed", "modified"]

def generate_event():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "name": random.choice(suspicious_names),
        "event_type": random.choice(event_types),
        "yara_match": random.choice(yara_matches)
    }

def simulate(n=10, filename="simulated_events.json"):
    """
    Generate n simulated events and save them to a JSON file.
    Returns the list of simulated events.
    """
    simulated_events = [generate_event() for _ in range(n)]

    output_path = os.path.join(output_dir, filename)
    with open(output_path, "w") as f:
        json.dump(simulated_events, f, indent=4)
    
    print(f"[✔] Simulated {n} events saved to {output_path}")
    return simulated_events

if __name__ == "__main__":
    simulate(20)
