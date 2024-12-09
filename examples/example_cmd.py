import openai
import typer
import arg_gpt.prompts as prompts
import arg_gpt.gpt_helpers as gpt_helpers
from arg_gpt.ai_func import get_ai_functions, ai_func
from dotenv import load_dotenv
import logging

# Import to ensure functions are registered
from examples.example_functions import *

load_dotenv()

log = logging.getLogger(__name__)

def run_conversation(prompt: str, functions: list):
    client = openai.Client()
    # Get functions at runtime instead of function definition time
    messages = prompts.request_detailed_result() + prompts.remain_functional() + prompts.user_prompt(prompt)
        
    response = gpt_helpers.call_gpt_with_function(client, functions, messages)
    messages.extend(gpt_helpers.interpret_response(response, functions))
    
    # Handle both dictionary and ChatCompletionMessage objects
    last_message = messages[-1]
    result = last_message.get('content', '') if isinstance(last_message, dict) else last_message.content
    print(result)  # Print the result
    return result

@ai_func
def calculate_sum(a: int, b: int) -> int:
    """
    Calculate the sum of two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b

def run_arg_prompt():
    typer.run(lambda x : run_conversation(x, functions=get_ai_functions()))
