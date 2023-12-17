import openai
import inspect
from pprint import pprint
import typer
import arg_gpt.prompts as prompts
import arg_gpt.gpt_helpers as gpt_helpers
from dotenv import load_dotenv
load_dotenv()

_GPT_FUNCTIONS = []

def reflect_on_interface():
    # get the name of the calling function
    caller_frame = inspect.currentframe().f_back

    # list the functions in the module
    module = inspect.getmodule(caller_frame)
    functions = inspect.getmembers(module, inspect.isfunction)
    print("Found the following public functions:")
    for name, func in functions:
        print(name)
        _GPT_FUNCTIONS.append(func)

def run_conversation(prompt):
    client = openai.Client()
    messages = prompts.request_detailed_result() + prompts.remain_functional() + prompts.user_prompt(prompt)
    functions = _GPT_FUNCTIONS
    while True:
        response = gpt_helpers.call_gpt_with_function(client, functions, messages)
        pprint(response)
        result = gpt_helpers.interpret_response(response, functions)
        messages.extend(result)
        if response.choices[0].finish_reason in ["stop", "max_tokens", "content_filter"]:
            break

    messages += prompts.summarize()
    response = gpt_helpers.call_gpt(client, messages)
    result = gpt_helpers.interpret_response(response, functions)

    pprint(result[-1].content)

def run_arg_prompt():
    typer.run(run_conversation)
