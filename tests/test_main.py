"""
Tests for the main module.
"""

import pytest
from main import hello_world


class TestHelloWorld:
    """Test cases for the hello_world function."""

    def test_hello_world_returns_string(self) -> None:
        """Test that hello_world returns a string."""
        # Arrange
        expected_type = str
        
        # Act
        result = hello_world()
        
        # Assert
        assert isinstance(result, expected_type)

    def test_hello_world_returns_expected_message(self) -> None:
        """Test that hello_world returns the expected message."""
        # Arrange
        expected_message = "Hello, World!"
        
        # Act
        result = hello_world()
        
        # Assert
        assert result == expected_message

    def test_hello_world_returns_non_empty_string(self) -> None:
        """Test that hello_world returns a non-empty string."""
        # Arrange
        # Act
        result = hello_world()
        
        # Assert
        assert len(result) > 0
        assert result.strip() != "" 