import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# -------------------------
# CONFIG
# -------------------------
dataset_path = 'processed_train.csv'   # <-- Your training dataset with labels
label_column = 'label'                      # <-- Change if your label column has a different name
output_encoder_file = 'target_encoder.joblib'

# -------------------------
# 1. Load Dataset
# -------------------------
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"🚫 Dataset file '{dataset_path}' not found!")

df = pd.read_csv(dataset_path)

if label_column not in df.columns:
    raise ValueError(f"🚫 Label column '{label_column}' not found in dataset!")

print(f"📄 Loaded dataset: {dataset_path} → {df.shape[0]} rows")

# -------------------------
# 2. Encode Target Column
# -------------------------
target_encoder = LabelEncoder()
y = df[label_column]
y_encoded = target_encoder.fit_transform(y)

# -------------------------
# 3. Save Encoder
# -------------------------
joblib.dump(target_encoder, output_encoder_file)
print(f"✅ Target label encoder saved to '{output_encoder_file}'")

# Optional: Display the class mapping
print("\n📊 Label Class Mapping:")
for i, cls in enumerate(target_encoder.classes_):
    print(f"  ➤ {i}: '{cls}'")
