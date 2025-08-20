from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from services.profile_service import ProfileService, get_profile_service
from schemas import ProfileEntryCreate, ProfileEntry, ProfileResponse, ProfileGenerationResponse
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=ProfileResponse)
async def get_profile(service: ProfileService = Depends(get_profile_service)):
    """Get all profile entries"""
    return service.get_all_entries()

@router.post("/entry", response_model=ProfileEntry)
async def create_profile_entry(
    entry_data: ProfileEntryCreate,
    service: ProfileService = Depends(get_profile_service)
):
    """Create a new profile entry"""
    return service.create_entry(entry_data)

@router.put("/entry/{entry_id}", response_model=ProfileEntry)
async def update_profile_entry(
    entry_id: str,
    entry_data: ProfileEntryCreate,
    service: ProfileService = Depends(get_profile_service)
):
    """Update an existing profile entry"""
    updated_entry = service.update_entry(entry_id, entry_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail="Profile entry not found")
    return updated_entry

@router.delete("/entry/{entry_id}")
async def delete_profile_entry(
    entry_id: str,
    service: ProfileService = Depends(get_profile_service)
):
    """Delete a profile entry"""
    success = service.delete_entry(entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile entry not found")
    return {"message": "Profile entry deleted successfully"}

@router.post("/generate", response_model=ProfileGenerationResponse)
async def generate_profile(
    files: List[UploadFile] = File(default=[]),
    links: str = Form(default=""),
    description: Optional[str] = Form(default=None),
    service: ProfileService = Depends(get_profile_service)
):
    """Generate a new profile based on uploaded files and links"""
    # Parse links from comma-separated string
    links_list = [link.strip() for link in links.split(",") if link.strip()] if links else []
    
    return await service.generate_new_profile(files, links_list, description) 