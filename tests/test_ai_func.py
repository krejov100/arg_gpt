"""Tests for ai_func module."""

import pytest
from arg_gpt.ai_func import (
    ai_func,
    get_ai_functions,
    get_function_schemas,
    get_function_by_name,
    clear_registry
)

@pytest.fixture(autouse=True)
def setup_teardown():
    """Clear registry before and after each test."""
    clear_registry()
    yield
    clear_registry()

def test_function_registration():
    """Test that functions are properly registered with schemas."""
    
    @ai_func
    def test_function(x: int, y: float) -> str:
        """Test function with type hints.
        
        Arguments:
            x: An integer value
            y: A float value
            
        Returns:
            A string result
        """
        return f"{x} + {y}"
    
    # Test function retrieval
    func = get_function_by_name("test_function")
    assert func is not None
    assert func.__name__ == "test_function"
    
    # Test function list
    functions = get_ai_functions()
    assert len(functions) == 1  # Only our test function should be registered
    
    # Test schema list
    schemas = get_function_schemas()
    assert len(schemas) == 1
    
    # Verify schema format
    schema = schemas[0]  # We know there's only one schema
    assert schema["type"] == "function"
    assert "function" in schema
    
    # Verify function schema
    func_schema = schema["function"]
    assert func_schema["name"] == "test_function"
    assert "description" in func_schema
    assert "parameters" in func_schema
    
    # Verify parameters
    params = func_schema["parameters"]
    assert params["type"] == "object"
    assert "properties" in params
    assert "required" in params
    
    # Verify parameter types
    properties = params["properties"]
    assert properties["x"]["type"] == "integer"
    assert properties["y"]["type"] == "number"

def test_function_execution():
    """Test that decorated functions can still be executed normally."""
    
    @ai_func
    def add_numbers(a: int, b: int) -> int:
        """Add two numbers.
        
        Arguments:
            a: First number
            b: Second number
            
        Returns:
            Sum of the numbers
        """
        return a + b
    
    # Test direct execution
    result = add_numbers(5, 3)
    assert result == 8
    
    # Test execution through registry
    func = get_function_by_name("add_numbers")
    result = func(5, 3)
    assert result == 8

def test_schema_format():
    """Test that schemas are formatted correctly for OpenAI API."""
    
    @ai_func
    def sample_function(text: str, count: int = 1) -> list:
        """Process text multiple times.
        
        Arguments:
            text: The text to process
            count: Number of times to process
            
        Returns:
            List of processed results
        """
        return [text] * count
    
    schemas = get_function_schemas()
    assert len(schemas) == 1
    schema = schemas[0]  # We know there's only one schema
    
    # Verify top-level structure
    assert schema["type"] == "function"
    assert "function" in schema
    
    # Verify function schema
    func_schema = schema["function"]
    assert func_schema["name"] == "sample_function"
    assert "description" in func_schema
    assert "parameters" in func_schema
    
    # Verify parameters include default value
    params = func_schema["parameters"]
    assert "count" in params["properties"]
    assert params["properties"]["count"]["type"] == "integer"
    assert "text" in params["required"]
    assert "count" not in params["required"]

def test_multiple_functions():
    """Test registering multiple functions."""
    
    @ai_func
    def func1(x: int) -> int:
        """First function."""
        return x

    @ai_func
    def func2(y: str) -> str:
        """Second function."""
        return y
    
    # Test function retrieval
    assert get_function_by_name("func1").__name__ == "func1"
    assert get_function_by_name("func2").__name__ == "func2"
    
    # Test function list
    functions = get_ai_functions()
    assert len(functions) == 2
    
    # Test schemas
    schemas = get_function_schemas()
    assert len(schemas) == 2
    names = {s["function"]["name"] for s in schemas}
    assert names == {"func1", "func2"}

def test_function_not_found():
    """Test error handling for unknown function names."""
