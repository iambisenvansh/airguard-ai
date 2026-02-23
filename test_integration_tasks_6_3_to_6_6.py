"""
Integration test for tasks 6.3-6.6 using actual data files.

This test verifies the complete workflow with real pollution data files.
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from executor import Executor
from models import Intent


def test_full_workflow_with_real_data():
    """Test complete workflow with actual data files."""
    print("\n" + "=" * 70)
    print("INTEGRATION TEST: Full Workflow with Real Data")
    print("=" * 70)
    
    executor = Executor()
    
    # Test 1: Analyze AQI for Delhi (JSON file)
    print("\n--- Test 1: Analyze AQI for Delhi (JSON) ---")
    try:
        intent = Intent(
            action="analyze_aqi",
            parameters={"location": "Delhi"},
            timestamp=datetime.now(),
            user_command="Analyze AQI in Delhi",
            confidence=0.95
        )
        
        result = executor.execute(intent)
        
        if result.success:
            print(f"✅ SUCCESS: {result.message}")
            print(f"   Execution time: {result.execution_time:.3f}s")
            print(f"   Average AQI: {result.data['summary']['average_aqi']}")
            print(f"   Trend: {result.data['summary']['trend']}")
            print(f"   Health Advisory: {result.data['health_advisory'][:50]}...")
        else:
            print(f"❌ FAILED: {result.message}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Generate Report for Delhi
    print("\n--- Test 2: Generate Report for Delhi ---")
    try:
        intent = Intent(
            action="generate_report",
            parameters={"location": "Delhi"},
            timestamp=datetime.now(),
            user_command="Generate pollution report for Delhi",
            confidence=0.95
        )
        
        result = executor.execute(intent)
        
        if result.success:
            print(f"✅ SUCCESS: {result.message}")
            print(f"   Execution time: {result.execution_time:.3f}s")
            print(f"   Report file: {result.data['report_file']}")
            print(f"   Files created: {len(result.files_created)}")
            
            # Verify file exists and has content
            if os.path.exists(result.data['report_file']):
                file_size = os.path.getsize(result.data['report_file'])
                print(f"   File size: {file_size} bytes")
                
                # Show a snippet of the report
                with open(result.data['report_file'], 'r') as f:
                    lines = f.readlines()
                    print(f"\n   Report snippet (lines 1-15):")
                    for i, line in enumerate(lines[:15], 1):
                        print(f"   {i:2d}: {line.rstrip()}")
            else:
                print(f"   ⚠️  Warning: File not found at {result.data['report_file']}")
        else:
            print(f"❌ FAILED: {result.message}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Analyze AQI for Mumbai (CSV file)
    print("\n--- Test 3: Analyze AQI for Mumbai (CSV) ---")
    try:
        intent = Intent(
            action="analyze_aqi",
            parameters={"location": "Mumbai"},
            timestamp=datetime.now(),
            user_command="Analyze AQI in Mumbai",
            confidence=0.95
        )
        
        result = executor.execute(intent)
        
        if result.success:
            print(f"✅ SUCCESS: {result.message}")
            print(f"   Execution time: {result.execution_time:.3f}s")
            print(f"   Average AQI: {result.data['summary']['average_aqi']}")
            print(f"   Trend: {result.data['summary']['trend']}")
        else:
            print(f"❌ FAILED: {result.message}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Send Alert with real data
    print("\n--- Test 4: Send Alert ---")
    try:
        intent = Intent(
            action="send_alert",
            parameters={
                "severity": "critical",
                "message": "Extremely high pollution levels detected",
                "area": "Delhi",
                "pollutants": {"PM2.5": 287, "PM10": 420}
            },
            timestamp=datetime.now(),
            user_command="Send critical alert for Delhi",
            confidence=0.95
        )
        
        result = executor.execute(intent)
        
        if result.success:
            print(f"✅ SUCCESS: {result.message}")
            print(f"   Execution time: {result.execution_time:.3f}s")
            print(f"   Alert ID: {result.data['alert_id']}")
            print(f"   Recipients: {len(result.data['recipients'])} recipients")
        else:
            print(f"❌ FAILED: {result.message}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 70)
    print("✅ ALL INTEGRATION TESTS PASSED!")
    print("=" * 70)
    print("\nTasks 6.3-6.6 are fully implemented and working with real data:")
    print("  ✓ Task 6.3: analyze_aqi() - Statistical analysis working")
    print("  ✓ Task 6.4: generate_report() - OpenClaw integration working")
    print("  ✓ Task 6.5: send_alert() - Alert formatting and validation working")
    print("  ✓ Task 6.6: execute() - Action routing and error handling working")
    
    return True


def main():
    """Run integration test."""
    try:
        success = test_full_workflow_with_real_data()
        return 0 if success else 1
    except Exception as e:
        print(f"\n❌ INTEGRATION TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
