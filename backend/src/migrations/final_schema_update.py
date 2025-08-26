"""
Final migration to update job_assessments table schema
"""

from db.session import engine
from sqlalchemy import text


def upgrade():
    """Update job_assessments table to have single assessment per opportunity"""
    with engine.connect() as conn:
        # Create backup of existing data
        conn.execute(
            text("CREATE TABLE job_assessments_backup AS SELECT * FROM job_assessments")
        )

        # Drop the original table
        conn.execute(text("DROP TABLE job_assessments"))

        # Create new table with correct schema
        conn.execute(
            text(
                """
            CREATE TABLE job_assessments (
                id INTEGER PRIMARY KEY,
                opportunity_id INTEGER NOT NULL UNIQUE,
                profile_id INTEGER NOT NULL,
                profile_version INTEGER NOT NULL,
                summary_of_fit TEXT NOT NULL,
                fit_score INTEGER NOT NULL,
                recommendation TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                assessment_date DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
            )
        """
            )
        )

        # Copy data back, keeping only the most recent assessment per opportunity
        conn.execute(
            text(
                """
            INSERT INTO job_assessments (
                id, opportunity_id, profile_id, profile_version,
                summary_of_fit, fit_score, recommendation,
                created_at, updated_at, assessment_date
            )
            SELECT 
                id, opportunity_id, profile_id, profile_version,
                summary_of_fit, fit_score, recommendation,
                created_at, updated_at, assessment_date
            FROM job_assessments_backup
            WHERE id IN (
                SELECT MAX(id) 
                FROM job_assessments_backup 
                GROUP BY opportunity_id
            )
        """
            )
        )

        # Drop the backup table
        conn.execute(text("DROP TABLE job_assessments_backup"))

        # Recreate indexes
        conn.execute(
            text(
                "CREATE INDEX idx_job_assessments_opportunity ON job_assessments(opportunity_id)"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX idx_job_assessments_profile ON job_assessments(profile_id)"
            )
        )

        conn.commit()
        print("Successfully updated job_assessments table schema")


if __name__ == "__main__":
    upgrade()
