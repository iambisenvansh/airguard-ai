# How to Convert Your AirGuard to LangGraph - Step by Step

## Overview

I've created `agent_langgraph_complete.py` that converts your sequential agent into a graph-based LangGraph workflow.

**What changes:**
- Agent orchestration → LangGraph StateGraph
- Function calls → Graph nodes
- Sequential logic → Explicit edges and routing

**What stays the same:**
- Parser, Policy, Executor, Logger (all reused!)
- Backend API integration
- Frontend compatibility

---

## Step 1: Install LangGraph

```bash
pip install langgraph langchain
```

Update `requirements_api.txt`:
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

Then install:
```bash
pip install -r requirements_api.txt
```

---

## Step 2: Use the New Agent File

I've created: `agent_langgraph_complete.py`

This file has everything you need:
- ✅ State definition (AirGuardState)
- ✅ All node functions
- ✅ Routing logic
- ✅ Graph construction
- ✅ AirGuardAgentLangGraph class
- ✅ Backward compatible interface

---

## Step 3: Test the LangGraph Version

**Option A: Test Directly**

```bash
python agent_langgraph_complete.py
```

You'll see:
```
======================================================================
PROCESSING COMMAND: Generate pollution report for Delhi
======================================================================

📊 Starting graph execution...

🧠 [PARSE NODE] Processing: Generate pollution report for Delhi
   ✅ Parsed: action=generate_report, confidence=0.95

🔒 [VALIDATE NODE] Checking policy for: generate_report
   Policy Decision: allowed=True
   Reason: Operator allowed

🔀 [ROUTER] Policy ALLOWED, routing to EXECUTE

⚡ [EXECUTE NODE] Executing: generate_report
   ✅ Execution completed in 1.23s
   Success: True

📝 [LOG NODE] Recording audit entry
   ✅ Audit logged

======================================================================
RESULT: ✅ SUCCESS
======================================================================
```

**Option B: Compare Old vs New**

```python
# test_both_agents.py
from agent import AirGuardAgent
from agent_langgraph_complete import AirGuardAgentLangGraph

old_agent = AirGuardAgent()
new_agent = AirGuardAgentLangGraph()

command = "Generate pollution report for Delhi"

result_old = old_agent.process_command(command)
result_new = new_agent.process_command(command)

# Check they produce same result
assert result_old["success"] == result_new["success"]
print("✅ Both agents produce same result!")
```

Run it:
```bash
python test_both_agents.py
```

---

## Step 4: Update Backend API to Use LangGraph

In `backend_api.py`, change the import:

**Before:**
```python
from agent import AirGuardAgent

agent = AirGuardAgent()
```

**After:**
```python
from agent_langgraph_complete import AirGuardAgentLangGraph

agent = AirGuardAgentLangGraph()
```

That's it! No other changes needed because the interface is the same.

---

## Step 5: Test Backend API

```bash
# Terminal 1: Start backend
python backend_api.py

# Terminal 2: Test API
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin", "password":"password123"}'

# Use the token to test command
curl -X POST http://localhost:5000/api/process_command \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"command":"Generate pollution report for Delhi"}'
```

You should see the same response as before!

---

## Step 6: Start Frontend (No Changes)

```bash
cd frontend
npm start
```

Frontend works the same - it calls the same API endpoints!

---

## Complete Migration Checklist

- [ ] Install langgraph: `pip install langgraph langchain`
- [ ] Copy `agent_langgraph_complete.py` to your project
- [ ] Test new agent: `python agent_langgraph_complete.py`
- [ ] Verify output format (same as before)
- [ ] Update `backend_api.py` imports
- [ ] Test backend API endpoints
- [ ] Test frontend (should work unchanged)
- [ ] Compare old vs new results
- [ ] Deploy new version

---

## Key Differences: Old vs New

### Old Sequential Agent (agent.py)

```python
def process_command(self, user_command):
    # Parse
    intent = self.parser.parse_intent(user_command)
    
    # Enforce & Execute
    result = self.enforcer.enforce_and_execute(intent)
    
    return result
```

**Flow:**
- Function calls in sequence
- State passed implicitly between functions
- Routing happens in if/else statements

### New LangGraph Agent

```python
def process_command(self, user_command):
    initial_state = {
        "user_command": user_command,
        "intent": None,
        ...
    }
    
    final_state = self.app.invoke(initial_state)
    return format_output(final_state)
```

**Flow:**
- Graph with explicit nodes
- State passed through AirGuardState dict
- Routing happens in conditional_edges

---

## Graph Visualization

Your new LangGraph:

```
                    [Start]
                       ↓
                  [Parse Node]
                  - Extract intent
                  - Set confidence
                       ↓
                [Validate Node]
                - Check policy
                - Allow or Block?
                       ↓
                   [Router]
                      / \
                    /     \
              Allowed   Blocked
                /           \
               ↓             ↓
         [Execute Node]  [Deny Node]
         - Run command   - Log denial
               \           /
                 \       /
                   ↓   ↓
                [Log Node]
                - Record audit
                       ↓
                    [End]
```

---

## What Each Node Does

### 1. Parse Node
```python
def parse_node(state):
    intent = parser.parse_intent(state['user_command'])
    return {...state, 'intent': intent}
```
- Parses natural language
- Extracts action & parameters
- Sets confidence score

### 2. Validate Node
```python
def validate_node(state):
    decision = policy_engine.validate_intent(state['intent'])
    return {...state, 'policy_allowed': decision.allowed}
```
- Checks security policy
- Sets allow/block decision
- Records reason

### 3. Router (Conditional)
```python
def route_policy_decision(state):
    if state['policy_allowed']:
        return "execute"
    else:
        return "deny"
```
- Decides which path to take
- Execute if allowed
- Deny if blocked

### 4. Execute Node
```python
def execute_node(state):
    result = executor.execute(state['intent'])
    return {...state, 'execution_result': result}
```
- Only runs if allowed
- Performs the action
- Records result

### 5. Deny Node
```python
def deny_node(state):
    return {...state, 'execution_result': {'success': False}}
```
- Only runs if blocked
- Records denial
- Returns error

### 6. Log Node
```python
def log_node(state):
    logger.log(state)
    return {...state, 'audit_logged': True}
```
- Always runs (both success and denial)
- Records audit trail
- Final step before return

---

## Advantages of LangGraph Version

✅ **Visual Flow** - Graph structure is explicit  
✅ **Easy Debugging** - See each node's execution  
✅ **Easy Modification** - Add/remove nodes easily  
✅ **State Explicit** - All data visible in AirGuardState  
✅ **Production Ready** - Industry-standard patterns  
✅ **Streaming** - Built-in `stream()` for real-time updates  

---

## Testing Different Scenarios

### Scenario 1: Allowed Command

```python
agent = AirGuardAgentLangGraph()
result = agent.process_command("Generate pollution report for Delhi")

# Output:
# 🧠 [PARSE NODE] ✅ Parsed
# 🔒 [VALIDATE NODE] allowed=True
# 🔀 [ROUTER] routing to EXECUTE
# ⚡ [EXECUTE NODE] ✅ Executed
# 📝 [LOG NODE] ✅ Logged
# Result: SUCCESS
```

### Scenario 2: Blocked Command

```python
result = agent.process_command("Shutdown the factory")

# Output:
# 🧠 [PARSE NODE] ✅ Parsed: action=shutdown_factory
# 🔒 [VALIDATE NODE] allowed=False (policy blocks it)
# 🔀 [ROUTER] routing to DENY
# ❌ [DENY NODE] Command blocked
# 📝 [LOG NODE] ✅ Logged denial
# Result: FAILED (blocked by policy)
```

### Scenario 3: Invalid Command

```python
result = agent.process_command("xyzabc nonsense")

# Output:
# 🧠 [PARSE NODE] ✅ Parsed: action=unknown
# 🔒 [VALIDATE NODE] allowed=False (no policy for unknown action)
# 🔀 [ROUTER] routing to DENY
# ❌ [DENY NODE] Unknown action blocked
# 📝 [LOG NODE] ✅ Logged
# Result: FAILED (unknown action)
```

---

## Migration Effort

| Task | Time |
|------|------|
| Install packages | 5 min |
| Copy new agent file | 2 min |
| Update imports in backend | 2 min |
| Test with direct calls | 5 min |
| Test with API | 5 min |
| Test with frontend | 5 min |
| Compare results | 5 min |
| **Total** | **~30 minutes** |

---

## Rollback (If Needed)

If you want to go back to the old agent:

```python
# In backend_api.py
from agent import AirGuardAgent  # Back to original
agent = AirGuardAgent()
```

That's it! Both agents have the same interface.

---

## Next Steps

1. **Test LangGraph version** - Run `python agent_langgraph_complete.py`
2. **Update backend.py** - Change import to LangGraph version
3. **Test end-to-end** - Login and execute command via frontend
4. **Compare results** - Old and new should be identical
5. **Deploy** - Switch to LangGraph in production

---

## Benefits After Migration

✅ **Better for Scaling** - Easier to add complex logic  
✅ **Industry Standard** - Enterprise AI development pattern  
✅ **Easier to Debug** - See each step explicitly  
✅ **Team Ready** - Clear flow for new developers  
✅ **Future Ready** - Add retry logic, parallel processing, etc.  

---

## Common Questions

**Q: Will frontend break?**  
A: No! Same interface, frontend calls same API.

**Q: Will data be lost?**  
A: No! All existing data in SQLite stays the same.

**Q: Can I go back?**  
A: Yes! Just change the import back to old agent.

**Q: Do I need both files?**  
A: For migration, yes. After, keep whichever you prefer.

**Q: Can I mix them?**  
A: Not recommended. Use one or the other.

---

## Summary

You now have:
1. ✅ Original sequential agent (agent.py) - Still works
2. ✅ New LangGraph agent (agent_langgraph_complete.py) - Drop-in replacement
3. ✅ Backend API - Works with both
4. ✅ Frontend - Works with both

**To use LangGraph:**

```bash
# 1. Install
pip install langgraph langchain

# 2. Test new agent
python agent_langgraph_complete.py

# 3. Update backend
# Change: from agent import AirGuardAgent
# To:     from agent_langgraph_complete import AirGuardAgentLangGraph

# 4. Run backend
python backend_api.py

# 5. Test with frontend
# npm start (no changes needed!)
```

**Done!** 🎉 Your AirGuard AI now uses LangGraph!
