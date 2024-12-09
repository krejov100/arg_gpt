from functools import wraps
from arg_gpt.gpt_function_reflection import doc_to_gpt_dict
from openai import OpenAI
from typing import Dict, Any, List, Tuple
from arg_gpt.gpt_helpers import interpret_response

from dotenv import load_dotenv
load_dotenv()

# Store both functions and their schemas
ai_func_registry: Dict[str, Tuple[callable, Dict[str, Any]]] = {}

client = OpenAI()

def clear_registry():
    """Clear the function registry. Used primarily for testing."""
    global ai_func_registry
    ai_func_registry = {}

def ai_func(func):
    """
    Decorator to register functions for AI use.
    
    Arguments:
        func: The function to register
        
    Returns:
        The wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    # Format the function schema properly for OpenAI API
    func_dict = doc_to_gpt_dict(func)
    schema = {
        "name": func.__name__,  # Required by OpenAI API
        "description": func_dict["function"]["description"],
        "parameters": func_dict["function"]["parameters"]
    }
    # Add returns info if present
    if "returns" in func_dict["function"]:
        schema["returns"] = func_dict["function"]["returns"]
    
    # Store both the function and its schema using the function name as key
    ai_func_registry[func.__name__] = (wrapper, schema)
    return wrapper

def get_ai_functions() -> List[callable]:
    """Get the list of registered functions."""
    return [func for func, _ in ai_func_registry.values()]

def get_function_by_name(name: str) -> callable:
    """Get a registered function by its name."""
    if name in ai_func_registry:
        return ai_func_registry[name][0]
    raise KeyError(f"Function '{name}' not found in registry")

def get_function_schemas() -> List[Dict[str, Any]]:
    """Get the list of function schemas for OpenAI API."""
    return [
        {
            "type": "function",
            "function": schema
        }
        for _, schema in ai_func_registry.values()
    ]