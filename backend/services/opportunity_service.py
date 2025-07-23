from sqlalchemy.orm import Session
from typing import List
from backend.schemas import OpportunityCreate, Opportunity as OpportunitySchema
from backend.models.opportunity import Opportunity, ALLOWED_STATUSES
from backend.db.opportunity_dao import (
    create_opportunity,
    get_opportunities,
    delete_opportunity,
)
from backend.llm.job_description_parser import parse_opportunity_from_link

class OpportunityService:
    @staticmethod
    def get_all(skip: int, limit: int, db: Session) -> List[Opportunity]:
        return get_opportunities(db, skip=skip, limit=limit)

    @staticmethod
    def create(opportunity: OpportunityCreate, db: Session) -> Opportunity:
        if opportunity.status not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: {opportunity.status}")
        # Example enrichment (stub)
        # opportunity = enrich_opportunity_notes(opportunity)
        return create_opportunity(db, opportunity)

    @staticmethod
    def create_from_link(link: str, db: Session) -> Opportunity:
        # Use LLM/Enricher to parse the link and get OpportunityCreate data
        parsed_opportunity = parse_opportunity_from_link(link)
        return OpportunityService.create(parsed_opportunity, db)

    @staticmethod
    def delete(opportunity_id: int, db: Session):
        deleted = delete_opportunity(db, opportunity_id)
        if not deleted:
            raise ValueError("Opportunity not found")
        return {"message": "Opportunity deleted successfully"} 