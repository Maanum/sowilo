"""
Simple migration to add updated_at column to job_assessments table
"""

from db.session import engine
from sqlalchemy import text


def upgrade():
    """Add updated_at column to job_assessments table"""
    with engine.connect() as conn:
        # Check if the updated_at column already exists
        result = conn.execute(text("PRAGMA table_info(job_assessments)"))
        columns = [row[1] for row in result.fetchall()]

        if "updated_at" not in columns:
            # Add updated_at column
            conn.execute(
                text(
                    "ALTER TABLE job_assessments ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                )
            )

            # Update existing records to have updated_at = created_at
            conn.execute(
                text(
                    "UPDATE job_assessments SET updated_at = created_at WHERE updated_at IS NULL"
                )
            )

            conn.commit()
            print("Successfully added updated_at column")
        else:
            print("updated_at column already exists")


if __name__ == "__main__":
    upgrade()
