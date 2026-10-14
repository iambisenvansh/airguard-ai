# LangGraph Deep Dive - Comprehensive Guide

## Table of Contents

1. [What is LangGraph?](#what-is-langgraph)
2. [Core Concepts Deep](#core-concepts-deep)
3. [State Management](#state-management)
4. [Nodes in Detail](#nodes-in-detail)
5. [Edges in Detail](#edges-in-detail)
6. [Routing Systems](#routing-systems)
7. [Error Handling](#error-handling)
8. [Advanced Patterns](#advanced-patterns)
9. [Performance](#performance)
10. [Best Practices](#best-practices)

---

## What is LangGraph?

### Definition

LangGraph is a **framework for building agentic AI systems** using **directed graphs** and **state management**.

**Core Idea:** Instead of writing linear code:
```python
result = step1(input)
result = step2(result)
result = step3(result)
return result
```

You build a **graph** where:
- Nodes = operations/functions
- Edges = flow between nodes
- State = shared data
- Routing = conditional logic

### Why LangGraph?

**Problem it solves:**
- ❌ Linear workflows can't branch
- ❌ Complex logic becomes nested and hard to read
- ❌ State management is implicit
- ❌ Difficult to add features later

**Solution LangGraph provides:**
- ✅ Explicit branching
- ✅ Clear visual flow
- ✅ Explicit state management
- ✅ Easy feature additions

### Use Cases

**Perfect for:**
1. Multi-step decision making
2. Conditional branching based on results
3. Retry logic and error recovery
4. Parallel processing paths
5. Complex state management
6. Agent systems

**AirGuard Example:**
```
Command → Parse → Validate → [Decision Point]
                                 ├─ Allowed → Execute
                                 └─ Blocked → Deny
                                 ↓
                               Log → Return
```

---

## Core Concepts Deep

### 1. Graph (StateGraph)

A graph is the **blueprint** of your workflow.

```python
from langgraph.graph import StateGraph

graph = StateGraph(YourStateType)
```

**What it does:**
- Defines nodes
- Defines edges (connections)
- Compiles into executable workflow

**Lifecycle:**
```
Create → Add Nodes → Add Edges → Compile → Run
```

### 2. State (TypedDict)

State is the **central data structure** that flows through the graph.

```python
from typing import TypedDict

class MyState(TypedDict):
    user_input: str
    processed: bool
    result: str
    error: str
```

**Properties:**
- ✅ Every node can read from state
- ✅ Every node can modify state
- ✅ Modified state passed to next node
- ✅ Type-safe (enforced by TypedDict)

**Why separate state:**
- Clear data flow
- Testable
- Traceable
- Debuggable

### 3. Nodes

Nodes are **functions** that perform operations.

```python
def my_node(state: MyState) -> MyState:
    # Read from state
    user_input = state["user_input"]
    
    # Do something
    result = process(user_input)
    
    # Update state
    return {
        **state,  # Keep existing data
        "result": result,
        "processed": True
    }
```

**Node requirements:**
- Takes state as input
- Returns modified state
- Can't modify state in-place (functional programming)
- Should be pure (no side effects ideally)

**Node types:**
1. **Regular nodes** - Normal functions
2. **Conditional nodes** - Return routing decision
3. **Sub-graphs** - Nested graphs

### 4. Edges

Edges connect nodes and define flow.

```python
# Simple edge - always connect
graph.add_edge("node1", "node2")

# Conditional edge - decision based on state
graph.add_conditional_edges(
    "node1",
    decide_next,  # Function that returns next node name
    {
        "yes": "node2",
        "no": "node3"
    }
)

# End node
graph.add_edge("final_node", END)
```

**Edge types:**
1. **Simple edge** - Always go to next node
2. **Conditional edge** - Decide based on state
3. **Loop edge** - Can go back to previous node

---

## State Management

### Deep State Concepts

#### State as Single Source of Truth

All data lives in state:

```python
class CommandState(TypedDict):
    # Input
    user_command: str
    user_id: str
    
    # Intermediate results
    parsed_intent: dict
    policy_decision: str
    
    # Output
    execution_result: dict
    
    # Metadata
    errors: list
    execution_time: float
```

#### State Updates

Always use spread operator to create new state:

```python
# ✅ CORRECT - Functional update
def my_node(state):
    return {
        **state,
        "new_field": "value"
    }

# ❌ WRONG - Modifying in place
def my_node(state):
    state["new_field"] = "value"  # Bad!
    return state
```

#### State Validation

TypedDict provides type hints:

```python
class CommandState(TypedDict):
    command: str          # Required
    result: str           # Required
    
class OptionalCommandState(TypedDict, total=False):
    metadata: str         # Optional
    timestamp: str        # Optional
```

#### State Access Patterns

```python
# Read
command = state["user_command"]
if "result" in state:
    result = state["result"]

# Write
new_state = {**state, "processed": True}

# Multiple updates
new_state = {
    **state,
    "field1": value1,
    "field2": value2,
    "field3": value3
}
```

---

## Nodes in Detail

### Node Structure

```python
def node_name(state: StateType) -> StateType:
    """
    Description of what this node does
    
    Args:
        state: The current state
        
    Returns:
        Updated state
    """
    # Extract needed data
    input_data = state["field1"]
    
    # Perform operation
    try:
        result = perform_operation(input_data)
    except Exception as e:
        # Handle error
        return {
            **state,
            "error": str(e),
            "success": False
        }
    
    # Return updated state
    return {
        **state,
        "result": result,
        "success": True
    }
```

### Node Patterns

#### Pattern 1: Data Transformation

```python
def transform_node(state):
    """Transform input into output format"""
    input_data = state["raw_input"]
    transformed = transform(input_data)
    return {**state, "transformed": transformed}
```

#### Pattern 2: Validation

```python
def validate_node(state):
    """Validate data and set flag"""
    data = state["data"]
    is_valid = validate(data)
    return {**state, "is_valid": is_valid}
```

#### Pattern 3: Decision Making

```python
def decide_node(state):
    """Make decision and set result"""
    decision = make_decision(state["inputs"])
    return {**state, "decision": decision}
```

#### Pattern 4: Error Handling

```python
def safe_node(state):
    """Safely perform operation with error handling"""
    try:
        result = risky_operation(state["input"])
        return {**state, "result": result, "error": None}
    except Exception as e:
        return {**state, "result": None, "error": str(e)}
```

#### Pattern 5: Conditional Update

```python
def conditional_update_node(state):
    """Update state based on condition"""
    if state["should_update"]:
        new_value = compute_new_value(state)
    else:
        new_value = state["current_value"]
    
    return {**state, "value": new_value}
```

### Node Ordering

Node names matter for readability:

```python
# Good names (semantic)
graph.add_node("parse", parse_node)
graph.add_node("validate", validate_node)
graph.add_node("execute", execute_node)

# Bad names (unclear)
graph.add_node("step1", step1_func)
graph.add_node("step2", step2_func)
```

---

## Edges in Detail

### Simple Edges

```python
# Sequential flow
graph.add_edge("parse", "validate")
graph.add_edge("validate", "execute")
graph.add_edge("execute", "log")
graph.add_edge("log", END)
```

**Visualization:**
```
[parse] → [validate] → [execute] → [log] → [END]
```

### Conditional Edges

```python
def route_decision(state):
    """Decide which node to go to next"""
    if state["policy_allowed"]:
        return "execute"
    else:
        return "deny"

graph.add_conditional_edges(
    "validate",
    route_decision,
    {
        "execute": "execute",
        "deny": "deny"
    }
)
```

**Visualization:**
```
[validate]
    ├─ policy_allowed=True  → [execute]
    └─ policy_allowed=False → [deny]
```

### Loop Edges

```python
def should_retry(state):
    if state["attempts"] < 3 and not state["success"]:
        return "retry"
    else:
        return "end"

graph.add_conditional_edges(
    "try_operation",
    should_retry,
    {
        "retry": "try_operation",  # Loop back!
        "end": END
    }
)
```

**Visualization:**
```
[try_operation]
    ├─ success=False & attempts<3 → [back to try_operation]
    └─ success=True OR attempts≥3 → [END]
```

### Parallel Edges

Multiple edges from same node:

```python
# Both nodes run after parse (in sequence, not parallel)
graph.add_edge("parse", "validate")
graph.add_edge("parse", "log")  # Also goes here

# Results:
# parse → validate AND parse → log
# (depends on graph structure)
```

---

## Routing Systems

### Simple Routing

```python
def route_simple(state):
    if state["flag"]:
        return "path_a"
    else:
        return "path_b"
```

### Complex Routing

```python
def route_complex(state):
    if state["priority"] == "high":
        return "urgent_path"
    elif state["priority"] == "normal":
        return "normal_path"
    elif state["retry_count"] < 3:
        return "retry_path"
    else:
        return "error_path"
```

### Dynamic Routing

```python
def route_dynamic(state):
    # Determine path based on input data
    data_type = type(state["data"]).__name__
    routing_map = {
        "str": "text_handler",
        "dict": "json_handler",
        "list": "array_handler"
    }
    return routing_map.get(data_type, "default_handler")
```

---

## Error Handling

### Try-Catch in Nodes

```python
def safe_node(state):
    try:
        result = operation(state["input"])
        return {**state, "result": result, "error": None}
    except ValueError as e:
        return {**state, "result": None, "error": f"Value error: {e}"}
    except Exception as e:
        return {**state, "result": None, "error": f"Unknown error: {e}"}
```

### Error Routing

```python
def route_error(state):
    if state["error"]:
        return "error_handler"
    else:
        return "next_step"

graph.add_node("error_handler", error_handler_node)
graph.add_conditional_edges("operation_node", route_error, {
    "error_handler": "error_handler",
    "next_step": "next_step"
})
```

### Error Recovery

```python
def recovery_node(state):
    """Attempt to recover from error"""
    error = state["error"]
    
    if "timeout" in error:
        # Retry with longer timeout
        return {**state, "retry_timeout": 60}
    elif "connection" in error:
        # Try different server
        return {**state, "server": "backup"}
    else:
        # Give up
        return {**state, "recovery_attempted": False}
```

---

## Advanced Patterns

### Pattern 1: Validation Pipeline

```
[Input] → [Validate Schema] → [Validate Logic] → [Process] → [Output]
           ├─ Failed → [Error Handler]
           └─ Passed → Continue
```

### Pattern 2: Multi-Step Decision

```
[Input] 
  → [Check A] → Yes/No?
       ├─ Yes → [Check B] → Yes/No?
       │        ├─ Yes → [Action XY]
       │        └─ No → [Action X]
       └─ No → [Action Y]
```

### Pattern 3: Retry with Backoff

```
[Attempt]
    ├─ Success → [Done]
    └─ Fail
       ├─ Attempt 1: Retry (0 delay)
       ├─ Attempt 2: Retry (1s delay)
       ├─ Attempt 3: Retry (2s delay)
       └─ Attempt 4: Error → [End]
```

### Pattern 4: Fan-Out / Fan-In

```
[Start]
    ↓
[Process Parallel]
    ├─ [Worker 1]
    ├─ [Worker 2]
    └─ [Worker 3]
    ↓
[Combine Results]
    ↓
[End]
```

### Pattern 5: Sub-Graphs

```
[Main Graph]
    ├─ [Regular Node]
    ├─ [Sub-Graph 1]
    │   ├─ [Sub-Node A]
    │   └─ [Sub-Node B]
    └─ [Regular Node]
```

---

## Performance

### Optimization Tips

#### 1. Node Efficiency

```python
# ❌ Slow - Duplicate work
def slow_node(state):
    data = state["data"]
    processed = heavy_processing(data)  # Every time!
    return {**state, "result": processed}

# ✅ Fast - Cache results
def fast_node(state):
    if state.get("cached_result"):
        return state  # Use cache
    
    data = state["data"]
    processed = heavy_processing(data)
    return {**state, "result": processed, "cached_result": True}
```

#### 2. State Size

```python
# ❌ Large state - Slow passing
state = {
    "large_data": [1]*1000000,
    "result": None
}

# ✅ Compact state - Fast passing
state = {
    "large_data_ref": "reference_to_large_data",
    "result": None
}
```

#### 3. Conditional vs Sequential

```python
# ❌ Sequential - Always runs
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", "node_c")

# ✅ Conditional - Skips unnecessary nodes
def route(state):
    if state["skip_b"]:
        return "node_c"
    else:
        return "node_b"
```

---

## Best Practices

### 1. Clear Naming

```python
# ✅ Good
graph.add_node("parse_input", parse_input_node)
graph.add_node("validate_schema", validate_schema_node)

# ❌ Bad
graph.add_node("step1", func1)
graph.add_node("step2", func2)
```

### 2. Single Responsibility

```python
# ✅ Each node does one thing
def parse_node(state):
    return {**state, "parsed": parse(state["input"])}

def validate_node(state):
    return {**state, "valid": validate(state["parsed"])}

# ❌ Node does too much
def do_everything_node(state):
    parsed = parse(state["input"])
    valid = validate(parsed)
    executed = execute(parsed)
    logged = log(executed)
    return {**state, "result": logged}
```

### 3. Error Handling

```python
# ✅ Handle errors gracefully
def safe_node(state):
    try:
        result = operation(state["data"])
        return {**state, "result": result, "error": None}
    except Exception as e:
        return {**state, "result": None, "error": str(e)}

# ❌ No error handling
def unsafe_node(state):
    result = operation(state["data"])  # Could crash!
    return {**state, "result": result}
```

### 4. State Documentation

```python
# ✅ Document state structure
class ProcessState(TypedDict):
    """State flowing through the processing graph
    
    user_input: str - The raw user input
    parsed: dict - Parsed intent from input
    validated: bool - Whether parsed intent is valid
    result: dict - Final processing result
    error: str - Error message if any
    """
    user_input: str
    parsed: dict
    validated: bool
    result: dict
    error: str
```

### 5. Routing Logic

```python
# ✅ Clear routing
def route_decision(state):
    """Route based on validation result"""
    if state["validated"]:
        return "process"
    else:
        return "error"

# ❌ Unclear routing
def route(state):
    return "a" if state["x"] else "b"  # What does this mean?
```

---

## Summary: LangGraph Depth

| Concept | Key Points |
|---------|-----------|
| **Graph** | Blueprint of workflow, StateGraph creates executable |
| **State** | Central data structure, TypedDict enforces types |
| **Nodes** | Functions, must be pure, return updated state |
| **Edges** | Connections, can be simple or conditional |
| **Routing** | Logic to decide which node runs next |
| **Errors** | Handle in nodes, route to error handlers |
| **Performance** | Cache results, minimize state size, use conditionals |
| **Best Practices** | Clear names, single responsibility, good error handling |

---

## Next: Real Implementation

Now you understand LangGraph deeply. Next step: implement in your AirGuard AI!

See `LANGGRAPH_MIGRATION_STEPS.md` for complete implementation guide.
