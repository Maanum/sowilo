#!/usr/bin/env python3
"""
Simple test script to verify job assessment functionality
"""

import asyncio
import os
import sys

sys.path.append("src")

from src.db.session import get_db
from src.models.opportunity import Opportunity
from src.models.profile import Profile
from src.services.assessment_service import AssessmentService


async def test_assessment():
    """Test the assessment service"""
    print("Testing job assessment functionality...")

    # Get database session
    db = next(get_db())

    try:
        # Check if we have opportunities and profiles
        opportunities = db.query(Opportunity).all()
        profiles = db.query(Profile).all()

        print(f"Found {len(opportunities)} opportunities and {len(profiles)} profiles")

        if not opportunities:
            print("No opportunities found. Please add some opportunities first.")
            return

        if not profiles:
            print("No profiles found. Please add a profile first.")
            return

        # Use the first opportunity and profile for testing
        opportunity = opportunities[0]
        profile = profiles[0]

        print(
            f"Testing assessment for opportunity: {opportunity.title} at {opportunity.company}"
        )
        print(f"Using profile ID: {profile.id}")

        # Create assessment service
        assessment_service = AssessmentService()

        # Generate assessment (this will be a fallback since we don't have OpenAI key)
        assessment = await assessment_service.assess_opportunity(
            opportunity, profile, db
        )

        print(f"Assessment created with ID: {assessment.id}")
        print(f"Fit score: {assessment.fit_score}/7")
        print(f"Summary: {assessment.summary_of_fit}")
        print(f"Recommendation: {assessment.recommendation}")

        # Save to database
        db.add(assessment)
        db.commit()
        print("Assessment saved to database successfully!")

    except Exception as e:
        print(f"Error during testing: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(test_assessment())
