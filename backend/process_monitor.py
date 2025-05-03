import psutil
import time
import json
import os
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    Fore = Style = None

# === CONFIG ===
log_path = os.path.join("..", "data", "logs", "process_events_log.json")
SUSPICIOUS_KEYWORDS = ["encrypt", "ransom", "locker"]
MONITOR_DURATION_SECONDS = 20  # Monitor for 20 seconds

# Ensure log directory exists
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# Load existing events
if os.path.exists(log_path):
    with open(log_path, "r") as f:
        try:
            all_events = json.load(f)
        except json.JSONDecodeError:
            all_events = []
else:
    all_events = []

def is_suspicious(proc_name):
    name_lower = proc_name.lower()
    return any(keyword in name_lower for keyword in SUSPICIOUS_KEYWORDS)

def get_current_processes():
    processes = {}
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            processes[proc.info['pid']] = proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

if __name__ == "__main__":
    print(f"[INFO] Monitoring system processes for {MONITOR_DURATION_SECONDS} seconds...")

    known_processes = get_current_processes()
    start_time = time.time()

    try:
        while (time.time() - start_time) < MONITOR_DURATION_SECONDS:
            current_processes = get_current_processes()

            new_pids = set(current_processes.keys()) - set(known_processes.keys())
            for pid in new_pids:
                proc_info = current_processes[pid]
                event = {
                    "timestamp": datetime.now().isoformat(),
                    "pid": pid,
                    "name": proc_info.get('name', 'Unknown'),
                    "create_time": datetime.fromtimestamp(proc_info.get('create_time', time.time())).isoformat(),
                    "suspicious": is_suspicious(proc_info.get('name', ''))
                }

                if event["suspicious"]:
                    if Fore:
                        print(Fore.RED + f"[!] Suspicious process detected: {event['name']} (PID: {pid})" + Style.RESET_ALL)
                    else:
                        print(f"[!] Suspicious process detected: {event['name']} (PID: {pid})")
                else:
                    print(f"[INFO] New process detected: {event['name']} (PID: {pid})")

                all_events.append(event)

                # Update known processes after processing new ones
                known_processes = current_processes
    
            # Save updated log as a proper JSON array after processing all new processes
            with open(log_path, "w") as f:
                json.dump(all_events, f, indent=4)
            time.sleep(1)

    except KeyboardInterrupt:
        print("[INFO] Monitoring stopped by user.")

    print(f"[INFO] Monitoring completed after {int(time.time() - start_time)} seconds.")
