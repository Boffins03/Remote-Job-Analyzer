from flask import Blueprint, jsonify, current_app
from sqlalchemy import func, extract
from app.models import Job, Company

stats_bp = Blueprint("stats", __name__)


# --------------------------------------------------------
# 1) Overview Stats
# --------------------------------------------------------
@stats_bp.route("/stats/overview", methods=["GET"])
def get_overview():
    session = current_app.session

    # Total jobs
    total_jobs = session.query(func.count(Job.id)).scalar()

    # Total companies
    total_companies = session.query(func.count(Company.id)).scalar()

    # Top hiring companies
    top_company = (
        session.query(Company.name, func.count(Job.id))
        .join(Job)
        .group_by(Company.id)
        .order_by(func.count(Job.id).desc())
        .first()
    )

    top_company_name = top_company[0] if top_company else None

   # Average salary (if exists)
    avg_salary = session.query(func.avg(Job.salary)).scalar()

    return jsonify({
        "total_jobs": total_jobs,
        "total_companies": total_companies,
        # "top_skill": top_company_name,
        "avg_salary": float(avg_salary) if avg_salary else None
    }) 


# --------------------------------------------------------
# 2) Job Trends (Jobs per Month)
# --------------------------------------------------------
@stats_bp.route("/stats/job-trends", methods=["GET"])
def job_trends():
    session = current_app.session

    monthly_counts = (
        session.query(
            extract("year", Job.scraped_at).label("year"),
            extract("month", Job.scraped_at).label("month"),
            func.count(Job.id).label("total")
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )

    results = [
        {
            "year": int(year),
            "month": int(month),
            "total_jobs": total
        }
        for year, month, total in monthly_counts
    ]

    return jsonify(results)


# --------------------------------------------------------
# 3) Top Job Titles
# --------------------------------------------------------
@stats_bp.route("/stats/top-titles", methods=["GET"])
def top_titles():
    session = current_app.session

    titles = (
        session.query(
            func.lower(Job.title).label("title"),
            func.count(Job.id).label("count")
        )
        .group_by("title")
        .order_by(func.count(Job.id).desc())
        .limit(10)
        .all()
    )

    return jsonify([
        {"title": title, "count": count}
        for title, count in titles
    ])


# --------------------------------------------------------
# 4) Salary Statistics
# --------------------------------------------------------
@stats_bp.route("/stats/salary", methods=["GET"])
def salary_stats():
    session = current_app.session

    # If your DB has a single numeric salary field:
    min_salary = session.query(func.min(Job.salary)).scalar()
    max_salary = session.query(func.max(Job.salary)).scalar()
    avg_salary = session.query(func.avg(Job.salary)).scalar()

    if min_salary is None or max_salary is None:
        return jsonify({
            "error": "No valid salary data found",
            "min_salary": None,
            "max_salary": None,
            "avg_salary": None
        })

    return jsonify({
        "min_salary": float(min_salary),
        "max_salary": float(max_salary),
        "avg_salary": float(avg_salary)
    })
