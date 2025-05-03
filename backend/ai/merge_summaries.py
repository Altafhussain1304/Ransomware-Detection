import json
import os

# Define file paths
monitor_path = os.path.join('../../data/logs/monitor', 'summary_for_ui.json')
simulated_path = os.path.join('../../data/logs/simulated', 'summary_for_ui.json')
output_path = os.path.join('../../data/logs', 'final_summary.json')

def merge_summaries():
    with open(monitor_path, 'r') as f:
        monitor_data = json.load(f)

    with open(simulated_path, 'r') as f:
        simulated_data = json.load(f)

    combined = {
        'monitoring_summary': monitor_data,
        'simulated_summary': simulated_data
    }

    with open(output_path, 'w') as f:
        json.dump(combined, f, indent=4)

    print(f"[✔] Merged summary saved to: {output_path}")

if __name__ == "__main__":
    merge_summaries()

