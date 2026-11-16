"""
Tsebisa – Community Service Delivery Reporting System
DIIC3110 ICT4D Group Project (Pilot Prototype)

A lightweight system that simulates USSD/SMS citizen reporting
for service delivery problems in Lesotho.
Designed for feature-phone realities: simple menus, Sesotho first,
reference numbers, and a basic partner dashboard.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import sqlite3
import os
import random
import string

app = Flask(__name__)
app.secret_key = "tsebisa-ict4d-pilot-2026-limkokwing"

DB_PATH = os.path.join(os.path.dirname(__file__), "tsebisa.db")

# -------------------------------------------------
# Database helpers
# -------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference TEXT UNIQUE NOT NULL,
            submission_channel TEXT DEFAULT 'Website',
            category TEXT NOT NULL,
            description TEXT,
            location TEXT,
            phone TEXT,
            language TEXT DEFAULT 'st',
            status TEXT DEFAULT 'received',
            created_at TEXT NOT NULL,
            updated_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_ref TEXT,
            note TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def generate_reference():
    """Generate a short human-friendly reference e.g. TSE-7K2M"""
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TSE-{code}"

# -------------------------------------------------
# Category definitions (Sesotho + English)
# -------------------------------------------------
CATEGORIES = {
    "water": {"st": "Metsi (pompo / pipe e robehileng)", "en": "Water (broken pump / pipe)"},
    "roads": {"st": "Litsela (mekoallo / mekoti)", "en": "Roads (potholes / damage)"},
    "refuse": {"st": "Lithoto (ho bokella)", "en": "Refuse collection"},
    "lights": {"st": "Mabone a seterata", "en": "Street lights"},
    "other": {"st": "Tse ding", "en": "Other"},
}

STATUS_LABELS = {
    "received": {"st": "E amohetsoe", "en": "Received"},
    "in_progress": {"st": "E ntse e sebetsoa", "en": "In progress"},
    "closed": {"st": "E koetsoe", "en": "Closed"},
}

# -------------------------------------------------
# Routes – Citizen side (USSD-style flow)
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/report", methods=["GET", "POST"])
def report_start():
    """Step 1: Choose language"""
    if request.method == "POST":
        session["lang"] = request.form.get("lang", "st")
        return redirect(url_for("report_category"))
    return render_template("report_language.html")

@app.route("/report/category", methods=["GET", "POST"])
def report_category():
    lang = session.get("lang", "st")
    if request.method == "POST":
        session["category"] = request.form.get("category")
        return redirect(url_for("report_details"))
    return render_template("report_category.html", lang=lang, categories=CATEGORIES)

@app.route("/report/details", methods=["GET", "POST"])
def report_details():
    lang = session.get("lang", "st")
    category = session.get("category")
    if not category:
        return redirect(url_for("report_start"))

    if request.method == "POST":
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        phone = request.form.get("phone", "").strip()

        ref = generate_reference()
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn = get_db()
        conn.execute(
            "INSERT INTO reports (reference, submission_channel, category, description, location, phone, language, status, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (ref, 'Website', category, description, location, phone, lang, "received", now)
        )
        conn.commit()
        conn.close()

        session.clear()
        return render_template("report_success.html", ref=ref, lang=lang)

    return render_template("report_details.html", lang=lang, category=category, categories=CATEGORIES)

# -------------------------------------------------
# Partner / Admin Dashboard
# -------------------------------------------------
def normalize_status_filter(status_value):
    if status_value in STATUS_LABELS:
        return status_value
    return "all"

@app.route("/dashboard")
def dashboard():
    status_filter = normalize_status_filter(request.args.get("status", "all"))
    conn = get_db()
    if status_filter == "all":
        rows = conn.execute("SELECT * FROM reports ORDER BY created_at DESC").fetchall()
    else:
        rows = conn.execute("SELECT * FROM reports WHERE status=? ORDER BY created_at DESC", (status_filter,)).fetchall()
    conn.close()
    return render_template("dashboard.html", reports=rows, categories=CATEGORIES, status_labels=STATUS_LABELS, current_filter=status_filter)

@app.route("/dashboard/update/<reference>", methods=["POST"])
def update_status(reference):
    new_status = request.form.get("status")
    current_filter = normalize_status_filter(request.form.get("current_filter") or request.args.get("status") or "all")
    if new_status in STATUS_LABELS:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        conn.execute("UPDATE reports SET status=?, updated_at=? WHERE reference=?", (new_status, now, reference))
        conn.commit()
        conn.close()
        flash(f"Report {reference} updated to {new_status}", "success")
    return redirect(url_for("dashboard", status=current_filter))

@app.route("/dashboard/report/<reference>")
def view_report(reference):
    current_filter = normalize_status_filter(request.args.get("status", "all"))
    conn = get_db()
    report = conn.execute("SELECT * FROM reports WHERE reference=?", (reference,)).fetchone()
    conn.close()
    if not report:
        return "Report not found", 404
    return render_template("report_view.html", report=report, categories=CATEGORIES, status_labels=STATUS_LABELS, current_filter=current_filter)

# -------------------------------------------------
# Simple API for future USSD gateway integration
# -------------------------------------------------
@app.route("/api/ussd", methods=["POST"])
def ussd_api():
    """
    Placeholder endpoint for real USSD gateway (Africa's Talking style).
    In production this would parse sessionId, phoneNumber, text, etc.
    """
    # For the demo, we simulate a complete USSD report submission
    # so you can see 'USSD' in the dashboard.
    ref = generate_reference()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    conn = get_db()
    conn.execute(
        "INSERT INTO reports (reference, submission_channel, category, description, location, phone, language, status, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
        (ref, 'USSD', 'water', 'Simulated USSD Report', 'Ha Makoa', '+26650000000', 'st', 'received', now)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "status": "ok",
        "message": "USSD report simulated successfully",
        "reference": ref
    })

@app.route("/api/reports")
def api_reports():
    conn = get_db()
    rows = conn.execute("SELECT reference, submission_channel, category, status, created_at FROM reports ORDER BY created_at DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# -------------------------------------------------
# User guides
# -------------------------------------------------
@app.route("/guide")
def guide():
    return render_template("guide.html")

# -------------------------------------------------
if __name__ == "__main__":
    init_db()
    print("=" * 50)
    print("Tsebisa Pilot Server starting...")
    print("Citizen reporting:  http://127.0.0.1:5000/")
    print("Partner dashboard:  http://127.0.0.1:5000/dashboard")
    print("User guide:         http://127.0.0.1:5000/guide")
    print("=" * 50)
    
    # Required for Render deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)