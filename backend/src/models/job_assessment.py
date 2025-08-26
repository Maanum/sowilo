from datetime import date, datetime

from db.base import Base
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)


class JobAssessment(Base):
    __tablename__ = "job_assessments"

    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(
        Integer,
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    profile_id = Column(
        Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    profile_version = Column(Integer, nullable=False)

    # Assessment results
    summary_of_fit = Column(Text, nullable=False)
    fit_score = Column(Integer, nullable=False)  # 1-7 scale
    recommendation = Column(Text, nullable=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assessment_date = Column(Date, default=date.today)

    __table_args__ = {"extend_existing": True}
