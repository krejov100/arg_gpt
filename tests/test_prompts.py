"""Tests for prompts module."""

from arg_gpt.prompts import (
    user_prompt,
    system_prompt,
    request_detailed_result,
    summarize,
    remain_functional
)

def test_user_prompt():
    """Test user prompt message formatting."""
    message = "test message"
    result = user_prompt(message)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["role"] == "user"
    assert result[0]["content"] == message

def test_system_prompt():
    """Test system prompt message formatting."""
    message = "test message"
    result = system_prompt(message)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["role"] == "system"
    assert result[0]["content"] == message

def test_request_detailed_result():
    """Test request detailed result combined prompts."""
    result = request_detailed_result()
    
    assert isinstance(result, list)
    assert len(result) == 2  # Two system messages
    assert all(msg["role"] == "system" for msg in result)
    assert "assumptions" in result[0]["content"].lower()
    assert "detailed" in result[1]["content"].lower()

def test_summarize():
    """Test summarize system prompt."""
    result = summarize()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["role"] == "system"
    assert "summarize" in result[0]["content"].lower()
    assert "third person" in result[0]["content"].lower()

def test_remain_functional():
    """Test remain functional system prompt."""
    result = remain_functional()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["role"] == "system"
    assert "functions provided" in result[0]["content"].lower()

def test_prompt_combinations():
    """Test combining multiple prompts."""
    user_msg = "test message"
    combined = request_detailed_result() + remain_functional() + user_prompt(user_msg)
    
    assert isinstance(combined, list)
    assert len(combined) == 4  # 2 from detailed_result + 1 from remain_functional + 1 user prompt
    assert combined[-1]["role"] == "user"
    assert combined[-1]["content"] == user_msg
