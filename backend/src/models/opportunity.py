from sqlalchemy import Column, Integer, String
from db.base import Base

ALLOWED_STATUSES = [
    "Applied",
    "Screening",
    "Rejected",
    "Did Not Apply",
    "Interviewing",
    "To Apply"
]

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    level = Column(String, nullable=True)
    min_salary = Column(Integer, nullable=True)
    max_salary = Column(Integer, nullable=True)
    posting_link = Column(String, nullable=True)
    resume_link = Column(String, nullable=True)
    cover_letter_link = Column(String, nullable=True)
    company = Column(String, index=True)
    status = Column(String, default="To Apply", nullable=False) 