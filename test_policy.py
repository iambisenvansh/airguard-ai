"""
Unit tests for PolicyEngine class.

Tests the policy validation, rule matching, and error handling.
"""

import pytest
import json
import os
from datetime import datetime
from policy import PolicyEngine
from models import Intent, PolicyDecision


class TestPolicyEngine:
    """Test suite for PolicyEngine class."""
    
    def test_init_loads_policy_file(self):
        """Test that PolicyEngine loads policy.json on initialization."""
        engine = PolicyEngine("policy.json")
        
        assert engine.policy_data is not None
        assert len(engine.rules) > 0
        assert engine.default_policy == "deny"
    
    def test_validate_allowed_action_generate_report(self):
        """Test that generate_report action is allowed."""
        engine = PolicyEngine("policy.json")
        
        intent = Intent(
            action="generate_report",
            parameters={"location": "Delhi"},
            timestamp=datetime.now(),
            user_command="Generate pollution report for Delhi",
            confidence=0.95
        )
        
        decision = engine.validate_intent(intent)
        
        assert decision.allowed is True
        assert decision.rule_name == "generate_report"
        assert "read-only" in decision.reason.lower()
        assert decision.constraints is not None
        assert "max_file_size_mb" in decision.constraints
    
    def test_validate_allowed_action_analyze_aqi(self):
        """Test that analyze_aqi action is allowed."""
        engine = PolicyEngine("policy.json")
        
        intent = Intent(
            action="analyze_aqi",
            parameters={"location": "Delhi"},
            timestamp=datetime.now(),
            user_command="Analyze AQI in Delhi",
            confidence=0.9
        )
        
        decision = engine.validate_intent(intent)
        
        assert decision.allowed is True
        assert decision.rule_name == "analyze_aqi"
        assert decision.constraints is not None
    
    def test_validate_allowed_action_send_alert(self):
        """Test that send_alert action is allowed."""
        engine = PolicyEngine("policy.json")
        
        intent = Intent(
            action="send_alert",
            parameters={"severity": "critical", "message": "High pollution"},
            timestamp=datetime.now(),
            user_command="Send alert about high pollution",
            confidence=0.85
        )
        
        decision = engine.validate_intent(intent)
        
        assert decision.allowed is True
        assert decision.rule_name == "send_alert"
        assert "public safety" in decision.reason.lower()
    
    def test_validate_blocked_action_shutdown_factory(self):
        """Test that shutdown_factory action is blocked."""
        engine = PolicyEngine("policy.json")
        
        intent = Intent(
            action="shutdown_factory",
            parameters={"factory_id": "F123", "location": "Mayapuri"},
            timestamp=datetime.now(),
            user_command="Shutdown factory in Mayapuri",
            confidence=0.92
        )
        
        decision = engine.validate_intent(intent)
        
        assert decision.allowed is False
        assert decision.rule_name == "shutdown_factory"
        assert "human authorization" in decision.reason.lower()
        assert decision.constraints is None
    
    def test_validate_blocked_action_issue_fine(self):
        """Test that issue_fine action is blocked."""
        engine = PolicyEngine("policy.json")
        
        intent = Intent(
            action="issue_fine",
            parameters={"factory_id": "F456", "amount": 50000},
            timestamp=datetime.now(),
            user_command="Issue fine to polluting factory",
            confidence=0.88
        )
        
        decision = engine.validate_intent(intent)
        
        assert decision.allowed is False
        assert decision.rule_name == "issue_fine"
        assert "legal" in decision.reason.lower() or "authorization" in decision.reason.lower()
    
    def test_validate_unknown_action_uses_default_policy(self):
        """Test that unknown actions use default deny policy."""
        engine = PolicyEngine("policy.json")
        
        intent = Intent(
            action="unknown_action",
            parameters={},
            timestamp=datetime.now(),
            user_command="Do something unknown",
            confidence=0.5
        )
        
        decision = engine.validate_intent(intent)
        
        assert decision.allowed is False
        assert decision.rule_name == "default"
        assert "not explicitly allowed" in decision.reason.lower()
    
    def test_get_allowed_actions(self):
        """Test that get_allowed_actions returns correct list."""
        engine = PolicyEngine("policy.json")
        
        allowed = engine.get_allowed_actions()
        
        assert isinstance(allowed, list)
        assert "generate_report" in allowed
        assert "analyze_aqi" in allowed
        assert "send_alert" in allowed
        assert "shutdown_factory" not in allowed
        assert "issue_fine" not in allowed
    
    def test_get_policy_info(self):
        """Test that get_policy_info returns metadata."""
        engine = PolicyEngine("policy.json")
        
        info = engine.get_policy_info()
        
        assert "version" in info
        assert "rules_count" in info
        assert "default_policy" in info
        assert "allowed_actions" in info
        assert info["default_policy"] == "deny"
        assert info["rules_count"] > 0
    
    def test_policy_decision_structure(self):
        """Test that PolicyDecision has correct structure."""
        engine = PolicyEngine("policy.json")
        
        intent = Intent(
            action="generate_report",
            parameters={},
            timestamp=datetime.now(),
            user_command="Generate report",
            confidence=0.9
        )
        
        decision = engine.validate_intent(intent)
        
        # Verify PolicyDecision has all required fields
        assert hasattr(decision, 'allowed')
        assert hasattr(decision, 'reason')
        assert hasattr(decision, 'rule_name')
        assert hasattr(decision, 'constraints')
        
        # Verify types
        assert isinstance(decision.allowed, bool)
        assert isinstance(decision.reason, str)
        assert isinstance(decision.rule_name, str)
        assert decision.constraints is None or isinstance(decision.constraints, dict)
    
    def test_constraints_for_allowed_actions(self):
        """Test that allowed actions have appropriate constraints."""
        engine = PolicyEngine("policy.json")
        
        # Test generate_report constraints
        intent = Intent(
            action="generate_report",
            parameters={},
            timestamp=datetime.now(),
            user_command="Generate report",
            confidence=0.9
        )
        decision = engine.validate_intent(intent)
        assert decision.constraints is not None
        assert "max_file_size_mb" in decision.constraints
        
        # Test analyze_aqi constraints
        intent = Intent(
            action="analyze_aqi",
            parameters={},
            timestamp=datetime.now(),
            user_command="Analyze AQI",
            confidence=0.9
        )
        decision = engine.validate_intent(intent)
        assert decision.constraints is not None
        assert "max_data_points" in decision.constraints
    
    def test_missing_policy_file_raises_error(self):
        """Test that missing policy file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError) as exc_info:
            PolicyEngine("nonexistent_policy.json")
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_reload_policy_success(self):
        """Test that reload_policy successfully reloads the policy."""
        engine = PolicyEngine("policy.json")
        
        initial_rules_count = len(engine.rules)
        
        # Reload should succeed
        success = engine.reload_policy()
        
        assert success is True
        assert len(engine.rules) == initial_rules_count
    
    def test_reload_policy_with_missing_file(self):
        """Test that reload_policy handles missing file gracefully."""
        engine = PolicyEngine("policy.json")
        
        # Change to nonexistent file
        engine.policy_file = "nonexistent.json"
        
        # Reload should fail but not crash
        success = engine.reload_policy()
        
        assert success is False
        # Original policy should still be intact
        assert len(engine.rules) > 0


class TestPolicyEngineEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_action_name(self):
        """Test validation with empty action name."""
        engine = PolicyEngine("policy.json")
        
        # Create intent with empty action (should fail validation in Intent class)
        with pytest.raises(ValueError):
            Intent(
                action="",
                parameters={},
                timestamp=datetime.now(),
                user_command="Test",
                confidence=0.5
            )
    
    def test_multiple_validations_same_intent(self):
        """Test that validating same intent multiple times gives same result."""
        engine = PolicyEngine("policy.json")
        
        intent = Intent(
            action="generate_report",
            parameters={},
            timestamp=datetime.now(),
            user_command="Generate report",
            confidence=0.9
        )
        
        decision1 = engine.validate_intent(intent)
        decision2 = engine.validate_intent(intent)
        
        assert decision1.allowed == decision2.allowed
        assert decision1.reason == decision2.reason
        assert decision1.rule_name == decision2.rule_name
    
    def test_case_sensitive_action_matching(self):
        """Test that action matching is case-sensitive."""
        engine = PolicyEngine("policy.json")
        
        # Uppercase action should not match
        intent = Intent(
            action="GENERATE_REPORT",
            parameters={},
            timestamp=datetime.now(),
            user_command="Generate report",
            confidence=0.9
        )
        
        decision = engine.validate_intent(intent)
        
        # Should use default policy since no exact match
        assert decision.rule_name == "default"
        assert decision.allowed is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
