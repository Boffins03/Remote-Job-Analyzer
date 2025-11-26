from flask import Blueprint, render_template

routes = Blueprint("routes", __name__)

@routes.route("/")
def index():
    return render_template("index.html", title="Dashboard")

@routes.route("/charts")
def charts():
    return render_template("charts.html", title="Charts")

@routes.route("/jobs")
def jobs():
    return render_template("jobs.html", title="Jobs")
