from db.profile_dao import ProfileDAO
from schemas import ProfileEntryCreate, ProfileEntry, ProfileResponse, ProfileGenerationResponse, SourceContent
from utils.web_scraping import fetch_and_extract_text
from utils.file_text_extractor import extract_text_from_pdf_bytes, extract_text_from_txt_bytes
from llm.generate_new_experience_profile import generate_new_experience_profile
from db.session import get_db
from typing import List, Optional
from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session
import uuid

class ProfileService:
    def __init__(self, db: Session):
        self.dao = ProfileDAO(db)
    
    def get_all_entries(self, user_id: str = "default") -> ProfileResponse:
        """Get all profile entries"""
        entries = self.dao.get_all_entries(user_id)
        return ProfileResponse(entries=entries)
    
    def create_entry(self, entry_data: ProfileEntryCreate, user_id: str = "default") -> ProfileEntry:
        """Create a new profile entry"""
        return self.dao.create_entry(entry_data, user_id)
    
    def update_entry(self, entry_id: str, entry_data: ProfileEntryCreate, user_id: str = "default") -> Optional[ProfileEntry]:
        """Update an existing profile entry"""
        return self.dao.update_entry(entry_id, entry_data, user_id)
    
    def delete_entry(self, entry_id: str, user_id: str = "default") -> bool:
        """Delete a profile entry"""
        return self.dao.delete_entry(entry_id, user_id)
    
    async def generate_new_profile(self, files: List[UploadFile], links: List[str], description: Optional[str] = None, user_id: str = "default") -> ProfileGenerationResponse:
        """Generate a new profile based on uploaded files and links"""
        extracted_contents = []
        
        # Process links to extract content
        for link in links:
            try:
                content = await fetch_and_extract_text(link)
                extracted_contents.append(SourceContent(source=link, content=content))
                print(f"Successfully extracted content from link: {link}")
            except Exception as e:
                print(f"Failed to extract content from {link}: {e}")

        # Process uploaded files
        for file in files:
            try:
                # Read file bytes
                file_bytes = file.file.read()
                file.file.seek(0)  # Reset file pointer for potential future reads
                
                # Determine file type and extract content
                content = ""
                if file.filename.lower().endswith('.pdf'):
                    content = extract_text_from_pdf_bytes(file_bytes)
                elif file.filename.lower().endswith('.txt'):
                    content = extract_text_from_txt_bytes(file_bytes)
                else:
                    print(f"Unsupported file type: {file.filename}")
                    continue
                
                if content.strip():
                    extracted_contents.append(SourceContent(source=file.filename, content=content))
                    print(f"Successfully extracted content from file: {file.filename}")
                else:
                    print(f"No content extracted from file: {file.filename}")
                    
            except Exception as e:
                print(f"Failed to process file {file.filename}: {e}")

        # Add description if provided
        if description:
            extracted_contents.append(SourceContent(source="description", content=description))
        
        # Generate new profile entries
        generated_profile_response = generate_new_experience_profile(extracted_contents)

        print(generated_profile_response)
        
        # Only proceed if we have successfully generated entries
        if not generated_profile_response.entries:
            return ProfileGenerationResponse(
                message="Failed to generate profile entries. No changes made to existing profile.",
                entries=[]
            )
        
        try:
            # Convert generated entries to ProfileEntryCreate objects
            entries_to_create = []
            for entry in generated_profile_response.entries:
                entry_data = ProfileEntryCreate(
                    type=entry.type,
                    title=entry.title,
                    organization=entry.organization,
                    start_date=entry.start_date,
                    end_date=entry.end_date,
                    key_notes=entry.key_notes
                )
                entries_to_create.append(entry_data)
            
            # Atomically replace all entries: delete old ones and create new ones
            self.dao.delete_all_entries(user_id)
            created_entries = self.dao.create_multiple_entries(entries_to_create, user_id)
            
            return ProfileGenerationResponse(
                message=f"Successfully generated new profile with {len(created_entries)} entries based on {len(files)} files and {len(links)} links. Previous entries have been replaced.",
                entries=created_entries
            )
            
        except Exception as e:
            print(f"Error saving generated profile: {e}")
            return ProfileGenerationResponse(
                message=f"Generated {len(generated_profile_response.entries)} entries but failed to save them. No changes made to existing profile.",
                entries=[]
            )

def get_profile_service(db: Session = Depends(get_db)) -> ProfileService:
    """Dependency to get profile service"""
    return ProfileService(db) 