from sqlalchemy.orm import Session
from models.profile import Profile
from schemas import ProfileEntryCreate, ProfileEntry
from typing import List, Optional
import uuid

class ProfileDAO:
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_profile(self, user_id: str = "default") -> Profile:
        """Get existing profile or create a new one"""
        profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            profile = Profile(user_id=user_id)
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
        return profile
    
    def get_all_entries(self, user_id: str = "default") -> List[ProfileEntry]:
        """Get all profile entries for a user"""
        profile = self.get_or_create_profile(user_id)
        entries_data = profile.get_entries()
        return [ProfileEntry(**entry) for entry in entries_data]
    
    def create_entry(self, entry_data: ProfileEntryCreate, user_id: str = "default") -> ProfileEntry:
        """Create a new profile entry"""
        profile = self.get_or_create_profile(user_id)
        
        # Generate unique ID
        entry_id = str(uuid.uuid4())
        
        # Create entry with ID
        entry_dict = entry_data.model_dump()
        entry_dict['id'] = entry_id
        
        # Add to profile
        profile.add_entry(entry_dict)
        self.db.commit()
        
        return ProfileEntry(**entry_dict)
    
    def update_entry(self, entry_id: str, entry_data: ProfileEntryCreate, user_id: str = "default") -> Optional[ProfileEntry]:
        """Update an existing profile entry"""
        profile = self.get_or_create_profile(user_id)
        
        # Create updated entry with ID
        entry_dict = entry_data.model_dump()
        entry_dict['id'] = entry_id
        
        # Update in profile
        if profile.update_entry(entry_id, entry_dict):
            self.db.commit()
            return ProfileEntry(**entry_dict)
        return None
    
    def delete_entry(self, entry_id: str, user_id: str = "default") -> bool:
        """Delete a profile entry"""
        profile = self.get_or_create_profile(user_id)
        
        if profile.delete_entry(entry_id):
            self.db.commit()
            return True
        return False
    
    def delete_all_entries(self, user_id: str = "default") -> bool:
        """Delete all profile entries for a user"""
        profile = self.get_or_create_profile(user_id)
        profile.clear_entries()
        self.db.commit()
        return True
    
    def create_multiple_entries(self, entries_data: List[ProfileEntryCreate], user_id: str = "default") -> List[ProfileEntry]:
        """Create multiple profile entries atomically"""
        profile = self.get_or_create_profile(user_id)
        created_entries = []
        
        for entry_data in entries_data:
            # Generate unique ID
            entry_id = str(uuid.uuid4())
            
            # Create entry with ID
            entry_dict = entry_data.model_dump()
            entry_dict['id'] = entry_id
            
            # Add to profile
            profile.add_entry(entry_dict)
            created_entries.append(ProfileEntry(**entry_dict))
        
        self.db.commit()
        return created_entries 