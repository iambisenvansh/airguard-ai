"""
Unit tests for IntentParser.

Tests the intent parsing functionality including action matching,
parameter extraction, and confidence scoring.
"""

import pytest
from datetime import datetime
from intent import IntentParser
from models import Intent


class TestIntentParser:
    """Test suite for IntentParser class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = IntentParser()
    
    # Test action matching for generate_report
    def test_parse_generate_report_basic(self):
        """Test basic report generation command."""
        intent = self.parser.parse_intent("Generate pollution report for Delhi")
        
        assert intent.action == "generate_report"
        assert intent.parameters.get("location") == "Delhi"
        assert intent.confidence > 0.8
        assert intent.user_command == "Generate pollution report for Delhi"
    
    def test_parse_generate_report_variations(self):
        """Test various phrasings of report generation."""
        commands = [
            "Create report for Mumbai",
            "Make a report about Delhi",
            "Produce pollution report",
            "Generate report on air quality"
        ]
        
        for command in commands:
            intent = self.parser.parse_intent(command)
            assert intent.action == "generate_report"
            assert intent.confidence > 0.0
    
    # Test action matching for analyze_aqi
    def test_parse_analyze_aqi_basic(self):
        """Test basic AQI analysis command."""
        intent = self.parser.parse_intent("Analyze AQI in Delhi")
        
        assert intent.action == "analyze_aqi"
        assert intent.parameters.get("location") == "Delhi"
        assert intent.confidence > 0.8
    
    def test_parse_analyze_aqi_variations(self):
        """Test various phrasings of AQI analysis."""
        commands = [
            "Check air quality in Mumbai",
            "Examine AQI for Bangalore",
            "Review air quality data",
            "Analyze pollution in Delhi"
        ]
        
        for command in commands:
            intent = self.parser.parse_intent(command)
            assert intent.action == "analyze_aqi"
    
    # Test action matching for send_alert
    def test_parse_send_alert_basic(self):
        """Test basic alert sending command."""
        intent = self.parser.parse_intent("Send alert about high pollution")
        
        assert intent.action == "send_alert"
        assert intent.confidence > 0.8
    
    def test_parse_send_alert_with_severity(self):
        """Test alert with severity level."""
        intent = self.parser.parse_intent("Send critical alert for Delhi")
        
        assert intent.action == "send_alert"
        assert intent.parameters.get("severity") == "critical"
        assert intent.parameters.get("location") == "Delhi"
    
    def test_parse_send_alert_severity_mapping(self):
        """Test severity level mapping."""
        test_cases = [
            ("Send info alert", "info"),
            ("Send warning alert", "warning"),
            ("Send critical alert", "critical"),
            ("Send high priority alert", "critical"),
            ("Send low priority alert", "info")
        ]
        
        for command, expected_severity in test_cases:
            intent = self.parser.parse_intent(command)
            assert intent.action == "send_alert"
            assert intent.parameters.get("severity") == expected_severity
    
    # Test action matching for shutdown_factory
    def test_parse_shutdown_factory_basic(self):
        """Test factory shutdown command."""
        intent = self.parser.parse_intent("Shutdown factory in Mayapuri")
        
        assert intent.action == "shutdown_factory"
        assert intent.parameters.get("location") == "Mayapuri"
        assert intent.confidence > 0.8
    
    def test_parse_shutdown_factory_variations(self):
        """Test various phrasings of factory shutdown."""
        commands = [
            "Close factory in Delhi",
            "Stop factory operations",
            "Shut down the factory",
            "Halt production at factory"
        ]
        
        for command in commands:
            intent = self.parser.parse_intent(command)
            assert intent.action == "shutdown_factory"
    
    # Test action matching for issue_fine
    def test_parse_issue_fine_basic(self):
        """Test fine issuance command."""
        intent = self.parser.parse_intent("Issue fine to polluting factory")
        
        assert intent.action == "issue_fine"
        assert intent.confidence > 0.8
    
    def test_parse_issue_fine_variations(self):
        """Test various phrasings of fine issuance."""
        commands = [
            "Impose fine on factory",
            "Levy penalty for pollution",
            "Give fine to polluter",
            "Penalize the factory"
        ]
        
        for command in commands:
            intent = self.parser.parse_intent(command)
            assert intent.action == "issue_fine"
    
    # Test parameter extraction
    def test_extract_location_various_cities(self):
        """Test location extraction for different cities."""
        test_cases = [
            ("Generate report for Delhi", "Delhi"),
            ("Analyze AQI in Mumbai", "Mumbai"),
            ("Check pollution at Bangalore", "Bangalore"),
            ("Alert for Chennai", "Chennai"),
            ("Data from Kolkata", "Kolkata")
        ]
        
        for command, expected_location in test_cases:
            intent = self.parser.parse_intent(command)
            assert intent.parameters.get("location") == expected_location
    
    def test_extract_filename(self):
        """Test filename extraction from commands."""
        intent = self.parser.parse_intent("Generate report delhi_report.pdf")
        
        # Filename extraction is optional, check if present
        if "filename" in intent.parameters:
            assert intent.parameters["filename"] == "delhi_report.pdf"
    
    # Test confidence scoring
    def test_confidence_score_range(self):
        """Test that confidence scores are within valid range."""
        commands = [
            "Generate report for Delhi",
            "Analyze AQI",
            "Send alert",
            "Some random text that doesn't match"
        ]
        
        for command in commands:
            intent = self.parser.parse_intent(command)
            assert 0.0 <= intent.confidence <= 1.0
    
    def test_unknown_action_low_confidence(self):
        """Test that unknown actions have low confidence."""
        intent = self.parser.parse_intent("Do something completely unrelated")
        
        assert intent.action == "unknown"
        assert intent.confidence == 0.0
    
    # Test edge cases
    def test_empty_command(self):
        """Test handling of empty command."""
        intent = self.parser.parse_intent("")
        
        assert intent.action == "error"
        assert intent.confidence == 0.0
        assert "error" in intent.parameters
    
    def test_whitespace_only_command(self):
        """Test handling of whitespace-only command."""
        intent = self.parser.parse_intent("   ")
        
        assert intent.action == "error"
        assert intent.confidence == 0.0
    
    def test_none_command(self):
        """Test handling of None command."""
        intent = self.parser.parse_intent(None)
        
        assert intent.action == "error"
        assert intent.confidence == 0.0
    
    def test_very_long_command(self):
        """Test handling of very long command."""
        long_command = "Generate pollution report for Delhi " * 50
        intent = self.parser.parse_intent(long_command)
        
        assert intent.action == "generate_report"
        assert intent.user_command == long_command
    
    # Test intent structure validation
    def test_validate_intent_structure_valid(self):
        """Test validation of valid intent."""
        intent = self.parser.parse_intent("Generate report for Delhi")
        
        assert self.parser.validate_intent_structure(intent) is True
    
    def test_validate_intent_structure_none(self):
        """Test validation of None intent."""
        assert self.parser.validate_intent_structure(None) is False
    
    def test_validate_intent_structure_invalid_action(self):
        """Test validation of intent with invalid action."""
        # This should raise ValueError in Intent.__post_init__
        with pytest.raises(ValueError):
            Intent(
                action="",
                parameters={},
                timestamp=datetime.now(),
                user_command="test",
                confidence=0.5
            )
    
    # Test timestamp
    def test_intent_has_timestamp(self):
        """Test that parsed intent has a timestamp."""
        intent = self.parser.parse_intent("Generate report")
        
        assert isinstance(intent.timestamp, datetime)
        assert intent.timestamp is not None
    
    # Test user_command preservation
    def test_user_command_preserved(self):
        """Test that original user command is preserved."""
        original_command = "Generate pollution report for Delhi"
        intent = self.parser.parse_intent(original_command)
        
        assert intent.user_command == original_command
    
    # Test case insensitivity
    def test_case_insensitive_matching(self):
        """Test that pattern matching is case insensitive."""
        commands = [
            "GENERATE REPORT FOR DELHI",
            "generate report for delhi",
            "Generate Report For Delhi",
            "GeNeRaTe RePoRt FoR dElHi"
        ]
        
        for command in commands:
            intent = self.parser.parse_intent(command)
            assert intent.action == "generate_report"
    
    # Test multiple parameters
    def test_multiple_parameters_extraction(self):
        """Test extraction of multiple parameters."""
        intent = self.parser.parse_intent("Send critical alert for Delhi")
        
        assert intent.action == "send_alert"
        assert intent.parameters.get("location") == "Delhi"
        assert intent.parameters.get("severity") == "critical"
    
    # Test default severity for alerts
    def test_alert_default_severity(self):
        """Test that alerts without severity get default 'warning'."""
        intent = self.parser.parse_intent("Send alert for Delhi")
        
        assert intent.action == "send_alert"
        assert intent.parameters.get("severity") == "warning"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
