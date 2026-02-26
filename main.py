"""
AirGuard AI - Main Demo Script

This script demonstrates the complete AirGuard AI pollution monitoring system
for the hackathon judges. It shows:
1. Allowed actions (generate report, analyze AQI, send alert)
2. Blocked actions (shutdown factory, issue fine)
3. OpenClaw integration
4. Policy enforcement
5. Audit logging
"""

from agent import AirGuardAgent
import json


def print_separator():
    """Print a visual separator."""
    print("\n" + "="*80 + "\n")


def print_result(result):
    """Print formatted result."""
    if result["success"]:
        print(f"✅ SUCCESS: {result['message']}")
        if result.get("data"):
            print(f"📊 Data: {json.dumps(result['data'], indent=2)}")
        if result.get("files_created"):
            print(f"📄 Files Created: {result['files_created']}")
    else:
        print(f"❌ FAILED: {result['message']}")
        if result.get("data"):
            print(f"📊 Data: {json.dumps(result['data'], indent=2)}")


def main():
    """Run the AirGuard AI demo."""
    
    print("="*80)
    print("🌍 AIRGUARD AI - AUTONOMOUS POLLUTION MONITORING SYSTEM")
    print("="*80)
    print("\nDemo for Hackathon Judges")
    print("Showing: Intent Parsing, Policy Enforcement, OpenClaw Integration, Audit Logging")
    print_separator()
    
    # Initialize the agent
    agent = AirGuardAgent()
    
    print_separator()
    print("📋 ALLOWED ACTIONS (from policy):")
    print(agent.get_allowed_actions())
    
    # ========================================================================
    # DEMO 1: ALLOWED ACTION - Generate Report
    # ========================================================================
    print_separator()
    print("🟢 DEMO 1: ALLOWED ACTION - Generate Pollution Report")
    print("-" * 80)
    
    result1 = agent.process_command("Generate pollution report for Delhi")
    print_result(result1)
    
    # ========================================================================
    # DEMO 2: ALLOWED ACTION - Analyze AQI
    # ========================================================================
    print_separator()
    print("🟢 DEMO 2: ALLOWED ACTION - Analyze AQI Data")
    print("-" * 80)
    
    result2 = agent.process_command("Analyze AQI in Delhi")
    print_result(result2)
    
    # ========================================================================
    # DEMO 3: ALLOWED ACTION - Send Alert
    # ========================================================================
    print_separator()
    print("🟢 DEMO 3: ALLOWED ACTION - Send Pollution Alert")
    print("-" * 80)
    
    result3 = agent.process_command("Send critical alert about high pollution levels in Delhi")
    print_result(result3)
    
    # ========================================================================
    # DEMO 4: BLOCKED ACTION - Shutdown Factory
    # ========================================================================
    print_separator()
    print("🔴 DEMO 4: BLOCKED ACTION - Shutdown Factory")
    print("-" * 80)
    print("⚠️  This action should be BLOCKED by policy enforcement!")
    
    result4 = agent.process_command("Shutdown factory in Mayapuri")
    print_result(result4)
    
    # ========================================================================
    # DEMO 5: BLOCKED ACTION - Issue Fine
    # ========================================================================
    print_separator()
    print("🔴 DEMO 5: BLOCKED ACTION - Issue Fine")
    print("-" * 80)
    print("⚠️  This action should be BLOCKED by policy enforcement!")
    
    result5 = agent.process_command("Issue fine to polluting factory")
    print_result(result5)
    
    # ========================================================================
    # SYSTEM STATUS
    # ========================================================================
    print_separator()
    print("📊 SYSTEM STATUS & STATISTICS")
    print("-" * 80)
    
    status = agent.get_system_status()
    print(f"Total Actions Processed: {status['total_actions']}")
    print(f"✅ Successful Actions: {status['successful_actions']}")
    print(f"❌ Blocked Actions: {status['blocked_actions']}")
    print(f"⚠️  Errors: {status['errors']}")
    
    # ========================================================================
    # AUDIT LOG SAMPLE
    # ========================================================================
    print_separator()
    print("📝 AUDIT LOG SAMPLE (Last 3 entries)")
    print("-" * 80)
    
    logs = agent.logger.get_logs()
    for log in logs[-3:]:
        print(f"\nTimestamp: {log.get('timestamp')}")
        print(f"Action: {log.get('intent', {}).get('action')}")
        print(f"Status: {log.get('status')}")
        print(f"Command: {log.get('intent', {}).get('user_command')}")
    
    print_separator()
    print("✅ DEMO COMPLETE!")
    print("\nKey Features Demonstrated:")
    print("  ✓ Natural language intent parsing")
    print("  ✓ Policy-based security enforcement")
    print("  ✓ OpenClaw integration for file operations")
    print("  ✓ Blocked dangerous actions (shutdown, fines)")
    print("  ✓ Comprehensive audit logging")
    print("  ✓ Real-time pollution data analysis")
    print_separator()


if __name__ == "__main__":
    main()
