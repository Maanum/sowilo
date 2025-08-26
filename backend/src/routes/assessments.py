from typing import List

from db.session import get_db
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from models.job_assessment import JobAssessment
from models.opportunity import Opportunity
from models.profile import Profile
from schemas import JobAssessment as JobAssessmentSchema
from schemas import JobAssessmentCreate
from services.assessment_service import AssessmentService
from sqlalchemy.orm import Session, joinedload

router = APIRouter(tags=["assessments"])


def get_assessment_service():
    return AssessmentService()


@router.post(
    "/opportunities/{opportunity_id}/assess", response_model=JobAssessmentSchema
)
async def create_assessment(
    opportunity_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    assessment_service: AssessmentService = Depends(get_assessment_service),
    profile_id: int = 1,  # Default to profile ID 1 (the default profile)
):
    """Generate job assessment for opportunity-profile pair"""

    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    # Get the default profile (user_id="default")
    profile = db.query(Profile).filter(Profile.user_id == "default").first()
    if not profile:
        # Create the default profile if it doesn't exist
        profile = Profile(user_id="default")
        db.add(profile)
        db.commit()
        db.refresh(profile)

    # Generate assessment
    assessment = assessment_service.assess_opportunity(opportunity, profile, db)

    if assessment.id is None:  # New assessment
        db.add(assessment)
        db.commit()
        db.refresh(assessment)

    return assessment


@router.get("/opportunities/{opportunity_id}", response_model=JobAssessmentSchema)
async def get_opportunity_assessment(
    opportunity_id: int,
    db: Session = Depends(get_db),
    assessment_service: AssessmentService = Depends(get_assessment_service),
):
    """Get the single assessment for an opportunity"""
    assessment = assessment_service.get_assessment_for_opportunity(opportunity_id, db)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment


@router.get("/profiles/{profile_id}", response_model=List[JobAssessmentSchema])
async def get_profile_assessments(profile_id: int, db: Session = Depends(get_db)):
    """Get all assessments for a profile"""
    return (
        db.query(JobAssessment)
        .filter(JobAssessment.profile_id == profile_id)
        .options(joinedload(JobAssessment.opportunity))
        .all()
    )


@router.delete("/{assessment_id}")
async def delete_assessment(assessment_id: int, db: Session = Depends(get_db)):
    """Delete a job assessment"""
    assessment = (
        db.query(JobAssessment).filter(JobAssessment.id == assessment_id).first()
    )
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    db.delete(assessment)
    db.commit()
    return {"message": "Assessment deleted successfully"}
