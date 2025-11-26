# analysis/stats_service.py

from sqlalchemy.orm import Session
from app.db import engine
from analysis.queries import (
    QUERY_TOP_COMPANIES,
    QUERY_JOBS_PER_MONTH,
    QUERY_TOP_TITLES,
    QUERY_SALARY_STATS
)
import pandas as pd

def get_top_companies():
    with engine.connect() as conn:
        result = conn.execute(QUERY_TOP_COMPANIES)
        return [dict(row) for row in result]

def get_jobs_per_month():
    with engine.connect() as conn:
        result = conn.execute(QUERY_JOBS_PER_MONTH)
        data = pd.DataFrame(result, columns=["month", "total_jobs"])
        data["month"] = data["month"].astype(str)
        return data.to_dict(orient="records")

def get_top_titles():
    with engine.connect() as conn:
        result = conn.execute(QUERY_TOP_TITLES)
        return [dict(row) for row in result]

def get_salary_distribution():
    with engine.connect() as conn:
        result = conn.execute(QUERY_SALARY_STATS)
        salaries = [row[0] for row in result]

    # Convert "$120k – $200k" to numeric values
    cleaned = []
    for s in salaries:
        try:
            parts = s.replace("$", "").replace("k", "").split("–")
            low = int(parts[0].strip()) * 1000
            high = int(parts[1].strip()) * 1000
            cleaned.append({"min": low, "max": high})
        except:
            continue

    df = pd.DataFrame(cleaned)
    return {
        "min_salary": int(df["min"].min()),
        "max_salary": int(df["max"].max()),
        "avg_min_salary": int(df["min"].mean()),
        "avg_max_salary": int(df["max"].mean())
    }
