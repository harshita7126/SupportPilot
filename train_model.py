"""
SupportPilot - Model Training Script
------------------------------------
Trains a TF-IDF + Logistic Regression pipeline to classify IT support tickets
into five categories: Network, VPN, Password, Software, and Hardware.

Note:
- Uses `tickets_cleaned.csv` if available, otherwise falls back to `tickets.csv`.
- The current dataset contains 50 synthetic examples (10 per category).
  Evaluation accuracy on this small synthetic split does NOT guarantee
  real-world production performance.
"""

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANED_DATASET = os.path.join(BASE_DIR, "tickets_cleaned.csv")
RAW_DATASET = os.path.join(BASE_DIR, "tickets.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "ticket_classifier.pkl")

dataset_path = CLEANED_DATASET if os.path.exists(CLEANED_DATASET) else RAW_DATASET
print(f"Loading training dataset: {os.path.basename(dataset_path)}")

df = pd.read_csv(dataset_path)

X = df["ticket"]
y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english")),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Training Completed!")
print(f"Dataset size: {len(df)} synthetic rows (Train: {len(X_train)}, Test: {len(X_test)})")
print("Test Split Accuracy:", round(accuracy * 100, 2), "%")
print("Note: Small synthetic test set; accuracy does not guarantee production performance.")
print("\nClassification Report:")
print(classification_report(y_test, predictions))

os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"\nModel saved successfully to {os.path.relpath(MODEL_PATH, BASE_DIR)}!")
