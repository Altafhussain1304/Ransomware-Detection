import os
import subprocess
import psutil
from datetime import datetime
import time
import sys
from ai.predictor import predict
import json

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_screen()
        print("==== RansomSaver - Main Menu ====")
        print("1. Start File Monitoring")
        print("2. Start Process Monitoring")
        print("3. Start System Monitoring")
        print("4. Start Network Monitoring")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            subprocess.run([sys.executable, "file_monitor.py"])
        elif choice == "2":
            subprocess.run([sys.executable, "process_monitor.py"])
        elif choice == "3":
            subprocess.run([sys.executable, "system_monitor.py"])
        elif choice == "4":
            subprocess.run([sys.executable, "network_monitor.py"])
        elif choice == "5":
            print("Exiting RansomSaver Goodbye!")
            time.sleep(1)
            break
        else:
            print("Invalid choice. Please select a valid option.")
            time.sleep(2)

import argparse
import psutil
from datetime import datetime
import os

# Directory where logs will be stored
LOG_DIR = "../data/logs/monitor"  # <-- change to monitor folder
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, "monitor_log.json")  # <-- change filename

def append_events(new_events):
    # Load existing events as a list
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            try:
                all_events = json.load(f)
            except Exception:
                all_events = []
    else:
        all_events = []

    # Append new events (should be a list of dicts)
    all_events.extend(new_events)

    # Write back as a JSON array
    with open(log_file, "w") as f:
        json.dump(all_events, f, indent=2)

def log_processes():
    processes = []
    MODEL_FEATURES = ["name", "event_type", "yara_match"]

    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            info = proc.info
            info["timestamp"] = datetime.now().isoformat()

            features = {k: info.get(k, None) for k in MODEL_FEATURES}
            if features["event_type"] is None:
                features["event_type"] = "process"
            if features["yara_match"] is None:
                features["yara_match"] = "none"

            try:
                prediction = predict(features)
                info["prediction"] = prediction
            except Exception as e:
                info["prediction"] = "error"
                print(f"Error during prediction: {e}")

            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    append_events(processes)

def main():
    parser = argparse.ArgumentParser(description="RansomSaver Utility")
    parser.add_argument("--menu", action="store_true", help="Launch the main menu")
    parser.add_argument("--log-processes", action="store_true", help="Log running processes")
    args = parser.parse_args()

    # Default to menu if no arguments are provided
    if not any(vars(args).values()):
        main_menu()
    elif args.menu:
        main_menu()
    elif args.log_processes:
        print("Logging running processes...")
        log_processes()
        print(f"Logs written to {log_file}")
    else:
        print("No valid option provided. Use --menu or --log-processes.")

if __name__ == "__main__":
    main()
