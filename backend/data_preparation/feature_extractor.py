import os
import json
import csv

# ✅ Setup correct paths
base_dir = os.path.dirname(os.path.abspath(__file__))  # Set base_dir to the root of the project
base_dir = os.path.join(base_dir, "..", "..")  # Navigate two levels up to the project root
log_folder = os.path.join(base_dir, "data", "logs")
output_csv = os.path.join(log_folder, "dataset.csv")  # Save dataset.csv in the existing logs folder

# ✅ Ensure log folder exists
os.makedirs(log_folder, exist_ok=True)

# ✅ Collect all log files
log_files = [f for f in os.listdir(log_folder) if f.endswith(".json")]

if not log_files:
    print("[WARNING] No log files found in 'data/logs/'. Please check and add log files.")
    exit()

# ✅ Continue processing if log files are found
headers = ["type", "name", "event_type", "yara_match", "extra"]

with open(output_csv, "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    for log_file in log_files:
        file_path = os.path.join(log_folder, log_file)

        with open(file_path, "r", encoding='utf-8') as f:
            try:
                events = json.load(f)
            except json.JSONDecodeError:
                print(f"[!] Skipping invalid JSON file: {log_file}")
                continue

            for event in events:
                row = {
                    "type": log_file.replace("_log.json", ""),
                    "name": os.path.basename(event.get("src_path", "N/A")),
                    "event_type": event.get("event_type", "N/A"),
                    "yara_match": ",".join(event.get("yara_match", [])) if event.get("yara_match") else "",
                    "extra": ""
                }

                if "process" in log_file and "pid" in event:
                    row["extra"] = f"pid={event.get('pid')}, name={event.get('name')}"

                if "network" in log_file:
                    row["extra"] = f"{event.get('protocol', '')}:{event.get('port', '')} {event.get('status', '')}"

                if "system" in log_file:
                    row["extra"] = f"{event.get('cpu', '')}, mem={event.get('memory', '')}"

                print(f"[DEBUG] Writing row: {row}")

                writer.writerow(row)

print(f"[INFO] Dataset CSV created successfully at: {output_csv}")
