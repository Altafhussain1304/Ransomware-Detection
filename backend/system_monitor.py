import psutil
import json
import time
import os

# === CONFIGURATIONS ===
MAX_LOGS = 100
MAX_DURATION_SECONDS = 20

# === SETUP ===
log_dir = os.path.join("..", "data", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "system_monitor_log.json")

def log_system_stats():
    start_time = time.time()
    log_count = 0
    logs = []

    try:
        while log_count < MAX_LOGS and (time.time() - start_time) < MAX_DURATION_SECONDS:
            stats = {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory": dict(psutil.virtual_memory()._asdict()),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            logs.append(stats)
            print(f"[{log_count+1}] Logged system stats.")
            log_count += 1

        with open(log_file_path, "w") as f:
            json.dump(logs, f, indent=4)

        print(f"\n[INFO] Monitoring stopped. Logs saved to {log_file_path}")

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

if __name__ == "__main__":
    print("[INFO] Starting automatic system monitoring...")
    log_system_stats()
