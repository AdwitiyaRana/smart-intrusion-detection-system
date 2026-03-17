from flask import Flask, request, jsonify
import pandas as pd
import joblib
import numpy as np
import traceback
import os

app = Flask(__name__)

MODEL_PATH = 'random_forest_model.pkl'
FEATURES_PATH = 'feature_names.pkl'
DEFAULTS_PATH = 'feature_defaults.pkl'
ENCODERS_PATH = 'label_encoders.pkl'

model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURES_PATH)
feature_defaults = np.array(joblib.load(DEFAULTS_PATH))
label_encoders = joblib.load(ENCODERS_PATH)

categorical_cols = ['protocol_type', 'service', 'flag']


def preprocess_entry(raw_data):
    df = pd.DataFrame([raw_data])

   
    for col in df.columns:
        if col in feature_names:
            idx = feature_names.index(col)
            default_val = feature_defaults[idx]
            df[col] = df[col].fillna(default_val)

    # Encode categorical values
    for col in categorical_cols:
        if col in df.columns and col in label_encoders:
            known = set(label_encoders[col].classes_)
            df[col] = df[col].apply(lambda x: x if x in known else label_encoders[col].classes_[0])
            df[col] = label_encoders[col].transform(df[col])

    # One-hot encode
    df = pd.get_dummies(df, columns=categorical_cols)
    df = df.reindex(columns=feature_names, fill_value=0)
    return df


@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json

        if not input_data:
            return jsonify({'error': 'No data provided'}), 400

        if isinstance(input_data, dict):
            input_data = [input_data]

        predictions = []
        for entry in input_data:
            df = preprocess_entry(entry)
            pred_proba = model.predict_proba(df)
            pred_class = model.predict(df)

            confidence = float(np.max(pred_proba[0]) * 100)
            label = str(pred_class[0])  # Will be '0' or '1'
            is_attack = True if label == '1' else False

            result = {
                'prediction': label,
                'attack_detected': is_attack,
                'confidence': f"{confidence:.2f}%"
            }
            predictions.append(result)

        return jsonify(predictions)

    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)
    # app.run(debug=True)


