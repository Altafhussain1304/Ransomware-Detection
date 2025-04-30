import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle

# ✅ Load labeled dataset
df = pd.read_csv('../../data/logs/labeled_dataset.csv')

# Debug: Check unique labels in the dataset
print("Unique labels in the dataset:", df['label'].unique())

# Fill missing labels with a default value (e.g., 'unknown')
df['label'] = df['label'].fillna('unknown')

# Remove rows with 'unknown' labels
df = df[df['label'] != 'unknown']

# ✅ Select features and label
features = ['name', 'event_type', 'yara_match']
df = df.fillna('none')

# ✅ Encode categorical features
encoders = {}
X = pd.DataFrame()
for col in features:
    le = LabelEncoder()
    X[col] = le.fit_transform(df[col])
    encoders[col] = le

y = df['label']
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# ✅ Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Debug: Check label distribution in train and test sets
print("Training set label distribution:", pd.Series(y_train).value_counts())
print("Test set label distribution:", pd.Series(y_test).value_counts())

# ✅ Train model
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# ✅ Evaluate model
y_pred = clf.predict(X_test)

print("\n🟩 Model Evaluation Metrics:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=label_encoder.transform(label_encoder.classes_)))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, labels=label_encoder.transform(label_encoder.classes_), target_names=label_encoder.classes_))

# ✅ Save model and encoders
with open('../ai/model.pkl', 'wb') as f:
    pickle.dump(clf, f)

with open('../ai/encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

with open('../ai/label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

print("\n✅ Model training complete and saved.")
