"""Tests for gpt_helpers module."""

import pytest
from unittest.mock import Mock, patch
from arg_gpt.gpt_helpers import interpret_response, call_gpt_with_function

def test_successful_function_call():
    """Test successful function execution."""
    def test_func(x: int, y: int) -> int:
        return x + y

    # Mock OpenAI response
    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message = Mock()
    response.choices[0].message.tool_calls = [Mock()]
    response.choices[0].message.tool_calls[0].function = Mock()
    response.choices[0].message.tool_calls[0].function.name = "test_func"
    response.choices[0].message.tool_calls[0].function.arguments = '{"x": 1, "y": 2}'
    response.choices[0].message.tool_calls[0].id = "call_1"

    messages = interpret_response(response, [test_func])
    
    assert len(messages) == 2  # Original message + function result
    assert messages[1]["role"] == "tool"
    assert messages[1]["name"] == "test_func"
    assert messages[1]["content"] == "3"
    assert messages[1]["tool_call_id"] == "call_1"

def test_unknown_function():
    """Test handling of unknown function names."""
    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message = Mock()
    response.choices[0].message.tool_calls = [Mock()]
    response.choices[0].message.tool_calls[0].function = Mock()
    response.choices[0].message.tool_calls[0].function.name = "unknown_func"
    response.choices[0].message.tool_calls[0].id = "call_1"

    messages = interpret_response(response, [])
    
    assert len(messages) == 2
    assert "Unknown function" in messages[1]["content"]

def test_invalid_arguments():
    """Test handling of invalid JSON arguments."""
    def test_func(x: int) -> int:
        return x

    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message = Mock()
    response.choices[0].message.tool_calls = [Mock()]
    response.choices[0].message.tool_calls[0].function = Mock()
    response.choices[0].message.tool_calls[0].function.name = "test_func"
    response.choices[0].message.tool_calls[0].function.arguments = 'invalid json'
    response.choices[0].message.tool_calls[0].id = "call_1"

    messages = interpret_response(response, [test_func])
    
    assert len(messages) == 2
    assert "Invalid function arguments" in messages[1]["content"]

def test_function_execution_error():
    """Test handling of function execution errors."""
    def error_func():
        raise ValueError("Test error")

    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message = Mock()
    response.choices[0].message.tool_calls = [Mock()]
    response.choices[0].message.tool_calls[0].function = Mock()
    response.choices[0].message.tool_calls[0].function.name = "error_func"
    response.choices[0].message.tool_calls[0].function.arguments = '{}'
    response.choices[0].message.tool_calls[0].id = "call_1"

    messages = interpret_response(response, [error_func])
    
    assert len(messages) == 2
    assert "Error executing function" in messages[1]["content"]

def test_no_tool_calls():
    """Test handling of response with no tool calls."""
    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message = Mock()
    response.choices[0].message.tool_calls = None

    messages = interpret_response(response, [])
    
    assert len(messages) == 1  # Only the original message

def test_empty_response():
    """Test handling of empty response."""
    response = Mock()
    response.choices = []

    messages = interpret_response(response, [])
    
    assert len(messages) == 0

def test_none_response():
    """Test handling of None values in function response."""
    def none_func() -> None:
        return None

    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message = Mock()
    response.choices[0].message.tool_calls = [Mock()]
    response.choices[0].message.tool_calls[0].function = Mock()
    response.choices[0].message.tool_calls[0].function.name = "none_func"
    response.choices[0].message.tool_calls[0].function.arguments = '{}'
    response.choices[0].message.tool_calls[0].id = "call_1"

    messages = interpret_response(response, [none_func])
    
    assert len(messages) == 2
    assert messages[1]["content"] == "Function executed successfully"

def test_call_gpt_with_function():
    """Test calling GPT with function tools."""
    def test_func(x: int, y: str) -> str:
        """Test function with different parameter types.
        
        Arguments:
            x: A number parameter
            y: A string parameter
            
        Returns:
            A string result
        """
        return f"{x} {y}"

    # Mock the OpenAI client
    mock_client = Mock()
    mock_response = Mock()
    mock_client.chat.completions.create.return_value = mock_response

    # Test messages
    messages = [{"role": "user", "content": "Test message"}]

    # Call the function
    response = call_gpt_with_function(mock_client, [test_func], messages)

    # Verify the client was called with correct parameters
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]

    # Check basic parameters
    assert call_args["model"] == "gpt-3.5-turbo-1106"
    assert call_args["messages"] == messages
    assert call_args["max_tokens"] == 500

    # Check tools parameter
    tools = call_args["tools"]
    assert len(tools) == 1
    tool = tools[0]

    # Verify tool structure
    assert tool["type"] == "function"
    assert "function" in tool
    
    # Verify function details
    func_details = tool["function"]
    assert func_details["name"] == "test_func"
    assert "description" in func_details
    assert "parameters" in func_details

    # Verify parameters schema
    params = func_details["parameters"]
    assert params["type"] == "object"
    assert "properties" in params
    assert "required" in params
    
    # Verify parameter types
    properties = params["properties"]
    assert properties["x"]["type"] == "integer"
    assert properties["y"]["type"] == "string"

    # Verify the response is returned
    assert response == mock_response
