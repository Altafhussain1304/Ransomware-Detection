from file_actions import quarantine_file, auto_delete_if_enabled
import os

test_file = "testfile.txt"

# Create a test file
with open(test_file, "w") as f:
    f.write("This is a test.")

print("\n--- Quarantine or Auto-Delete Test ---")
print(f"[DEBUG] Checking file: {test_file}")
print(f"[DEBUG] Auto-delete setting from config.json...")

# Try auto-delete first; if not deleted, quarantine it
deleted = auto_delete_if_enabled(test_file)
if not deleted:
    print("[DEBUG] Auto-delete skipped or failed, trying quarantine...")
    quarantined = quarantine_file(test_file)
    print("Quarantine Result:", quarantined)
else:
    print("File was auto-deleted.")
