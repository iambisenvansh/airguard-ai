"""
Unit tests for AuditLogger class.

Tests the audit logging functionality including:
- Log writing with various intent types
- Log querying with different filters
- Handling of missing or corrupted log files
"""

import pytest
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from logger import AuditLogger
from models import Intent, PolicyDecision, ExecutionResult


@pytest.fixture
def temp_log_dir(tmp_path):
    """Create a temporary log directory for testing."""
    log_dir = tmp_path / "test_logs"
    log_dir.mkdir()
    return str(log_dir)


@pytest.fixture
def logger(temp_log_dir):
    """Create an AuditLogger instance with temporary directory."""
    return AuditLogger(log_dir=temp_log_dir)


@pytest.fixture
def sample_intent():
    """Create a sample intent for testing."""
    return Intent(
        action="generate_report",
        parameters={"location": "Delhi"},
        timestamp=datetime.now(),
        user_command="Generate pollution report for Delhi",
        confidence=0.95
    )


@pytest.fixture
def sample_policy_decision():
    """Create a sample policy decision for testing."""
    return PolicyDecision(
        allowed=True,
        reason="Report generation is a read-only operation",
        rule_name="generate_report",
        constraints=None
    )


@pytest.fixture
def sample_execution_result():
    """Create a sample execution result for testing."""
    return ExecutionResult(
        success=True,
        message="Report generated successfully",
        data={"report_file": "output/delhi_report.txt"},
        execution_time=1.23,
        files_created=["output/delhi_report.txt"]
    )


def test_logger_initialization(temp_log_dir):
    """Test that logger initializes and creates log directory."""
    logger = AuditLogger(log_dir=temp_log_dir)
    
    assert logger.log_dir.exists()
    assert logger.log_dir.is_dir()
    assert logger.log_file == Path(temp_log_dir) / "audit.log"


def test_log_successful_action(logger, sample_intent, sample_policy_decision, sample_execution_result):
    """Test logging a successful action."""
    logger.log_action(sample_intent, sample_policy_decision, sample_execution_result, "SUCCESS")
    
    # Verify log file was created
    assert logger.log_file.exists()
    
    # Read and verify log entry
    with open(logger.log_file, "r") as f:
        log_entry = json.loads(f.readline())
    
    assert log_entry["status"] == "SUCCESS"
    assert log_entry["intent"]["action"] == "generate_report"
    assert log_entry["policy_decision"]["allowed"] is True
    assert log_entry["result"]["success"] is True
    assert "timestamp" in log_entry


def test_log_blocked_action(logger, sample_intent):
    """Test logging a blocked action."""
    blocked_intent = Intent(
        action="shutdown_factory",
        parameters={"factory_id": "F123"},
        timestamp=datetime.now(),
        user_command="Shutdown factory in Mayapuri",
        confidence=0.90
    )
    
    blocked_decision = PolicyDecision(
        allowed=False,
        reason="Critical infrastructure control requires human authorization",
        rule_name="shutdown_factory",
        constraints=None
    )
    
    logger.log_action(blocked_intent, blocked_decision, None, "BLOCKED")
    
    # Read and verify log entry
    with open(logger.log_file, "r") as f:
        log_entry = json.loads(f.readline())
    
    assert log_entry["status"] == "BLOCKED"
    assert log_entry["intent"]["action"] == "shutdown_factory"
    assert log_entry["policy_decision"]["allowed"] is False
    assert log_entry["result"] is None


def test_log_error(logger):
    """Test logging an error."""
    logger.log_action(None, None, None, "ERROR")
    
    # Read and verify log entry
    with open(logger.log_file, "r") as f:
        log_entry = json.loads(f.readline())
    
    assert log_entry["status"] == "ERROR"
    assert log_entry["intent"] is None
    assert log_entry["policy_decision"] is None
    assert log_entry["result"] is None


def test_get_logs_all(logger, sample_intent, sample_policy_decision, sample_execution_result):
    """Test retrieving all logs."""
    # Log multiple actions
    logger.log_action(sample_intent, sample_policy_decision, sample_execution_result, "SUCCESS")
    logger.log_action(sample_intent, sample_policy_decision, sample_execution_result, "SUCCESS")
    
    logs = logger.get_logs()
    
    assert len(logs) == 2
    assert all(log["status"] == "SUCCESS" for log in logs)


def test_get_logs_with_status_filter(logger, sample_intent, sample_policy_decision, sample_execution_result):
    """Test retrieving logs filtered by status."""
    # Log different types of actions
    logger.log_action(sample_intent, sample_policy_decision, sample_execution_result, "SUCCESS")
    
    blocked_decision = PolicyDecision(
        allowed=False,
        reason="Action blocked",
        rule_name="test_rule",
        constraints=None
    )
    logger.log_action(sample_intent, blocked_decision, None, "BLOCKED")
    logger.log_action(None, None, None, "ERROR")
    
    # Filter by status
    success_logs = logger.get_logs(status_filter="SUCCESS")
    blocked_logs = logger.get_logs(status_filter="BLOCKED")
    error_logs = logger.get_logs(status_filter="ERROR")
    
    assert len(success_logs) == 1
    assert len(blocked_logs) == 1
    assert len(error_logs) == 1


def test_get_logs_with_time_filter(logger, sample_intent, sample_policy_decision, sample_execution_result):
    """Test retrieving logs filtered by time range."""
    now = datetime.now()
    
    # Log an action
    logger.log_action(sample_intent, sample_policy_decision, sample_execution_result, "SUCCESS")
    
    # Filter with time range
    start_time = now - timedelta(minutes=1)
    end_time = now + timedelta(minutes=1)
    
    logs = logger.get_logs(start_time=start_time, end_time=end_time)
    assert len(logs) == 1
    
    # Filter with future start time (should return empty)
    future_start = now + timedelta(hours=1)
    logs = logger.get_logs(start_time=future_start)
    assert len(logs) == 0


def test_get_logs_empty_file(logger):
    """Test retrieving logs when log file doesn't exist."""
    logs = logger.get_logs()
    assert logs == []


def test_get_logs_corrupted_entry(logger, temp_log_dir):
    """Test handling of corrupted log entries."""
    # Write a corrupted log entry
    with open(logger.log_file, "w") as f:
        f.write('{"timestamp": "2024-01-01T12:00:00", "status": "SUCCESS", "intent": null, "policy_decision": null, "result": null}\n')
        f.write('this is not valid json\n')
        f.write('{"timestamp": "2024-01-01T12:01:00", "status": "BLOCKED", "intent": null, "policy_decision": null, "result": null}\n')
    
    # Should skip corrupted entry and return valid ones
    logs = logger.get_logs()
    assert len(logs) == 2


def test_multiple_log_entries(logger, sample_intent, sample_policy_decision, sample_execution_result):
    """Test logging multiple actions and retrieving them."""
    # Log 5 actions
    for i in range(5):
        logger.log_action(sample_intent, sample_policy_decision, sample_execution_result, "SUCCESS")
    
    logs = logger.get_logs()
    assert len(logs) == 5
    
    # Verify all entries have timestamps
    for log in logs:
        assert "timestamp" in log
        assert "status" in log
        assert "intent" in log


def test_log_append_mode(logger, sample_intent, sample_policy_decision, sample_execution_result):
    """Test that logs are appended, not overwritten."""
    # Log first action
    logger.log_action(sample_intent, sample_policy_decision, sample_execution_result, "SUCCESS")
    logs = logger.get_logs()
    assert len(logs) == 1
    
    # Log second action
    logger.log_action(sample_intent, sample_policy_decision, sample_execution_result, "SUCCESS")
    logs = logger.get_logs()
    assert len(logs) == 2  # Should have both entries


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
