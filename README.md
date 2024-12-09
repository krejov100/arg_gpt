# arg-gpt

A Python package that simplifies building GPT interfaces for your Python code. This package helps you expose your Python functions to GPT models, enabling natural language interaction with your code.

## Installation

```bash
pip install arg-gpt
```

Or using Poetry:

```bash
poetry add arg-gpt
```

## Basic Setup

1. Set up your OpenAI API key in a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

2. Use the `@ai_func` decorator to register functions for GPT:

```python
from arg_gpt.ai_func import ai_func

@ai_func
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    return a + b
```

3. Create a CLI interface to interact with your functions:

```python
import openai
import typer
from arg_gpt.ai_func import get_ai_functions
import arg_gpt.prompts as prompts
import arg_gpt.gpt_helpers as gpt_helpers
from dotenv import load_dotenv

load_dotenv()

def run_conversation(prompt: str, functions: list):
    client = openai.Client()
    messages = prompts.request_detailed_result() + prompts.remain_functional() + prompts.user_prompt(prompt)
    response = gpt_helpers.call_gpt_with_function(client, functions, messages)
    messages.extend(gpt_helpers.interpret_response(response, functions))
    return messages[-1].content

if __name__ == "__main__":
    typer.run(lambda x: run_conversation(x, functions=get_ai_functions()))
```

Now you can interact with your functions using natural language:
```bash
python your_script.py "calculate the sum of 5 and 3"
```

## Examples

The package includes two example implementations in the [examples](./examples) directory:

### OpenAI Example
Located at [examples/example_cmd.py](./examples/example_cmd.py), this example demonstrates using arg-gpt with OpenAI's API.

To run this example:
1. Ensure you have set `OPENAI_API_KEY` in your `.env` file
2. Run the example:
```bash
python examples/example_cmd.py "your prompt here"
```

### Groq Example
Located at [examples/example_groq.py](./examples/example_groq.py), this example shows integration with Groq's LLM API.

To run this example:
1. Ensure you have set `GROQ_API_KEY` in your `.env` file
2. Run the example:
```bash
python examples/example_groq.py "your prompt here"
```

Both examples use a CLI interface where you can provide natural language prompts to interact with the registered functions. The examples will process your prompt and execute the appropriate functions based on your request.

## License

This project is licensed under the terms of the LICENSE file included in the repository.

## Author

Philip Krejov

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
