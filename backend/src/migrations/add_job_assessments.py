import os
import sqlite3
from pathlib import Path


def run_migration():
    """Add job_assessments table and update profiles table"""

    # Get database path
    backend_dir = Path(__file__).parent.parent.parent
    db_path = backend_dir / "opportunities.db"

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Add version column to profiles table if it doesn't exist
        cursor.execute(
            """
            ALTER TABLE profiles ADD COLUMN version INTEGER DEFAULT 1
        """
        )

        # Create job_assessments table
        cursor.execute(
            """
            CREATE TABLE job_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opportunity_id INTEGER NOT NULL,
                profile_id INTEGER NOT NULL,
                profile_version INTEGER NOT NULL,
                
                -- Assessment results
                summary_of_fit TEXT NOT NULL,
                fit_score INTEGER NOT NULL CHECK (fit_score >= 1 AND fit_score <= 7),
                recommendation TEXT NOT NULL,
                
                -- Metadata
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                assessment_date DATE DEFAULT CURRENT_DATE,
                
                -- Foreign key constraints
                FOREIGN KEY (opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
                
                -- Ensure one assessment per opportunity-profile-version combo
                UNIQUE(opportunity_id, profile_id, profile_version)
            )
        """
        )

        # Create indexes
        cursor.execute(
            """
            CREATE INDEX idx_job_assessments_opportunity ON job_assessments(opportunity_id)
        """
        )

        cursor.execute(
            """
            CREATE INDEX idx_job_assessments_profile ON job_assessments(profile_id)
        """
        )

        # Commit changes
        conn.commit()
        print("Migration completed successfully!")

    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Version column already exists in profiles table, continuing...")
        elif "table job_assessments already exists" in str(e):
            print("Job assessments table already exists, skipping...")
        else:
            raise e
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration()
