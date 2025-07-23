from pydantic import BaseModel, field_validator
from typing import Optional, Literal

ALLOWED_STATUSES = [
    "Applied",
    "Screening",
    "Rejected",
    "Did Not Apply",
    "Interviewing",
    "To Apply"
]

class OpportunityBase(BaseModel):
    title: str
    level: Optional[str] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    posting_link: Optional[str] = None
    resume_link: Optional[str] = None
    cover_letter_link: Optional[str] = None
    company: str
    status: Literal["Applied", "Screening", "Rejected", "Did Not Apply", "Interviewing", "To Apply"] = "To Apply"

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: {v}")
        return v

class OpportunityCreate(OpportunityBase):
    pass

class Opportunity(OpportunityBase):
    id: int

    class Config:
        from_attributes = True 