from typing import List

from db.opportunity_dao import create_opportunity, delete_opportunity, get_opportunities
from llm.job_description_parser import parse_opportunity_from_link_async
from models.opportunity import ALLOWED_STATUSES, Opportunity
from schemas import Opportunity as OpportunitySchema
from schemas import OpportunityCreate
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

