import os
import shutil
import json
from datetime import datetime

QUARANTINE_LOG = "data/logs/quarantine_log.json"
QUARANTINE_DIR = "data/quarantine"
FINAL_LOG = "data/logs/finalsummary.json"

def log_action(action_type, file_path, status, details=""):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action_type,
        "file_path": file_path,
        "status": status,
        "details": details
    }

    os.makedirs(os.path.dirname(FINAL_LOG), exist_ok=True)
    
    if not os.path.exists(FINAL_LOG):
        with open(FINAL_LOG, "w") as f:
            json.dump([], f, indent=4)

    with open(FINAL_LOG, "r") as f:
        logs = json.load(f)

    logs.append(log_entry)

    with open(FINAL_LOG, "w") as f:
        json.dump(logs, f, indent=4)

def quarantine_file(file_path, quarantine_folder=QUARANTINE_DIR):
    try:
        abs_source_path = os.path.abspath(file_path)
        print(f"[DEBUG] Quarantine - Source path: {abs_source_path}")
        print(f"[DEBUG] File exists before move? {os.path.exists(abs_source_path)}")

        if not os.path.exists(abs_source_path):
            raise FileNotFoundError(f"File not found: {abs_source_path}")

        os.makedirs(quarantine_folder, exist_ok=True)
        filename = os.path.basename(file_path)
        dest_path = os.path.join(os.path.abspath(quarantine_folder), filename)

        shutil.move(abs_source_path, dest_path)
        log_action("quarantine", abs_source_path, "success", f"Moved to {dest_path}")

        # Record in quarantine log
        hash_key = filename  # You can use sha256 later
        os.makedirs(os.path.dirname(QUARANTINE_LOG), exist_ok=True)

        if os.path.exists(QUARANTINE_LOG):
            with open(QUARANTINE_LOG, "r") as f:
                entries = json.load(f)
        else:
            entries = []

        entries.append({
            "hash": hash_key,
            "quarantined_path": dest_path,
            "original_path": abs_source_path
        })

        with open(QUARANTINE_LOG, "w") as f:
            json.dump(entries, f, indent=4)

        return True
    except Exception as e:
        log_action("quarantine", file_path, "failure", str(e))
        print(f"[ERROR] Quarantine failed: {e}")
        return False

def restore_file(quarantined_path, original_path):
    try:
        abs_quarantined_path = os.path.abspath(quarantined_path)
        abs_original_path = os.path.abspath(original_path)

        if not os.path.exists(abs_quarantined_path):
            raise FileNotFoundError(f"File not found: {abs_quarantined_path}")

        os.makedirs(os.path.dirname(abs_original_path), exist_ok=True)
        shutil.move(abs_quarantined_path, abs_original_path)
        log_action("restore", abs_quarantined_path, "success", f"Restored to {abs_original_path}")
        return True
    except Exception as e:
        log_action("restore", quarantined_path, "failure", str(e))
        print(f"[ERROR] Restore failed: {e}")
        return False

def delete_file(file_path):
    try:
        abs_file_path = os.path.abspath(file_path)
        if not os.path.exists(abs_file_path):
            raise FileNotFoundError(f"File not found: {abs_file_path}")

        os.remove(abs_file_path)
        log_action("delete", abs_file_path, "success", "File permanently deleted")
        return True
    except Exception as e:
        log_action("delete", file_path, "failure", str(e))
        print(f"[ERROR] Delete failed: {e}")
        return False

def auto_delete_if_enabled(file_path, config_path="config.json"):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        if config.get("auto_delete", False):
            print(f"[DEBUG] Auto-delete is enabled. Deleting {file_path}")
            return delete_file(file_path)
        else:
            log_action("auto_delete", file_path, "skipped", "Auto-delete disabled in config")
            return False
    except Exception as e:
        log_action("auto_delete", file_path, "failure", str(e))
        print(f"[ERROR] Auto-delete failed: {e}")
        return False

def restore_file_by_hash(file_hash):
    try:
        if not os.path.exists(QUARANTINE_LOG):
            raise FileNotFoundError("Quarantine log not found.")

        with open(QUARANTINE_LOG, "r") as f:
            entries = json.load(f)

        file_entry = next((e for e in entries if e["hash"] == file_hash), None)
        if not file_entry:
            raise ValueError("File hash not found in quarantine log.")

        restored = restore_file(file_entry["quarantined_path"], file_entry["original_path"])
        if restored:
            entries = [e for e in entries if e["hash"] != file_hash]
            with open(QUARANTINE_LOG, "w") as f:
                json.dump(entries, f, indent=4)
        return restored
    except Exception as e:
        log_action("restore_by_hash", file_hash, "failure", str(e))
        print(f"[ERROR] Restore by hash failed: {e}")
        return False

def delete_file_by_hash(file_hash):
    try:
        if not os.path.exists(QUARANTINE_LOG):
            raise FileNotFoundError("Quarantine log not found.")

        with open(QUARANTINE_LOG, "r") as f:
            entries = json.load(f)

        file_entry = next((e for e in entries if e["hash"] == file_hash), None)
        if not file_entry:
            raise ValueError("File hash not found in quarantine log.")

        deleted = delete_file(file_entry["quarantined_path"])
        if deleted:
            entries = [e for e in entries if e["hash"] != file_hash]
            with open(QUARANTINE_LOG, "w") as f:
                json.dump(entries, f, indent=4)
        return deleted
    except Exception as e:
        log_action("delete_by_hash", file_hash, "failure", str(e))
        print(f"[ERROR] Delete by hash failed: {e}")
        return False
