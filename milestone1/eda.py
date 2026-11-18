"""
SupportPilot - Exploratory Data Analysis (EDA) Script
-----------------------------------------------------
Standalone script for inspecting the IT support ticket dataset (tickets.csv).

Note on Dataset:
- The current `tickets.csv` is a small synthetic dataset (50 examples, 10 per category).
- It is NOT a real-world or Kaggle dataset.
- The Kaggle dataset discussed in class (`tobiasbueck/multilingual-customer-support-tickets`)
  is not present locally in this workspace.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "tickets.csv")


def run_eda(csv_path=DATASET_PATH):
    """Load the ticket dataset and print standard exploratory data analysis outputs."""
    if not os.path.exists(csv_path):
        print(f"Error: Dataset file not found at '{csv_path}'.")
        return

    print("=" * 65)
    print("SupportPilot - Exploratory Data Analysis (EDA)")
    print("=" * 65)
    print(f"Dataset file: {os.path.basename(csv_path)}")
    print("Note: Current tickets.csv contains synthetic examples, not Kaggle data.\n")

    # 1. Load dataset
    df = pd.read_csv(csv_path)

    # 2. Dataset shape
    print("1. Dataset Shape (rows, columns):")
    print(f"   {df.shape} -> {df.shape[0]} rows, {df.shape[1]} columns\n")

    # 3. Column names
    print("2. Column Names:")
    print(f"   {df.columns.tolist()}\n")

    # 4. First five rows
    print("3. First Five Rows (head):")
    print(df.head().to_string())
    print()

    # 5. Last five rows
    print("4. Last Five Rows (tail):")
    print(df.tail().to_string())
    print()

    # 6. Dataset info
    print("5. Dataset Information (info):")
    df.info()
    print()

    # 7. Missing values
    print("6. Missing Values per Column (isnull().sum()):")
    print(df.isnull().sum())
    print()

    # 8. Duplicate records
    duplicate_count = df.duplicated().sum()
    print("7. Duplicate Records Check:")
    print(f"   Total exact duplicate rows: {duplicate_count}")
    if duplicate_count > 0:
        print("   Duplicate rows:")
        print(df[df.duplicated(keep=False)].to_string())
    print()

    # 9. Category distribution
    if "category" in df.columns:
        print("8. Category Distribution (value_counts):")
        print(df["category"].value_counts())
        print()

    # 10. Summary statistics
    print("9. Summary Statistics (describe):")
    print(df.describe(include="all").to_string())
    print()

    print("=" * 65)
    print("EDA Completed.")
    print("=" * 65)


if __name__ == "__main__":
    run_eda()
