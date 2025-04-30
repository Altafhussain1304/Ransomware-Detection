import pickle
import pandas as pd
import os

def predict(input_dict):
    # Load the model
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    # Load the encoders
    encoders_path = os.path.join(os.path.dirname(__file__), 'encoders.pkl')
    with open(encoders_path, 'rb') as f:
        encoders = pickle.load(f)
    
    label_encoder_path = os.path.join(os.path.dirname(__file__), 'label_encoder.pkl')
    with open(label_encoder_path, 'rb') as f:
        label_encoder = pickle.load(f)
    
    # Preprocess the input
    df = pd.DataFrame([input_dict])
    for col, encoder in encoders.items():
        if col in df.columns:
            try:
                df[col] = encoder.transform(df[col])
            except ValueError as e:
                print(f"[!] Warning: Unseen label '{df[col].iloc[0]}' in column '{col}'. Using default value.")
                df[col] = encoder.transform([encoder.classes_[0]])  # Use the first class as a fallback
    
    # Make prediction
    prediction = model.predict(df)[0]
    return label_encoder.inverse_transform([prediction])[0]

if __name__ == "__main__":
    test_input = {
        'name': 'ransomware.exe',
        'event_type': 'created',  # Ensure this value exists in the training data
        'yara_match': 'SuspiciousFileNames'
    }
    result = predict(test_input)
    print("[✔] Prediction result:", result)
