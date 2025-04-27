import psutil
import json
from datetime import datetime
import os

# Define the log directory and file
LOG_DIR = "../data/logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, "process_log.json")

def log_processes():
    """
    Logs the current running processes into a JSON file.
    Ensures the file is a valid JSON array and appends new logs.
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            # Collect process information
            info = proc.info
            info["timestamp"] = datetime.now().isoformat()
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Skip processes that cannot be accessed
            continue

    # Read existing data from the log file
    try:
        with open(log_file, "r") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is invalid, start with an empty list
        existing_data = []

    # Append new process data to the existing data
    existing_data.extend(processes)

    # Write the updated data back to the log file as a valid JSON array
    with open(log_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    print(f"Logged {len(processes)} processes to {log_file}")

if __name__ == "__main__":
    print("Starting process logging...")
    log_processes()
    print("Process logging completed.")
