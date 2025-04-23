import psutil
import json
from datetime import datetime
import os

LOG_DIR = "../data/logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, "process_log.json")

def log_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            info = proc.info
            info["timestamp"] = datetime.now().isoformat()
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    with open(log_file, "a") as f:
        for p in processes:
            f.write(json.dumps(p) + "\n")

if __name__ == "__main__":
    print("Logging running processes...")
    log_processes()
    print(f"Logs written to {log_file}")


import json

# Actual path to the log file
log_path = "../data/logs/process_log.json"

fixed_data = []

with open(log_path, "r") as f:
    for line in f:
        fixed_data.append(json.loads(line))

# Save as a proper JSON array
with open("../data/logs/fixed_process_log.json", "w") as f:
    json.dump(fixed_data, f, indent=2)

print("Fixed log file saved to fixed_process_log.json")
