"""
SupportPilot - Main Flask Application (Milestone 1)
---------------------------------------------------
Handles IT support ticket submission, ML-based category classification
(TF-IDF + Logistic Regression), rule-based severity/priority assignment,
real processing time measurement, SQLite persistence, and dashboard analytics.
"""

import os
import re
import time
from flask import Flask, render_template, request, redirect, url_for, flash
from classifier import classify_ticket
from severity import calculate_severity, calculate_priority
from database import create_table, save_ticket, get_all_tickets, get_dashboard_stats

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = "supportpilot-dev-key"

create_table()

VALID_DEPARTMENTS = {"IT", "HR", "Finance", "Sales", "Operations", "Other"}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_ticket_form(form_data):
    """Validate all required ticket submission fields and return a list of errors."""
    errors = []
    required_labels = {
        "employee_name": "Employee Name",
        "employee_email": "Employee Email",
        "employee_id": "Employee ID",
        "department": "Department",
        "title": "Ticket Title",
        "description": "Ticket Description",
    }

    missing = [
        label for field, label in required_labels.items()
        if not form_data.get(field)
    ]
    if missing:
        errors.append("Please fill in all required fields: " + ", ".join(missing) + ".")

    email = form_data.get("employee_email", "")
    if email and not EMAIL_PATTERN.match(email):
        errors.append("Please enter a valid Employee Email address.")

    department = form_data.get("department", "")
    if department and department not in VALID_DEPARTMENTS:
        errors.append("Please select a valid Department from the list.")

    return errors


@app.route("/")
def home():
    tickets = get_all_tickets()
    stats = get_dashboard_stats()
    return render_template("index.html", tickets=tickets, stats=stats)


@app.route("/submit", methods=["POST"])
def submit_ticket():
    form_data = {
        "employee_name": request.form.get("employee_name", "").strip(),
        "employee_email": request.form.get("employee_email", "").strip(),
        "employee_id": request.form.get("employee_id", "").strip(),
        "department": request.form.get("department", "").strip(),
        "title": request.form.get("title", "").strip(),
        "description": request.form.get("description", "").strip(),
    }

    validation_errors = validate_ticket_form(form_data)
    if validation_errors:
        for err in validation_errors:
            flash(err, "danger")
        return redirect(url_for("home"))

    try:
        # Measure actual processing time for classification + severity + priority
        start_time = time.perf_counter()

        result = classify_ticket(
            title=form_data["title"],
            description=form_data["description"],
        )
        severity = calculate_severity(
            form_data["description"],
            title=form_data["title"],
        )
        priority = calculate_priority(severity)

        processing_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        ticket_data = {
            "employee_name": form_data["employee_name"],
            "employee_email": form_data["employee_email"],
            "employee_id": form_data["employee_id"],
            "department": form_data["department"],
            "title": form_data["title"],
            "description": form_data["description"],
            "category": result["category"],
            "confidence": result["confidence"],
            "severity": severity,
            "priority": priority,
            "processing_time_ms": processing_time_ms,
        }

        ticket_id = save_ticket(ticket_data)

        flash(
            f"Ticket #{ticket_id} submitted successfully! "
            f"Category: {result['category']} ({result['confidence']}% confidence) | "
            f"Severity: {severity} (Rule-based) | Priority: {priority} | "
            f"Processing Time: {processing_time_ms:.2f} ms",
            "success",
        )
    except Exception as exc:
        flash(f"An error occurred while processing the ticket: {exc}", "danger")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
