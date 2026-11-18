"""
SupportPilot - Ticket Category Classifier
-----------------------------------------
Loads the saved TF-IDF + Logistic Regression pipeline and predicts the
IT support category along with model probability confidence.

Note:
- Trained on a small synthetic dataset (50 tickets, 10 per category).
- Test accuracy on this small synthetic dataset does NOT guarantee
  real-world production performance.
"""

import os
import joblib
from preprocess import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "ticket_classifier.pkl")


def load_model(model_path=MODEL_PATH):
    """Load the saved TF-IDF + Logistic Regression pipeline from disk."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Saved model not found at '{model_path}'. "
            "Please run 'python train_model.py' first."
        )
    return joblib.load(model_path)


# Load the trained pipeline once when the module is imported
model = load_model()


def combine_ticket_text(ticket="", title=None, description=None):
    """Combine ticket title and description into a single cleaned text string."""
    parts = []
    if title is not None:
        parts.append(str(title))
    if ticket is not None and str(ticket).strip():
        parts.append(str(ticket))
    if description is not None:
        parts.append(str(description))

    raw_combined = " ".join(part.strip() for part in parts if part and str(part).strip())
    return clean_text(raw_combined)


def classify_ticket(ticket="", description=None, *, title=None):
    """
    Predict the IT support category and confidence score for a ticket.

    Supports:
    - classify_ticket("single combined text")
    - classify_ticket("title text", "description text")
    - classify_ticket(title="title text", description="description text")

    Safely handles empty, invalid, or completely unknown (out-of-vocabulary) inputs.
    """
    cleaned_text = combine_ticket_text(ticket=ticket, title=title, description=description)

    # Safe handling for empty or whitespace-only input
    if not cleaned_text:
        return {
            "ticket": "",
            "category": "Unknown",
            "confidence": 0.0,
        }

    # Safe handling for inputs with zero known terms in the TF-IDF vocabulary
    tfidf_step = model.named_steps.get("tfidf")
    if tfidf_step is not None:
        transformed = tfidf_step.transform([cleaned_text])
        if transformed.nnz == 0:
            return {
                "ticket": cleaned_text,
                "category": "Unknown",
                "confidence": 0.0,
            }

    prediction = model.predict([cleaned_text])[0]
    probabilities = model.predict_proba([cleaned_text])[0]
    confidence = float(max(probabilities) * 100)

    return {
        "ticket": cleaned_text,
        "category": str(prediction),
        "confidence": round(confidence, 2),
    }


if __name__ == "__main__":
    print("SupportPilot Ticket Classifier (type 'exit' as title to quit)")
    while True:
        ticket_title = input("\nEnter ticket title (or type exit): ").strip()
        if ticket_title.lower() == "exit":
            break
        ticket_description = input("Enter ticket description (optional): ").strip()
        result = classify_ticket(title=ticket_title, description=ticket_description)
        print("\nClassification Result")
        print("Processed Text:", result["ticket"] or "(empty)")
        print("Category:", result["category"])
        print("Confidence:", f"{result['confidence']}%")
