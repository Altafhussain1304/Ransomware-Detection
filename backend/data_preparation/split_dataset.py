import pandas as pd

# Load the labeled dataset
df = pd.read_csv('clean_dataset.csv')

# Separate features (X) and labels (y)
X = df.drop(columns=['label'])
y = df['label']

# Save to separate files
X.to_csv('X.csv', index=False)
y.to_csv('y.csv', index=False)

print("Dataset split into 'X.csv' and 'y.csv'.")