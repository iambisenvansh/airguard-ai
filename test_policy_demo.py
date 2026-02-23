"""
Demo script to showcase PolicyEngine functionality.

This script demonstrates how the PolicyEngine validates different types of
actions and shows the clear distinction between allowed and blocked actions.
"""

from datetime import datetime
from policy import PolicyEngine
from models import Intent


def print_decision(action_name: str, decision):
    """Print a formatted policy decision."""
    print(f"\n{'='*70}")
    print(f"Action: {action_name}")
    print(f"{'='*70}")
    print(f"Allowed: {decision.allowed}")
    print(f"Reason: {decision.reason}")
    print(f"Rule: {decision.rule_name}")
    if decision.constraints:
        print(f"Constraints: {decision.constraints}")
    print(f"{'='*70}")


def main():
    """Run PolicyEngine demo."""
    print("\n" + "="*70)
    print("AirGuard AI - PolicyEngine Demo")
    print("="*70)
    
    # Initialize PolicyEngine
    engine = PolicyEngine("policy.json")
    
    # Display policy info
    info = engine.get_policy_info()
    print(f"\nPolicy Version: {info['version']}")
    print(f"Default Policy: {info['default_policy']}")
    print(f"Total Rules: {info['rules_count']}")
    print(f"Allowed Actions: {', '.join(info['allowed_actions'])}")
    
    print("\n" + "="*70)
    print("TESTING ALLOWED ACTIONS")
    print("="*70)
    
    # Test 1: Generate Report (ALLOWED)
    intent1 = Intent(
        action="generate_report",
        parameters={"location": "Delhi"},
        timestamp=datetime.now(),
        user_command="Generate pollution report for Delhi",
        confidence=0.95
    )
    decision1 = engine.validate_intent(intent1)
    print_decision("generate_report", decision1)
    
    # Test 2: Analyze AQI (ALLOWED)
    intent2 = Intent(
        action="analyze_aqi",
        parameters={"location": "Delhi", "metric": "PM2.5"},
        timestamp=datetime.now(),
        user_command="Analyze AQI in Delhi for today",
        confidence=0.92
    )
    decision2 = engine.validate_intent(intent2)
    print_decision("analyze_aqi", decision2)
    
    # Test 3: Send Alert (ALLOWED)
    intent3 = Intent(
        action="send_alert",
        parameters={"severity": "critical", "message": "High pollution levels"},
        timestamp=datetime.now(),
        user_command="Send alert about high pollution levels",
        confidence=0.88
    )
    decision3 = engine.validate_intent(intent3)
    print_decision("send_alert", decision3)
    
    print("\n" + "="*70)
    print("TESTING BLOCKED ACTIONS")
    print("="*70)
    
    # Test 4: Shutdown Factory (BLOCKED)
    intent4 = Intent(
        action="shutdown_factory",
        parameters={"factory_id": "F123", "location": "Mayapuri"},
        timestamp=datetime.now(),
        user_command="Shutdown factory in Mayapuri",
        confidence=0.90
    )
    decision4 = engine.validate_intent(intent4)
    print_decision("shutdown_factory", decision4)
    
    # Test 5: Issue Fine (BLOCKED)
    intent5 = Intent(
        action="issue_fine",
        parameters={"factory_id": "F456", "amount": 50000},
        timestamp=datetime.now(),
        user_command="Issue fine to polluting factory",
        confidence=0.85
    )
    decision5 = engine.validate_intent(intent5)
    print_decision("issue_fine", decision5)
    
    print("\n" + "="*70)
    print("TESTING UNKNOWN ACTION (DEFAULT POLICY)")
    print("="*70)
    
    # Test 6: Unknown Action (DEFAULT DENY)
    intent6 = Intent(
        action="unknown_action",
        parameters={},
        timestamp=datetime.now(),
        user_command="Do something unknown",
        confidence=0.5
    )
    decision6 = engine.validate_intent(intent6)
    print_decision("unknown_action", decision6)
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✓ Allowed actions work correctly with constraints")
    print(f"✗ Blocked actions are denied with clear reasons")
    print(f"✗ Unknown actions default to DENY for security")
    print(f"\nPolicyEngine is ready for hackathon demo!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
