"""
LangGraph implementation of AirGuard AI Agent.

This refactors the current sequential agent into a graph-based workflow using LangGraph.
The graph makes the flow explicit and easy to modify.

Installation:
    pip install langgraph langchain python-dotenv

Current Flow (Sequential):
    Command → Parser → Enforcer → Executor → Logger → Result

LangGraph Flow (Graph-based):
    Command
        ↓
    [Parse Node]
        ↓
    [Validate Node]
        ↓
    [Decision] ← Branch point
        ├─ If Blocked → [Deny Node]
        └─ If Allowed → [Execute Node]
        ↓
    [Log Node]
        ↓
    [Return Result]
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal, Any
from datetime import datetime
import json
import time

# Import your existing components
from intent import IntentParser
from policy import PolicyEngine
from executor import Executor
from logger import AuditLogger
from enforce import Enforcer

# ============================================================================
# State Definition
# ============================================================================

class AirGuardState(TypedDict):
    """
    State that flows through the LangGraph graph.
    
    This represents all data that moves between nodes.
    Each node reads and modifies this state.
    """
    # Input
    user_command: str
    user_id: str
    
    # After Parse Node
    intent: dict  # {'action': ..., 'parameters': {...}, 'confidence': ...}
    parse_error: str
    
    # After Validate Node
    policy_allowed: bool
    policy_reason: str
    policy_rule: str
    
    # After Execute Node
    execution_result: dict
    execution_time: float
    files_created: list
    execution_error: str
    
    # After Log Node
    audit_logged: bool
    audit_entry: dict
    
    # Final result
    final_result: dict

# ============================================================================
# Initialize Components (Same as Before)
# ============================================================================

parser = IntentParser()
policy_engine = PolicyEngine("policy.json")
executor = Executor("data", "output")
logger = AuditLogger("logs")
enforcer = Enforcer(policy_engine, executor, logger)

# ============================================================================
# Node Functions - Each Does One Thing
# ============================================================================

def parse_node(state: AirGuardState) -> AirGuardState:
    """
    Node 1: Parse natural language command into structured intent
    
    INPUT from state: user_command
    OUTPUT to state: intent, parse_error
    """
    print(f"\n🧠 [PARSE NODE] Processing: {state['user_command']}")
    
    try:
        # Parse the command
        intent = parser.parse_intent(state['user_command'])
        
        # Convert to dict for state
        intent_dict = {
            'action': intent.action,
            'parameters': intent.parameters,
            'confidence': intent.confidence,
            'user_command': intent.user_command,
            'timestamp': intent.timestamp.isoformat()
        }
        
        print(f"   ✅ Parsed: action={intent.action}, confidence={intent.confidence}")
        
        # Update state
        return {
            **state,
            'intent': intent_dict,
            'parse_error': ''
        }
        
    except Exception as e:
        error_msg = f"Parse error: {str(e)}"
        print(f"   ❌ {error_msg}")
        
        return {
            **state,
            'intent': {},
            'parse_error': error_msg
        }


def validate_node(state: AirGuardState) -> AirGuardState:
    """
    Node 2: Validate parsed intent against security policy
    
    INPUT from state: intent
    OUTPUT to state: policy_allowed, policy_reason, policy_rule
    """
    print(f"\n🔒 [VALIDATE NODE] Checking policy for: {state['intent'].get('action', 'unknown')}")
    
    try:
        # Check if parse failed
        if state['parse_error']:
            print(f"   ⚠️ Skipping validation due to parse error")
            return {
                **state,
                'policy_allowed': False,
                'policy_reason': state['parse_error'],
                'policy_rule': 'error'
            }
        
        # Validate against policy
        from models import Intent
        
        # Reconstruct Intent object for policy validation
        intent_data = state['intent']
        intent = Intent(
            action=intent_data['action'],
            parameters=intent_data['parameters'],
            timestamp=datetime.fromisoformat(intent_data['timestamp']),
            user_command=intent_data['user_command'],
            confidence=intent_data['confidence']
        )
        
        # Get policy decision
        policy_decision = policy_engine.validate_intent(intent)
        
        print(f"   Policy Decision: allowed={policy_decision.allowed}")
        print(f"   Reason: {policy_decision.reason}")
        
        return {
            **state,
            'policy_allowed': policy_decision.allowed,
            'policy_reason': policy_decision.reason,
            'policy_rule': policy_decision.rule_name
        }
        
    except Exception as e:
        error_msg = f"Validation error: {str(e)}"
        print(f"   ❌ {error_msg}")
        
        return {
            **state,
            'policy_allowed': False,
            'policy_reason': error_msg,
            'policy_rule': 'error'
        }


def execute_node(state: AirGuardState) -> AirGuardState:
    """
    Node 3: Execute the approved command
    
    INPUT from state: intent (action and parameters)
    OUTPUT to state: execution_result, execution_time, files_created, execution_error
    
    This node only runs if policy_allowed is True (see conditional routing)
    """
    print(f"\n⚡ [EXECUTE NODE] Executing: {state['intent'].get('action', 'unknown')}")
    
    start_time = time.time()
    
    try:
        # Reconstruct Intent object for execution
        from models import Intent
        
        intent_data = state['intent']
        intent = Intent(
            action=intent_data['action'],
            parameters=intent_data['parameters'],
            timestamp=datetime.fromisoformat(intent_data['timestamp']),
            user_command=intent_data['user_command'],
            confidence=intent_data['confidence']
        )
        
        # Execute the command
        result = executor.execute(intent)
        
        execution_time = time.time() - start_time
        
        print(f"   ✅ Execution completed in {execution_time:.2f}s")
        print(f"   Success: {result.success}")
        
        return {
            **state,
            'execution_result': {
                'success': result.success,
                'message': result.message,
                'data': result.data
            },
            'execution_time': execution_time,
            'files_created': result.files_created,
            'execution_error': ''
        }
        
    except Exception as e:
        execution_time = time.time() - start_time
        error_msg = f"Execution error: {str(e)}"
        print(f"   ❌ {error_msg}")
        
        return {
            **state,
            'execution_result': {'success': False, 'message': error_msg},
            'execution_time': execution_time,
            'files_created': [],
            'execution_error': error_msg
        }


def deny_node(state: AirGuardState) -> AirGuardState:
    """
    Node 4: Handle denied commands (policy blocked)
    
    This node runs instead of execute_node when policy_allowed is False
    """
    print(f"\n❌ [DENY NODE] Command blocked by policy")
    print(f"   Reason: {state['policy_reason']}")
    
    return {
        **state,
        'execution_result': {
            'success': False,
            'message': f"Action blocked: {state['policy_reason']}",
            'blocked_by_policy': True
        },
        'execution_time': 0.0,
        'files_created': [],
        'execution_error': state['policy_reason']
    }


def log_node(state: AirGuardState) -> AirGuardState:
    """
    Node 5: Log to audit trail
    
    INPUT from state: intent, policy_decision, execution_result
    OUTPUT to state: audit_logged, audit_entry
    """
    print(f"\n📝 [LOG NODE] Recording audit entry")
    
    try:
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': state['user_id'],
            'command': state['user_command'],
            'action': state['intent'].get('action', 'unknown'),
            'policy_allowed': state['policy_allowed'],
            'policy_reason': state['policy_reason'],
            'execution_success': state['execution_result'].get('success', False),
            'execution_time': state['execution_time'],
            'files_created': state['files_created']
        }
        
        # Log the entry
        logger.log(json.dumps(audit_entry))
        
        print(f"   ✅ Audit logged")
        
        return {
            **state,
            'audit_logged': True,
            'audit_entry': audit_entry
        }
        
    except Exception as e:
        error_msg = f"Logging error: {str(e)}"
        print(f"   ⚠️ {error_msg}")
        
        return {
            **state,
            'audit_logged': False,
            'audit_entry': {'error': error_msg}
        }


# ============================================================================
# Routing Functions - Conditional Logic
# ============================================================================

def route_policy_decision(state: AirGuardState) -> Literal["execute", "deny"]:
    """
    Conditional routing based on policy decision
    
    This function determines whether to execute or deny based on policy_allowed
    """
    if state['parse_error']:
        print(f"\n🔀 [ROUTER] Parse error detected, routing to DENY")
        return "deny"
    
    if state['policy_allowed']:
        print(f"\n🔀 [ROUTER] Policy ALLOWED, routing to EXECUTE")
        return "execute"
    else:
        print(f"\n🔀 [ROUTER] Policy BLOCKED, routing to DENY")
        return "deny"


# ============================================================================
# Build the Graph
# ============================================================================

def build_airguard_graph() -> StateGraph:
    """
    Construct the AirGuard LangGraph workflow
    
    Graph structure:
        [Parse] → [Validate] → [Router Decision]
                                    ├─ execute → [Execute]
                                    └─ deny ────→ [Deny]
                                    ↓
                                  [Log] → [End]
    """
    graph = StateGraph(AirGuardState)
    
    # Add nodes
    print("📐 Building AirGuard LangGraph...")
    graph.add_node("parse", parse_node)
    graph.add_node("validate", validate_node)
    graph.add_node("execute", execute_node)
    graph.add_node("deny", deny_node)
    graph.add_node("log", log_node)
    
    # Set entry point
    graph.set_entry_point("parse")
    
    # Add edges (always go from parse → validate)
    graph.add_edge("parse", "validate")
    
    # Conditional routing from validate (CRITICAL DECISION POINT)
    graph.add_conditional_edges(
        "validate",
        route_policy_decision,
        {
            "execute": "execute",
            "deny": "deny"
        }
    )
    
    # Both execute and deny flow to log
    graph.add_edge("execute", "log")
    graph.add_edge("deny", "log")
    
    # Log is the end
    graph.add_edge("log", END)
    
    print("✅ Graph built successfully!")
    
    return graph


# ============================================================================
# AirGuard LangGraph Agent Class
# ============================================================================

class AirGuardAgentLangGraph:
    """
    LangGraph-based implementation of AirGuard Agent
    
    This replaces the sequential agent.py with a graph-based approach.
    All existing components (parser, policy, executor, logger) are still used,
    but the flow is now explicit through a state graph.
    """
    
    def __init__(self):
        """Initialize the LangGraph-based agent"""
        self.graph_def = build_airguard_graph()
        self.app = self.graph_def.compile()
        print("\n🤖 AirGuard LangGraph Agent initialized!\n")
    
    def process_command(self, user_command: str, user_id: str = "admin") -> dict:
        """
        Process a command through the LangGraph
        
        Args:
            user_command: Natural language command
            user_id: ID of the user
            
        Returns:
            Dictionary with complete processing result
        """
        print("=" * 70)
        print(f"PROCESSING COMMAND: {user_command}")
        print("=" * 70)
        
        # Create initial state
        initial_state: AirGuardState = {
            "user_command": user_command,
            "user_id": user_id,
            "intent": {},
            "parse_error": "",
            "policy_allowed": False,
            "policy_reason": "",
            "policy_rule": "",
            "execution_result": {},
            "execution_time": 0.0,
            "files_created": [],
            "execution_error": "",
            "audit_logged": False,
            "audit_entry": {},
            "final_result": {}
        }
        
        # Run through the graph
        print("\n📊 Starting graph execution...\n")
        final_state = self.app.invoke(initial_state)
        
        # Format output (same as old agent for compatibility)
        output = {
            "success": final_state["execution_result"].get("success", False),
            "command": user_command,
            "intent": final_state["intent"],
            "policy_decision": {
                "allowed": final_state["policy_allowed"],
                "reason": final_state["policy_reason"],
                "rule": final_state["policy_rule"]
            },
            "result": final_state["execution_result"],
            "execution_time": final_state["execution_time"],
            "files_created": final_state["files_created"],
            "audit_logged": final_state["audit_logged"]
        }
        
        print("\n" + "=" * 70)
        print(f"RESULT: {'✅ SUCCESS' if output['success'] else '❌ FAILED'}")
        print("=" * 70 + "\n")
        
        return output
    
    def process_command_stream(self, user_command: str, user_id: str = "admin"):
        """
        Process command and stream results node-by-node.
        
        Useful for real-time UI updates or debugging.
        
        Args:
            user_command: Natural language command
            user_id: ID of the user
            
        Yields:
            Events as each node executes
        """
        initial_state: AirGuardState = {
            "user_command": user_command,
            "user_id": user_id,
            "intent": {},
            "parse_error": "",
            "policy_allowed": False,
            "policy_reason": "",
            "policy_rule": "",
            "execution_result": {},
            "execution_time": 0.0,
            "files_created": [],
            "execution_error": "",
            "audit_logged": False,
            "audit_entry": {},
            "final_result": {}
        }
        
        # Stream events as each node completes
        for event in self.app.stream(initial_state):
            yield event
    
    def get_graph_structure(self) -> str:
        """
        Get visual representation of the graph
        
        Returns:
            ASCII art diagram of the graph structure
        """
        try:
            return self.graph_def.get_graph().draw_ascii()
        except:
            return "Unable to draw graph"
    
    def get_system_status(self) -> dict:
        """
        Get system status and statistics (same as original)
        
        Returns:
            Dictionary with status info
        """
        logs = logger.get_logs()
        
        total_actions = len(logs)
        blocked_actions = len([log for log in logs if log.get("status") == "BLOCKED"])
        successful_actions = len([log for log in logs if log.get("status") == "SUCCESS"])
        errors = len([log for log in logs if log.get("status") == "ERROR"])
        
        return {
            "total_actions": total_actions,
            "successful_actions": successful_actions,
            "blocked_actions": blocked_actions,
            "errors": errors,
            "allowed_actions": policy_engine.get_allowed_actions()
        }


# ============================================================================
# Usage Examples
# ============================================================================

if __name__ == "__main__":
    # Create the agent
    agent = AirGuardAgentLangGraph()
    
    # Show graph structure
    print("\nGraph Structure:")
    print(agent.get_graph_structure())
    
    # Example 1: Execute command
    print("\n\n" + "🎯" * 35)
    print("EXAMPLE 1: Generate Report")
    print("🎯" * 35)
    result1 = agent.process_command(
        "Generate pollution report for Delhi"
    )
    print(f"\nResult: {json.dumps(result1, indent=2)}")
    
    # Example 2: Blocked command
    print("\n\n" + "🎯" * 35)
    print("EXAMPLE 2: Blocked Command (Policy Denied)")
    print("🎯" * 35)
    result2 = agent.process_command(
        "Shutdown the factory"  # This will be blocked by policy
    )
    print(f"\nResult: {json.dumps(result2, indent=2)}")
    
    # Example 3: Streaming execution
    print("\n\n" + "🎯" * 35)
    print("EXAMPLE 3: Streaming Execution")
    print("🎯" * 35)
    print("\nStreaming events as they occur:")
    for event in agent.process_command_stream("Analyze AQI in Mumbai"):
        print(f"Event: {event}")
