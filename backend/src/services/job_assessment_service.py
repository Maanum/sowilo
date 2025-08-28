import re
from typing import Any, Dict, Optional

import openai
from config import settings
from models.job_assessment import JobAssessment
from models.opportunity import Opportunity
from models.profile import Profile
from sqlalchemy.orm import Session


class AssessmentService:
    def __init__(self, openai_client=None):
        self.client = openai_client or openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    def assess_opportunity(
        self, opportunity: Opportunity, profile: Profile, db: Session
    ) -> JobAssessment:
        """Generate AI assessment of opportunity fit for profile"""

        # Check if assessment already exists for this opportunity
        existing = (
            db.query(JobAssessment)
            .filter(JobAssessment.opportunity_id == opportunity.id)
            .first()
        )

        # Generate new assessment
        prompt = self._build_assessment_prompt(opportunity, profile)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Use cost-effective model
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert career counselor and recruiter. Provide honest, actionable job fit assessments.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=500,
            )

            assessment_data = self._parse_assessment_response(
                response.choices[0].message.content
            )

            if existing:
                # Update existing assessment
                existing.profile_id = profile.id
                existing.profile_version = profile.version
                existing.summary_of_fit = assessment_data["summary"]
                existing.fit_score = assessment_data["score"]
                existing.recommendation = assessment_data["recommendation"]
                # updated_at will be automatically set by SQLAlchemy
                db.commit()
                db.refresh(existing)
                return existing
            else:
                # Create new assessment
                assessment = JobAssessment(
                    opportunity_id=opportunity.id,
                    profile_id=profile.id,
                    profile_version=profile.version,
                    summary_of_fit=assessment_data["summary"],
                    fit_score=assessment_data["score"],
                    recommendation=assessment_data["recommendation"],
                )
                return assessment

        except Exception as e:
            # Fallback assessment if AI fails
            fallback_assessment = JobAssessment(
                opportunity_id=opportunity.id,
                profile_id=profile.id,
                profile_version=profile.version,
                summary_of_fit="Assessment could not be generated automatically. Manual review recommended.",
                fit_score=4,
                recommendation="Review this opportunity manually to determine fit.",
            )

            if existing:
                # Update existing assessment with fallback
                existing.profile_id = profile.id
                existing.profile_version = profile.version
                existing.summary_of_fit = fallback_assessment.summary_of_fit
                existing.fit_score = fallback_assessment.fit_score
                existing.recommendation = fallback_assessment.recommendation
                db.commit()
                db.refresh(existing)
                return existing
            else:
                return fallback_assessment

    def get_assessment_for_opportunity(
        self, opportunity_id: int, db: Session
    ) -> Optional[JobAssessment]:
        """Get the single assessment for an opportunity"""
        return (
            db.query(JobAssessment)
            .filter(JobAssessment.opportunity_id == opportunity_id)
            .first()
        )

    def _build_assessment_prompt(
        self, opportunity: Opportunity, profile: Profile
    ) -> str:
        # Extract profile data from JSON entries
        entries = profile.get_entries()

        # Organize profile data by type
        personal_info = []
        experience_entries = []
        education_entries = []
        skills_entries = []

        for entry in entries:
            entry_type = entry.get("type", "")
            if entry_type == "personal":
                personal_info.append(entry)
            elif entry_type == "experience":
                experience_entries.append(entry)
            elif entry_type == "education":
                education_entries.append(entry)
            elif "skills" in entry_type.lower():
                skills_entries.append(entry)

        # Format experience
        experience_text = ""
        for exp in experience_entries:
            title = exp.get("title", "")
            org = exp.get("organization", "")
            start_date = exp.get("start_date", "")
            end_date = exp.get("end_date", "")
            notes = exp.get("key_notes", [])

            experience_text += f"- {title} at {org} ({start_date} to {end_date})\n"
            for note in notes:
                experience_text += f"  • {note}\n"
            experience_text += "\n"

        # Format skills
        skills_text = ""
        for skill_entry in skills_entries:
            notes = skill_entry.get("key_notes", [])
            skills_text += ", ".join(notes)

        # Format education
        education_text = ""
        for edu in education_entries:
            title = edu.get("title", "")
            org = edu.get("organization", "")
            education_text += f"- {title} from {org}\n"

        # Format personal info
        personal_text = ""
        for personal in personal_info:
            notes = personal.get("key_notes", [])
            personal_text = " ".join(notes)

        return f"""
Assess job fit for this opportunity and candidate profile:

OPPORTUNITY:
Title: {opportunity.title}
Company: {opportunity.company}
Level: {opportunity.level or "Not specified"}
Salary Range: {opportunity.min_salary or "Not specified"} - {opportunity.max_salary or "Not specified"}

CANDIDATE PROFILE:
Personal Summary: {personal_text}

Experience:
{experience_text}

Skills: {skills_text}

Education:
{education_text}

Provide assessment in this EXACT format:

SUMMARY OF FIT:
[2-3 sentences on how well the role matches skills, experience, and career goals. Highlight key strengths and any potential gaps.]

FIT SCORE: [Single integer 1-7 where 1=poor fit, 7=excellent fit]

RECOMMENDATION:
[1-2 sentences with actionable recommendation like "Strong candidate - prioritize application" or "Consider if no better options available"]
        """

    def _parse_assessment_response(self, response: str) -> Dict[str, Any]:
        """Parse structured AI response into components"""

        # Default values
        summary = "Assessment parsing failed - manual review needed."
        score = 4
        recommendation = "Manual review recommended."

        try:
            # Extract summary
            summary_match = re.search(
                r"SUMMARY OF FIT:\s*(.+?)(?=FIT SCORE:|$)",
                response,
                re.DOTALL | re.IGNORECASE,
            )
            if summary_match:
                summary = summary_match.group(1).strip()

            # Extract score
            score_match = re.search(r"FIT SCORE:\s*(\d+)", response, re.IGNORECASE)
            if score_match:
                score = int(score_match.group(1))
                score = max(1, min(7, score))  # Ensure 1-7 range

            # Extract recommendation
            rec_match = re.search(
                r"RECOMMENDATION:\s*(.+?)$", response, re.DOTALL | re.IGNORECASE
            )
            if rec_match:
                recommendation = rec_match.group(1).strip()

        except Exception as e:
            print(f"Error parsing assessment response: {e}")

        return {"summary": summary, "score": score, "recommendation": recommendation}
