import pandas as pd
import sys

# Load cleaned dataset
df = pd.read_csv('clean_dataset.csv')

# Debugging: Print column names
print("Columns in dataset:", df.columns)

# Improved labeling logic
def label_row(row):
    try:
        # Label as 'malicious' if the name contains specific keywords
        if isinstance(row['name'], str) and any(keyword in row['name'].lower() for keyword in ['ransom', 'malware', 'virus', 'trojan', 'worm']):
            return 'malicious'
        
        # Label as 'malicious' if yara_match contains specific keywords
        if isinstance(row['yara_match'], str) and any(keyword in row['yara_match'].lower() for keyword in ['encrypt', 'suspicious', 'dangerous', 'threat', 'malicious']):
            return 'malicious'
        
        # Label as 'malicious' if event_type matches specific values
        if isinstance(row['event_type'], str) and row['event_type'].lower() in ['execute', 'created', 'delete', 'modify', 'access']:
            return 'malicious'
    except KeyError:
        pass
    return 'benign'

# Check if the required columns exist
required_columns = ['name', 'yara_match', 'event_type']  # Ensure column names are correct
for col in required_columns:
    if col not in df.columns:
        print(f"[✘] Required column '{col}' not found in dataset.")
        df['label'] = 'benign'  # Default label if required columns are missing
        df.to_csv('labeled_dataset.csv', index=False)
        print("[✔] Labeled dataset saved as labeled_dataset.csv")
        sys.exit()

# Apply labeling function
df['label'] = df.apply(label_row, axis=1)
print("Label distribution after applying label_row:", df['label'].value_counts())

# Inject 30 extra malicious samples for training balance
extra_malicious = pd.DataFrame([
    {
        "type": "file_events",
        "name": f"malicious_sample_{i}.exe",
        "event_type": event,
        "yara_match": yara,
        "extra": "",
        "timestamp": f"2025-05-01T12:{i:02d}:00",
        "label": "malicious"
    }
    for i, (event, yara) in enumerate(
        zip(
            ["execute", "created", "delete", "modify", "access"] * 20,
            ["encrypt", "suspicious", "dangerous", "threat", "malicious"] * 20
        ), 1
    )
])

df = pd.concat([df, extra_malicious], ignore_index=True)

# Save labeled dataset
df.to_csv('labeled_dataset.csv', index=False)
print("[✔] Labeled dataset saved as labeled_dataset.csv")
print("Unique labels in the dataset:", df['label'].unique())
