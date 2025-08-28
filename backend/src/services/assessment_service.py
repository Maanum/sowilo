from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.assessment_dao import AssessmentDAO
from db.opportunity_dao import OpportunityDAO
from models.job_assessment import JobAssessment
from models.profile import Profile
from api.openai_client import gpt_chat_complete
import logging

logger = logging.getLogger(__name__)


class AssessmentService:
    @staticmethod
    def generate_for_opportunity(db_factory=SessionLocal, opportunity_id: int = None, kind: str = "initial") -> None:
        """
        Background-safe entrypoint. Opens its own session from db_factory.
        1) Upsert a row with status 'pending' (respect unique(opportunity_id, kind)).
        2) Fetch opportunity + any needed context (JD text, company, etc.).
        3) Call LLM parser/generator as needed.
        4) Persist summary/details and set status='succeeded' or 'failed'.
        """
        if opportunity_id is None:
            logger.error("generate_for_opportunity called without opportunity_id")
            return

        try:
            with db_factory() as db:
                # idempotency check / upsert 'pending'
                assessment = AssessmentDAO.get_by_opportunity_and_kind(db, opportunity_id, kind)
                if assessment and assessment.status == "succeeded":
                    logger.info(f"Assessment already exists for opportunity {opportunity_id}, kind {kind}")
                    return
                    
                if not assessment:
                    try:
                        assessment = AssessmentDAO.create(db, opportunity_id=opportunity_id, kind=kind, status="pending")
                        db.commit()
                        db.refresh(assessment)
                        logger.info(f"Created pending assessment for opportunity {opportunity_id}")
                    except IntegrityError:
                        db.rollback()
                        assessment = AssessmentDAO.get_by_opportunity_and_kind(db, opportunity_id, kind)
                        if assessment and assessment.status == "succeeded":
                            logger.info(f"Assessment already exists (concurrent creation) for opportunity {opportunity_id}")
                            return

                # fetch opportunity context
                opp = OpportunityDAO.get_by_id(db, opportunity_id)
                if not opp:
                    logger.error(f"Opportunity {opportunity_id} not found")
                    AssessmentDAO.update_status(db, assessment.id, "failed", message="Opportunity missing")
                    db.commit()
                    return

                # Build input text (title, company, description, link, etc.)
                input_text = AssessmentDAO.build_input_text_from_opportunity(opp)
                logger.info(f"Generating assessment for opportunity {opportunity_id}")

                # Call LLM to generate assessment summary
                summary = AssessmentService._make_assessment(input_text)

                AssessmentDAO.update_success(db, assessment.id, summary=summary)
                
                # Also create a JobAssessment for backward compatibility
                AssessmentService._create_job_assessment(db, opp, summary)
                
                db.commit()
                logger.info(f"Successfully generated assessment for opportunity {opportunity_id}")
                
        except Exception as e:
            logger.exception(f"Assessment generation failed for opportunity {opportunity_id}: {e}")
            try:
                with db_factory() as db:
                    a = AssessmentDAO.get_by_opportunity_and_kind(db, opportunity_id, kind)
                    if a:
                        AssessmentDAO.update_status(db, a.id, "failed", message=str(e))
                        db.commit()
            except Exception:
                logger.exception("Failed to record assessment failure status")

    @staticmethod
    def _make_assessment(input_text: str) -> str:
        """Generate an initial assessment summary using LLM"""
        try:
            system_prompt = """
You are a career advisor analyzing job opportunities. 
Given job posting information, provide a concise initial assessment focusing on:
1. What makes this role appealing or concerning
2. Key requirements and qualifications needed
3. Potential career growth opportunities
4. Any red flags or notable aspects

Keep the assessment informative but concise (2-3 paragraphs maximum).
"""
            
            user_prompt = f"""
Analyze this job opportunity and provide an initial assessment:

{input_text}
"""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = gpt_chat_complete(messages=messages, model="gpt-4o-mini")
            return response.strip()
            
        except Exception as e:
            logger.warning(f"LLM assessment failed: {e}")
            return f"Initial assessment could not be generated automatically. Manual review recommended for this opportunity. Error: {str(e)}"

    @staticmethod
    def _create_job_assessment(db: Session, opportunity, summary: str):
        """Create a JobAssessment record for backward compatibility"""
        try:
            # Check if JobAssessment already exists
            existing = db.query(JobAssessment).filter(JobAssessment.opportunity_id == opportunity.id).first()
            if existing:
                logger.info(f"JobAssessment already exists for opportunity {opportunity.id}")
                return
            
            # Get or create default profile
            profile = db.query(Profile).filter(Profile.user_id == "default").first()
            if not profile:
                profile = Profile(user_id="default")
                db.add(profile)
                db.flush()  # Get ID without committing
            
            # Create JobAssessment with default values
            job_assessment = JobAssessment(
                opportunity_id=opportunity.id,
                profile_id=profile.id,
                profile_version=profile.version,
                summary_of_fit=summary,
                fit_score=4,  # Default neutral score
                recommendation="Initial assessment generated. Consider reviewing opportunity details and fit."
            )
            
            db.add(job_assessment)
            logger.info(f"Created JobAssessment for opportunity {opportunity.id}")
            
        except Exception as e:
            logger.warning(f"Failed to create JobAssessment for opportunity {opportunity.id}: {e}")
            # Don't raise - this is a fallback system