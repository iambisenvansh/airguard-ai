# 🏗️ AirGuard AI - Detailed Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE LAYER                               │
│                                                                              │
│  User Command: "Generate pollution report for Delhi"                        │
│  User Command: "Shutdown factory in Mayapuri"                               │
│  User Command: "Analyze AQI in Delhi"                                       │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AGENT ORCHESTRATION LAYER                              │
│                          (agent.py)                                         │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ AirGuardAgent                                                        │  │
│  │ - Coordinates all system components                                  │  │
│  │ - Routes commands through the pipeline                              │  │
│  │ - Manages component lifecycle                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
        ┌─────────────────────┐   ┌─────────────────────┐
        │  INTENT PARSER      │   │  POLICY ENGINE      │
        │  (intent.py)        │   │  (policy.py)        │
        │                     │   │                     │
        │ Converts natural    │   │ Validates against   │
        │ language to         │   │ security rules      │
        │ structured intents  │   │                     │
        │                     │   │ Reads policy.json   │
        │ Input:              │   │                     │
        │ "Generate report"   │   │ Output:             │
        │                     │   │ PolicyDecision      │
        │ Output:             │   │ (allowed/blocked)   │
        │ Intent object       │   │                     │
        └──────────┬──────────┘   └──────────┬──────────┘
                   │                         │
                   └────────────┬────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SECURITY ENFORCEMENT LAYER                               │
│                      (enforce.py) ⭐ CRITICAL                               │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Enforcer                                                             │  │
│  │                                                                      │  │
│  │ CRITICAL SECURITY GATEWAY:                                          │  │
│  │                                                                      │  │
│  │ 1. Receives Intent + PolicyDecision                                 │  │
│  │ 2. Checks: if NOT policy_decision.allowed:                          │  │
│  │    ├─ BLOCK action                                                  │  │
│  │    ├─ Log denial                                                    │  │
│  │    └─ Return error                                                  │  │
│  │ 3. If allowed:                                                      │  │
│  │    ├─ Execute action                                                │  │
│  │    ├─ Log success                                                   │  │
│  │    └─ Return result                                                 │  │
│  │                                                                      │  │
│  │ NO CODE PATH BYPASSES THIS CHECK!                                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Decision Point:                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ if not policy_decision.allowed:                                     │   │
│  │     return BLOCKED_RESULT                                           │   │
│  │ else:                                                               │   │
│  │     proceed to EXECUTOR                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
            ❌ BLOCKED                   ✅ ALLOWED
                    │                         │
                    ▼                         ▼
        ┌─────────────────────┐   ┌─────────────────────┐
        │  DENIAL RESULT      │   │  EXECUTOR LAYER     │
        │                     │   │  (executor.py)      │
        │ - Action blocked    │   │                     │
        │ - Reason logged     │   │ Routes to handlers: │
        │ - Audit entry       │   │                     │
        │                     │   │ ├─ generate_report()│
        │ Examples:           │   │ ├─ analyze_aqi()    │
        │ ❌ Shutdown factory │   │ └─ send_alert()     │
        │ ❌ Issue fine       │   │                     │
        └─────────────────────┘   │ Each handler:       │
                                  │ - Reads data        │
                                  │ - Processes         │
                                  │ - Returns result    │
                                  └──────────┬──────────┘
                                             │
                                             ▼
                        ┌────────────────────────────────────┐
                        │  OPENCLAW INTEGRATION LAYER        │
                        │  (executor.py - OpenClaw calls)    │
                        │                                    │
                        │  from openclaw import Computer     │
                        │  pc = Computer()                   │
                        │                                    │
                        │  Operations:                       │
                        │  ├─ pc.read_file()                 │
                        │  ├─ pc.write_file()                │
                        │  └─ pc.open_file()                 │
                        │                                    │
                        │  File Operations:                  │
                        │  ├─ Read: data/*.json              │
                        │  ├─ Write: output/*.txt            │
                        │  └─ Manage: reports/               │
                        └────────────────────────────────────┘
                                             │
                                             ▼
                        ┌────────────────────────────────────┐
                        │  DATA LAYER                        │
                        │                                    │
                        │  Input Data:                       │
                        │  ├─ data/delhi_pollution.json      │
                        │  ├─ data/mumbai_pollution.json     │
                        │  └─ data/mumbai_pollution.csv      │
                        │                                    │
                        │  Output Data:                      │
                        │  ├─ output/reports/                │
                        │  └─ output/analysis/               │
                        └────────────────────────────────────┘
                                             │
                                             ▼
                        ┌────────────────────────────────────┐
                        │  AUDIT LOGGING LAYER               │
                        │  (logger.py)                       │
                        │                                    │
                        │  Logs ALL actions:                 │
                        │  ├─ Timestamp                      │
                        │  ├─ User command                   │
                        │  ├─ Intent parsed                  │
                        │  ├─ Policy decision                │
                        │  ├─ Execution result               │
                        │  └─ Status (SUCCESS/BLOCKED/ERROR) │
                        │                                    │
                        │  Output: logs/audit.log (JSON)     │
                        └────────────────────────────────────┘
```

---

## Detailed Component Interactions

### 1. **Intent Parser (intent.py)**
```
Input: Natural Language Command
  ↓
Pattern Matching Engine
  ├─ Detects action keywords
  ├─ Extracts parameters
  └─ Calculates confidence score
  ↓
Output: Intent Object
  {
    action: "generate_report",
    parameters: {"location": "Delhi"},
    confidence: 0.95,
    timestamp: "2024-01-15T10:30:45",
    user_command: "Generate pollution report for Delhi"
  }
```

### 2. **Policy Engine (policy.py)**
```
Input: Intent Object
  ↓
Load policy.json Rules
  ├─ Check if action exists in rules
  ├─ Verify constraints
  └─ Apply default policy (DENY)
  ↓
Output: PolicyDecision Object
  {
    allowed: true/false,
    reason: "Report generation is read-only",
    rule_name: "generate_report",
    constraints: {...}
  }
```

### 3. **Enforcer (enforce.py) - CRITICAL SECURITY GATEWAY**
```
Input: Intent + PolicyDecision
  ↓
CRITICAL CHECK:
  if not policy_decision.allowed:
    ├─ Create denial result
    ├─ Log blocked attempt
    └─ Return error (NO EXECUTION)
  else:
    ├─ Call executor.execute()
    ├─ Log success
    └─ Return result
  ↓
Output: ExecutionResult or DenialResult
```

### 4. **Executor (executor.py)**
```
Input: Approved Intent
  ↓
Route by Action Type:
  ├─ generate_report
  │  ├─ Read pollution data (OpenClaw)
  │  ├─ Analyze data
  │  └─ Write report (OpenClaw)
  │
  ├─ analyze_aqi
  │  ├─ Read data (OpenClaw)
  │  ├─ Calculate statistics
  │  └─ Return analysis
  │
  └─ send_alert
     ├─ Format alert message
     ├─ Log alert
     └─ Return confirmation
  ↓
Output: ExecutionResult
  {
    success: true,
    message: "Report generated",
    data: {...},
    execution_time: 0.234,
    files_created: ["output/report.txt"]
  }
```

### 5. **Audit Logger (logger.py)**
```
Input: Intent + PolicyDecision + Result + Status
  ↓
Create Log Entry:
  {
    timestamp: "2024-01-15T10:30:45.123456",
    intent: {...},
    policy_decision: {...},
    result: {...},
    status: "SUCCESS" | "BLOCKED" | "ERROR"
  }
  ↓
Append to logs/audit.log (JSON format)
  ↓
Output: Audit Trail for Compliance
```

---

## Data Flow Diagram

```
┌──────────────────┐
│  User Command    │
│  "Generate       │
│   report for     │
│   Delhi"         │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ AGENT.PROCESS_COMMAND()                                      │
│                                                              │
│ 1. parser.parse_intent(command)                              │
│    └─> Intent(action="generate_report", ...)                │
│                                                              │
│ 2. enforcer.enforce_and_execute(intent)                      │
│    ├─> policy_engine.validate_intent(intent)                │
│    │   └─> PolicyDecision(allowed=true, ...)                │
│    │                                                         │
│    ├─> if not allowed: BLOCK & LOG                          │
│    │                                                         │
│    └─> else: executor.execute(intent)                       │
│        ├─> Read data via OpenClaw                           │
│        ├─> Process data                                     │
│        ├─> Write output via OpenClaw                        │
│        └─> ExecutionResult(success=true, ...)               │
│                                                              │
│ 3. logger.log_action(...)                                    │
│    └─> Append to audit.log                                  │
│                                                              │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────┐
│  Return Result   │
│  {               │
│   success: true, │
│   message: "...",│
│   data: {...}    │
│  }               │
└──────────────────┘
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                              │
└─────────────────────────────────────────────────────────────────┘

Layer 1: POLICY DEFINITION (policy.json)
┌─────────────────────────────────────────────────────────────────┐
│ Allowed Actions:                                                │
│ ✅ generate_report (read-only)                                  │
│ ✅ analyze_aqi (read-only)                                      │
│ ✅ send_alert (public safety)                                   │
│                                                                 │
│ Blocked Actions:                                                │
│ ❌ shutdown_factory (requires human authorization)              │
│ ❌ issue_fine (requires legal review)                           │
│                                                                 │
│ Default Policy: DENY (fail-safe)                                │
└─────────────────────────────────────────────────────────────────┘
                            ▼
Layer 2: POLICY VALIDATION (policy.py)
┌─────────────────────────────────────────────────────────────────┐
│ Validates every intent against policy rules                     │
│ Returns PolicyDecision(allowed=true/false)                      │
└─────────────────────────────────────────────────────────────────┘
                            ▼
Layer 3: ENFORCEMENT (enforce.py) ⭐ CRITICAL
┌─────────────────────────────────────────────────────────────────┐
│ CRITICAL CHECK:                                                 │
│                                                                 │
│ if not policy_decision.allowed:                                 │
│     BLOCK ACTION                                                │
│     LOG DENIAL                                                  │
│     RETURN ERROR                                                │
│                                                                 │
│ NO CODE PATH BYPASSES THIS CHECK!                               │
│ NO EXCEPTIONS!                                                  │
│ NO BACKDOORS!                                                   │
└─────────────────────────────────────────────────────────────────┘
                            ▼
Layer 4: EXECUTION (executor.py)
┌─────────────────────────────────────────────────────────────────┐
│ Only executes if all security layers approve                    │
│ Uses OpenClaw for safe file operations                          │
│ Tracks execution time and files created                         │
└─────────────────────────────────────────────────────────────────┘
                            ▼
Layer 5: AUDIT LOGGING (logger.py)
┌─────────────────────────────────────────────────────────────────┐
│ Logs ALL actions (allowed, blocked, errors)                     │
│ Maintains audit trail for compliance                            │
│ JSON format for easy analysis                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Structure & Responsibilities

```
airguard-ai/
│
├── agent.py ⭐ MAIN ENTRY POINT
│   └─ AirGuardAgent class
│      ├─ Orchestrates all components
│      ├─ process_command() - main method
│      └─ get_system_status() - statistics
│
├── intent.py
│   └─ IntentParser class
│      ├─ parse_intent() - NLP processing
│      └─ Pattern matching engine
│
├── policy.py
│   └─ PolicyEngine class
│      ├─ validate_intent() - policy check
│      ├─ get_allowed_actions()
│      └─ Loads policy.json
│
├── enforce.py ⭐ CRITICAL SECURITY
│   └─ Enforcer class
│      ├─ enforce_and_execute() - CRITICAL METHOD
│      ├─ Policy validation check
│      └─ Blocks unauthorized actions
│
├── executor.py
│   └─ Executor class
│      ├─ execute() - routes to handlers
│      ├─ generate_report()
│      ├─ analyze_aqi()
│      ├─ send_alert()
│      └─ OpenClaw integration (self.pc = Computer())
│
├── logger.py
│   └─ AuditLogger class
│      ├─ log_action() - logs all actions
│      ├─ get_logs() - retrieves logs
│      └─ JSON format audit trail
│
├── models.py
│   ├─ Intent class
│   ├─ PolicyDecision class
│   ├─ ExecutionResult class
│   └─ Data structures
│
├── policy.json ⭐ SECURITY RULES
│   ├─ Allowed actions
│   ├─ Blocked actions
│   ├─ Constraints
│   ├─ Rate limiting
│   └─ File operation rules
│
├── main.py
│   └─ Demo script
│      ├─ Shows allowed actions
│      ├─ Shows blocked actions
│      └─ Displays audit logs
│
├── data/
│   ├─ delhi_pollution.json
│   ├─ mumbai_pollution.json
│   └─ mumbai_pollution.csv
│
├── logs/
│   └─ audit.log (JSON audit trail)
│
└── output/
    └─ Generated reports
```

---

## Request-Response Flow Example

### Example 1: ALLOWED ACTION ✅

```
User: "Generate pollution report for Delhi"
  │
  ├─> agent.process_command()
  │
  ├─> intent_parser.parse_intent()
  │   └─> Intent(action="generate_report", parameters={"location": "Delhi"})
  │
  ├─> enforcer.enforce_and_execute()
  │   │
  │   ├─> policy_engine.validate_intent()
  │   │   └─> PolicyDecision(allowed=true, reason="read-only operation")
  │   │
  │   ├─> Check: if not allowed? NO, so proceed
  │   │
  │   ├─> executor.execute()
  │   │   ├─> Read data/delhi_pollution.json (OpenClaw)
  │   │   ├─> Analyze AQI data
  │   │   ├─> Write output/report.txt (OpenClaw)
  │   │   └─> ExecutionResult(success=true, files_created=[...])
  │   │
  │   └─> logger.log_action(status="SUCCESS")
  │
  └─> Return: {success: true, message: "Report generated", data: {...}}

Result: ✅ Report generated successfully
```

### Example 2: BLOCKED ACTION ❌

```
User: "Shutdown factory in Mayapuri"
  │
  ├─> agent.process_command()
  │
  ├─> intent_parser.parse_intent()
  │   └─> Intent(action="shutdown_factory", parameters={"location": "Mayapuri"})
  │
  ├─> enforcer.enforce_and_execute()
  │   │
  │   ├─> policy_engine.validate_intent()
  │   │   └─> PolicyDecision(allowed=false, reason="requires human authorization")
  │   │
  │   ├─> Check: if not allowed? YES, so BLOCK
  │   │
  │   ├─> Create DenialResult
  │   │
  │   └─> logger.log_action(status="BLOCKED")
  │
  └─> Return: {success: false, message: "❌ BLOCKED: requires human authorization"}

Result: ❌ Action blocked by policy enforcement
```

---

## Key Security Features

### 1. **Fail-Safe Design**
- Default policy: DENY
- Unknown actions are blocked by default
- No action executes without explicit approval

### 2. **No Bypass Paths**
- Executor can only be called through Enforcer
- Enforcer always checks policy first
- No code path skips security checks

### 3. **Comprehensive Logging**
- Every action logged (allowed, blocked, errors)
- Includes timestamp, command, intent, decision, result
- JSON format for easy analysis

### 4. **Constraint Validation**
- File size limits
- Rate limiting
- Directory restrictions
- File type restrictions

### 5. **OpenClaw Integration**
- All file operations through OpenClaw
- Secure file handling
- Sandboxed operations

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ENVIRONMENT                   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Python Runtime (3.9+)                               │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │ AirGuard AI Application                        │ │  │
│  │  │                                                │ │  │
│  │  │ ├─ agent.py                                   │ │  │
│  │  │ ├─ intent.py                                  │ │  │
│  │  │ ├─ policy.py                                  │ │  │
│  │  │ ├─ enforce.py                                 │ │  │
│  │  │ ├─ executor.py                                │ │  │
│  │  │ ├─ logger.py                                  │ │  │
│  │  │ └─ models.py                                  │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │ Dependencies                                   │ │  │
│  │  │ ├─ openclaw (AI agent framework)              │ │  │
│  │  │ └─ Standard library (json, time, datetime)    │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │ Data & Configuration                          │ │  │
│  │  │ ├─ policy.json (security rules)               │ │  │
│  │  │ ├─ data/ (pollution data)                     │ │  │
│  │  │ ├─ logs/ (audit trail)                        │ │  │
│  │  │ └─ output/ (generated reports)                │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Summary

**AirGuard AI** is a secure AI agent system with:

1. **Multi-layer Architecture**: Intent → Policy → Enforcement → Execution → Logging
2. **Security-First Design**: Policy validation before any action
3. **Critical Enforcement Layer**: Blocks dangerous operations
4. **OpenClaw Integration**: Safe file operations
5. **Comprehensive Audit Trail**: Every action logged
6. **Fail-Safe Defaults**: DENY by default
7. **Real-World Application**: Pollution monitoring for Delhi

The key innovation is the **Enforcer** layer that acts as an impenetrable security gateway, ensuring no dangerous action can execute without explicit policy approval.
