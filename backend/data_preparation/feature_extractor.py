import os
import json
import csv
import re

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
# Update the headers to include 'cpu' and 'mem'
headers = ["type", "name", "event_type", "yara_match", "extra", "cpu", "mem"]

with open(output_csv, "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    # Add this function to extract numeric values from the 'extra' column
    def extract_numeric_values(extra):
        cpu = re.search(r'cpu=(\d+)', extra)
        mem = re.search(r'mem=(\d+)', extra)
        return {
            'cpu': int(cpu.group(1)) if cpu else 0,
            'mem': int(mem.group(1)) if mem else 0
        }

    for log_file in log_files:
        file_path = os.path.join(log_folder, log_file)

        with open(file_path, "r", encoding='utf-8') as f:
            try:
                events = json.load(f)
            except json.JSONDecodeError:
                print(f"[!] Skipping invalid JSON file: {log_file}")
                continue

            # Update the row processing logic to include extracted values
            for event in events:
                row = {
                    "type": log_file.replace("_log.json", ""),
                    "name": os.path.basename(event.get("src_path", "N/A")),
                    "event_type": event.get("event_type", "N/A"),
                    "yara_match": ",".join(event.get("yara_match", [])) if event.get("yara_match") else "",
                    "extra": event.get("extra", "")
                }

                # Extract CPU and memory values from the 'extra' field
                extracted = extract_numeric_values(event.get("extra", ""))
                row.update(extracted)

                # Write the row to the CSV
                writer.writerow(row)

print(f"[INFO] Dataset CSV created successfully at: {output_csv}")
