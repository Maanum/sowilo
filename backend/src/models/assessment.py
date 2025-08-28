from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, DateTime, func
from db.base import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False)
    kind = Column(String(32), nullable=False, default="initial")
    status = Column(String(16), nullable=False, default="pending")
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("opportunity_id", "kind", name="uq_assessment_opp_kind"),
    )