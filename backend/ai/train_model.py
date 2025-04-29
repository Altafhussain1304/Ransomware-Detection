import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load labeled dataset
df = pd.read_csv('../../data/logs/labeled_dataset.csv')

# Select features and label
features = ['name', 'event_type', 'yara_match']
df = df.fillna('none')

# Encode categorical features
encoders = {}
X = pd.DataFrame()
for col in features:
    le = LabelEncoder()
    X[col] = le.fit_transform(df[col])
    encoders[col] = le

y = df['label']
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# Save model and encoders
with open('../ai/model.pkl', 'wb') as f:
    pickle.dump(clf, f)

with open('../ai/encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

with open('../ai/label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

print("[+] Model training complete and saved.")
