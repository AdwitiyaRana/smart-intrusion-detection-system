import numpy as np

# Replace with your actual file path
data = np.load('nslkdd_preprocessed.npz', allow_pickle=True)

# Extract arrays
X_train = data['X_train']
X_test = data['X_test']
y_train = data['y_train']
y_test = data['y_test']

print("✅ Data loaded from .npz file:")
print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"y_test shape: {y_test.shape}")

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# Initialize models
dt_model = DecisionTreeClassifier(random_state=42)
rf_model = RandomForestClassifier(random_state=42)

# Cross-validation (5-fold)
dt_scores = cross_val_score(dt_model, X_train, y_train, cv=5)
rf_scores = cross_val_score(rf_model, X_train, y_train, cv=5)

# Results
print("\n🌳 Decision Tree CV Accuracy Scores:", dt_scores)
print("✅ Decision Tree Mean CV Accuracy: {:.4f}".format(np.mean(dt_scores)))

print("\n🌲 Random Forest CV Accuracy Scores:", rf_scores)
print("✅ Random Forest Mean CV Accuracy: {:.4f}".format(np.mean(rf_scores)))


# Fit and evaluate on the test set
rf_model.fit(X_train, y_train)
dt_model.fit(X_train, y_train)

rf_test_accuracy = rf_model.score(X_test, y_test)
dt_test_accuracy = dt_model.score(X_test, y_test)

print("🌲 Random Forest Test Accuracy:", rf_test_accuracy)
print("🌳 Decision Tree Test Accuracy:", dt_test_accuracy)
