"""Tests for the gpt_function_reflection module."""

from typing import List, Dict, Optional, Union, Tuple
import pytest
from arg_gpt.gpt_function_reflection import doc_to_gpt_dict

def test_simple_function():
    """Test reflection on a simple function with basic types."""
    def sample(name: str, age: int) -> str:
        """A simple function with basic types.
        
        Arguments:
            name: The person's name
            age: The person's age
            
        Returns:
            A greeting message
        """
        return f"Hello {name}, you are {age} years old"
    
    result = doc_to_gpt_dict(sample)
    assert result["function"]["name"] == "sample"
    assert "description" in result["function"]
    
    params = result["function"]["parameters"]
    assert "name" in params["properties"]
    assert params["properties"]["name"]["type"] == "string"
    assert "age" in params["properties"]
    assert params["properties"]["age"]["type"] == "integer"
    
    assert result["function"]["returns"]["type"] == "string"

def test_complex_types():
    """Test reflection on a function with complex type annotations."""
    def complex_sample(
        items: List[int],
        config: Dict[str, Union[str, int]],
        optional_data: Optional[List[str]] = None
    ) -> Dict[str, List[Union[str, int]]]:
        """Function with complex type annotations.
        
        Arguments:
            items: List of numbers to process
            config: Configuration dictionary with string/integer values
            optional_data: Optional list of strings
            
        Returns:
            Processed data as a dictionary
        """
        return {"result": []}
    
    result = doc_to_gpt_dict(complex_sample)
    params = result["function"]["parameters"]["properties"]
    
    # Test items parameter
    assert params["items"]["type"] == "array"
    assert params["items"]["items"]["type"] == "integer"
    
    # Test config parameter
    assert params["config"]["type"] == "object"
    assert "anyOf" in params["config"]["additionalProperties"]
    value_types = {t["type"] for t in params["config"]["additionalProperties"]["anyOf"]}
    assert value_types == {"string", "integer"}
    
    # Test optional_data parameter
    assert params["optional_data"]["nullable"] == True
    assert params["optional_data"]["type"] == "array"
    assert params["optional_data"]["items"]["type"] == "string"
    
    # Test return type
    returns = result["function"]["returns"]
    assert returns["type"] == "object"
    assert returns["additionalProperties"]["type"] == "array"

def test_default_values():
    """Test reflection on a function with default values."""
    def with_defaults(
        required_arg: str,
        optional_str: str = "default",
        optional_int: int = 42,
        optional_list: List[str] = None
    ) -> None:
        """Function with default values.
        
        Arguments:
            required_arg: A required string argument
            optional_str: An optional string with default
            optional_int: An optional integer with default
            optional_list: An optional list with None default
        """
        pass
    
    result = doc_to_gpt_dict(with_defaults)
    params = result["function"]["parameters"]
    
    # Test required parameters
    assert "required_arg" in params["required"]
    assert "optional_str" not in params["required"]
    assert "optional_int" not in params["required"]
    assert "optional_list" not in params["required"]
    
    # Test default values
    props = params["properties"]
    assert "default" not in props["required_arg"]
    assert props["optional_str"]["default"] == "default"
    assert props["optional_int"]["default"] == 42
    assert props["optional_list"]["default"] is None

def test_nested_types():
    """Test reflection on a function with deeply nested type annotations."""
    def nested_sample(
        matrix: List[List[float]],
        lookup: Dict[str, Dict[str, List[int]]],
        points: List[Tuple[float, float]]
    ) -> List[Dict[str, Union[str, List[int]]]]:
        """Function with deeply nested type annotations.
        
        Arguments:
            matrix: 2D matrix of floating point numbers
            lookup: Nested dictionary with string keys and list values
            points: List of coordinate tuples
            
        Returns:
            List of dictionaries with mixed types
        """
        return []
    
    result = doc_to_gpt_dict(nested_sample)
    params = result["function"]["parameters"]["properties"]
    
    # Test matrix parameter (nested lists)
    assert params["matrix"]["type"] == "array"
    assert params["matrix"]["items"]["type"] == "array"
    assert params["matrix"]["items"]["items"]["type"] == "number"
    
    # Test lookup parameter (nested dicts)
    assert params["lookup"]["type"] == "object"
    nested_dict = params["lookup"]["additionalProperties"]
    assert nested_dict["type"] == "object"
    assert nested_dict["additionalProperties"]["type"] == "array"
    assert nested_dict["additionalProperties"]["items"]["type"] == "integer"
    
    # Test points parameter (list of tuples)
    assert params["points"]["type"] == "array"
    assert params["points"]["items"]["type"] == "array"

def test_docstring_descriptions():
    """Test that docstring descriptions are properly extracted."""
    def sample(name: str, age: int) -> str:
        """Process user information.
        
        Arguments:
            name: The user's full name
            age: The user's age in years
            
        Returns:
            A formatted string with user info
        """
        return f"{name} is {age} years old"
    
    result = doc_to_gpt_dict(sample)
    
    # Test function description
    assert "Process user information" in result["function"]["description"]
    
    # Test parameter descriptions
    params = result["function"]["parameters"]["properties"]
    assert "user's full name" in params["name"]["description"].lower()
    assert "user's age in years" in params["age"]["description"].lower()
    
    # Test return description
    assert "formatted string" in result["function"]["returns"]["description"].lower()

def test_invalid_function():
    """Test handling of invalid function input."""
    with pytest.raises(ValueError):
        doc_to_gpt_dict("not a function")
    
    with pytest.raises(ValueError):
        doc_to_gpt_dict(42)
