"""
Unit tests for core data models.

Tests validation logic and serialization for Intent, PolicyDecision, and ExecutionResult.
"""

import pytest
from datetime import datetime
from models import Intent, PolicyDecision, ExecutionResult


class TestIntent:
    """Test cases for Intent dataclass."""
    
    def test_valid_intent_creation(self):
        """Test creating a valid intent."""
        intent = Intent(
            action="generate_report",
            parameters={"location": "Delhi"},
            timestamp=datetime.now(),
            user_command="Generate pollution report for Delhi",
            confidence=0.95
        )
        assert intent.action == "generate_report"
        assert intent.parameters == {"location": "Delhi"}
        assert intent.confidence == 0.95
    
    def test_intent_validation_empty_action(self):
        """Test that empty action raises ValueError."""
        with pytest.raises(ValueError, match="action must be a non-empty string"):
            Intent(
                action="",
                parameters={},
                timestamp=datetime.now(),
                user_command="test",
                confidence=0.5
            )
    
    def test_intent_validation_invalid_confidence(self):
        """Test that confidence outside 0-1 range raises ValueError."""
        with pytest.raises(ValueError, match="confidence must be a float between 0.0 and 1.0"):
            Intent(
                action="test",
                parameters={},
                timestamp=datetime.now(),
                user_command="test",
                confidence=1.5
            )
    
    def test_intent_to_dict(self):
        """Test intent serialization to dictionary."""
        now = datetime.now()
        intent = Intent(
            action="analyze_aqi",
            parameters={"location": "Mumbai"},
            timestamp=now,
            user_command="Analyze AQI in Mumbai",
            confidence=0.85
        )
        result = intent.to_dict()
        assert result["action"] == "analyze_aqi"
        assert result["parameters"] == {"location": "Mumbai"}
        assert result["timestamp"] == now.isoformat()
        assert result["confidence"] == 0.85


class TestPolicyDecision:
    """Test cases for PolicyDecision dataclass."""
    
    def test_valid_policy_decision_creation(self):
        """Test creating a valid policy decision."""
        decision = PolicyDecision(
            allowed=True,
            reason="Report generation is a read-only operation",
            rule_name="generate_report",
            constraints={"max_file_size_mb": 10}
        )
        assert decision.allowed is True
        assert decision.rule_name == "generate_report"
        assert decision.constraints == {"max_file_size_mb": 10}
    
    def test_policy_decision_validation_empty_reason(self):
        """Test that empty reason raises ValueError."""
        with pytest.raises(ValueError, match="reason must be a non-empty string"):
            PolicyDecision(
                allowed=False,
                reason="",
                rule_name="test"
            )
    
    def test_policy_decision_to_dict(self):
        """Test policy decision serialization to dictionary."""
        decision = PolicyDecision(
            allowed=False,
            reason="Action requires authorization",
            rule_name="shutdown_factory",
            constraints=None
        )
        result = decision.to_dict()
        assert result["allowed"] is False
        assert result["reason"] == "Action requires authorization"
        assert result["rule_name"] == "shutdown_factory"
        assert result["constraints"] is None


class TestExecutionResult:
    """Test cases for ExecutionResult dataclass."""
    
    def test_valid_execution_result_creation(self):
        """Test creating a valid execution result."""
        result = ExecutionResult(
            success=True,
            message="Report generated successfully",
            data={"report_file": "output/delhi_report.txt"},
            execution_time=1.23,
            files_created=["output/delhi_report.txt"]
        )
        assert result.success is True
        assert result.execution_time == 1.23
        assert len(result.files_created) == 1
    
    def test_execution_result_validation_negative_time(self):
        """Test that negative execution time raises ValueError."""
        with pytest.raises(ValueError, match="execution_time must be a non-negative number"):
            ExecutionResult(
                success=True,
                message="test",
                execution_time=-1.0
            )
    
    def test_execution_result_default_values(self):
        """Test that default values are set correctly."""
        result = ExecutionResult(
            success=False,
            message="Execution failed"
        )
        assert result.data is None
        assert result.execution_time == 0.0
        assert result.files_created == []
    
    def test_execution_result_to_dict(self):
        """Test execution result serialization to dictionary."""
        result = ExecutionResult(
            success=True,
            message="Analysis complete",
            data={"aqi": 287},
            execution_time=0.5,
            files_created=[]
        )
        result_dict = result.to_dict()
        assert result_dict["success"] is True
        assert result_dict["message"] == "Analysis complete"
        assert result_dict["data"] == {"aqi": 287}
        assert result_dict["execution_time"] == 0.5
        assert result_dict["files_created"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
