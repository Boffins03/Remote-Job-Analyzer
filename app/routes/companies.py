from flask import Blueprint, jsonify, current_app
from app.models import Company, Job

companies_bp = Blueprint("companies", __name__)

@companies_bp.route("/companies", methods=["GET"])
def get_companies():
    session = current_app.session  # FIXED

    companies = session.query(Company).all()
    output = []

    for c in companies:
        output.append({
            "id": c.id,
            "name": c.name,
            "job_count": len(c.jobs)
        })

    return jsonify(output)
