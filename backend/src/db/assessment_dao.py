from typing import Optional
from sqlalchemy.orm import Session
from models.assessment import Assessment
from models.opportunity import Opportunity


class AssessmentDAO:
    @staticmethod
    def get_by_opportunity_and_kind(db: Session, opportunity_id: int, kind: str) -> Optional[Assessment]:
        """Get assessment by opportunity_id and kind"""
        return db.query(Assessment).filter(
            Assessment.opportunity_id == opportunity_id,
            Assessment.kind == kind
        ).first()

    @staticmethod
    def create(db: Session, opportunity_id: int, kind: str = "initial", status: str = "pending") -> Assessment:
        """Create a new assessment"""
        assessment = Assessment(
            opportunity_id=opportunity_id,
            kind=kind,
            status=status
        )
        db.add(assessment)
        return assessment

    @staticmethod
    def update_status(db: Session, assessment_id: int, status: str, message: str = None) -> None:
        """Update assessment status"""
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        if assessment:
            assessment.status = status
            if message and status == "failed":
                assessment.summary = f"Error: {message}"

    @staticmethod
    def update_success(db: Session, assessment_id: int, summary: str) -> None:
        """Update assessment with successful result"""
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        if assessment:
            assessment.status = "succeeded"
            assessment.summary = summary

    @staticmethod
    def build_input_text_from_opportunity(opportunity: Opportunity) -> str:
        """Build input text from opportunity for LLM processing"""
        parts = []
        
        if opportunity.title:
            parts.append(f"Job Title: {opportunity.title}")
        
        if opportunity.company:
            parts.append(f"Company: {opportunity.company}")
            
        if opportunity.level:
            parts.append(f"Level: {opportunity.level}")
            
        if opportunity.min_salary or opportunity.max_salary:
            salary_parts = []
            if opportunity.min_salary:
                salary_parts.append(f"${opportunity.min_salary:,}")
            if opportunity.max_salary:
                salary_parts.append(f"${opportunity.max_salary:,}")
            parts.append(f"Salary: {' - '.join(salary_parts)}")
            
        if opportunity.posting_link:
            parts.append(f"Posting Link: {opportunity.posting_link}")
        
        return "\n\n".join(parts)