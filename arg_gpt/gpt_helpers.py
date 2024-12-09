import logging
import re
import inspect
import json
from typing import List, Dict, Any
from .gpt_function_reflection import doc_to_gpt_dict

log = logging.getLogger(__name__)

def create_tools_dict(functions):
    tools_dict = []
    for func in functions:
        func_dict = doc_to_gpt_dict(func)
        tool = {
            "type": "function",
            "function": {
                "name": func.__name__,  # Explicitly set the name
                "description": func_dict["function"]["description"],
                "parameters": func_dict["function"]["parameters"]
            }
        }
        # Add returns info if present
        if "returns" in func_dict["function"]:
            tool["function"]["returns"] = func_dict["function"]["returns"]
        tools_dict.append(tool)
    return tools_dict

def call_gpt_with_function(client, functions, messages, model="gpt-3.5-turbo-1106"):
    # convert list of functions to list of dicts
    tools_dict = create_tools_dict(functions)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools_dict,
        max_tokens=500
    )
    return response

def interpret_response(response, functions) -> List[Dict[str, Any]]:
    """
    Interpret the OpenAI API response and execute any function calls.
    
    Arguments:
        response: The OpenAI API response object
        functions: List of available functions that can be called
        
    Returns:
        List of message dictionaries for the conversation
    """
    # Create function lookup dictionary
    func_dict = {func.__name__: func for func in functions}
    messages = []
    
    try:
        # Get the response message from the first choice
        if not response.choices:
            log.warning("No choices in response")
            return messages
            
        response_message = response.choices[0].message
        log.info("Processing response message: %s", response_message)
        
        # Always append the response message
        messages.append(response_message)
        
        # Check if there are any tool calls
        tool_calls = getattr(response_message, 'tool_calls', None)
        if not tool_calls:
            log.info("No tool calls in response")
            return messages
            
        # Process each tool call
        for tool_call in tool_calls:
            try:
                # Get function details
                function_name = tool_call.function.name
                log.info("Processing function call: %s", function_name)
                
                # Look up the function
                function_to_call = func_dict.get(function_name)
                if function_to_call is None:
                    log.warning("Unknown function name: %s", function_name)
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": f"Error: Unknown function '{function_name}'"
                    })
                    continue
                
                # Parse arguments
                try:
                    function_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError as e:
                    log.error("Failed to parse function arguments: %s", e)
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": f"Error: Invalid function arguments - {str(e)}"
                    })
                    continue
                
                # Execute function
                try:
                    log.info("Executing %s with args: %s", function_name, function_args)
                    function_response = function_to_call(**function_args)
                    # Convert response to string, handle None case
                    response_content = str(function_response) if function_response is not None else "Function executed successfully"
                except Exception as e:
                    log.error("Function execution failed: %s", e)
                    response_content = f"Error executing function: {str(e)}"
                
                # Append the result
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": response_content
                })
                
            except Exception as e:
                log.error("Error processing tool call: %s", e)
                messages.append({
                    "tool_call_id": getattr(tool_call, 'id', 'unknown'),
                    "role": "tool",
                    "name": getattr(tool_call, 'function.name', 'unknown'),
                    "content": f"Error processing tool call: {str(e)}"
                })
                
    except Exception as e:
        log.error("Error interpreting response: %s", e)
        messages.append({
            "role": "tool",
            "content": f"Error interpreting response: {str(e)}"
        })
    
    return messages
