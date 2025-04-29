import pandas as pd

# Load cleaned dataset
df = pd.read_csv('clean_dataset.csv')

# Debugging: Print column names
print("Columns in dataset:", df.columns)

# Improved labeling logic
def label_row(row):
    try:
        # Check if yara_matches is a non-empty list or meaningful string
        if isinstance(row['yara_matches'], str) and row['yara_matches'].strip() != '[]':
            return 'suspicious'
    except KeyError:
        pass
    return 'benign'

# Apply labeling function
if 'yara_matches' in df.columns:
    df['label'] = df.apply(label_row, axis=1)
else:
    print("[✘] Column 'yara_matches' not found in dataset.")
    df['label'] = 'benign'  # Default label if column is missing

# Save labeled dataset
df.to_csv('labeled_dataset.csv', index=False)
print("[✔] Labeled dataset saved as labeled_dataset.csv")
