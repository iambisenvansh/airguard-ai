# 🌍 AirGuard AI - Autonomous Pollution Monitoring System

**An AI-powered agent for pollution monitoring in Delhi with secure policy enforcement and OpenClaw integration.**

---

## 📋 Overview

AirGuard AI is an autonomous AI agent system that monitors air pollution in Delhi. It converts natural language commands into structured actions, validates them against security policies, and executes approved operations while blocking dangerous actions like factory shutdowns or fine issuance.

### Key Features

✅ **Natural Language Processing** - Converts commands like "Generate pollution report" into structured intents  
✅ **Policy-Based Security** - Enforces strict security rules to prevent unauthorized actions  
✅ **OpenClaw Integration** - Uses OpenClaw for secure file operations and system interactions  
✅ **Audit Logging** - Maintains comprehensive logs of all actions for compliance  
✅ **Real-Time Analysis** - Analyzes AQI data with statistical calculations  
✅ **Blocked Actions** - Prevents dangerous operations (factory shutdown, fine issuance)

---

## 🏗️ Architecture

```
User Command → Intent Parser → Policy Engine → Enforcer → Executor (OpenClaw) → Result
                                                    ↓
                                              Audit Logger
```

### Components

1. **agent.py** - Main controller orchestrating the entire system
2. **intent.py** - Parses natural language into structured intents
3. **policy.json** - Security policy rules (allow/block actions)
4. **policy.py** - Policy engine that validates intents
5. **enforce.py** - **CRITICAL** - Security enforcement layer
6. **executor.py** - Executes actions using OpenClaw
7. **logger.py** - Audit logging for all actions
8. **models.py** - Core data structures (Intent, PolicyDecision, ExecutionResult)

---

## 📁 Project Structure

```
airguard-ai/
├── agent.py              # Main controller
├── intent.py             # Intent parser
├── policy.json           # Security policy rules
├── policy.py             # Policy engine
├── enforce.py            # Enforcement layer (CRITICAL!)
├── executor.py           # Executor with OpenClaw
├── logger.py             # Audit logger
├── models.py             # Data models
├── main.py               # Demo script
├── data/                 # Pollution data files
│   ├── delhi_pollution.json
│   └── mumbai_pollution.json
├── logs/                 # Audit logs
└── output/               # Generated reports
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup

1. **Install OpenClaw:**
   ```bash
   pip install openclaw
   ```

2. **Navigate to project directory:**
   ```bash
   cd airguard-ai
   ```

3. **Verify structure:**
   ```bash
   ls -la
   # Should see: agent.py, intent.py, policy.json, enforce.py, executor.py, etc.
   ```

---

## 🎮 Usage

### Run the Demo

```bash
python main.py
```

This will demonstrate:
- ✅ Allowed actions (generate report, analyze AQI, send alert)
- ❌ Blocked actions (shutdown factory, issue fine)
- 📊 System statistics and audit logs

### Example Commands

**Allowed Actions:**
```python
from agent import AirGuardAgent

agent = AirGuardAgent()

# Generate pollution report
result = agent.process_command("Generate pollution report for Delhi")

# Analyze AQI data
result = agent.process_command("Analyze AQI in Delhi")

# Send alert
result = agent.process_command("Send critical alert about high pollution")
```

**Blocked Actions:**
```python
# These will be BLOCKED by policy enforcement
result = agent.process_command("Shutdown factory in Mayapuri")
# ❌ BLOCKED: Critical infrastructure control requires human authorization

result = agent.process_command("Issue fine to polluting factory")
# ❌ BLOCKED: Financial penalties require legal review and human authorization
```

---

## 🔒 Security Model

### Policy Rules (policy.json)

**Allowed Actions:**
- `generate_report` - Read-only operation
- `analyze_aqi` - Data analysis operation
- `send_alert` - Public safety notification

**Blocked Actions:**
- `shutdown_factory` - Requires human authorization
- `issue_fine` - Requires legal review

**Default Policy:** DENY (fail-safe)

### Enforcement Layer (enforce.py)

The enforcement layer is the **critical security gateway**:

```python
# CRITICAL CHECK - Judges will review this!
if not policy_decision.allowed:
    # Block the action
    return denial_result
```

---

## 🔧 OpenClaw Integration

OpenClaw is used for all file and system operations:

```python
from openclaw import Computer

pc = Computer()

# Read pollution data files
data = pc.read_file("data/delhi_pollution.json")

# Write report files
pc.write_file("output/report.txt", content)

# Open generated reports
pc.open_file("output/report.txt")
```

---

## 📊 Sample Output

```
🌍 AIRGUARD AI - AUTONOMOUS POLLUTION MONITORING SYSTEM
================================================================================

🟢 DEMO 1: ALLOWED ACTION - Generate Pollution Report
💬 User Command: "Generate pollution report for Delhi"
🧠 Parsed Intent: generate_report (confidence: 0.95)
✅ SUCCESS: Report generated successfully
📄 Files Created: ['output/delhi_report_2024-01-15.txt']

🔴 DEMO 4: BLOCKED ACTION - Shutdown Factory
💬 User Command: "Shutdown factory in Mayapuri"
🧠 Parsed Intent: shutdown_factory (confidence: 0.95)
❌ BLOCKED: Critical infrastructure control requires human authorization
```

---

## 📝 Audit Logs

All actions are logged to `logs/audit.log` in JSON format:

```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "intent": {
    "action": "shutdown_factory",
    "user_command": "Shutdown factory in Mayapuri"
  },
  "policy_decision": {
    "allowed": false,
    "reason": "Critical infrastructure control requires human authorization"
  },
  "status": "BLOCKED"
}
```

---

## 🎯 For Hackathon Judges

### What to Check

1. **enforce.py** - Security enforcement layer with policy validation
2. **policy.json** - Clear allow/block rules
3. **executor.py** - OpenClaw integration (`from openclaw import Computer`)
4. **main.py** - Run the demo to see blocked actions
5. **logs/** - Audit trail of all actions

### Run the Demo

```bash
python main.py
```

You'll see:
- ✅ 3 allowed actions executing successfully
- ❌ 2 blocked actions with clear denial messages
- 📊 System statistics
- 📝 Audit log samples

---

## 🛠️ Customization

### Modify Policy Rules

Edit `policy.json` to add/remove allowed actions:

```json
{
  "action": "new_action",
  "allowed": true,
  "reason": "Description of why this is allowed",
  "constraints": {
    "max_file_size_mb": 10
  }
}
```

### Add New Actions

1. Add pattern to `intent.py`
2. Add rule to `policy.json`
3. Add handler to `executor.py`

---

## 📞 Support

For questions or issues, contact the AirGuard AI team.

---

## 📄 License

This project is created for hackathon demonstration purposes.

---

**Built with ❤️ for cleaner air in Delhi**
