"""
Verification tests for Task 2.2: Intent Structure Validation

This test file verifies that the validate_intent_structure() method:
1. Exists and is callable
2. Checks required fields (action, parameters, timestamp)
3. Handles malformed or ambiguous commands gracefully
4. Returns True for valid intents and False for invalid ones

Requirements mapped: 1.4
"""

import sys
sys.path.insert(0, '.')

import pytest
from datetime import datetime
from intent import IntentParser
from models import Intent


class TestTask22Verification:
    """Verification tests for Task 2.2 requirements."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = IntentParser()
    
    # Requirement 1: Method exists
    def test_validate_intent_structure_method_exists(self):
        """Verify that validate_intent_structure() method exists."""
        assert hasattr(self.parser, 'validate_intent_structure')
        assert callable(self.parser.validate_intent_structure)
    
    # Requirement 2: Checks required fields - action
    def test_validates_action_field(self):
        """Verify that method checks for valid action field."""
        # Valid intent with action
        valid_intent = Intent(
            action="generate_report",
            parameters={"location": "Delhi"},
            timestamp=datetime.now(),
            user_command="Generate report",
            confidence=0.9
        )
        assert self.parser.validate_intent_structure(valid_intent) is True
        
        # Intent with empty action should fail at creation (ValueError)
        with pytest.raises(ValueError):
            Intent(
                action="",
                parameters={},
                timestamp=datetime.now(),
                user_command="test",
                confidence=0.5
            )
    
    # Requirement 2: Checks required fields - parameters
    def test_validates_parameters_field(self):
        """Verify that method checks for valid parameters field."""
        # Valid intent with parameters dict
        valid_intent = Intent(
            action="analyze_aqi",
            parameters={"location": "Mumbai"},
            timestamp=datetime.now(),
            user_command="Analyze AQI",
            confidence=0.8
        )
        assert self.parser.validate_intent_structure(valid_intent) is True
        
        # Empty parameters dict is valid
        valid_intent_empty_params = Intent(
            action="send_alert",
            parameters={},
            timestamp=datetime.now(),
            user_command="Send alert",
            confidence=0.7
        )
        assert self.parser.validate_intent_structure(valid_intent_empty_params) is True
    
    # Requirement 2: Checks required fields - timestamp
    def test_validates_timestamp_field(self):
        """Verify that method checks for valid timestamp field."""
        # Valid intent with timestamp
        valid_intent = Intent(
            action="generate_report",
            parameters={},
            timestamp=datetime.now(),
            user_command="Generate report",
            confidence=0.9
        )
        assert self.parser.validate_intent_structure(valid_intent) is True
    
    # Requirement 3: Handles malformed commands gracefully
    def test_handles_malformed_commands_gracefully(self):
        """Verify that method handles malformed/ambiguous commands gracefully."""
        # Empty command
        intent_empty = self.parser.parse_intent("")
        assert self.parser.validate_intent_structure(intent_empty) is True
        assert intent_empty.action == "error"
        
        # Gibberish command
        intent_gibberish = self.parser.parse_intent("asdfghjkl random gibberish")
        assert self.parser.validate_intent_structure(intent_gibberish) is True
        assert intent_gibberish.action == "unknown"
        
        # Ambiguous command
        intent_ambiguous = self.parser.parse_intent("do something")
        assert self.parser.validate_intent_structure(intent_ambiguous) is True
        
        # Special characters
        intent_special = self.parser.parse_intent("!@#$%^&*()")
        assert self.parser.validate_intent_structure(intent_special) is True
    
    # Requirement 4: Returns True for valid intents
    def test_returns_true_for_valid_intents(self):
        """Verify that method returns True for valid intents."""
        valid_commands = [
            "Generate pollution report for Delhi",
            "Analyze AQI in Mumbai",
            "Send critical alert about pollution",
            "Shutdown factory in Mayapuri",
            "Issue fine to polluting factory"
        ]
        
        for command in valid_commands:
            intent = self.parser.parse_intent(command)
            assert self.parser.validate_intent_structure(intent) is True, \
                f"Failed for command: {command}"
    
    # Requirement 4: Returns False for invalid intents
    def test_returns_false_for_invalid_intents(self):
        """Verify that method returns False for invalid intents."""
        # None intent
        assert self.parser.validate_intent_structure(None) is False
    
    # Additional validation: Confidence score
    def test_validates_confidence_score(self):
        """Verify that method validates confidence score range."""
        # Valid confidence scores
        for confidence in [0.0, 0.5, 1.0]:
            intent = Intent(
                action="test_action",
                parameters={},
                timestamp=datetime.now(),
                user_command="test",
                confidence=confidence
            )
            assert self.parser.validate_intent_structure(intent) is True
    
    # Additional validation: User command preservation
    def test_validates_user_command_field(self):
        """Verify that method checks user_command field."""
        original_command = "Generate report for Delhi"
        intent = self.parser.parse_intent(original_command)
        
        assert self.parser.validate_intent_structure(intent) is True
        assert intent.user_command == original_command
    
    # Integration test: Full pipeline
    def test_full_validation_pipeline(self):
        """Test the full validation pipeline with various commands."""
        test_cases = [
            ("Generate report for Delhi", True, "generate_report"),
            ("Analyze AQI", True, "analyze_aqi"),
            ("Send alert", True, "send_alert"),
            ("", True, "error"),
            ("random gibberish", True, "unknown"),
        ]
        
        for command, should_be_valid, expected_action in test_cases:
            intent = self.parser.parse_intent(command)
            is_valid = self.parser.validate_intent_structure(intent)
            
            assert is_valid == should_be_valid, \
                f"Validation failed for command: '{command}'"
            assert intent.action == expected_action, \
                f"Action mismatch for command: '{command}'"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
