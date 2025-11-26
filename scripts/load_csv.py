# scripts/load_csv.py

import pandas as pd
from datetime import datetime

from sqlalchemy.orm import Session
from app.db import engine
from app.models import Company, Source, Job

CSV_PATH = "data/processed/jobs_clean.csv"


def load_csv():
    df = pd.read_csv(CSV_PATH)

    session = Session(bind=engine)

    # ➤ Ensure the source exists (example: "remoteok")
    source_name = "remoteok"
    source = session.query(Source).filter_by(name=source_name).first()
    if not source:
        source = Source(name=source_name)
        session.add(source)
        session.commit()

    for _, row in df.iterrows():

        # -----------------------------------
        # 1️⃣ Insert or get company
        # -----------------------------------
        company_name = row["company"] if pd.notna(row["company"]) else "Unknown"

        company = session.query(Company).filter_by(name=company_name).first()
        if not company:
            company = Company(name=company_name)
            session.add(company)
            session.commit()

        # -----------------------------------
        # 2️⃣ Avoid duplicate jobs by apply_link
        # -----------------------------------
        existing_job = session.query(Job).filter_by(apply_link=row["apply_link"]).first()
        if existing_job:
            continue  # skip duplicate

        # -----------------------------------
        # 3️⃣ Insert job
        # -----------------------------------
        job = Job(
            title=row["title"],
            location=row["location"],
            salary=row["salary"],
            apply_link=row["apply_link"],
            company_id=company.id,
            source_id=source.id,
            scraped_at=datetime.utcnow(),
        )

        session.add(job)

    session.commit()
    session.close()

    print("✅ CSV loaded successfully into normalized schema.")


if __name__ == "__main__":
    load_csv()




# # scripts/load_csv.py
# import pandas as pd
# from sqlalchemy import text
# from app.db import engine
# from datetime import datetime

# CSV_PATH = "data/processed/jobs_clean.csv"

# df = pd.read_csv(CSV_PATH)

# with engine.begin() as conn:
#     for _, row in df.iterrows():
#         conn.execute(text("""
#             INSERT INTO jobs (title, company, location, salary, apply_link, source, scraped_at)
#             VALUES (:title, :company, :location, :salary, :apply_link, :source, :scraped_at)
#             ON CONFLICT (apply_link) DO NOTHING;
#         """), {
#             "title": row["title"],
#             "company": row["company"],
#             "location": row["location"],
#             "salary": row["salary"],
#             "apply_link": row["apply_link"],
#             "source": "remoteok",
#             "scraped_at": datetime.now()
#         })

# print("CSV loaded successfully.")
