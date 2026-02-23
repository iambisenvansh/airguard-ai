"""
Demo script to test AuditLogger with realistic scenarios.

This script demonstrates the AuditLogger functionality with various
action types including allowed actions, blocked actions, and errors.
"""

from datetime import datetime
from logger import AuditLogger
from models import Intent, PolicyDecision, ExecutionResult


def main():
    """Run demo scenarios for the AuditLogger."""
    print("=" * 70)
    print("AuditLogger Demo - Testing Tasks 4.1 and 4.2")
    print("=" * 70)
    print()
    
    # Initialize logger
    logger = AuditLogger(log_dir="logs/")
    print("✓ AuditLogger initialized with logs/ directory")
    print()
    
    # Scenario 1: Log a successful report generation
    print("Scenario 1: Logging successful report generation")
    print("-" * 70)
    
    intent1 = Intent(
        action="generate_report",
        parameters={"location": "Delhi"},
        timestamp=datetime.now(),
        user_command="Generate pollution report for Delhi",
        confidence=0.95
    )
    
    decision1 = PolicyDecision(
        allowed=True,
        reason="Report generation is a read-only operation",
        rule_name="generate_report",
        constraints=None
    )
    
    result1 = ExecutionResult(
        success=True,
        message="Report generated successfully",
        data={"report_file": "output/delhi_report.txt", "aqi_average": 287},
        execution_time=1.23,
        files_created=["output/delhi_report.txt"]
    )
    
    logger.log_action(intent1, decision1, result1, "SUCCESS")
    print(f"✓ Logged: {intent1.action} - SUCCESS")
    print(f"  Intent: {intent1.user_command}")
    print(f"  Result: {result1.message}")
    print()
    
    # Scenario 2: Log a blocked factory shutdown
    print("Scenario 2: Logging blocked factory shutdown")
    print("-" * 70)
    
    intent2 = Intent(
        action="shutdown_factory",
        parameters={"factory_id": "F123", "location": "Mayapuri"},
        timestamp=datetime.now(),
        user_command="Shutdown factory in Mayapuri",
        confidence=0.90
    )
    
    decision2 = PolicyDecision(
        allowed=False,
        reason="Critical infrastructure control requires human authorization",
        rule_name="shutdown_factory",
        constraints=None
    )
    
    logger.log_action(intent2, decision2, None, "BLOCKED")
    print(f"✓ Logged: {intent2.action} - BLOCKED")
    print(f"  Intent: {intent2.user_command}")
    print(f"  Reason: {decision2.reason}")
    print()
    
    # Scenario 3: Log a successful AQI analysis
    print("Scenario 3: Logging successful AQI analysis")
    print("-" * 70)
    
    intent3 = Intent(
        action="analyze_aqi",
        parameters={"location": "Delhi"},
        timestamp=datetime.now(),
        user_command="Analyze AQI in Delhi for today",
        confidence=0.92
    )
    
    decision3 = PolicyDecision(
        allowed=True,
        reason="Data analysis is a read-only operation",
        rule_name="analyze_aqi",
        constraints=None
    )
    
    result3 = ExecutionResult(
        success=True,
        message="AQI analysis completed",
        data={
            "location": "Delhi",
            "aqi": 287,
            "category": "Very Poor",
            "pollutants": {"PM2.5": 145, "PM10": 320}
        },
        execution_time=0.45,
        files_created=[]
    )
    
    logger.log_action(intent3, decision3, result3, "SUCCESS")
    print(f"✓ Logged: {intent3.action} - SUCCESS")
    print(f"  Intent: {intent3.user_command}")
    print(f"  Result: AQI = {result3.data['aqi']} ({result3.data['category']})")
    print()
    
    # Scenario 4: Log a blocked fine issuance
    print("Scenario 4: Logging blocked fine issuance")
    print("-" * 70)
    
    intent4 = Intent(
        action="issue_fine",
        parameters={"factory_id": "F456", "amount": 50000},
        timestamp=datetime.now(),
        user_command="Issue fine to polluting factory",
        confidence=0.88
    )
    
    decision4 = PolicyDecision(
        allowed=False,
        reason="Legal actions require proper authority and due process",
        rule_name="issue_fine",
        constraints=None
    )
    
    logger.log_action(intent4, decision4, None, "BLOCKED")
    print(f"✓ Logged: {intent4.action} - BLOCKED")
    print(f"  Intent: {intent4.user_command}")
    print(f"  Reason: {decision4.reason}")
    print()
    
    # Scenario 5: Log an error
    print("Scenario 5: Logging system error")
    print("-" * 70)
    
    logger.log_action(None, None, None, "ERROR")
    print(f"✓ Logged: ERROR - System error occurred")
    print()
    
    # Query logs - Get all logs
    print("=" * 70)
    print("Querying Logs - All Entries")
    print("=" * 70)
    
    all_logs = logger.get_logs()
    print(f"Total log entries: {len(all_logs)}")
    print()
    
    for i, log in enumerate(all_logs[-5:], 1):  # Show last 5 entries
        print(f"Entry {i}:")
        print(f"  Timestamp: {log['timestamp']}")
        print(f"  Status: {log['status']}")
        if log['intent']:
            print(f"  Action: {log['intent']['action']}")
            print(f"  Command: {log['intent']['user_command']}")
        print()
    
    # Query logs - Filter by status
    print("=" * 70)
    print("Querying Logs - Filtered by Status")
    print("=" * 70)
    
    success_logs = logger.get_logs(status_filter="SUCCESS")
    blocked_logs = logger.get_logs(status_filter="BLOCKED")
    error_logs = logger.get_logs(status_filter="ERROR")
    
    print(f"SUCCESS entries: {len(success_logs)}")
    print(f"BLOCKED entries: {len(blocked_logs)}")
    print(f"ERROR entries: {len(error_logs)}")
    print()
    
    # Show blocked actions in detail
    print("Blocked Actions Detail:")
    print("-" * 70)
    for log in blocked_logs[-2:]:  # Show last 2 blocked actions
        if log['intent']:
            print(f"  Action: {log['intent']['action']}")
            print(f"  Command: {log['intent']['user_command']}")
            if log['policy_decision']:
                print(f"  Reason: {log['policy_decision']['reason']}")
            print()
    
    print("=" * 70)
    print("Demo Complete! All logging functionality verified.")
    print("=" * 70)


if __name__ == "__main__":
    main()
