from typing import List

from db.session import get_db, SessionLocal
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from schemas import Opportunity as OpportunitySchema
from schemas import OpportunityCreate
from services.opportunity_service import OpportunityService
from services.assessment_service import AssessmentService
from sqlalchemy.orm import Session

router = APIRouter()


class LinkRequest(BaseModel):
    link: str


@router.get("/", response_model=List[OpportunitySchema])
def get_opportunities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return OpportunityService.get_all(skip=skip, limit=limit, db=db)


@router.post("/", response_model=OpportunitySchema)
async def create_opportunity(
    opportunity: OpportunityCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        opp = await OpportunityService.create(opportunity, db)
        db.commit()  # ensure opp.id is persisted
        db.refresh(opp)
        
        background_tasks.add_task(
            AssessmentService.generate_for_opportunity,
            db_factory=SessionLocal,
            opportunity_id=opp.id,
            kind="initial",
        )
        return opp
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/from-link", response_model=OpportunitySchema)
async def create_opportunity_from_link(
    link_req: LinkRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        opp = await OpportunityService.create_from_link(link_req.link, db)
        db.commit()
        db.refresh(opp)
        
        background_tasks.add_task(
            AssessmentService.generate_for_opportunity,
            db_factory=SessionLocal,
            opportunity_id=opp.id,
            kind="initial",
        )
        return opp
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{opportunity_id}")
def delete_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    try:
        return OpportunityService.delete(opportunity_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
