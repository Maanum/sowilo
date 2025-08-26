import json
from typing import Any, Dict, List

from db.base import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        String, unique=True, index=True, default="default"
    )  # Single user for now
    entries_json = Column(Text, default="[]")  # Store as JSON string
    version = Column(Integer, default=1)  # Profile version for tracking changes

    def get_entries(self) -> List[Dict[str, Any]]:
        """Get profile entries as a list of dictionaries"""
        try:
            return json.loads(self.entries_json) if self.entries_json else []
        except json.JSONDecodeError:
            return []

    def set_entries(self, entries: List[Dict[str, Any]]) -> None:
        """Set profile entries from a list of dictionaries"""
        self.entries_json = json.dumps(entries, default=str)

    def add_entry(self, entry: Dict[str, Any]) -> None:
        """Add a new entry to the profile"""
        entries = self.get_entries()
        entries.append(entry)
        self.set_entries(entries)

    def update_entry(self, entry_id: str, updated_entry: Dict[str, Any]) -> bool:
        """Update an existing entry by ID"""
        entries = self.get_entries()
        for i, entry in enumerate(entries):
            if entry.get("id") == entry_id:
                entries[i] = updated_entry
                self.set_entries(entries)
                return True
        return False

    def delete_entry(self, entry_id: str) -> bool:
        """Delete an entry by ID"""
        entries = self.get_entries()
        for i, entry in enumerate(entries):
            if entry.get("id") == entry_id:
                del entries[i]
                self.set_entries(entries)
                return True
        return False

    def clear_entries(self) -> None:
        """Clear all entries from the profile"""
        self.set_entries([])

    __table_args__ = {"extend_existing": True}
