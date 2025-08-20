from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from schemas import OpportunityCreate, Opportunity as OpportunitySchema
from db.session import get_db
from services.opportunity_service import OpportunityService

router = APIRouter()

class LinkRequest(BaseModel):
    link: str

@router.get("/", response_model=List[OpportunitySchema])
def get_opportunities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return OpportunityService.get_all(skip=skip, limit=limit, db=db)

@router.post("/", response_model=OpportunitySchema)
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db)):
    try:
        return OpportunityService.create(opportunity, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/from-link", response_model=OpportunitySchema)
def create_opportunity_from_link(link_req: LinkRequest, db: Session = Depends(get_db)):
    try:
        return OpportunityService.create_from_link(link_req.link, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{opportunity_id}")
def delete_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    try:
        return OpportunityService.delete(opportunity_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 