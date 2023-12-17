import logging
import re
import inspect
import json

log = logging.getLogger(__name__)

def translate_type(arg_type: inspect.Parameter):
    if arg_type == str:
        return "string"
    elif arg_type == int:
        return "integer"
    elif arg_type == float:
        return "number"
    elif arg_type == bool:
        return "boolean"
    elif arg_type is inspect.Signature.empty:
        return "null"
    else:
        raise ValueError("Unsupported type: {}".format(type))


def doc_to_dict(func):
    if not callable(func):
        raise ValueError("Provided argument is not a function.")

    doc = inspect.getdoc(func)
    if not doc:
        raise ValueError("Function does not have a docstring.")

    # Extracting the first line for description
    lines = doc.split('\n')
    description = lines[0].strip()

    # Parsing the arguments section
    args_section = re.search(r'Arguments\s*:(.*)', doc, re.DOTALL)
    if not args_section:
        raise ValueError("Arguments section not found in the docstring.")

    args_text = args_section.group(1).strip()
    params_match = re.findall(r'(\w+):\s*(.+)', args_text)

    func_dict = {
        "function": {
            "name": func.__name__,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            }
        }
    }

    for param, desc in params_match:
        arg_type = inspect.signature(func).parameters[param].annotation
        # Assuming all parameters are strings for simplicity
        func_dict["function"]["parameters"]["properties"][param] = {
            # use reflection to get the type of the parameter
            "type": translate_type(arg_type),
            "description": desc.strip()
        }
        # Assuming all parameters are required
        func_dict["function"]["parameters"]["required"].append(param)

    return func_dict


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
