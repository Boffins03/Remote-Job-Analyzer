from app.db import SessionLocal
from app.models import Job

session = SessionLocal()

jobs = session.query(Job).limit(5).all()

for job in jobs:
    print(job.title, "-", job.company)
