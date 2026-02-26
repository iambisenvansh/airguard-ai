"""
Main Agent Controller for AirGuard AI system.

This module implements the AirGuardAgent class that orchestrates the entire
pollution monitoring system, coordinating intent parsing, policy validation,
enforcement, and execution.
"""

from typing import Dict, Any
from intent import IntentParser
from policy import PolicyEngine
from executor import Executor
from logger import AuditLogger
from enforce import Enforcer


class AirGuardAgent:
    """
    Main controller for the AirGuard AI pollution monitoring system.
    
    The AirGuardAgent coordinates all system components to process user commands:
    1. Parse natural language command into structured intent
    2. Validate intent against security policy
    3. Enforce policy and execute approved actions
    4. Log all actions for audit trail
    
    This is the main entry point for the hackathon demo.
    
    Attributes:
        parser: IntentParser for natural language processing
        policy_engine: PolicyEngine for security validation
        executor: Executor for performing actions
        logger: AuditLogger for audit trail
        enforcer: Enforcer for security enforcement
    """
    
    def __init__(self, data_dir: str = "airguard-ai/data", 
                 output_dir: str = "airguard-ai/output",
                 log_dir: str = "airguard-ai/logs",
                 policy_file: str = "airguard-ai/policy.json"):
        """
        Initialize the AirGuard AI agent with all components.
        
        Args:
            data_dir: Directory containing pollution data
            output_dir: Directory for generated reports
            log_dir: Directory for audit logs
            policy_file: Path to policy configuration file
        """
        # Initialize all components
        self.parser = IntentParser()
        self.policy_engine = PolicyEngine(policy_file)
        self.executor = Executor(data_dir, output_dir)
        self.logger = AuditLogger(log_dir)
        self.enforcer = Enforcer(self.policy_engine, self.executor, self.logger)
        
        print("🤖 AirGuard AI Agent initialized successfully!")
        print(f"📁 Data directory: {data_dir}")
        print(f"📁 Output directory: {output_dir}")
        print(f"📁 Log directory: {log_dir}")
        print(f"🔒 Policy file: {policy_file}")
    
    def process_command(self, user_command: str) -> Dict[str, Any]:
        """
        Process a natural language command through the full pipeline.
        
        This is the main method for the hackathon demo!
        
        Args:
            user_command: Natural language command from user
            
        Returns:
            Dictionary with success status, message, and data
        """
        print(f"\n💬 User Command: \"{user_command}\"")
        
        try:
            # Step 1: Parse intent
            intent = self.parser.parse_intent(user_command)
            print(f"🧠 Parsed Intent: {intent.action} (confidence: {intent.confidence})")
            
            # Step 2: Enforce and execute
            result = self.enforcer.enforce_and_execute(intent)
            
            return result
            
        except Exception as e:
            error_msg = f"Agent error: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "message": error_msg,
                "data": None
            }
    
    def get_allowed_actions(self) -> list:
        """Get list of allowed actions from policy."""
        return self.policy_engine.get_allowed_actions()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and statistics."""
        logs = self.logger.get_logs()
        
        total_actions = len(logs)
        blocked_actions = len([log for log in logs if log.get("status") == "BLOCKED"])
        successful_actions = len([log for log in logs if log.get("status") == "SUCCESS"])
        errors = len([log for log in logs if log.get("status") == "ERROR"])
        
        return {
            "total_actions": total_actions,
            "successful_actions": successful_actions,
            "blocked_actions": blocked_actions,
            "errors": errors,
            "allowed_actions": self.get_allowed_actions()
        }
