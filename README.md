# SupportPilot – AI Ticket Resolution Agent

SupportPilot is an AI-powered IT support ticket processing system organized in a milestone-based structure. Milestone 1 classifies incoming IT support tickets, identifies severity using rule-based keyword detection, assigns priority, measures processing time, stores tickets in SQLite, and displays ticket analytics on a Bootstrap web dashboard.

## Milestone Overview

- **`milestone1/`** — Ticket Processing and Classification (completed): dataset exploration, preprocessing, TF-IDF + Logistic Regression classification, rule-based severity and priority assignment, SQLite persistence, processing time tracking, and Bootstrap analytics dashboard.
- **`milestone2/`** — Reserved for future development.

## Features (Milestone 1)

- Ticket submission through a Bootstrap web interface
- Automatic category classification into **Network**, **VPN**, **Password**, **Software**, and **Hardware**
- TF-IDF text feature extraction and Logistic Regression classification
- Prediction confidence display and safe handling of empty or unknown inputs
- Rule-based severity detection (**Critical**, **High**, **Medium**, **Low**)
- Automatic priority assignment (**P1–P4**)
- Actual ticket processing time measurement (in milliseconds)
- SQLite database storage (`milestone1/tickets.db`)
- Live dashboard analytics and submitted tickets table
- Standalone exploratory data analysis (`eda.py`) and data preprocessing (`preprocess.py`) scripts

## Technology Stack

- Python
- Flask
- Pandas
- Scikit-learn (TF-IDF + Logistic Regression)
- SQLite
- HTML and Bootstrap
- Joblib

## Project Structure

```text
SupportPilot/
│
├── README.md
├── .gitignore
├── LICENSE
│
├── milestone1/
│   ├── app.py
│   ├── classifier.py
│   ├── database.py
│   ├── eda.py
│   ├── preprocess.py
│   ├── severity.py
│   ├── train_model.py
│   ├── requirements.txt
│   ├── tickets.csv
│   ├── tickets_cleaned.csv
│   │
│   ├── models/
│   │   └── ticket_classifier.pkl
│   │
│   └── templates/
│       └── index.html
│
└── milestone2/
    └── (empty – reserved for future development)
```

> Note: `milestone1/tickets.db` is created/used locally at runtime and is ignored by Git via `.gitignore`.

## Installation

1. Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd SupportPilot
```

2. Navigate to the `milestone1` directory and install dependencies:

```bash
cd milestone1
pip install -r requirements.txt
```

## Running Milestone 1

From inside the `milestone1/` directory:

```bash
# Optional: Run Exploratory Data Analysis
python eda.py

# Optional: Run Data Preprocessing and Cleaning (creates tickets_cleaned.csv)
python preprocess.py

# Optional: Retrain the TF-IDF + Logistic Regression model
python train_model.py

# Start the Flask web application
python app.py
```

Alternatively, you can also start the app directly from the repository root:

```bash
python milestone1/app.py
```

Then open **http://127.0.0.1:5000/** in your browser.

## Ticket Processing Workflow

1. Employee submits an IT support ticket via the web form.
2. Input fields are validated server-side.
3. Ticket title and description are combined and transformed using TF-IDF.
4. Logistic Regression predicts the ticket category and confidence score.
5. Rule-based keyword logic identifies ticket severity.
6. Priority is mapped from severity (`P1–P4`).
7. Processing time is measured and all ticket fields are saved in SQLite (`milestone1/tickets.db`).
8. The dashboard updates with live category, severity, priority, and processing time analytics.

## Severity and Priority Mapping

| Severity (Rule-based) | Priority |
|---|---|
| Critical | P1 |
| High | P2 |
| Medium | P3 |
| Low | P4 |

## Model Evaluation

The current model achieved **90.0% accuracy** on a 10-sample test split from a 50-row synthetic dataset (`tickets_cleaned.csv`). This is a preliminary academic result and does not guarantee real-world production performance.

## Limitations

- The classifier is trained on a small 50-row synthetic dataset (10 examples per category), not a real-world or Kaggle dataset.
- Prediction confidence may be low for unfamiliar ticket wording, and completely out-of-vocabulary inputs are labeled `Unknown`.
- Severity detection uses keyword-based rules, not machine learning.
- This is a beginner-level academic prototype, not a production IT support system.

## Project Status

- **Milestone 1 – Ticket Processing and Classification:** Complete
- **Milestone 2:** Planned (directory reserved)
