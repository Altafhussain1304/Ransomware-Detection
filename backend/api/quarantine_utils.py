import os
import shutil

QUARANTINE_FOLDER = os.path.join(os.getcwd(), "quarantine")

def simulate_quarantine(filepath):
    if not os.path.exists(QUARANTINE_FOLDER):
        os.makedirs(QUARANTINE_FOLDER)

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    filename = os.path.basename(filepath)
    quarantined_path = os.path.join(QUARANTINE_FOLDER, filename)

    shutil.move(filepath, quarantined_path)
    return quarantined_path
