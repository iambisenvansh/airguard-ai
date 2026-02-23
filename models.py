"""
Core data models for AirGuard AI system.

This module defines the fundamental data structures used throughout the system:
- Intent: Structured representation of user commands
- PolicyDecision: Result of policy validation
- ExecutionResult: Outcome of action execution
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime


@dataclass
class Intent:
    """
    Structured representation of a user command.
    
    Attributes:
        action: The type of action to perform (e.g., "generate_report", "analyze_aqi")
        parameters: Action-specific parameters extracted from the command
        timestamp: When the intent was created
        user_command: Original natural language command from the user
        confidence: Parser confidence score (0.0 to 1.0)
    
    Example:
        >>> intent = Intent(
        ...     action="generate_report",
        ...     parameters={"location": "Delhi"},
        ...     timestamp=datetime.now(),
        ...     user_command="Generate pollution report for Delhi",
        ...     confidence=0.95
        ... )
    """
    action: str
    parameters: Dict[str, Any]
    timestamp: datetime
    user_command: str
    confidence: float
    
    def __post_init__(self):
        """Validate intent fields after initialization."""
        if not self.action or not isinstance(self.action, str):
            raise ValueError("action must be a non-empty string")
        
        if not isinstance(self.parameters, dict):
            raise ValueError("parameters must be a dictionary")
        
        if not isinstance(self.timestamp, datetime):
            raise ValueError("timestamp must be a datetime object")
        
        if not isinstance(self.confidence, (int, float)) or not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be a float between 0.0 and 1.0")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert intent to dictionary for logging and serialization.
        
        Returns:
            Dictionary representation of the intent
        """
        return {
            "action": self.action,
            "parameters": self.parameters,
            "timestamp": self.timestamp.isoformat(),
            "user_command": self.user_command,
            "confidence": self.confidence
        }


@dataclass
class PolicyDecision:
    """
    Result of policy validation for an intent.
    
    Attributes:
        allowed: Whether the action is permitted by policy
        reason: Human-readable explanation for the decision
        rule_name: Name of the policy rule that was matched
        constraints: Optional additional constraints to apply during execution
    
    Example:
        >>> decision = PolicyDecision(
        ...     allowed=False,
        ...     reason="Critical infrastructure control requires human authorization",
        ...     rule_name="shutdown_factory",
        ...     constraints=None
        ... )
    """
    allowed: bool
    reason: str
    rule_name: str
    constraints: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate policy decision fields after initialization."""
        if not isinstance(self.allowed, bool):
            raise ValueError("allowed must be a boolean")
        
        if not self.reason or not isinstance(self.reason, str):
            raise ValueError("reason must be a non-empty string")
        
        if not self.rule_name or not isinstance(self.rule_name, str):
            raise ValueError("rule_name must be a non-empty string")
        
        if self.constraints is not None and not isinstance(self.constraints, dict):
            raise ValueError("constraints must be a dictionary or None")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert policy decision to dictionary.
        
        Returns:
            Dictionary representation of the policy decision
        """
        return {
            "allowed": self.allowed,
            "reason": self.reason,
            "rule_name": self.rule_name,
            "constraints": self.constraints
        }


@dataclass
class ExecutionResult:
    """
    Outcome of executing an approved action.
    
    Attributes:
        success: Whether the execution completed successfully
        message: Human-readable status message
        data: Optional result data from the execution
        execution_time: Time taken to execute in seconds
        files_created: List of file paths created during execution
    
    Example:
        >>> result = ExecutionResult(
        ...     success=True,
        ...     message="Report generated successfully",
        ...     data={"report_file": "output/delhi_report.txt"},
        ...     execution_time=1.23,
        ...     files_created=["output/delhi_report.txt"]
        ... )
    """
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    execution_time: float = 0.0
    files_created: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate execution result fields after initialization."""
        if not isinstance(self.success, bool):
            raise ValueError("success must be a boolean")
        
        if not self.message or not isinstance(self.message, str):
            raise ValueError("message must be a non-empty string")
        
        if self.data is not None and not isinstance(self.data, dict):
            raise ValueError("data must be a dictionary or None")
        
        if not isinstance(self.execution_time, (int, float)) or self.execution_time < 0:
            raise ValueError("execution_time must be a non-negative number")
        
        if not isinstance(self.files_created, list):
            raise ValueError("files_created must be a list")
        
        # Validate all items in files_created are strings
        if not all(isinstance(f, str) for f in self.files_created):
            raise ValueError("all items in files_created must be strings")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert execution result to dictionary.
        
        Returns:
            Dictionary representation of the execution result
        """
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "execution_time": self.execution_time,
            "files_created": self.files_created
        }
