import psutil
import json
import time
import os

# === SETUP ===
log_dir = os.path.join("..", "data", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "network_monitor_log.json")

# Load existing logs if available
if os.path.exists(log_file_path):
    with open(log_file_path, "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
else:
    logs = []

MAX_LOGS = 100
MAX_DURATION_SECONDS = 20

start_time = time.time()
log_count = 0

try:
    print("[INFO] Monitoring network connections...")

    while log_count < MAX_LOGS and (time.time() - start_time) < MAX_DURATION_SECONDS:
        connections = psutil.net_connections(kind="inet")
        snapshot = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "connections": [
                {
                    "fd": conn.fd,
                    "family": str(conn.family),
                    "type": str(conn.type),
                    "laddr": conn.laddr.ip if conn.laddr else None,
                    "lport": conn.laddr.port if conn.laddr else None,
                    "raddr": conn.raddr.ip if conn.raddr else None,
                    "rport": conn.raddr.port if conn.raddr else None,
                    "status": conn.status,
                    "pid": conn.pid
                }
                for conn in connections
            ]
        }
        logs.append(snapshot)
        log_count += 1
        print(f"[{log_count}] Logged network connections")
        time.sleep(1)

    # Write all logs to file
    with open(log_file_path, "w") as f:
        json.dump(logs, f, indent=4)

    print("\n[INFO] Monitoring complete.")

except Exception as e:
    print(f"[ERROR] {e}")
