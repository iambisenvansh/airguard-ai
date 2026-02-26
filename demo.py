"""
AirGuard AI - Professional Demo Script
Beautiful formatted output for hackathon presentation
"""

from agent import AirGuardAgent
import json


def print_header():
    """Print main header."""
    print("\n" + "="*80)
    print("🌍 AIRGUARD AI - AUTONOMOUS POLLUTION MONITORING SYSTEM")
    print("="*80)
    print("Demo for Hackathon Judges | Delhi Pollution Monitoring")
    print("="*80 + "\n")


def print_section(title, emoji="📋"):
    """Print section header."""
    print("\n" + "-"*80)
    print(f"{emoji} {title}")
    print("-"*80)


def print_command_info(command, action, success):
    """Print command execution info."""
    status = "✅ SUCCESS" if success else "❌ FAILED"
    print(f"\nCommand: \"{command}\"")
    print(f"Action: {action}")
    print(f"Status: {status}")


def print_data_formatted(data, indent=0):
    """Print data in a beautiful formatted way."""
    indent_str = "  " * indent
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{indent_str}{key}:")
                print_data_formatted(value, indent + 1)
            elif isinstance(value, list):
                print(f"{indent_str}{key}: {value}")
            else:
                print(f"{indent_str}{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            print(f"{indent_str}• {item}")
    else:
        print(f"{indent_str}{data}")


def run_demo():
    """Run the complete demo."""
    
    print_header()
    
    # Initialize agent
    print("🚀 Initializing AirGuard AI Agent...")
    agent = AirGuardAgent()
    print("✅ Agent initialized successfully!\n")
    
    # Show allowed actions
    print_section("ALLOWED ACTIONS (from policy.json)", "🔓")
    allowed = agent.get_allowed_actions()
    for action in allowed:
        print(f"  ✓ {action}")

    
    # ========================================================================
    # DEMO 1: Generate Report
    # ========================================================================
    print_section("DEMO 1: Generate Pollution Report", "📊")
    
    command1 = "Generate pollution report for Delhi"
    result1 = agent.process_command(command1)
    
    print_command_info(command1, "generate_report", result1["success"])
    print(f"Message: {result1['message']}")
    
    if result1.get("data"):
        print("\nData:")
        print_data_formatted(result1["data"])
    
    if result1.get("files_created"):
        print(f"\n📄 Files Created: {result1['files_created']}")
    
    if result1.get("execution_time"):
        print(f"⏱️  Execution Time: {result1['execution_time']:.3f} seconds")
    
    # ========================================================================
    # DEMO 2: Analyze AQI
    # ========================================================================
    print_section("DEMO 2: Analyze AQI Data", "🔬")
    
    command2 = "Analyze AQI in Delhi"
    result2 = agent.process_command(command2)
    
    print_command_info(command2, "analyze_aqi", result2["success"])
    print(f"Message: {result2['message']}")
    
    if result2.get("data"):
        print("\nData:")
        print_data_formatted(result2["data"])
    
    if result2.get("execution_time"):
        print(f"⏱️  Execution Time: {result2['execution_time']:.3f} seconds")
    
    # ========================================================================
    # DEMO 3: Send Alert
    # ========================================================================
    print_section("DEMO 3: Send Pollution Alert", "🚨")
    
    command3 = "Send alert about high pollution levels in Delhi"
    result3 = agent.process_command(command3)
    
    print_command_info(command3, "send_alert", result3["success"])
    print(f"Message: {result3['message']}")
    
    if result3.get("data"):
        print("\nData:")
        print_data_formatted(result3["data"])
    
    if result3.get("execution_time"):
        print(f"⏱️  Execution Time: {result3['execution_time']:.3f} seconds")
    
    # ========================================================================
    # DEMO 4: BLOCKED - Shutdown Factory
    # ========================================================================
    print_section("DEMO 4: BLOCKED ACTION - Shutdown Factory", "🔴")
    print("⚠️  This action should be BLOCKED by policy enforcement!\n")
    
    command4 = "Shutdown factory in Mayapuri"
    result4 = agent.process_command(command4)
    
    print_command_info(command4, "shutdown_factory", result4["success"])
    print(f"Message: {result4['message']}")
    
    if result4.get("data"):
        print("\nReason for Blocking:")
        print_data_formatted(result4["data"])

    
    # ========================================================================
    # DEMO 5: BLOCKED - Issue Fine
    # ========================================================================
    print_section("DEMO 5: BLOCKED ACTION - Issue Fine", "🔴")
    print("⚠️  This action should be BLOCKED by policy enforcement!\n")
    
    command5 = "Issue fine to polluting factory"
    result5 = agent.process_command(command5)
    
    print_command_info(command5, "issue_fine", result5["success"])
    print(f"Message: {result5['message']}")
    
    if result5.get("data"):
        print("\nReason for Blocking:")
        print_data_formatted(result5["data"])
    
    # ========================================================================
    # System Statistics
    # ========================================================================
    print_section("SYSTEM STATISTICS", "📊")
    
    status = agent.get_system_status()
    print(f"\n  Total Actions Processed: {status['total_actions']}")
    print(f"  ✅ Successful Actions: {status['successful_actions']}")
    print(f"  ❌ Blocked Actions: {status['blocked_actions']}")
    print(f"  ⚠️  Errors: {status['errors']}")
    
    # ========================================================================
    # Audit Log Sample
    # ========================================================================
    print_section("AUDIT LOG SAMPLE (Last 3 Entries)", "📝")
    
    logs = agent.logger.get_logs()
    for i, log in enumerate(logs[-3:], 1):
        print(f"\n  Entry {i}:")
        print(f"    Timestamp: {log.get('timestamp')}")
        print(f"    Action: {log.get('intent', {}).get('action')}")
        print(f"    Status: {log.get('status')}")
        print(f"    Command: \"{log.get('intent', {}).get('user_command')}\"")
    
    # ========================================================================
    # Summary
    # ========================================================================
    print_section("DEMO COMPLETE", "✅")
    
    print("\n🎯 Key Features Demonstrated:")
    print("  ✓ Natural language intent parsing")
    print("  ✓ Policy-based security enforcement")
    print("  ✓ OpenClaw integration for file operations")
    print("  ✓ Blocked dangerous actions (shutdown, fines)")
    print("  ✓ Comprehensive audit logging")
    print("  ✓ Real-time pollution data analysis")
    
    print("\n" + "="*80)
    print("Thank you for reviewing AirGuard AI!")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_demo()
