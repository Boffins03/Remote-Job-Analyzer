# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# -----------------------
# Database connection URL
# -----------------------
DATABASE_URL = "postgresql+psycopg2://postgres:ILoveYou@localhost:8080/jobs"

# -----------------------
# SQLAlchemy Engine
# -----------------------
engine = create_engine(DATABASE_URL, echo=False)

# -----------------------
# Session Factory
# -----------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
