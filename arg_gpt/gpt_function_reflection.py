"""
Module for extracting and processing Python function metadata through reflection.

This module provides functionality to analyze Python functions and convert their
signatures, docstrings, and type hints into structured data suitable for API documentation
or function schema generation.
"""

import inspect
import re
import typing
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, Union, get_args, get_origin
from .doc_string_helpers import DocstringParser

class TypeTranslator:
    """Translates Python types to API schema types."""

    SIMPLE_TYPE_MAP = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        tuple: "array",
        dict: "object",
        None: "null",
        type(None): "null",
        inspect.Signature.empty: "null"
    }

    @classmethod
    def translate_recursive(cls, type_hint: Type, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Recursively translate a Python type hint into an API schema type definition.
        
        Arguments:
            type_hint: The Python type hint to translate
            description: Optional description of the type
            
        Returns:
            A dictionary containing the translated type information with nested structure
        """
        result = {}
        
        # Add description if provided
        if description:
            result["description"] = description

        # Handle simple types
        if type_hint in cls.SIMPLE_TYPE_MAP:
            result["type"] = cls.SIMPLE_TYPE_MAP[type_hint]
            return result

        origin = get_origin(type_hint)
        if origin is None:
            result["type"] = cls.SIMPLE_TYPE_MAP.get(type_hint, "null")
            return result

        # Handle Union types (including Optional)
        if origin is Union:
            args = get_args(type_hint)
            # Handle Optional[T] as a special case
            if len(args) == 2 and type(None) in args:
                non_none_type = next(arg for arg in args if arg is not type(None))
                result = cls.translate_recursive(non_none_type, description)
                result["nullable"] = True
                return result
            result["anyOf"] = [
                cls.translate_recursive(arg)
                for arg in args
            ]
            return result

        # Handle List types
        if origin is list:
            args = get_args(type_hint)
            item_type = args[0] if args else Any
            result["type"] = "array"
            modified_desc = f"An array of {description}" if description else None
            result["items"] = cls.translate_recursive(item_type, modified_desc)
            return result

        # Handle Dict types
        if origin is dict:
            args = get_args(type_hint)
            key_type, value_type = args if args else (Any, Any)
            result["type"] = "object"
            modified_desc = f"A dictionary of {description}" if description else None
            result["additionalProperties"] = cls.translate_recursive(value_type, modified_desc)
            return result

        # Handle other generic types
        if hasattr(type_hint, '__args__'):
            result["type"] = cls.SIMPLE_TYPE_MAP.get(origin, "object")
            args = get_args(type_hint)
            if args:
                modified_desc = f"An instance of {description}" if description else None
                result["items"] = cls.translate_recursive(args[0], modified_desc)
            return result

        result["type"] = "object"
        return result

    @classmethod
    def translate(cls, type_hint: Type, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Translate a Python type hint into an API schema type definition.
        This is the main entry point that wraps the recursive translation.
        
        Arguments:
            type_hint: The Python type hint to translate
            description: Optional description of the type
            
        Returns:
            A dictionary containing the translated type information
        """
        return cls.translate_recursive(type_hint, description)

class FunctionInspector:
    """Inspects Python functions and extracts their metadata."""

    def __init__(self, func: callable):
        """Initialize with a function to inspect."""
        if not callable(func):
            raise ValueError(f"Provided argument '{func}' is not callable")
        self.func = func
        self.signature = inspect.signature(func)
        self.docstring = inspect.getdoc(func) or ""
        self.doc_sections = DocstringParser.parse(self.docstring)

    def get_description(self) -> str:
        """Extract the function's description from its docstring."""
        if 'Description' in self.doc_sections:
            return self.doc_sections['Description'].content
        return "No description available."

    def get_parameter_info(self) -> Dict[str, Any]:
        """Extract parameter information from the function signature and docstring."""
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }

        args_section = next((
            section for name, section in self.doc_sections.items()
            if name in ["Arguments", "Args", "Parameters"]
        ), None)

        param_descriptions = {}
        if args_section:
            param_matches = re.findall(r'(\w+):\s*(.+?)(?=\w+:|$)', args_section.content, re.DOTALL)
            param_descriptions = {name.strip(): desc.strip() for name, desc in param_matches}

        for name, param in self.signature.parameters.items():
            if param.default is inspect.Parameter.empty:
                parameters["required"].append(name)

            description = param_descriptions.get(name)
            param_info = TypeTranslator.translate(param.annotation, description)

            if param.default is not inspect.Parameter.empty:
                param_info["default"] = param.default

            parameters["properties"][name] = param_info

        return parameters

    def get_return_info(self) -> Optional[Dict[str, Any]]:
        """Extract return type information from the function."""
        return_annotation = self.signature.return_annotation
        if return_annotation is not inspect.Signature.empty:
            # Look for return description in docstring
            return_section = next((
                section for name, section in self.doc_sections.items()
                if name in ["Returns", "Return"]
            ), None)
            description = return_section.content if return_section else None
            return TypeTranslator.translate(return_annotation, description)
        return None

    def to_gpt_dict(self) -> Dict[str, Any]:
        """Convert the function's metadata to a dictionary format."""
        result = {
            "function": {
                "name": self.func.__name__,
                "description": self.get_description(),
                "parameters": self.get_parameter_info()
            }
        }

        return_info = self.get_return_info()
        if return_info:
            result["function"]["returns"] = return_info

        return result

def doc_to_gpt_dict(func: callable) -> Dict[str, Any]:
    """
    Convert a function's metadata to a dictionary format.
    
    Arguments:
        func: The function to analyze
        
    Returns:
        A dictionary containing the function's metadata
    """
    inspector = FunctionInspector(func)
    return inspector.to_gpt_dict()
