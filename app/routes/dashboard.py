# app/routes/dashboard.py
from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index_page():
    return render_template("index.html")

@dashboard_bp.route("/charts")
def charts_page():
    return render_template("charts.html")

@dashboard_bp.route("/jobs")
def jobs_page():
    return render_template("jobs.html")
