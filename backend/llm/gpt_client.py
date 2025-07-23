# Stub for OpenAI GPT client
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
    
MODEL = 'gpt-4o-mini'
openai = OpenAI()

def gpt_chat_complete(messages, model=MODEL, **kwargs):

    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    return json.loads(result)