import pickle
import pandas as pd
import os

def encode_input(value, encoder, col_name):
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        print(f"[!] Warning: Unseen label '{value}' in column '{col_name}'. Using fallback.")
        fallback_value = 'unknown' if 'unknown' in encoder.classes_ else encoder.classes_[0]
        return encoder.transform([fallback_value])[0]

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
    encoded_input = {}
    for col in input_dict:
        if col in encoders:
            encoded_input[col] = encode_input(input_dict[col], encoders[col], col)
        else:
            print(f"[!] Warning: Column '{col}' not found in encoders. Assigning default value.")
            encoded_input[col] = 0  # Assign a default encoding, e.g., 0

    df = pd.DataFrame([encoded_input])

    # Make prediction
    prediction = model.predict(df)[0]
    decoded_label = label_encoder.inverse_transform([prediction])[0]
    return decoded_label

# === Sample testing block ===
if __name__ == "__main__":
    test_input_1 = {
        'name': 'ransomware.exe',  # Test malicious-like
        'event_type': 'created',
        'yara_match': 'SuspiciousFileNames'
    }
    result = predict(test_input_1)
    print("[✔] Prediction result:", result)

    test_input_2 = {
        'name': 'abc.exe',  # Test with unseen/random process
        'event_type': 'created',
        'yara_match': 'SuspiciousName'
    }
    result = predict(test_input_2)
    print("[✔] Prediction result:", result)

    test_input_3 = {
        'name': 'unknown_process.exe',  # Unseen process
        'event_type': 'renamed',        # Unseen event_type
        'yara_match': 'SuspiciousAPI'   # Unseen yara_match
    }
    result = predict(test_input_3)
    print("[✔] Prediction result:", result)
