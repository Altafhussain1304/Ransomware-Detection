import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from datetime import datetime
from yara_scanner import scan_file

# Optional extras
try:
    import winsound  # For alert beep (Windows only)
except ImportError:
    winsound = None

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    Fore = Style = None

# === CONFIG ===
log_path = os.path.join("..", "data", "logs", "file_events_log.json")
MAX_EVENTS = 50
MAX_DURATION_SECONDS = 20

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

event_counter = 0
start_time = time.time()
lock = threading.Lock()

def process_initial_scan_event(file_path):
    """Handles YARA scan for initial files at startup."""
    global event_counter

    event_info = {
        "event_type": "initial_scan",
        "src_path": file_path,
        "timestamp": datetime.now().isoformat()
    }

    matches = scan_file(file_path)
    if matches:
        event_info["yara_matches"] = matches

        if Fore:
            print(Fore.RED + f"[!] YARA Match found in {file_path}: {matches}" + Style.RESET_ALL)
        else:
            print(f"[!] YARA Match found in {file_path}: {matches}")
        
        if winsound:
            winsound.Beep(1000, 300)
    else:
        print(event_info)

    with lock:
        all_events.append(event_info)
        event_counter += 1

        with open(log_path, "w") as f:
            json.dump(all_events, f, indent=4)

class FileEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        global event_counter

        if event.is_directory or event_counter >= MAX_EVENTS:
            return

        event_info = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "timestamp": datetime.now().isoformat()
        }

        matches = scan_file(event.src_path)
        if matches:
            event_info["yara_matches"] = matches

            if Fore:
                print(Fore.RED + f"[!] YARA Match found in {event.src_path}: {matches}" + Style.RESET_ALL)
            else:
                print(f"[!] YARA Match found in {event.src_path}: {matches}")

            if winsound:
                winsound.Beep(1000, 300)
        else:
            print(event_info)

        with lock:
            all_events.append(event_info)
            event_counter += 1

            with open(log_path, "w") as f:
                json.dump(all_events, f, indent=4)

if __name__ == "__main__":
    path = "."  # Monitor current directory
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"[INFO] Monitoring '{os.path.abspath(path)}' for {MAX_DURATION_SECONDS}s or {MAX_EVENTS} events...")

    # ➔ Initial YARA Scan
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            process_initial_scan_event(file_path)

    try:
        while (time.time() - start_time) < MAX_DURATION_SECONDS and event_counter < MAX_EVENTS:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    observer.stop()
    observer.join()
    print(f"[INFO] Monitoring stopped after {event_counter} events or {int(time.time() - start_time)} seconds.")
