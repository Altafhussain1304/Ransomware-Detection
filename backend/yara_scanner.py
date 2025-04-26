import yara
import os

# === CONFIGURATION ===
RULES_DIR = os.path.join("..", "rules")
RULES_FILE = os.path.join(RULES_DIR, "rules.yara")

def load_yara_rules():
    if not os.path.exists(RULES_FILE):
        raise FileNotFoundError(f"YARA rules file not found: {RULES_FILE}")
    return yara.compile(filepath=RULES_FILE)

def scan_file(filepath):
    try:
        rules = load_yara_rules()
        matches = rules.match(filepath)
        return [match.rule for match in matches]
    except Exception as e:
        print(f"[ERROR] YARA scanning failed for {filepath}: {e}")
        return []
