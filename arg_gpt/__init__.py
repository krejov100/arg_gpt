"""
arg_gpt package initialization.
Exposes the main functionality for AI function integration.
"""

from .ai_func import (
    ai_func,
    get_ai_functions,
    get_function_schemas,
    get_function_by_name,
    clear_registry
)

__all__ = [
    'ai_func',
    'get_ai_functions',
    'get_function_schemas',
    'get_function_by_name',
    'clear_registry'
]
