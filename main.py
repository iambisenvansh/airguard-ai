#!/usr/bin/env python3
"""
AirGuard AI - Main Demo Script

This script demonstrates the complete AirGuard AI autonomous agent system with:
- Natural language command processing
- Policy-based security enforcement
- OpenClaw integration for system operations
- Comprehensive audit logging

CRITICAL FOR HACKATHON: This demo shows both ALLOWED and BLOCKED actions to
demonstrate the policy enforcement layer.

Run this script to see the system in action!
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import AirGuardAgent
from intent import IntentParser
from policy import PolicyEngine
from enforce import Enforcer
from executor import Executor
from logger import AuditLogger


def print_separator(char="=", length=80):
    """Print a separator line."""
    print(char * length)


def print_header(title):
    """Print a formatted header."""
    print_separator()
    print(f"  {title}")
    print_separator()
    print()


def print_result(result, command):
    """Print formatted command result."""
    print(f"Command: \"{command}\"")
    print(f"Action: {result.get('action', 'unknown')}")
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    
    if result.get('data'):
        print(f"\nData:")
        for key, value in result['data'].items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {key}: {value}")
    
    if result.get('files'):
        print(f"\nFiles Created:")
        for file in result['files']:
            print(f"  - {file}")
    
    if result.get('execution_time'):
        print(f"\nExecution Time: {result['execution_time']:.3f} seconds")
    
    if result.get('blocked_reason'):
        print(f"\n⚠️  BLOCKED REASON: {result['blocked_reason']}")
        print(f"Policy Rule: {result.get('policy_rule', 'unknown')}")
    
    print()


def main():
    """
    Main demo function that initializes the system and runs example commands.
    
    This demonstrates:
    1. System initialization with all components
    2. Allowed actions (generate report, analyze AQI, send alert)
    3. Blocked actions (shutdown factory, issue fine)
    4. Audit log viewing
    """
    print_header("AIRGUARD AI - AUTONOMOUS POLLUTION MONITORING SYSTEM")
    print("Hackathon Demo - Policy-Based AI Agent with OpenClaw Integration")
    print()
    
    # ========================================================================
    # STEP 1: Initialize all system components
    # ========================================================================
    print("Initializing AirGuard AI system...")
    print()
    
    try:
        # Create components
        logger = AuditLogger(log_dir="logs/")
        intent_parser = IntentParser()
        policy_engine = PolicyEngine(policy_file="policy.json")
        executor = Executor(data_dir="data/", output_dir="output/")
        enforcer = Enforcer(executor, logger)
        
        # Initialize agent
        agent = AirGuardAgent(intent_parser, policy_engine, enforcer, logger)
        
        print("✓ System initialized successfully!")
        print()
        
        # Show allowed actions
        status = agent.get_status()
        print(f"Allowed Actions: {', '.join(status['allowed_actions'])}")
        print()
        
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        return 1
    
    # ========================================================================
    # STEP 2: Demonstrate ALLOWED actions
    # ========================================================================
    print_header("DEMO PART 1: ALLOWED ACTIONS")
    print("These actions are permitted by the security policy and will execute.\n")
    
    # Example 1: Generate pollution