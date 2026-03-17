import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
import pickle

# -------------------------
# 1. Load Dataset
# -------------------------
train_path = 'kdd_train.csv'
test_path = 'kdd_testdataset.csv'

# Define column names (no 'difficulty' column)
col_names = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment",
    "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted",
    "num_root", "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
    "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate",
    "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
    "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label"
]

# Read datasets without header rows (header=None)
df_train = pd.read_csv(train_path, names=col_names, header=0, low_memory=False)
df_test = pd.read_csv(test_path, names=col_names, header=0, low_memory=False)

# -------------------------
# 2. Encode Categorical Features and Save Encoders
# -------------------------
categorical_cols = ['protocol_type', 'service', 'flag']
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df_train[col] = le.fit_transform(df_train[col])
    df_test[col] = le.transform(df_test[col])
    encoders[col] = le

# Save encoders for future use in entry preprocessing
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

# -------------------------
# 3. Encode Labels (normal=0, attack=1)
# -------------------------
df_train['label'] = df_train['label'].apply(lambda x: 0 if x == 'normal' else 1)
df_test['label'] = df_test['label'].apply(lambda x: 0 if x == 'normal' else 1)

# -------------------------
# 4. One-Hot Encode Categorical Features
# -------------------------
df_train = pd.get_dummies(df_train, columns=categorical_cols)
df_test = pd.get_dummies(df_test, columns=categorical_cols)

# Align columns in both datasets (to ensure they match)
df_train, df_test = df_train.align(df_test, join='inner', axis=1)

# -------------------------
# 5. Separate Features and Labels
# -------------------------
X_train = df_train.drop('label', axis=1)
y_train = df_train['label']
X_test = df_test.drop('label', axis=1)
y_test = df_test['label']

# -------------------------
# 6. Save as Compressed .npz
# -------------------------
np.savez('nslkdd_preprocessed.npz', X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)

# -------------------------
# 7. Export to CSV
# -------------------------
X_train['label'] = y_train
X_test['label'] = y_test

X_train.to_csv('processed_train.csv', index=False)
X_test.to_csv('processed_test.csv', index=False)

print("✅ Preprocessing complete. Saved:")
print(" - 'nslkdd_preprocessed.npz'")
print(" - 'processed_train.csv'")
print(" - 'processed_test.csv'")
print(" - 'label_encoders.pkl' ✅ (for future preprocessing)")
