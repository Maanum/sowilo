from sqlalchemy.orm import Session
from typing import List
from models.opportunity import Opportunity
from schemas import OpportunityCreate

def create_opportunity(db: Session, opportunity: OpportunityCreate) -> Opportunity:
    db_opportunity = Opportunity(**opportunity.model_dump())
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity

def get_opportunities(db: Session, skip: int = 0, limit: int = 100) -> List[Opportunity]:
    return db.query(Opportunity).offset(skip).limit(limit).all()

def delete_opportunity(db: Session, opportunity_id: int) -> bool:
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if opportunity is None:
        return False
    db.delete(opportunity)
    db.commit()
    return True 