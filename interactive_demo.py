"""
AirGuard AI - Interactive Demo
User can type their own commands
"""

from agent import AirGuardAgent


def print_header():
    """Print main header."""
    print("\n" + "="*80)
    print("🌍 AIRGUARD AI - INTERACTIVE MODE")
    print("="*80)
    print("Type your commands or 'help' for examples, 'quit' to exit")
    print("="*80 + "\n")


def show_help():
    """Show example commands."""
    print("\n📋 EXAMPLE COMMANDS:")
    print("  ✅ Allowed:")
    print("    - Generate pollution report for Delhi")
    print("    - Analyze AQI in Mumbai")
    print("    - Send alert about high pollution levels")
    print("\n  ❌ Blocked (will be denied):")
    print("    - Shutdown factory in Mayapuri")
    print("    - Issue fine to polluting factory")
    print()


def print_result(result):
    """Print formatted result."""
    if result["success"]:
        print(f"✅ SUCCESS: {result['message']}")
        if result.get("data"):
            print(f"\n📊 Result:")
            # Print data in a readable format
            data = result["data"]
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, dict):
                        print(f"  {key}:")
                        for k, v in value.items():
                            print(f"    {k}: {v}")
                    else:
                        print(f"  {key}: {value}")
            else:
                print(f"  {data}")
        
        if result.get("files_created"):
            print(f"\n📄 Files Created: {result['files_created']}")
        
        if result.get("execution_time"):
            print(f"⏱️  Execution Time: {result['execution_time']:.3f} seconds")
    else:
        print(f"❌ {result['message']}")
        if result.get("data"):
            print(f"\n📊 Details:")
            for key, value in result["data"].items():
                print(f"  {key}: {value}")


def main():
    """Run interactive demo."""
    print_header()
    
    # Initialize agent
    print("🚀 Initializing AirGuard AI Agent...")
    try:
        agent = AirGuardAgent()
        print("✅ Agent ready!\n")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    show_help()
    
    # Interactive loop
    while True:
        # Get user input
        try:
            user_input = input("💬 Your command: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Goodbye!")
            break
        
        # Handle special commands
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if user_input.lower() == 'help':
            show_help()
            continue
        
        if user_input.lower() == 'status':
            # Show system status
            status = agent.get_system_status()
            print("\n📊 SYSTEM STATUS:")
            print(f"  Total Actions: {status['total_actions']}")
            print(f"  ✅ Successful: {status['successful_actions']}")
            print(f"  ❌ Blocked: {status['blocked_actions']}")
            print(f"  ⚠️  Errors: {status['errors']}")
            print(f"  🔓 Allowed Actions: {', '.join(status['allowed_actions'])}")
            print()
            continue
        
        if not user_input:
            print("⚠️  Please enter a command\n")
            continue
        
        # Process the command
        print(f"\n🧠 Processing: \"{user_input}\"")
        print("-" * 80)
        
        try:
            result = agent.process_command(user_input)
            print_result(result)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 80 + "\n")


if __name__ == "__main__":
    main()
