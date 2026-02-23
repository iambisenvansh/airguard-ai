"""
Policy Engine for AirGuard AI system.

This module implements the PolicyEngine class that loads and evaluates security
policy rules to determine if intents are allowed, blocked, or require special handling.
"""

import json
import os
from typing import Dict, Any, List, Optional
from models import Intent, PolicyDecision


class PolicyEngine:
    """
    Policy Engine that validates intents against security policy rules.
    
    The PolicyEngine loads policy rules from a JSON configuration file and
    evaluates intents to determine if they should be allowed or blocked.
    It provides clear denial reasons and supports policy constraints.
    
    Attributes:
        policy_file: Path to the policy JSON configuration file
        policy_data: Loaded policy configuration
        rules: List of policy rules
        default_policy: Default action when no rule matches ("allow" or "deny")
        default_reason: Default reason for denied actions
    
    Example:
        >>> engine = PolicyEngine("policy.json")
        >>> intent = Intent(
        ...     action="generate_report",
        ...     parameters={"location": "Delhi"},
        ...     timestamp=datetime.now(),
        ...     user_command="Generate report",
        ...     confidence=0.9
        ... )
        >>> decision = engine.validate_intent(intent)
        >>> print(decision.allowed)
        True
    """
    
    def __init__(self, policy_file: str = "policy.json"):
        """
        Initialize the PolicyEngine and load policy rules.
        
        Args:
            policy_file: Path to the policy JSON configuration file
        
        Raises:
            FileNotFoundError: If policy file doesn't exist
            json.JSONDecodeError: If policy file is invalid JSON
            ValueError: If policy file is missing required fields
        """
        self.policy_file = policy_file
        self.policy_data: Dict[str, Any] = {}
        self.rules: List[Dict[str, Any]] = []
        self.default_policy: str = "deny"
        self.default_reason: str = "Action not explicitly allowed by security policy"
        
        # Load policy rules from file
        self._load_policy()
    
    def _load_policy(self) -> None:
        """
        Load and parse policy rules from JSON file.
        
        This method reads the policy file, validates its structure, and
        extracts the rules, default policy, and default reason.
        
        Raises:
            FileNotFoundError: If policy file doesn't exist
            json.JSONDecodeError: If policy file is invalid JSON
            ValueError: If policy file is missing required fields
        """
        # Check if policy file exists
        if not os.path.exists(self.policy_file):
            raise FileNotFoundError(
                f"Policy file not found: {self.policy_file}. "
                "Please ensure policy.json exists in the current directory."
            )
        
        try:
            # Read and parse JSON file
            with open(self.policy_file, 'r', encoding='utf-8') as f:
                self.policy_data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in policy file: {self.policy_file}",
                e.doc,
                e.pos
            )
        
        # Validate required fields
        if "rules" not in self.policy_data:
            raise ValueError(
                f"Policy file {self.policy_file} is missing required 'rules' field"
            )
        
        if not isinstance(self.policy_data["rules"], list):
            raise ValueError(
                f"Policy file {self.policy_file} 'rules' field must be a list"
            )
        
        # Extract policy configuration
        self.rules = self.policy_data["rules"]
        self.default_policy = self.policy_data.get("default_policy", "deny")
        self.default_reason = self.policy_data.get(
            "default_reason",
            "Action not explicitly allowed by security policy"
        )
        
        # Validate each rule has required fields
        for i, rule in enumerate(self.rules):
            if "action" not in rule:
                raise ValueError(
                    f"Policy rule at index {i} is missing required 'action' field"
                )
            if "allowed" not in rule:
                raise ValueError(
                    f"Policy rule at index {i} is missing required 'allowed' field"
                )
            if "reason" not in rule:
                raise ValueError(
                    f"Policy rule at index {i} is missing required 'reason' field"
                )
    
    def validate_intent(self, intent: Intent) -> PolicyDecision:
        """
        Validate an intent against policy rules.
        
        This method checks if the intent's action is allowed by the policy rules.
        It returns a PolicyDecision with the allowed status, reason, and any
        constraints that should be applied during execution.
        
        Args:
            intent: The intent to validate
        
        Returns:
            PolicyDecision with allowed status, reason, rule name, and constraints
        
        Example:
            >>> intent = Intent(action="shutdown_factory", ...)
            >>> decision = engine.validate_intent(intent)
            >>> print(decision.allowed)
            False
            >>> print(decision.reason)
            'Critical infrastructure control requires human authorization'
        """
        # Search for matching rule
        for rule in self.rules:
            if rule["action"] == intent.action:
                # Found matching rule - return decision based on rule
                return PolicyDecision(
                    allowed=rule["allowed"],
                    reason=rule["reason"],
                    rule_name=rule["action"],
                    constraints=rule.get("constraints")
                )
        
        # No matching rule found - apply default policy
        default_allowed = (self.default_policy == "allow")
        
        return PolicyDecision(
            allowed=default_allowed,
            reason=self.default_reason,
            rule_name="default",
            constraints=None
        )
    
    def get_allowed_actions(self) -> List[str]:
        """
        Get list of all allowed action types.
        
        This method provides introspection into which actions are permitted
        by the policy. Useful for displaying available commands to users.
        
        Returns:
            List of action names that are allowed by policy
        
        Example:
            >>> engine = PolicyEngine("policy.json")
            >>> allowed = engine.get_allowed_actions()
            >>> print(allowed)
            ['generate_report', 'analyze_aqi', 'send_alert']
        """
        allowed_actions = []
        
        for rule in self.rules:
            if rule.get("allowed", False):
                allowed_actions.append(rule["action"])
        
        return allowed_actions
    
    def reload_policy(self) -> bool:
        """
        Reload policy rules from file.
        
        This method allows runtime updates to the policy without restarting
        the system. Useful for updating security rules dynamically.
        
        Returns:
            True if policy was successfully reloaded, False otherwise
        
        Example:
            >>> engine = PolicyEngine("policy.json")
            >>> # ... modify policy.json ...
            >>> success = engine.reload_policy()
            >>> print(success)
            True
        """
        try:
            self._load_policy()
            return True
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            # Log error but don't crash - keep using existing policy
            print(f"Warning: Failed to reload policy: {e}")
            return False
    
    def get_policy_info(self) -> Dict[str, Any]:
        """
        Get information about the current policy configuration.
        
        Returns:
            Dictionary with policy metadata including version, rules count,
            default policy, and allowed actions
        
        Example:
            >>> engine = PolicyEngine("policy.json")
            >>> info = engine.get_policy_info()
            >>> print(info["version"])
            '1.0'
        """
        return {
            "version": self.policy_data.get("version", "unknown"),
            "description": self.policy_data.get("description", ""),
            "rules_count": len(self.rules),
            "default_policy": self.default_policy,
            "allowed_actions": self.get_allowed_actions(),
            "policy_file": self.policy_file
        }
