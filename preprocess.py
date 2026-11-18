"""
SupportPilot - Data Preprocessing and Cleaning Script
-----------------------------------------------------
Standalone script that cleans `tickets.csv` and saves the cleaned output
to `tickets_cleaned.csv` without modifying the original `tickets.csv`.

Cleaning steps:
1. Handle missing values safely (drops rows missing ticket text or category;
   does NOT invent or guess missing category labels).
2. Remove HTML tags and URLs where present, while preserving useful ticket text.
3. Convert ticket text to lowercase.
4. Remove unnecessary whitespace (leading, trailing, and repeated spaces).
5. Remove rows with empty ticket descriptions (or empty categories).
6. Remove duplicate records.
"""

import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(BASE_DIR, "tickets.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "tickets_cleaned.csv")

# Compiled regex patterns for basic HTML tag and URL removal
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
URL_PATTERN = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)
WHITESPACE_PATTERN = re.compile(r"\s+")


def clean_text(text):
    """
    Clean a single ticket text string:
    - Safely handle non-string / NaN inputs
    - Remove basic HTML tags (e.g., <p>, <br>, <b>)
    - Remove URLs (http://..., https://..., www....)
    - Convert text to lowercase
    - Collapse extra whitespace into single spaces and trim ends

    Preserves meaningful ticket words, numbers, and error terms.
    """
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""

    cleaned = str(text)
    cleaned = HTML_TAG_PATTERN.sub(" ", cleaned)
    cleaned = URL_PATTERN.sub(" ", cleaned)
    cleaned = cleaned.lower()
    cleaned = WHITESPACE_PATTERN.sub(" ", cleaned).strip()
    return cleaned


def preprocess_dataset(input_path=INPUT_CSV, output_path=OUTPUT_CSV):
    """Load raw tickets CSV, apply cleaning steps, and save tickets_cleaned.csv."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input dataset not found: {input_path}")

    print("=" * 65)
    print("SupportPilot - Data Preprocessing and Cleaning")
    print("=" * 65)

    # Read original dataset (original file is never modified)
    df = pd.read_csv(input_path)
    initial_rows = len(df)
    print(f"Loaded '{os.path.basename(input_path)}' with {initial_rows} rows.")

    required_columns = {"ticket", "category"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Expected columns {required_columns}, but found {set(df.columns)}."
        )

    # 1. Handle missing values without guessing category labels
    missing_before = df[["ticket", "category"]].isnull().sum().to_dict()
    df = df.dropna(subset=["ticket", "category"]).copy()
    rows_after_dropna = len(df)
    print(f"Missing values found before dropping: {missing_before}")
    print(f"Rows dropped due to missing values: {initial_rows - rows_after_dropna}")

    # 2. Clean ticket text (HTML removal, URL removal, lowercase, whitespace)
    #    Keep category names cleanly trimmed (preserving original category casing)
    df["ticket"] = df["ticket"].apply(clean_text)
    df["category"] = df["category"].astype(str).apply(
        lambda val: WHITESPACE_PATTERN.sub(" ", val).strip()
    )

    # 3. Remove empty ticket descriptions or empty categories
    rows_before_empty = len(df)
    df = df[(df["ticket"] != "") & (df["category"] != "")].copy()
    rows_after_empty = len(df)
    print(
        f"Rows removed due to empty ticket descriptions/categories: "
        f"{rows_before_empty - rows_after_empty}"
    )

    # 4. Remove duplicate records
    rows_before_dedup = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    rows_after_dedup = len(df)
    print(f"Duplicate rows removed: {rows_before_dedup - rows_after_dedup}")

    # 5. Save cleaned dataset to a separate file (do not overwrite tickets.csv)
    df.to_csv(output_path, index=False)

    print(f"\nCleaned dataset saved to '{os.path.basename(output_path)}'.")
    print(f"Final row count: {len(df)} (original: {initial_rows})")
    print("\nCategory distribution in cleaned dataset:")
    print(df["category"].value_counts())
    print("\nSample cleaned rows:")
    print(df.head().to_string())
    print("=" * 65)

    return df


if __name__ == "__main__":
    preprocess_dataset()
