import inspect
import re
import typing

def validate_callable(func):
    if not callable(func):
        raise ValueError(f"Provided argument '{func}' is not a function.")

def get_docstring(func):
    doc = inspect.getdoc(func)
    if not doc:
        raise ValueError(f"Function '{func.__name__}' does not have a docstring.")
    return doc

def extract_description(doc):
    lines = doc.split('\n')
    try:
        args_start_index = lines.index("Arguments:")
    except ValueError:
        raise ValueError("Arguments section not found in the docstring.")
    return " ".join(line.strip() for line in lines[:args_start_index]).strip()

def extract_arguments_section(doc):
    args_start_index = doc.split('\n').index("Arguments:")
    return "\n".join(doc.split('\n')[args_start_index + 1:]).strip()

def translate_type(arg_type: inspect.Parameter):
    if arg_type == str:
        return "string"
    elif arg_type == int:
        return "integer"
    elif arg_type == float:
        return "number"
    elif arg_type == bool:
        return "boolean"
    elif arg_type == list:
        return "array"
    elif arg_type is inspect.Signature.empty:
        return "null"
    else:
        raise ValueError("Unsupported type: {}".format(type))


def recursive_translate_type(arg_type, desc):
    if hasattr(arg_type, '__origin__'):
        # Handle generic types like List, Dict, etc.
        origin_type = translate_type(typing.get_origin(arg_type))

        if hasattr(arg_type, '__args__'):
            # Recursively translate each argument type
            modified_desc = "An instance of " + desc
            return {"type": origin_type, "items": recursive_translate_type(arg_type.__args__[0], modified_desc),
                    "description": desc}
    else:
            # Translate simple types
        return {"type": translate_type(arg_type), "description": desc}

def process_parameter(param, desc, signature):
    if param not in signature.parameters:
        raise ValueError(f"Parameter '{param}' not found in function signature.")
    arg_type = signature.parameters[param].annotation

    return recursive_translate_type(arg_type, desc)

def process_function_parameters(func, args_text):
    params_match = re.findall(r'(\w+):\s*(.+)', args_text)
    signature = inspect.signature(func)
    parameters = {"type": "object", "properties": {}, "required": []}

    for param, desc in params_match:
        parameters["properties"][param] = process_parameter(param, desc, signature)
        parameters["required"].append(param)

    return parameters

def build_function_dict(func, description, parameters):
    return {
        "function": {
            "name": func.__name__,
            "description": description,
            "parameters": parameters
        }
    }

def doc_to_dict(func):
    validate_callable(func)
    doc = get_docstring(func)
    description = extract_description(doc)
    args_text = extract_arguments_section(doc)
    parameters = process_function_parameters(func, args_text)
    return build_function_dict(func, description, parameters)
