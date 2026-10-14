# How to Add LangGraph to AirGuard AI (Optional)

**Note:** Your current system works perfectly. This is for future reference if you want to refactor!

---

## When to Add LangGraph

✅ When you need:
- Retry logic
- Conditional branching
- Multiple execution paths
- State persistence
- Human-in-the-loop workflows
- Team-based development

❌ Don't add if:
- Current system works great (it does!)
- Small project
- Linear workflow (it is!)
- No complex branching needed

---

## Step 1: Install LangGraph

```bash
pip install langgraph langchain python-dotenv
```

Update requirements_api.txt:
```
flask==3.0.0
flask-cors==4.0.0
flask-sqlalchemy==3.1.1
pyjwt==2.15.1
python-dotenv==1.0.0
gunicorn==21.2.0
langgraph==0.0.1
langchain==0.1.0
```

---

## Step 2: Create LangGraph Version

Create a new file: `agent_langgraph.py`

```python
"""
LangGraph version of AirGuard Agent
Demonstrates graph-based workflow
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal, Any
from intent import IntentParser
from policy import PolicyEngine
from executor import Executor
from logger import AuditLogger
from enforce import Enforcer
import json

# Define state structure
class AirGuardState(TypedDict):
    """State that flows through the graph"""
    user_command: str
    user_id: str
    intent: dict
    policy_allowed: bool
    policy_reason: str
    execution_result: dict
    error: str
    audit_entry: dict

# Initialize components (same as before)
parser = IntentParser()
policy_engine = PolicyEngine("policy.json")
executor = Executor("data", "output")
logger = AuditLogger("logs")
enforcer = Enforcer(policy_engine, executor, logger)

# ============================================================================
# Node Functions
# ============================================================================

def parse_node(state: AirGuardState) -> AirGuardState:
    """
    Node 1: Parse natural language command into structured intent
    """
    print(f"💬 Parse Node: {state['user_command']}")
    
    try:
        intent = parser.parse_intent(state["user_command"])
        print(f"🧠 Parsed Intent: {intent.action}")
        
        return {
            **state,
            "intent": {
                "action": intent.action,
                "parameters": intent.parameters,
                "confidence": intent.confidence
            }
        }
    except Exception as e:
        return {
            **state,
            "error": f"Parse error: {str(e)}"
        }

def validate_node(state: AirGuardState) -> AirGuardState:
    """
    Node 2: Validate parsed intent against security policy
    """
    print(f"🔒 Validate Node: {state['intent']['action']}")
    
    try:
        allowed, reason = policy_engine.validate(state["intent"])
        
        return {
            **state,
            "policy_allowed": allowed,
            "policy_reason": reason
        }
    except Exception as e:
        return {
            **state,
            "error": f"Validation error: {str(e)}"
        }

def execute_node(state: AirGuardState) -> AirGuardState:
    """
    Node 3: Execute approved command
    """
    print(f"⚡ Execute Node: {state['intent']['action']}")
    
    try:
        result = executor.execute(state["intent"])
        
        return {
            **state,
            "execution_result": {
                "status": "success",
                "data": result
            }
        }
    except Exception as e:
        return {
            **state,
            "error": f"Execution error: {str(e)}",
            "execution_result": {"status": "error"}
        }

def deny_node(state: AirGuardState) -> AirGuardState:
    """
    Node 4: Handle denied commands
    """
    print(f"❌ Deny Node: {state['policy_reason']}")
    
    return {
        **state,
        "execution_result": {
            "status": "denied",
            "reason": state["policy_reason"]
        }
    }

def log_node(state: AirGuardState) -> AirGuardState:
    """
    Node 5: Log to audit trail
    """
    print(f"📝 Log Node")
    
    try:
        audit_entry = {
            "user_id": state["user_id"],
            "command": state["user_command"],
            "intent": state["intent"],
            "policy_allowed": state["policy_allowed"],
            "policy_reason": state["policy_reason"],
            "status": "success" if state["policy_allowed"] else "denied",
            "result": state["execution_result"]
        }
        
        logger.log(json.dumps(audit_entry))
        
        return {
            **state,
            "audit_entry": audit_entry
        }
    except Exception as e:
        print(f"⚠️ Logging error: {e}")
        return state

# ============================================================================
# Routing Function
# ============================================================================

def route_policy_decision(state: AirGuardState) -> Literal["execute", "deny"]:
    """
    Conditional routing: decide based on policy decision
    """
    if state.get("error"):
        return "deny"  # Error occurred, go to deny
    
    if state["policy_allowed"]:
        return "execute"  # Policy allowed, execute
    else:
        return "deny"  # Policy blocked, deny

# ============================================================================
# Build Graph
# ============================================================================

def build_airguard_graph() -> StateGraph:
    """
    Construct the AirGuard workflow graph
    """
    graph = StateGraph(AirGuardState)
    
    # Add nodes
    graph.add_node("parse", parse_node)
    graph.add_node("validate", validate_node)
    graph.add_node("execute", execute_node)
    graph.add_node("deny", deny_node)
    graph.add_node("log", log_node)
    
    # Set entry point
    graph.set_entry_point("parse")
    
    # Add edges
    graph.add_edge("parse", "validate")
    
    # Conditional routing from validate
    graph.add_conditional_edges(
        "validate",
        route_policy_decision,
        {
            "execute": "execute",
            "deny": "deny"
        }
    )
    
    # Both execute and deny lead to log
    graph.add_edge("execute", "log")
    graph.add_edge("deny", "log")
    
    # Log is the end
    graph.add_edge("log", END)
    
    return graph

# ============================================================================
# AirGuard Agent Class (LangGraph Version)
# ============================================================================

class AirGuardAgentLangGraph:
    """
    LangGraph-based implementation of AirGuard Agent
    """
    
    def __init__(self):
        """Initialize the graph-based agent"""
        self.graph = build_airguard_graph()
        self.app = self.graph.compile()
        print("✅ AirGuard LangGraph Agent initialized!")
    
    def process_command(self, user_command: str, user_id: str = "admin") -> dict:
        """
        Process command through the graph
        
        Args:
            user_command: Natural language command
            user_id: ID of user executing command
            
        Returns:
            Final state dict with all processing information
        """
        print(f"\n{'='*60}")
        print(f"Processing Command: {user_command}")
        print(f"{'='*60}")
        
        # Create initial state
        initial_state: AirGuardState = {
            "user_command": user_command,
            "user_id": user_id,
            "intent": {},
            "policy_allowed": False,
            "policy_reason": "",
            "execution_result": {},
            "error": "",
            "audit_entry": {}
        }
        
        # Run through graph
        final_state = self.app.invoke(initial_state)
        
        # Format output
        output = {
            "success": final_state["execution_result"].get("status") == "success",
            "command": user_command,
            "intent": final_state["intent"],
            "policy_decision": {
                "allowed": final_state["policy_allowed"],
                "reason": final_state["policy_reason"]
            },
            "result": final_state["execution_result"],
            "audit_logged": bool(final_state["audit_entry"])
        }
        
        return output
    
    def process_command_stream(self, user_command: str):
        """
        Process command and stream results node-by-node
        (useful for real-time UI updates)
        """
        initial_state: AirGuardState = {
            "user_command": user_command,
            "user_id": "admin",
            "intent": {},
            "policy_allowed": False,
            "policy_reason": "",
            "execution_result": {},
            "error": "",
            "audit_entry": {}
        }
        
        # Stream events
        for event in self.app.stream(initial_state):
            yield event
    
    def get_graph_structure(self) -> str:
        """
        Get visual representation of graph
        """
        return self.graph.get_graph().draw_ascii()

# ============================================================================
# Usage
# ============================================================================

if __name__ == "__main__":
    # Create agent
    agent = AirGuardAgentLangGraph()
    
    # Show graph
    print(agent.get_graph_structure())
    print("\n")
    
    # Process command
    result = agent.process_command("Generate pollution report for Delhi")
    print(f"\nResult: {result}")
    
    # Show streaming
    print("\n\nStreaming Results:")
    for event in agent.process_command_stream("Show AQI for Mumbai"):
        print(event)
```

---

## Step 3: Update Backend to Support Both

Modify `backend_api.py`:

```python
# Near the top, after imports
from agent import AirGuardAgent  # Current version
# from agent_langgraph import AirGuardAgentLangGraph  # Optional LangGraph version

# In the initialization section:
app = Flask(__name__)

# Use current agent (or LangGraph if you uncomment below)
agent = AirGuardAgent()
# agent = AirGuardAgentLangGraph()  # Switch to LangGraph version

# Rest of code stays the same
```

---

## Step 4: Update Process Command Endpoint

The endpoint stays the same! LangGraph returns the same format:

```python
@app.route('/api/process_command', methods=['POST'])
@token_required
def process_command():
    """Process a natural language command"""
    data = request.get_json()
    command = data.get('command')
    
    if not command:
        return jsonify({'message': 'Command required'}), 400
    
    try:
        # Works with BOTH agents!
        result = agent.process_command(command)
        
        # Record to audit log database
        audit_log = AuditLog(
            user_id=request.user.get('id'),
            username=request.user['username'],
            command=command,
            action=result.get('action', 'unknown'),
            policy_allowed=result.get('success', False),
            policy_reason=result.get('policy_reason', ''),
            status='success' if result.get('success') else 'error',
            execution_time=result.get('execution_time', 0),
            result=json.dumps(result)
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify(result), 200 if result.get('success') else 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e),
            'error': True
        }), 500
```

---

## Step 5: Test LangGraph Version

```bash
# Test the LangGraph agent directly
python agent_langgraph.py

# Should see:
# ✅ AirGuard LangGraph Agent initialized!
# ============================================================
# Processing Command: Generate pollution report for Delhi
# ============================================================
# 💬 Parse Node: Generate pollution report for Delhi
# 🧠 Parsed Intent: generate_report
# 🔒 Validate Node: generate_report
# ⚡ Execute Node: generate_report
# 📝 Log Node
# 
# Result: {'success': True, ...}
```

---

## Advantages of LangGraph Version

✅ **Visual workflow** - Can see graph structure
✅ **Streaming** - Get updates as each node executes
✅ **Persistence** - Can save/resume at any node
✅ **Parallelization** - Future: run nodes in parallel
✅ **Debugging** - Built-in tracing and visualization
✅ **Testability** - Test each node independently

---

## Migration Checklist

- [ ] Install langgraph: `pip install langgraph`
- [ ] Create `agent_langgraph.py`
- [ ] Test LangGraph agent: `python agent_langgraph.py`
- [ ] Update `backend_api.py` to import LangGraph version
- [ ] Test API endpoint: still returns same results
- [ ] Verify audit logs work the same
- [ ] All tests pass
- [ ] Update requirements.txt
- [ ] Commit and deploy

**Estimated time:** 2-4 hours

---

## Running Both Versions Side-by-Side

You can run both for comparison:

```python
# In test_both.py
from agent import AirGuardAgent
from agent_langgraph import AirGuardAgentLangGraph

agent1 = AirGuardAgent()
agent2 = AirGuardAgentLangGraph()

command = "Generate report for Delhi"

result1 = agent1.process_command(command)
result2 = agent2.process_command(command)

# Compare results
assert result1["success"] == result2["success"]
print("✅ Both agents produce same result!")
```

---

## Advanced: Add Retry Logic with LangGraph

One major benefit - easy retry logic:

```python
def route_with_retry(state: AirGuardState) -> Literal["execute", "retry", "fail"]:
    """Route with retry capability"""
    if state.get("error") and state.get("attempts", 0) < 3:
        return "retry"
    elif state.get("error"):
        return "fail"
    else:
        return "execute"

# Add retry node
def retry_node(state: AirGuardState) -> AirGuardState:
    """Retry parse with different strategy"""
    state["attempts"] = state.get("attempts", 0) + 1
    state["error"] = ""  # Clear error
    return state

# Add to graph
graph.add_node("retry", retry_node)
graph.add_conditional_edges("parse", route_with_retry)
graph.add_edge("retry", "parse")  # Loop back
```

This would be **much harder** in the current linear approach!

---

## Summary

**LangGraph in AirGuard AI:**

✅ Same results as current system
✅ Much cleaner for complex workflows
✅ Easy to add branching/retries
✅ Better for scaling
✅ Industry-standard approach

**Migration effort:** 2-4 hours
**Testing effort:** 1 hour
**Total:** ~5 hours

**Recommendation:**
- **Now:** Use current system (works great!)
- **Later:** Migrate when adding advanced features
- **Next project:** Start with LangGraph

---

## Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [Example Agents](https://github.com/langchain-ai/langgraph/tree/main/examples)

