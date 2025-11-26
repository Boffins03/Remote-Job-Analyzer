from flask import Blueprint, jsonify
from app.db import SessionLocal
from app.models import Job

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/jobs")
def get_jobs():
    session = SessionLocal()  # ← create session here

    try:
        jobs = session.query(Job).all()

        results = []
        for job in jobs:
            results.append({
                "id": job.id,
                "title": job.title,
                "company": job.company.name if job.company else None,
                "location": job.location,
                "salary": job.salary,
                "apply_link": job.apply_link,
                "source": job.source.name if job.source else None,
            })

        # return render_template("jobs.html", jobs=results)
        return jsonify({"jobs": results})

    finally:
        session.close()
