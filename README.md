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
