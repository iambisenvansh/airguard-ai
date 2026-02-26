"""
Test suite for Enforcer constraint application (Task 7.2).

This test verifies that the apply_constraints() method properly validates
and applies policy constraints before execution.
"""

import pytest
from datetime import datetime
from models import Intent, PolicyDecision, ExecutionResult
from enforce import Enforcer
from executor import Executor
from logger import AuditLogger


class TestConstraintApplication:
    """Test constraint validation and application."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.executor = Executor(data_dir="data", output_dir="output")
        self.logger = AuditLogger(log_dir="logs")
        self.enforcer = Enforcer(self.executor, self.logger)
    
    def test_apply_constraints_with_no_constraints(self):
        """Test that intent is returned unchanged when no constraints."""
        intent = Intent(
            action="generate_report",
            parameters={"location": "Delhi"},
            timestamp=datetime.now(),
            user_command="Generate report",
            confidence=0.9
        )
        
        result = self.enforcer.apply_constraints(intent, None)
        assert result == intent
        
        result = self.enforcer.apply_constraints(intent, {})
        assert result == intent
    
    def test_generate_report_format_constraint_valid(self):
        """Test valid format constraint for generate_report."""
        intent = Intent(
            action="generate_report",
            parameters={"location": "Delhi", "format": "txt"},
            timestamp=datetime.now(),
            user_command="Generate report",
            confidence=0.9
        )
        
        constraints = {
            "allowed_formats": ["txt", "json", "pdf"],
            "max_file_size_mb": 10
        }
        
        result = self.enforcer.apply_constraints(intent, constraints)
        assert result.parameters["_policy_constraints"] == constraints
        assert result.parameters["_max_file_size_mb"] == 10
    
    def test_generate_report_format_constraint_invalid(self):
        """Test invalid format constraint for generate_report."""
        intent = Intent(
            action="generate_report",
            parameters={"location": "Delhi", "format": "exe"},
            timestamp=datetime.now(),
            user_command="Generate report",
            confidence=0.9
        )
        
        constraints = {
            "allowed_formats": ["txt", "json", "pdf"]
        }
        
        with pytest.raises(ValueError) as exc_info:
            self.enforcer.apply_constraints(intent, constraints)
        
        assert "Format 'exe' not allowed" in str(exc_info.value)
        assert "txt, json, pdf" in str(exc_info.value)
    
    def test_analyze_aqi_metric_constraint_valid(self):
        """Test valid metric constraint for analyze_aqi."""
        intent = Intent(
            action="analyze_aqi",
            parameters={"location": "Delhi", "metrics": ["PM2.5", "PM10"]},
            timestamp=datetime.now(),
            user_command="Analyze AQI",
            confidence=0.9
        )
        
        constraints = {
            "allowed_metrics": ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"],
            "max_data_points": 10000
        }
        
        result = self.enforcer.apply_constraints(intent, constraints)
        assert result.parameters["_policy_constraints"] == constraints
        assert result.parameters["_max_data_points"] == 10000
    
    def test_analyze_aqi_metric_constraint_invalid(self):
        """Test invalid metric constraint for analyze_aqi."""
        intent = Intent(
            action="analyze_aqi",
            parameters={"location": "Delhi", "metrics": ["INVALID_METRIC"]},
            timestamp=datetime.now(),
            user_command="Analyze AQI",
            confidence=0.9
        )
        
        constraints = {
            "allowed_metrics": ["PM2.5", "PM10", "NO2"]
        }
        
        with pytest.raises(ValueError) as exc_info:
            self.enforcer.apply_constraints(intent, constraints)
        
        assert "Metric 'INVALID_METRIC' not allowed" in str(exc_info.value)
    
    def test_send_alert_severity_constraint_valid(self):
        """Test valid severity constraint for send_alert."""
        intent = Intent(
            action="send_alert",
            parameters={
                "severity": "warning",
                "message": "High pollution detected",
                "area": "Delhi"
            },
            timestamp=datetime.now(),
            user_command="Send alert",
            confidence=0.9
        )
        
        constraints = {
            "allowed_severity_levels": ["info", "warning", "critical"],
            "max_message_length": 500
        }
        
        result = self.enforcer.apply_constraints(intent, constraints)
        assert result.parameters["_policy_constraints"] == constraints
    
    def test_send_alert_severity_constraint_invalid(self):
        """Test invalid severity constraint for send_alert."""
        intent = Intent(
            action="send_alert",
            parameters={
                "severity": "extreme",
                "message": "Test",
                "area": "Delhi"
            },
            timestamp=datetime.now(),
            user_command="Send alert",
            confidence=0.9
        )
        
        constraints = {
            "allowed_severity_levels": ["info", "warning", "critical"]
        }
        
        with pytest.raises(ValueError) as exc_info:
            self.enforcer.apply_constraints(intent, constraints)
        
        assert "Severity level 'extreme' not allowed" in str(exc_info.value)
    
    def test_send_alert_message_length_constraint_valid(self):
        """Test valid message length constraint for send_alert."""
        intent = Intent(
            action="send_alert",
            parameters={
                "severity": "warning",
                "message": "Short message",
                "area": "Delhi"
            },
            timestamp=datetime.now(),
            user_command="Send alert",
            confidence=0.9
        )
        
        constraints = {
            "max_message_length": 500
        }
        
        result = self.enforcer.apply_constraints(intent, constraints)
        assert result.parameters["_policy_constraints"] == constraints
    
    def test_send_alert_message_length_constraint_invalid(self):
        """Test invalid message length constraint for send_alert."""
        long_message = "x" * 501  # Exceeds 500 character limit
        
        intent = Intent(
            action="send_alert",
            parameters={
                "severity": "warning",
                "message": long_message,
                "area": "Delhi"
            },
            timestamp=datetime.now(),
            user_command="Send alert",
            confidence=0.9
        )
        
        constraints = {
            "max_message_length": 500
        }
        
        with pytest.raises(ValueError) as exc_info:
            self.enforcer.apply_constraints(intent, constraints)
        
        assert "exceeds maximum length of 500 characters" in str(exc_info.value)
        assert "Current length: 501" in str(exc_info.value)
    
    def test_enforce_and_execute_with_constraint_violation(self):
        """Test that constraint violations are caught during enforcement."""
        intent = Intent(
            action="send_alert",
            parameters={
                "severity": "invalid_level",
                "message": "Test",
                "area": "Delhi"
            },
            timestamp=datetime.now(),
            user_command="Send alert",
            confidence=0.9
        )
        
        policy_decision = PolicyDecision(
            allowed=True,
            reason="Alert sending is permitted",
            rule_name="send_alert",
            constraints={
                "allowed_severity_levels": ["info", "warning", "critical"]
            }
        )
        
        # The enforcer should catch the constraint violation
        result = self.enforcer.enforce_and_execute(intent, policy_decision)
        
        # Should return error result
        assert result.success is False
        assert "Severity level 'invalid_level' not allowed" in result.message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
