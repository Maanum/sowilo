from pydantic import BaseModel, field_validator
from typing import Optional, Literal, List
from datetime import date

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

# Profile schemas
class ProfileEntryBase(BaseModel):
    type: Literal["experience", "education", "personal"]
    title: Optional[str] = None
    organization: Optional[str] = None
    start_date: Optional[str] = None  # YYYY-MM-DD format
    end_date: Optional[str] = None    # YYYY-MM-DD format
    key_notes: List[str] = []

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v):
        if v is not None:
            try:
                date.fromisoformat(v)
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        return v

class ProfileEntryCreate(ProfileEntryBase):
    pass

class ProfileEntry(ProfileEntryBase):
    id: str

    class Config:
        from_attributes = True

class ProfileResponse(BaseModel):
    entries: List[ProfileEntry]

# Profile Generation schemas
class ProfileGenerationRequest(BaseModel):
    files: List[str] = []  # List of file URLs/identifiers
    links: List[str] = []  # List of URLs to analyze
    description: Optional[str] = None  # Additional description/context

class ProfileGenerationResponse(BaseModel):
    message: str
    entries: List[ProfileEntry] 

# Used for generating new profile
class SourceContent(BaseModel):
    source: str  # URL or filename
    content: str