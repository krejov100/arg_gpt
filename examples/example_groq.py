import os
from groq import Groq
import arg_gpt.prompts as prompts
import arg_gpt.gpt_helpers as gpt_helpers
from arg_gpt.ai_func import get_ai_functions, ai_func
from dotenv import load_dotenv
import logging
import typer

# Import to ensure functions are registered
from examples.example_functions import *

load_dotenv()

log = logging.getLogger(__name__)

def run_conversation(prompt: str, functions: list):
    """
    Run a conversation with Groq's API using registered functions.
    Similar to the OpenAI version but adapted for Groq's API format.
    """
    client = Groq()
    
    # Get functions at runtime instead of function definition time
    messages = prompts.request_detailed_result() + prompts.remain_functional() + prompts.user_prompt(prompt)
    
    # Format functions for Groq's API
    tools_dict = gpt_helpers.create_tools_dict(functions)
    
    # Call Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools_dict,
        tool_choice="auto",
        temperature=0.5,
        max_tokens=1024
    )
    
    # Use the library's existing interpret_response function
    messages.extend(gpt_helpers.interpret_response(response, functions))
    
    # Handle both dictionary and ChatCompletionMessage objects
    last_message = messages[-1]
    result = last_message.get('content', '') if isinstance(last_message, dict) else last_message.content
    print(result)  # Print the result
    return result

def run_arg_prompt():
    """CLI entry point that uses typer like the OpenAI example"""
    typer.run(lambda x: run_conversation(x, functions=get_ai_functions()))