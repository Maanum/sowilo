from typing import List

from openai.types.chat import ChatCompletionToolParam
from schemas import ProfileGenerationRequest

profile_create: List[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "profile_create",
            "description": "Generate a new profile.",
            "parameters": {
                "type": "object",
                "properties": {
                    "entries": {
                        "title": "Entries",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "title": "ProfileEntry",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "enum": [
                                        "experience",
                                        "education",
                                        "personal",
                                        "project",
                                    ],
                                    "title": "Type",
                                },
                                "title": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Title",
                                    "default": None,
                                },
                                "organization": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Organization",
                                    "default": None,
                                },
                                "start_date": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Start Date (ISO format, e.g. YYYY-MM-DD)",
                                    "description": "Start date in ISO 8601 format (YYYY-MM-DD)",
                                    "default": None,
                                },
                                "end_date": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "End Date (ISO format, e.g. YYYY-MM-DD)",
                                    "description": "End date in ISO 8601 format (YYYY-MM-DD)",
                                    "default": None,
                                },
                                "end_date": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "End Date",
                                    "default": None,
                                },
                                "key_notes": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "title": "Key Notes",
                                    "default": [],
                                },
                            },
                        },
                    }
                },
                "required": ["entries"],
            },
        },
    }
]
