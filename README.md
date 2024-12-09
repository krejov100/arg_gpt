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

For detailed usage examples, check out the [examples](./examples) directory:
- [Basic Command Line Interface](./examples/example_cmd.py)
- [Groq Integration](./examples/example_groq.py)

## License

This project is licensed under the terms of the LICENSE file included in the repository.

## Author

Philip Krejov

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
