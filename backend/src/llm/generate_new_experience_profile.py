import json
from typing import List

from api.openai_client import gpt_chat_complete
from llm.tools import profile_create
from schemas import ProfileEntry, ProfileGenerationResponse, SourceContent

SYSTEM_PROMPT = """
You are a professional resume and portfolio parser that extracts structured information from multiple sources including resumes, GitHub repositories, and other professional documents.

Your task is to analyze ALL provided content and create a comprehensive professional profile by combining information from:
1. RESUME/CV - Job titles, companies, dates, responsibilities, achievements
2. GITHUB REPOSITORIES - Projects, technologies, skills, contributions
3. EDUCATION - Degrees, institutions, graduation dates, relevant coursework
4. PERSONAL INFO - Contact information, summary, key skills

For each entry, provide:
- type: "experience", "education", "personal", or "project" (for GitHub/portfolio work)
- title: Job title, degree, project name, or personal identifier
- organization: Company name, institution, or project platform
- start_date/end_date: In YYYY-MM-DD format when available
- key_notes: Important details like responsibilities, achievements, skills, technologies used

IMPORTANT: When combining information from multiple sources:
- Merge duplicate information intelligently
- Extract technical skills from GitHub repositories and add them to relevant experience
- Include project work as separate entries with type "project"
- Ensure all professional experience is captured comprehensively
"""


def generate_new_experience_profile(
    sources: List[SourceContent],
) -> ProfileGenerationResponse:
    # Combine all content with source labels for better context
    combined_content_parts = []
    for source in sources:
        source_label = f"[SOURCE: {source.source}]"
        combined_content_parts.append(f"{source_label}\n{source.content}")

    combined_content = "\n\n" + "=" * 50 + "\n\n".join(combined_content_parts)

    user_message = f"""
    Please analyze the following combined content from multiple sources and extract a comprehensive professional profile.
    
    The content includes information from:
    - Resume/CV files
    - GitHub repositories and projects
    - Other professional documents
    
    Focus on extracting and combining:
    - Work experience with job titles, companies, dates, and key achievements
    - Project work from GitHub repositories with technologies and descriptions
    - Education history with degrees and institutions
    - Technical skills, programming languages, and tools
    - Contact information and personal details
    
    IMPORTANT: Combine information intelligently from all sources to create a complete profile.
    If the same information appears in multiple sources, merge it into a single comprehensive entry.
    
    Here is the combined content to analyze:
    ---
    {combined_content}
    ---
    
    Extract as much professional experience as possible, including specific job responsibilities, achievements, and technical skills from all sources.
    """

    try:

        response = gpt_chat_complete(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            tools=profile_create,
            enforce_json=False,
        )

        tool_calls = getattr(response.choices[0].message, "tool_calls", None)
        if not tool_calls:
            print(f"Unexpected response from LLM: {response}")
            return ProfileGenerationResponse(
                entries=[], message="No tool calls received from LLM"
            )
        tool_call = tool_calls[0]
        entries = json.loads(tool_call.function.arguments)["entries"]

        # Remove GPT-generated ID if present and create ProfileEntry objects
        parsed_entries = []
        id_counter = 0
        for e in entries:
            print(f"Parsed entry: {e}")
            print(f"Type of entry: {type(e)}")
            if isinstance(e, dict):
                # Automatically generate an id for the entry starting at 0
                e["id"] = str(id_counter)
                id_counter += 1

                try:
                    parsed_entries.append(ProfileEntry(**e))
                except Exception as entry_error:
                    print(f"Failed to parse entry {e}: {entry_error}")
                    continue

        return ProfileGenerationResponse(
            entries=parsed_entries, message="Generated from LLM"
        )
    except Exception as e:
        print(f"Error in generate_new_experience_profile: {e}")
        # Return empty response on error
        return ProfileGenerationResponse(
            entries=[], message=f"Error generating profile: {str(e)}"
        )
