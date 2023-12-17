import logging
import re
import inspect
import json
from .gpt_function import doc_to_dict
log = logging.getLogger(__name__)


def call_gpt_with_function(client, functions, messages, model="gpt-3.5-turbo-1106"):
    # convert list of functions to list of dicts
    tools_dict = [{"type": "function", **doc_to_dict(func)} for func in functions]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools_dict,
        max_tokens=500
    )
    return response


def call_gpt(client, messages, model="gpt-3.5-turbo-1106"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=500
    )
    return response


def interpret_response(response, functions):
    func_dict = {func.__name__: func for func in functions}
    num_choices = len(response.choices)
    logging.info("%d Choices", num_choices)
    messages = []
    response_message = response.choices[0].message

    logging.info("Response message: %s", response_message)

    tool_calls = response_message.tool_calls
    messages.append(response_message)
    if not tool_calls:
        return messages
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = func_dict.get(function_name)

        if function_to_call is None:
            logging.warning("Unknown function name: %s", function_name)
            continue

        function_args = json.loads(tool_call.function.arguments)
        function_response = str(function_to_call(**function_args))
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response,
        })
    return messages
