import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import pickle
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Load labeled dataset
dataset_path = "../../backend/data_preparation/labeled_dataset.csv"
df = pd.read_csv(dataset_path)  # dataset_path points to labeled_dataset.csv

# Check unique labels
print("Unique labels in the dataset:", df['label'].unique())
print("Label distribution:", df['label'].value_counts())

# ✅ Clean and prepare data
df['label'] = df['label'].fillna('unknown')
df = df[df['label'] != 'unknown']
df = df.fillna('none')

# ✅ Select features
features = ['name', 'event_type', 'yara_match']
encoders = {}
X = pd.DataFrame()

for col in features:
    le = LabelEncoder()
    X[col] = le.fit_transform(df[col])
    encoders[col] = le

# ✅ Encode labels
y = df['label']
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# ✅ Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Debug: Show label distribution
print("Training set label distribution:", pd.Series(y_train).value_counts())
print("Test set label distribution:", pd.Series(y_test).value_counts())

# ✅ Train model
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# ✅ Predict and evaluate
y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
cm = confusion_matrix(y_test, y_pred)

print("\n🟩 Model Evaluation Metrics:")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-score: {f1:.4f}")
print("\nClassification Report:\n", report)

# ✅ Save evaluation report
os.makedirs('../../data/eval', exist_ok=True)
with open('../../data/eval/model_evaluation.json', 'w') as f:
    json.dump({
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'classification_report': report
    }, f, indent=4)

# ✅ Save confusion matrix image
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig('../../data/eval/confusion_matrix.png')
plt.close()

# ✅ Save model and encoders
with open('../ai/model.pkl', 'wb') as f:
    pickle.dump(clf, f)

with open('../ai/encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

with open('../ai/label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

print("\n✅ Model training complete and saved.")
print("[📁] Evaluation report: ../../data/eval/model_evaluation.json")
print("[🖼️] Confusion matrix image: ../../data/eval/confusion_matrix.png")

