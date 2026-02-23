"""
AirGuard AI Agent - Main Controller

This module implements the AirGuardAgent class, which is the main controller that
orchestrates the entire workflow. The agent coordinates intent parsing, policy
validation, enforcement, and execution while ensuring all actions are logged.

CRITICAL FOR HACKATHON: This is the main entry point that demonstrates the complete
autonomous AI agent system with policy-based security enforcement.
"""

from typing import Dict, Any
from intent import IntentParser
from policy import PolicyEngine
from enforce import Enforcer
from logger import AuditLogger


class AirGuardAgent:
    """
    Main controller for the AirGuard AI autonomous agent system.
    
    The AirGuardAgent orchestrates the complete workflow:
    1. Parse natural language commands into structured intents
    2. Validate intents against security policies
    3. Enforce policy decisions (block or allow)
    4. Execute approved actions
    5. Log all actions for audit trails
    
    This demonstrates a complete autonomous AI agent with:
    - Natural language understanding
    - Policy-based security
    - Enforcement layer preventing unauthorized actions
    - Comprehensive audit logging
    - OpenClaw integration for system operations
    
    Attributes:
        intent_parser: Parses natural language into structured intents
        policy_engine: Validates intents against security policies
        enforcer: Enforces policy decisions and executes approved actions
        logger: Maintains audit logs of all actions
    
    Example:
        >>> agent = AirGuardAgent(parser, policy, enforcer, logger)
        >>> 
        >>> # Allowed action
        >>> result = agent.process_command("Generate pollution report for Delhi")
        >>> print(result["success"])
        True
        >>> 
        >>> # Blocked action
        >>> result = agent.process_command("Shutdown factory in Mayapuri")
        >>> print(result["success"])
        False
        >>> print(result["message"])
        'Action blocked by policy: Critical infrastructure control requires human authorization'
    """
    
    def __init__(
        self,
        intent_parser: IntentParser,
        policy_engine: PolicyEngine,
        enforcer: Enforcer,
        logger: AuditLogger
    ):
        """
        Initialize the AirGuardAgent with all required components.
        
        Args:
            intent_parser: IntentParser instance for parsing commands
            policy_engine: PolicyEngine instance for policy validation
            enforcer: Enforcer instance for enforcement and execution
            logger: AuditLogger instance for audit trails
        """
        self.intent_parser = intent_parser
        self.policy_engine = policy_engine
        self.enforcer = enforcer
        self.logger = logger
        
        # Statistics tracking
        self._stats = {
            "total_commands": 0,
            "successful_actions": 0,
            "blocked_actions": 0,
            "errors": 0
        }
    
    def process_command(self, user_command: str) -> Dict[str, Any]:
        """
        Process a natural language command through the full pipeline.
        
        This is the main entry point for the agent. It coordinates all components
        to process a user command from natural language to execution.
        
        Pipeline:
        1. Validate input
        2. Parse intent from natural language
        3. Validate intent structure
        4. Check policy (allowed or blocked?)
        5. If blocked: return denial with reason
        6. If allowed: enforce and execute
        7. Log everything
        8. Return result to user
        
        Args:
            user_command: Natural language command from user
        
        Returns:
            Dictionary with keys:
            - success (bool): Whether the action succeeded
            - message (str): Human-readable status message
            - data (dict, optional): Result data if successful
            - files (list, optional): Created files if any
            - action (str, optional): Action type that was attempted
        
        Example:
            >>> # Allowed action
            >>> result = agent.process_command("Generate report for Delhi")
            >>> print(result)
            {
                "success": True,
                "message": "Action completed successfully",
                "data": {"report_file": "output/delhi_report.txt", ...},
                "files": ["output/delhi_report.txt"],
                "action": "generate_report"
            }
            
            >>> # Blocked action
            >>> result = agent.process_command("Shutdown factory")
            >>> print(result)
            {
                "success": False,
                "message": "Action blocked by policy: Critical infrastructure control requires human authorization",
                "action": "shutdown_factory"
            }
        """
        # Update statistics
        self._stats["total_commands"] += 1
        
        # Step 1: Validate input
        if not user_command or not isinstance(user_command, str):
            self._stats["errors"] += 1
            return {
                "success": False,
                "message": "Invalid command input: command must be a non-empty string"
            }
        
        if not user_command.strip():
            self._stats["errors"] += 1
            return {
                "success": False,
                "message": "Invalid command input: command cannot be empty or whitespace"
            }
        
        try:
            # Step 2: Parse intent from natural language
            intent = self.intent_parser.parse_intent(user_command)
            
            # Step 3: Validate intent structure
            if not self.intent_parser.validate_intent_structure(intent):
                self._stats["errors"] += 1
                self.logger.log_action(
                    intent=intent,
                    policy_decision=None,
                    result=None,
                    status="ERROR"
                )
                return {
                    "success": False,
                    "message": "Could not parse command into valid intent",
                    "action": intent.action if intent else "unknown"
                }
            
            # Step 4: Validate against policy
            policy_decision = self.policy_engine.validate_intent(intent)
            
            # Step 5: Check if action is allowed
            if not policy_decision.allowed:
                # Action is BLOCKED by policy
                self._stats["blocked_actions"] += 1
                
                # The enforcer will log this, but we return the denial immediately
                result = self.enforcer.enforce_and_execute(intent, policy_decision)
                
                return {
                    "success": False,
                    "message": result.message,
                    "action": intent.action,
                    "blocked_reason": policy_decision.reason,
                    "policy_rule": policy_decision.rule_name
                }
            
            # Step 6: Execute approved action (enforcer handles logging)
            execution_result = self.enforcer.enforce_and_execute(intent, policy_decision)
            
            # Step 7: Update statistics
            if execution_result.success:
                self._stats["successful_actions"] += 1
            else:
                self._stats["errors"] += 1
            
            # Step 8: Return result to user
            response = {
                "success": execution_result.success,
                "message": execution_result.message,
                "action": intent.action
            }
            
            # Add optional fields if present
            if execution_result.data:
                response["data"] = execution_result.data
            
            if execution_result.files_created:
                response["files"] = execution_result.files_created
            
            if execution_result.execution_time:
                response["execution_time"] = execution_result.execution_time
            
            return response
            
        except Exception as e:
            # Handle unexpected errors
            self._stats["errors"] += 1
            
            # Log error
            self.logger.log_action(
                intent=None,
                policy_decision=None,
                result=None,
                status="ERROR"
            )
            
            return {
                "success": False,
                "message": f"System error: {str(e)}"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current system status and statistics.
        
        Returns:
            Dictionary with system status including:
            - total_commands: Total commands processed
            - successful_actions: Number of successful executions
            - blocked_actions: Number of blocked actions
            - errors: Number of errors
            - allowed_actions: List of actions allowed by policy
        
        Example:
            >>> status = agent.get_status()
            >>> print(status)
            {
                "total_commands": 10,
                "successful_actions": 6,
                "blocked_actions": 3,
                "errors": 1,
                "allowed_actions": ["generate_report", "analyze_aqi", "send_alert"]
            }
        """
        return {
            "total_commands": self._stats["total_commands"],
            "successful_actions": self._stats["successful_actions"],
            "blocked_actions": self._stats["blocked_actions"],
            "errors": self._stats["errors"],
            "allowed_actions": self.policy_engine.get_allowed_actions()
        }
