# Stub for OpenAI GPT client
import json
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env file from the backend directory
backend_dir = Path(__file__).parent.parent.parent
env_path = backend_dir / ".env"
print(f"Loading .env from: {env_path}")
print(f"File exists: {env_path.exists()}")

load_dotenv(env_path, override=True)

api_key = os.getenv("OPENAI_API_KEY")
print(f"API key loaded: {'Yes' if api_key else 'No'}")

MODEL = "gpt-4o-mini"

# Only initialize OpenAI client if API key is available
if api_key:
    from openai import OpenAI

    openai = OpenAI()
    print("OpenAI client initialized successfully")
else:
    openai = None
    print("OpenAI client NOT initialized - no API key")


def gpt_chat_complete(messages, model=MODEL, tools=None, enforce_json=False, **kwargs):
    """
    Complete a chat conversation with GPT.

    Args:
        messages: List of message dictionaries with 'role' and 'content'
        model: The GPT model to use (default: MODEL)
        tools: List of tools to use (default: None)
        enforce_json: If True, forces JSON response format and returns parsed JSON.
                     If False, returns raw text response.
        **kwargs: Additional arguments to pass to OpenAI API

    Returns:
        If tools are provided: Raw response object (to access tool_calls)
        If enforce_json=True: Parsed JSON object
        If enforce_json=False: Raw text response string
    """

    if openai is None:
        raise RuntimeError(
            "OpenAI client not initialized. Please check your OPENAI_API_KEY environment variable."
        )

    # Prepare API call parameters
    api_params = {"model": model, "messages": messages, "tools": tools, **kwargs}
    # Add JSON response format if requested
    if enforce_json:
        api_params["response_format"] = {"type": "json_object"}

    try:
        print(f"Making OpenAI API call with model: {model}")
        response = openai.chat.completions.create(**api_params)

        if response is None:
            raise RuntimeError("OpenAI API returned None response")

        print(f"OpenAI API call successful, response type: {type(response)}")

        # If tools are provided, return the raw response object
        if tools:
            return response

        result = response.choices[0].message.content

        # Parse JSON if requested, otherwise return raw text
        if enforce_json:
            return json.loads(result)
        else:
            return result

    except Exception as e:
        print(f"OpenAI API call failed: {str(e)}")
        print(f"API params: {api_params}")
        raise RuntimeError(f"OpenAI API call failed: {str(e)}")
