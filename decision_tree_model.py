import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Step 1: Load data
data = np.load('nslkdd_preprocessed.npz', allow_pickle=True)  # <- Replace with your file name
X_train = data['X_train']
X_test = data['X_test']
y_train = data['y_train']
y_test = data['y_test']

# Step 2: Initialize and train the model
model = DecisionTreeClassifier(criterion='gini', max_depth=None, random_state=42)
model.fit(X_train, y_train)

# Step 3: Evaluate the model
y_pred = model.predict(X_test)

print("🔍 Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))
print("\n🧮 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Step 4: Save the model
joblib.dump(model, 'decision_tree_nsl_model.pkl')
print("✅ Model saved as 'decision_tree_nsl_model.pkl'")
