# app/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


# -------------------------------------------------
# COMPANY TABLE
# -------------------------------------------------
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    # Relationships
    jobs = relationship("Job", back_populates="company")

    def __repr__(self):
        return f"<Company {self.name}>"


# -------------------------------------------------
# SOURCE TABLE
# (remoteok, weworkremotely, etc.)
# -------------------------------------------------
class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    jobs = relationship("Job", back_populates="source")

    def __repr__(self):
        return f"<Source {self.name}>"


# ----------------------------------------------
# SKILL TABLE
# ----------------------------------------------
# class Skill(Base):
#     __tablename__ = "skills"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(100), unique=True, nullable=False)

#     job_links = relationship("JobSkill", back_populates="skill")

#     def __repr__(self):
#         return f"<Skill {self.name}>"

# ----------------------------------------------
# JOB ↔ SKILL Many-to-Many Table
# ----------------------------------------------
# class JobSkill(Base):
#     __tablename__ = "job_skills"

#     job_id = Column(Integer, ForeignKey("jobs.id"), primary_key=True)
#     skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)

#     job = relationship("Job", back_populates="skill_links")
#     skill = relationship("Skill", back_populates="job_links")


# -------------------------------------------------
# JOB TABLE
# -------------------------------------------------
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(Text, nullable=False)
    location = Column(Text, nullable=True)
    salary = Column(Integer, nullable=True)
    apply_link = Column(Text, unique=True, nullable=False)

    company_id = Column(Integer, ForeignKey("companies.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))

    # skill_links = relationship("JobSkill", back_populates="job")

    scraped_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="jobs")
    source = relationship("Source", back_populates="jobs")

    # Prevent duplicate jobs for same link
    __table_args__ = (UniqueConstraint("apply_link", name="uq_apply_link"),)

    def __repr__(self):
        return f"<Job {self.title}>"    
