from api.openai_client import gpt_chat_complete
from schemas import OpportunityCreate
from utils.web_scraping import fetch_and_extract_text

SYSTEM_PROMPT = """
You are a job parser. Given raw text from a job posting, extract structured information
that matches this schema:

{
  title: str
  company: str
  level: Optional[str]
  min_salary: Optional[int]
  max_salary: Optional[int]
}

Respond only with a JSON object matching this schema. Do not explain your answer.
If salary is not found, leave it null. If level is not clear, leave it null.
"""


async def parse_opportunity_from_link_async(link: str) -> OpportunityCreate:
    job_description_content = await fetch_and_extract_text(link)

    gpt_response = gpt_chat_complete(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": job_description_content},
        ],
        enforce_json=True,
    )

    parsed_opportunity = {
        **gpt_response,  # Everything parsed by GPT
        "status": "To Apply",  # Override status
        "posting_link": link,  # Override link
    }

    return OpportunityCreate(**parsed_opportunity)
