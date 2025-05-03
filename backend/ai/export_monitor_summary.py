import json
from datetime import datetime

monitor_log_path = "../../data/logs/monitor/monitor_log.json"
summary_output_path = "../../data/logs/monitor/summary_for_ui.json"

def export_summary():
    try:
        # Load the entire JSON array at once
        with open(monitor_log_path, "r") as f:
            events = json.load(f)

        malicious = sum(1 for e in events if e.get("prediction") == "malicious")
        benign = sum(1 for e in events if e.get("prediction") == "benign")

        summary = {
            "total_events": len(events),
            "malicious": malicious,
            "benign": benign,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(summary_output_path, "w") as f:
            json.dump(summary, f, indent=4)

        print(f"[✔] Exported monitor summary to: {summary_output_path}")

    except Exception as e:
        print(f"[✖] Error exporting summary: {e}")

if __name__ == "__main__":
    export_summary()
