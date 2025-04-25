import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# === CONFIG ===
log_path = os.path.join("..", "data", "logs", "file_events_log.json")
MAX_EVENTS = 50                # Stop after 50 file events
MAX_DURATION_SECONDS = 20     # Stop after 60 seconds

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
        print(event_info)
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

    try:
        while (time.time() - start_time) < MAX_DURATION_SECONDS and event_counter < MAX_EVENTS:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    observer.stop()
    observer.join()
    print(f"[INFO] Monitoring stopped after {event_counter} events or {int(time.time() - start_time)} seconds.")
