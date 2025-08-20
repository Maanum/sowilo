"""
A simple CLI assistant that uses OpenAI's API and a mock Todoist task list, supporting tool calls for task management.
"""
import os
import json
from pprint import pprint
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam
from llm.tools import tools


MODEL = "gpt-4o-mini"

load_dotenv()
chat_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def add_message(messages: List[Dict[str, Any]], role: str, text: Optional[str], tool_call_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Append a message to the messages list, omitting content if None."""
    msg = {"role": role}
    if text is not None:
        msg["content"] = text
    if role == "tool" and tool_call_id is not None:
        msg["tool_call_id"] = tool_call_id
    messages.append(msg)
    return messages

def handle_tool_call(messages: List[Dict[str, Any]], response: Any) -> List[Dict[str, Any]]:
    tool_calls = getattr(response.choices[0].message, "tool_calls", None)
    if not tool_calls:
        return messages
    tool_call = tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    if tool_call.function.name == "profile_create":
        deleted = delete_task(int(args["task_id"]))
        content = f"Task {args['task_id']} deleted" if deleted else f"Task {args['task_id']} not found"
    else:
        content = f"Unknown tool call: {tool_call.function.name}"
    # Only add one tool message per tool call
    messages = add_message(messages, "tool", content, tool_call.id)
    return messages

def chat(messages: List[Dict[str, Any]], tools: List[ChatCompletionToolParam] = None) -> Optional[str]:
    response = chat_client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    # If the assistant is making a tool call, do NOT add an assistant message, just handle the tool call
    if hasattr(response.choices[0].message, "tool_calls") and response.choices[0].message.tool_calls:
        messages = handle_tool_call(messages, response)  # This adds the 'tool' message
        return chat(messages)  # Immediately call again

    return response.choices[0].message.content if response else None

def execute_llm_interaction(messages: List[Dict[str, Any]], tools: List[ChatCompletionToolParam] = None) -> Optional[str]:
    return(chat(messages, tools))
    