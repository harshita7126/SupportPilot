"""
SupportPilot - SQLite Database Module
-------------------------------------
Manages SQLite persistence for submitted IT support tickets, including
safe schema migration for `processing_time_ms` and real-time dashboard analytics.
"""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "tickets.db")

CATEGORIES = ["Network", "VPN", "Password", "Software", "Hardware"]
SEVERITIES = ["Critical", "High", "Medium", "Low"]
PRIORITIES = ["P1", "P2", "P3", "P4"]


def get_connection():
    """Create and return a SQLite connection to tickets.db."""
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    """
    Create the tickets table if it does not exist, and safely migrate
    existing databases by adding `processing_time_ms` if missing.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT,
            employee_email TEXT,
            employee_id TEXT,
            department TEXT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            confidence REAL,
            severity TEXT,
            priority TEXT,
            processing_time_ms REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Safe schema migration for existing tickets.db without overwriting existing data
    cursor.execute("PRAGMA table_info(tickets)")
    existing_columns = {row[1] for row in cursor.fetchall()}
    if "processing_time_ms" not in existing_columns:
        cursor.execute("ALTER TABLE tickets ADD COLUMN processing_time_ms REAL")

    connection.commit()
    connection.close()


def save_ticket(ticket_data):
    """Insert a processed ticket record into SQLite and return its new ticket ID."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO tickets (
            employee_name, employee_email, employee_id,
            department, title, description, category,
            confidence, severity, priority, processing_time_ms
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket_data["employee_name"],
        ticket_data["employee_email"],
        ticket_data["employee_id"],
        ticket_data["department"],
        ticket_data["title"],
        ticket_data["description"],
        ticket_data["category"],
        ticket_data["confidence"],
        ticket_data["severity"],
        ticket_data["priority"],
        ticket_data.get("processing_time_ms")
    ))
    connection.commit()
    ticket_id = cursor.lastrowid
    connection.close()
    return ticket_id


def get_all_tickets():
    """Return all submitted tickets ordered by newest first."""
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY id DESC")
    tickets = cursor.fetchall()
    connection.close()
    return tickets


def get_dashboard_stats():
    """
    Compute real dashboard analytics from the SQLite tickets table.
    Only real measured `processing_time_ms` values (non-NULL) are averaged.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets")
    total_tickets = cursor.fetchone()[0]

    # Category counts (ensure all 5 core categories are always present)
    category_counts = {cat: 0 for cat in CATEGORIES}
    cursor.execute("SELECT category, COUNT(*) FROM tickets GROUP BY category")
    for category, count in cursor.fetchall():
        if category in category_counts:
            category_counts[category] = count
        else:
            category_counts[category or "Unknown"] = count

    # Severity counts
    severity_counts = {sev: 0 for sev in SEVERITIES}
    cursor.execute("SELECT severity, COUNT(*) FROM tickets GROUP BY severity")
    for severity, count in cursor.fetchall():
        if severity in severity_counts:
            severity_counts[severity] = count

    # Priority distribution
    priority_counts = {prio: 0 for prio in PRIORITIES}
    cursor.execute("SELECT priority, COUNT(*) FROM tickets GROUP BY priority")
    for priority, count in cursor.fetchall():
        if priority in priority_counts:
            priority_counts[priority] = count

    # Average real processing time (ignoring legacy rows where processing_time_ms is NULL)
    cursor.execute("""
        SELECT AVG(processing_time_ms), COUNT(processing_time_ms)
        FROM tickets
        WHERE processing_time_ms IS NOT NULL
    """)
    avg_time, measured_count = cursor.fetchone()
    avg_processing_time_ms = round(avg_time, 2) if avg_time is not None else None

    connection.close()

    return {
        "total_tickets": total_tickets,
        "category_counts": category_counts,
        "severity_counts": severity_counts,
        "priority_counts": priority_counts,
        "avg_processing_time_ms": avg_processing_time_ms,
        "measured_tickets_count": measured_count,
    }


create_table()
