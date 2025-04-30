import pandas as pd
import sys

# Load cleaned dataset
df = pd.read_csv('clean_dataset.csv')

# Debugging: Print column names
print("Columns in dataset:", df.columns)

# Improved labeling logic
def label_row(row):
    try:
        # Assign 'suspicious' if yara_match contains specific keywords
        if isinstance(row['yara_match'], str) and 'encrypt' in row['yara_match'].lower():
            return 'suspicious'
        # Assign 'malicious' if the file name contains 'ransom'
        if isinstance(row['name'], str) and 'ransom' in row['name'].lower():
            return 'malicious'
    except KeyError:
        pass
    return 'benign'

# Check if the required columns exist
required_columns = ['name', 'yara_match']  # Ensure column names are correct
for col in required_columns:
    if col not in df.columns:
        print(f"[✘] Required column '{col}' not found in dataset.")
        df['label'] = 'benign'  # Default label if required columns are missing
        df.to_csv('labeled_dataset.csv', index=False)
        print("[✔] Labeled dataset saved as labeled_dataset.csv")
        sys.exit()

# Apply labeling function
df['label'] = df.apply(label_row, axis=1)

# Save labeled dataset
df.to_csv('labeled_dataset.csv', index=False)
print("[✔] Labeled dataset saved as labeled_dataset.csv")
print("Unique labels in the dataset:", df['label'].unique())
