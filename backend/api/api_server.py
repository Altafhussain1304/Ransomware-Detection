from flask import Flask, jsonify, request
import json
import os
import shutil
import datetime
import time

app = Flask(__name__)

# ---------- Global Paths ----------
QUARANTINE_DIR = r'C:/Users/SuperUser/OneDrive/Desktop/RansomSaver/backend/data/quarantine'
ORIGINAL_DIR = r'C:/Users/SuperUser/OneDrive/Desktop/RansomSaver/backend'
ACTION_LOG_PATH = r'C:/Users/SuperUser/OneDrive/Desktop/RansomSaver/backend/data/action_log.json'

# ---------- Global Configuration ----------
AUTO_DELETE_DAYS = 7  # Auto-delete files older than 7 days in quarantine

# ---------- Logging Function ----------
def log_action(entry):
    try:
        if os.path.exists(ACTION_LOG_PATH):
            with open(ACTION_LOG_PATH, 'r') as f:
                data = json.load(f)
        else:
            data = []

        data.append(entry)
        with open(ACTION_LOG_PATH, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Failed to log action:", e)

# ---------- Endpoint 1: Final Summary ----------
@app.route('/api/summary', methods=['GET'])
def get_summary():
    try:
        summary_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/logs/final_summary.json'))
        print("[DEBUG] Using path:", summary_path)
        with open(summary_path, 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        print("[ERROR] /api/summary:", str(e))
        return jsonify({'error': str(e)}), 500

# ---------- Endpoint 2: Monitor Summary ----------
@app.route('/api/monitor-summary', methods=['GET'])
def get_monitor_summary():
    try:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/logs/monitor/summary_for_ui.json'))
        print("[DEBUG] Using path:", path)
        with open(path, 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        print("[ERROR] /api/monitor-summary:", str(e))
        return jsonify({'error': str(e)}), 500

# ---------- Endpoint 3: Simulated Summary ----------
@app.route('/api/simulated-summary', methods=['GET'])
def get_simulated_summary():
    try:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/logs/simulated/summary_for_ui.json'))
        print("[DEBUG] Using path:", path)
        with open(path, 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        print("[ERROR] /api/simulated-summary:", str(e))
        return jsonify({'error': str(e)}), 500

# ---------- Endpoint 4: Restore File ----------
@app.route('/api/restore', methods=['POST'])
def restore_file():
    try:
        file_name = request.json.get('file_name')
        if not file_name:
            return jsonify({'error': 'File name is required'}), 400

        quarantine_path = os.path.join(QUARANTINE_DIR, file_name)
        if not os.path.exists(quarantine_path):
            return jsonify({'error': 'File not found in quarantine'}), 404

        original_path = os.path.join(ORIGINAL_DIR, file_name)
        shutil.move(quarantine_path, original_path)

        # Log restore action
        log_action({
            "action": "restore",
            "file": file_name,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reason": "User requested restore",
            "auto": False
        })

        return jsonify({'message': f'File {file_name} restored successfully'}), 200

    except Exception as e:
        print("[ERROR] /api/restore:", str(e))
        return jsonify({'error': str(e)}), 500

from flask import request
from quarantine_utils import simulate_quarantine

@app.route('/api/simulate_quarantine', methods=['POST'])
def api_simulate_quarantine():
    try:
        data = request.get_json()
        filepath = data.get("filepath")

        if not filepath:
            return jsonify({"error": "Missing 'filepath' in request."}), 400

        simulate_quarantine(filepath)
        return jsonify({"message": f"File '{filepath}' quarantined successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- Endpoint 5: Delete File ----------
@app.route('/api/delete', methods=['POST'])
def delete_file():
    try:
        file_name = request.json.get('file_name')
        if not file_name:
            return jsonify({'error': 'File name is required'}), 400

        file_path = os.path.join(QUARANTINE_DIR, file_name)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found in quarantine'}), 404

        os.remove(file_path)

        # Log delete action
        log_action({
            "action": "delete",
            "file": file_name,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reason": "User requested deletion",
            "auto": False
        })

        return jsonify({'message': f'File {file_name} deleted successfully'}), 200

    except Exception as e:
        print("[ERROR] /api/delete:", str(e))
        return jsonify({'error': str(e)}), 500

# ---------- Endpoint 6: List Files in Quarantine ----------
@app.route('/api/quarantine/list', methods=['GET'])
def list_quarantine_files():
    try:
        files = os.listdir(QUARANTINE_DIR)
        if not files:
            return jsonify({'message': 'No files in quarantine'}), 200
        return jsonify({'files': files}), 200
    except Exception as e:
        print("[ERROR] /api/quarantine/list:", str(e))
        return jsonify({'error': str(e)}), 500

# ---------- Endpoint 7: Trigger Auto-Delete from Frontend ----------
@app.route('/api/quarantine/auto-delete', methods=['POST'])
def trigger_auto_delete():
    try:
        auto_delete_quarantined_files()
        return jsonify({'message': 'Auto-delete operation completed successfully'}), 200
    except Exception as e:
        print("[ERROR] /api/quarantine/auto-delete:", str(e))
        return jsonify({'error': str(e)}), 500

# ---------- Endpoint 8: Re-scan Quarantined File ----------
def scan_file(file_path):
    """
    Dummy scan logic for demonstration.
    Replace this with your actual YARA/AI scan logic.
    Returns a dict with scan results.
    """
    # Example: always returns clean for demonstration
    # Replace with actual scan logic as needed
    return {
        "status": "clean",
        "details": "No threats detected."
    }

@app.route('/api/quarantine/rescan', methods=['POST'])
def rescan_quarantined_file():
    """
    Re-scan a quarantined file using the existing scan logic.
    Expects JSON: { "file_name": "example.docx" }
    """
    try:
        data = request.get_json()
        file_name = data.get('file_name')
        if not file_name:
            return jsonify({'error': 'file_name is required'}), 400

        file_path = os.path.join(QUARANTINE_DIR, file_name)
        if not os.path.exists(file_path):
            return jsonify({'error': f'File {file_name} not found in quarantine.'}), 404

        # Use your existing scan logic here
        scan_result = scan_file(file_path)

        # Log the action
        log_action({
            "action": "rescan",
            "file": file_name,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reason": "User requested re-scan",
            "auto": False,
            "scan_result": scan_result
        })

        return jsonify({
            'file_name': file_name,
            'scan_result': scan_result
        }), 200
    except Exception as e:
        log_action({
            "action": "rescan",
            "file": data.get('file_name', 'unknown'),
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reason": f"Error: {str(e)}",
            "auto": False
        })
        return jsonify({'error': f'Error rescanning file: {e}'}), 500

# ---------- Auto-Delete Functionality ----------
def auto_delete_quarantined_files():
    try:
        current_time = time.time()  # Get current time in seconds
        for file_name in os.listdir(QUARANTINE_DIR):
            file_path = os.path.join(QUARANTINE_DIR, file_name)
            if os.path.isfile(file_path):
                # Get the time of last modification of the file
                file_mod_time = os.path.getmtime(file_path)
                # Check if the file is older than the defined period
                if current_time - file_mod_time > AUTO_DELETE_DAYS * 86400:  # 86400 seconds in a day
                    os.remove(file_path)
                    # Log auto-deletion action
                    log_action({
                        "action": "auto-delete",
                        "file": file_name,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "reason": "File was quarantined for too long",
                        "auto": True
                    })
                    print(f"[INFO] Auto-deleted {file_name} from quarantine.")
    except Exception as e:
        print("[ERROR] auto_delete_quarantined_files:", str(e))

# ---------- Start Server ----------
if __name__ == '__main__':
    # Call auto-delete function before starting the server
    auto_delete_quarantined_files()
    app.run(debug=True, port=5000)
