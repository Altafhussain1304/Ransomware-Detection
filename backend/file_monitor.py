import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from yara_scanner import scan_file

# Optional extras:
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

def process_initial_scan_event(file_path):
    event_info = {
        "event_type": "initial_scan",
        "src_path": file_path,
        "timestamp": datetime.now().isoformat()
    }

    matches = scan_file(file_path)
    if matches:
        event_info["yara_matches"] = matches
        if Fore:
            print(Fore.YELLOW + f"[!] YARA Match found during initial scan in {file_path}: {matches}" + Style.RESET_ALL)
        else:
            print(f"[!] YARA Match found during initial scan in {file_path}: {matches}")
    else:
        print(event_info)

    all_events.append(event_info)

def process_event(event_type, file_path):
    global event_counter

    if event_counter >= MAX_EVENTS:
        return

    event_info = {
        "event_type": event_type,
        "src_path": file_path,
        "timestamp": datetime.now().isoformat()
    }

    # Run YARA scan
    try:
        matches = scan_file(file_path)
        if matches:
            event_info["yara_matches"] = matches
            if Fore:
                print(Fore.RED + f"[!] YARA Match found in {file_path}: {matches}" + Style.RESET_ALL)
            else:
                print(f"[!] YARA Match found in {file_path}: {matches}")
    except Exception as e:
        print(f"[ERROR] Failed to scan file {file_path}: {e}")

        if winsound:
            winsound.Beep(1000, 300)
    else:
        print(event_info)

    all_events.append(event_info)
    event_counter += 1

    # Save updated log
    with open(log_path, "w") as f:
        json.dump(all_events, f, indent=4)

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process_event("created", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            process_event("modified", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            process_event("moved", event.dest_path)

    def on_deleted(self, event):
        if not event.is_directory:
            process_event("deleted", event.src_path)

if __name__ == "__main__":
    path = "."  # Monitor current directory
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print(f"[INFO] Monitoring '{os.path.abspath(path)}' for {MAX_DURATION_SECONDS}s or {MAX_EVENTS} events...")

    # 🔁 Scan all files in the folder once at start
    process_initial_scan_event(full_path)
    for file in files:
            full_path = os.path.join(root, file)
            process_event("initial_scan", full_path)

    try:
        while (time.time() - start_time) < MAX_DURATION_SECONDS and event_counter < MAX_EVENTS:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    observer.stop()
    observer.join()
    print(f"[INFO] Monitoring stopped after {event_counter} events or {int(time.time() - start_time)} seconds.")
