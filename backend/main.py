import os
import subprocess
import psutil
from datetime import datetime
import time
import sys

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
import json
from datetime import datetime
import os

# Directory where logs will be stored
LOG_DIR = "../data/logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Create logs folder if it doesn't exist
log_file = os.path.join(LOG_DIR, "process_log.json")  # Path to the log file

def log_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            info = proc.info  # Get process info (pid, name, username)
            info["timestamp"] = datetime.now().isoformat()  # Add timestamp
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue  # Skip processes that are no longer available or inaccessible

    # Write process information to the log file
    with open(log_file, "a") as f:
        for p in processes:
            f.write(json.dumps(p) + "\n")  # Each process info in JSON format

def main():
    parser = argparse.ArgumentParser(description="RansomSaver Utility")
    parser.add_argument("--menu", action="store_true", help="Launch the main menu")
    parser.add_argument("--log-processes", action="store_true", help="Log running processes")
    args = parser.parse_args()

    if args.menu:
        main_menu()
    elif args.log_processes:
        print("Logging running processes...")
        log_processes()
        print(f"Logs written to {log_file}")
    else:
        print("No valid option provided. Use --menu or --log-processes.")

if __name__ == "__main__":
    main()
