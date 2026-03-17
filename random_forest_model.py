'''import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Step 1: Load preprocessed dataset
data = np.load('nslkdd_preprocessed.npz', allow_pickle=True)  # Replace with your actual file name

# Check the contents of the file
print("Arrays in file:", data.files)

# Step 2: Extract data arrays
X_train = data['X_train']
X_test = data['X_test']
y_train = data['y_train']
y_test = data['y_test']

# Step 3: Initialize and train the Random Forest model
model = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
model.fit(X_train, y_train)

# Step 4: Predict on test data
y_pred = model.predict(X_test)

# Step 5: Evaluate model performance
print("\n✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))
print("\n🧮 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Step 6: Save the trained model for later use
joblib.dump(model, 'random_forest_nsl_model.pkl')
print("\n💾 Model saved as 'random_forest_nsl_model.pkl'")



import numpy as np
import pandas as pd
import pickle

feature_names = X_train.columns.tolist()

# 1. Compute default (mean) values from training features
feature_defaults = np.mean(X_train, axis=0)

# 2. Save to a .pkl file (for use in Flask app)
with open('feature_defaults.pkl', 'wb') as f:
    pickle.dump(feature_defaults.tolist(), f)

# 3. Save to a .csv file for manual review or reporting
df_defaults = pd.DataFrame([feature_defaults], columns=feature_names)  # `feature_names` should be a list of column names
df_defaults.to_csv('feature_defaults.csv', index=False)

print("Model and feature defaults saved to both .pkl and .csv files.")



import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load CSV with column names
df = pd.read_csv('processed_train.csv')
X_train = df.drop('label', axis=1)
y_train = df['label']

# Train with feature names
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
with open('random_forest_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved with feature names")
'''


import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import pickle

# Step 1: Load preprocessed dataset
# Prefer using CSV for feature name access
train_df = pd.read_csv('processed_train.csv')
X_train = train_df.drop('label', axis=1)
y_train = train_df['label']

# Optional: Also load test data for evaluation
try:
    test_df = pd.read_csv('processed_test.csv')
    X_test = test_df.drop('label', axis=1)
    y_test = test_df['label']
except FileNotFoundError:
    X_test, y_test = None, None
    print("⚠️ 'processed_test.csv' not found. Skipping evaluation.")

# Step 2: Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
model.fit(X_train, y_train)

# Step 3: Evaluate model performance (if test data available)
if X_test is not None and y_test is not None:
    y_pred = model.predict(X_test)
    print("\n✅ Accuracy:", accuracy_score(y_test, y_pred))
    print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))
    print("\n🧮 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Step 4: Save the trained model
joblib.dump(model, 'random_forest_model.pkl')
print("\n💾 Model saved as 'random_forest_model.pkl'")

# Step 5: Save feature defaults and feature names
feature_defaults = X_train.mean().values
feature_names = X_train.columns.tolist()

# Save defaults to .pkl
with open('feature_defaults.pkl', 'wb') as f:
    pickle.dump(feature_defaults.tolist(), f)

# Save defaults to .csv for manual review
df_defaults = pd.DataFrame([feature_defaults], columns=feature_names)
df_defaults.to_csv('feature_defaults.csv', index=False)

# Save feature names to use in later prediction scripts
with open('feature_names.pkl', 'wb') as f:
    pickle.dump(feature_names, f)

print("\n📁 Feature defaults and feature names saved.")
