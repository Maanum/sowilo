from typing import List

from db.opportunity_dao import create_opportunity, delete_opportunity, get_opportunities
from llm.job_description_parser import parse_opportunity_from_link_async
from models.opportunity import ALLOWED_STATUSES, Opportunity
from models.profile import Profile
from schemas import Opportunity as OpportunitySchema
from schemas import OpportunityCreate
from services.assessment_service import AssessmentService
from sqlalchemy.orm import Session


class OpportunityService:
    @staticmethod
    def get_all(skip: int, limit: int, db: Session) -> List[Opportunity]:
        return get_opportunities(db, skip=skip, limit=limit)

    @staticmethod
    async def create(opportunity: OpportunityCreate, db: Session) -> Opportunity:
        if opportunity.status not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: {opportunity.status}")

        # Create the opportunity
        created_opportunity = create_opportunity(db, opportunity)

        # Auto-generate assessment
        await OpportunityService._generate_initial_assessment(created_opportunity, db)

        return created_opportunity

    @staticmethod
    async def create_from_link(link: str, db: Session) -> Opportunity:
        # Use LLM/Enricher to parse the link and get OpportunityCreate data
        parsed_opportunity = await parse_opportunity_from_link_async(link)
        return await OpportunityService.create(parsed_opportunity, db)

    @staticmethod
    def delete(opportunity_id: int, db: Session):
        deleted = delete_opportunity(db, opportunity_id)
        if not deleted:
            raise ValueError("Opportunity not found")
        return {"message": "Opportunity deleted successfully"}

    @staticmethod
    async def _generate_initial_assessment(opportunity: Opportunity, db: Session):
        """Generate initial assessment for a new opportunity"""
        try:
            # Get the default profile
            profile = db.query(Profile).filter(Profile.user_id == "default").first()
            if not profile:
                # Create the default profile if it doesn't exist
                profile = Profile(user_id="default")
                db.add(profile)
                db.commit()
                db.refresh(profile)

            # Generate assessment
            assessment_service = AssessmentService()
            assessment = await assessment_service.assess_opportunity(
                opportunity, profile, db
            )

            if assessment.id is None:  # New assessment
                db.add(assessment)
                db.commit()
                db.refresh(assessment)

        except Exception as e:
            # Log error but don't fail opportunity creation
            print(
                f"Failed to generate initial assessment for opportunity {opportunity.id}: {e}"
            )
            db.rollback()
