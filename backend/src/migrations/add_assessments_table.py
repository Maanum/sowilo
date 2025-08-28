import os
import sqlite3
from pathlib import Path


def run_migration():
    """Add assessments table for initial opportunity assessments"""

    # Get database path
    backend_dir = Path(__file__).parent.parent.parent
    db_path = backend_dir / "opportunities.db"

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Create assessments table
        cursor.execute(
            """
            CREATE TABLE assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opportunity_id INTEGER NOT NULL,
                kind VARCHAR(32) NOT NULL DEFAULT 'initial',
                status VARCHAR(16) NOT NULL DEFAULT 'pending',
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                -- Foreign key constraints
                FOREIGN KEY (opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE,
                
                -- Ensure one assessment per opportunity-kind combo
                UNIQUE(opportunity_id, kind)
            )
        """
        )

        # Create indexes
        cursor.execute(
            """
            CREATE INDEX idx_assessments_opportunity ON assessments(opportunity_id)
        """
        )

        cursor.execute(
            """
            CREATE INDEX idx_assessments_status ON assessments(status)
        """
        )

        # Commit changes
        conn.commit()
        print("Migration completed successfully!")

    except sqlite3.OperationalError as e:
        if "table assessments already exists" in str(e):
            print("Assessments table already exists, skipping...")
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