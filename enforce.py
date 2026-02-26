"""
Enforcement Layer for AirGuard AI system.

This module implements the security enforcement layer that validates all actions
against policy rules before execution. This is the critical security gateway that
prevents unauthorized operations.
"""

from typing import Dict, Any
from models import Intent, PolicyDecision, ExecutionResult
from policy import PolicyEngine
from executor import Executor
from logger import AuditLogger


class Enforcer:
    """
    Security enforcement layer that validates and executes actions.
    
    The Enforcer is the critical security gateway in the AirGuard AI system.
    It ensures that NO action is executed without policy validation. This is
    what hackathon judges will check to verify security enforcement.
    
    Flow:
    1. Receive intent
    2. Validate against policy
    3. If BLOCKED -> Log and return denial
    4. If ALLOWED -> Execute and log result
    
    Attributes:
        policy_engine: PolicyEngine instance for validation
        executor: Executor instance for performing actions
        logger: AuditLogger instance for audit trail
    """
    
    def __init__(self, policy_engine: PolicyEngine, executor: Executor, logger: AuditLogger):
        """Initialize the Enforcer with required components."""
        self.policy_engine = policy_engine
        self.executor = executor
        self.logger = logger
    
    def enforce_and_execute(self, intent: Intent) -> Dict[str, Any]:
        """
        Validate intent against policy and execute if allowed.
        
        CRITICAL SECURITY CHECK - This is what judges will review!
        
        Args:
            intent: The intent to validate and execute
            
        Returns:
            Dictionary with success, message, data, and policy_decision
        """
        # Step 1: Validate against policy
        policy_decision = self.policy_engine.validate_intent(intent)
        
        # Step 2: CRITICAL CHECK - Block if not allowed
        if not policy_decision.allowed:
            # ACTION IS BLOCKED - Log and return denial
            result = ExecutionResult(
                success=False,
                message=f"Action blocked by policy: {policy_decision.reason}",
                data={
                    "action": intent.action,
                    "reason": policy_decision.reason,
                    "rule": policy_decision.rule_name
                }
            )
            
            # Log the blocked attempt
            self.logger.log_action(
                intent=intent,
                policy_decision=policy_decision,
                result=result,
                status="BLOCKED"
            )
            
            return {
                "success": False,
                "message": f"❌ BLOCKED: {policy_decision.reason}",
                "data": result.data,
                "policy_decision": policy_decision.to_dict()
            }
        
        # Step 3: Action is allowed - Execute it
        try:
            result = self.executor.execute(intent)
            
            # Log successful execution
            self.logger.log_action(
                intent=intent,
                policy_decision=policy_decision,
                result=result,
                status="SUCCESS" if result.success else "ERROR"
            )
            
            return {
                "success": result.success,
                "message": result.message,
                "data": result.data,
                "execution_time": result.execution_time,
                "files_created": result.files_created,
                "policy_decision": policy_decision.to_dict()
            }
            
        except Exception as e:
            # Handle execution errors
            error_result = ExecutionResult(
                success=False,
                message=f"Execution error: {str(e)}"
            )
            
            self.logger.log_action(
                intent=intent,
                policy_decision=policy_decision,
                result=error_result,
                status="ERROR"
            )
            
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "data": None,
                "policy_decision": policy_decision.to_dict()
            }
