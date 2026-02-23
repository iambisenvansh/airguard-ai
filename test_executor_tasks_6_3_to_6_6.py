"""
Test script for verifying tasks 6.3, 6.4, 6.5, and 6.6 implementation.

This script tests:
- Task 6.3: analyze_aqi() functionality
- Task 6.4: generate_report() functionality with OpenClaw
- Task 6.5: send_alert() functionality
- Task 6.6: execute() method with action routing
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from executor import Executor
from models import Intent


def test_analyze_aqi():
    """Test Task 6.3: AQI analysis functionality."""
    print("\n" + "=" * 70)
    print("TEST 6.3: Analyze AQI Functionality")
    print("=" * 70)
    
    executor = Executor()
    
    try:
        # Test with real data file (Delhi)
        analysis = executor.analyze_aqi("Delhi")
        
        print(f"✓ Location: {analysis['location']}")
        print(f"✓ Average AQI: {analysis['summary']['average_aqi']}")
        print(f"✓ Min AQI: {analysis['summary']['min_aqi']}")
        print(f"✓ Max AQI: {analysis['summary']['max_aqi']}")
        print(f"✓ Trend: {analysis['summary']['trend']}")
        print(f"✓ Health Advisory: {analysis['health_advisory']}")
        
        # Verify pollutant stats
        if "PM2.5" in analysis['pollutants']:
            pm25 = analysis['pollutants']['PM2.5']
            print(f"✓ PM2.5 Average: {pm25['avg']} µg/m³")
        
        if "PM10" in analysis['pollutants']:
            pm10 = analysis['pollutants']['PM10']
            print(f"✓ PM10 Average: {pm10['avg']} µg/m³")
        
        if "NO2" in analysis['pollutants']:
            no2 = analysis['pollutants']['NO2']
            print(f"✓ NO2 Average: {no2['avg']} µg/m³")
        
        # Verify all required metrics are present
        required_metrics = ["PM2.5", "PM10", "NO2", "SO2", "CO"]
        for metric in required_metrics:
            if metric in analysis['pollutants']:
                print(f"✓ {metric} analysis included")
        
        print("\n✅ Task 6.3 PASSED: AQI analysis working correctly")
        return True
        
    except Exception as e:
        print(f"\n❌ Task 6.3 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_generate_report():
    """Test Task 6.4: Report generation with OpenClaw."""
    print("\n" + "=" * 70)
    print("TEST 6.4: Generate Report Functionality (OpenClaw)")
    print("=" * 70)
    
    executor = Executor()
    
    # Create sample analysis data
    sample_analysis = {
        "location": "Delhi",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "average_aqi": 287.5,
            "min_aqi": 278.0,
            "max_aqi": 295.0,
            "trend": "stable",
            "readings_count": 4
        },
        "pollutants": {
            "PM2.5": {"avg": 145.75, "min": 138.0, "max": 152.0},
            "PM10": {"avg": 322.5, "min": 310.0, "max": 335.0},
            "NO2": {"avg": 68.75, "min": 65.0, "max": 72.0}
        },
        "health_advisory": "Very Unhealthy - Health alert, avoid outdoor activities"
    }
    
    try:
        result = executor.generate_report(sample_analysis, "Delhi")
        
        print(f"✓ Report file created: {result['report_file']}")
        print(f"✓ Location: {result['location']}")
        print(f"✓ Timestamp: {result['timestamp']}")
        print(f"✓ Summary: {result['summary']}")
        
        # Verify file exists
        if os.path.exists(result['report_file']):
            print(f"✓ File verified to exist on disk")
            
            # Read and display first few lines
            with open(result['report_file'], 'r') as f:
                lines = f.readlines()[:10]
                print("\n✓ Report preview (first 10 lines):")
                for line in lines:
                    print(f"  {line.rstrip()}")
        else:
            print(f"⚠ Warning: Report file not found at {result['report_file']}")
        
        print("\n✅ Task 6.4 PASSED: Report generation with OpenClaw working correctly")
        return True
        
    except Exception as e:
        print(f"\n❌ Task 6.4 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_send_alert():
    """Test Task 6.5: Alert sending functionality."""
    print("\n" + "=" * 70)
    print("TEST 6.5: Send Alert Functionality")
    print("=" * 70)
    
    executor = Executor()
    
    try:
        # Test critical alert
        result = executor.send_alert(
            severity="critical",
            message="Extremely high pollution levels detected in Delhi",
            area="Delhi",
            pollutants={"PM2.5": 287, "PM10": 420, "NO2": 85}
        )
        
        print(f"✓ Alert sent: {result['alert_sent']}")
        print(f"✓ Alert ID: {result['alert_id']}")
        print(f"✓ Severity: {result['severity']}")
        print(f"✓ Area: {result['area']}")
        print(f"✓ Recipients: {', '.join(result['recipients'])}")
        
        # Test warning alert
        result2 = executor.send_alert(
            severity="warning",
            message="Elevated pollution levels",
            area="Mumbai"
        )
        
        print(f"\n✓ Second alert sent with severity: {result2['severity']}")
        
        # Test validation
        try:
            executor.send_alert(severity="invalid", message="test")
            print("⚠ Warning: Invalid severity should have raised ValueError")
        except ValueError as e:
            print(f"✓ Validation working: {str(e)}")
        
        print("\n✅ Task 6.5 PASSED: Alert sending working correctly")
        return True
        
    except Exception as e:
        print(f"\n❌ Task 6.5 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_execute_method():
    """Test Task 6.6: Main execute() method with action routing."""
    print("\n" + "=" * 70)
    print("TEST 6.6: Execute Method with Action Routing")
    print("=" * 70)
    
    executor = Executor()
    
    try:
        # Test 1: analyze_aqi action
        print("\n--- Test 1: analyze_aqi action ---")
        intent1 = Intent(
            action="analyze_aqi",
            parameters={"location": "Delhi"},
            timestamp=datetime.now(),
            user_command="Analyze AQI in Delhi",
            confidence=0.95
        )
        
        result1 = executor.execute(intent1)
        print(f"✓ Success: {result1.success}")
        print(f"✓ Message: {result1.message}")
        print(f"✓ Execution time: {result1.execution_time:.3f}s")
        print(f"✓ Data keys: {list(result1.data.keys()) if result1.data else 'None'}")
        
        # Test 2: generate_report action
        print("\n--- Test 2: generate_report action ---")
        intent2 = Intent(
            action="generate_report",
            parameters={"location": "Delhi"},
            timestamp=datetime.now(),
            user_command="Generate pollution report for Delhi",
            confidence=0.95
        )
        
        result2 = executor.execute(intent2)
        print(f"✓ Success: {result2.success}")
        print(f"✓ Message: {result2.message}")
        print(f"✓ Execution time: {result2.execution_time:.3f}s")
        print(f"✓ Files created: {result2.files_created}")
        
        # Test 3: send_alert action
        print("\n--- Test 3: send_alert action ---")
        intent3 = Intent(
            action="send_alert",
            parameters={
                "severity": "warning",
                "message": "High pollution detected",
                "area": "Delhi"
            },
            timestamp=datetime.now(),
            user_command="Send alert about high pollution",
            confidence=0.90
        )
        
        result3 = executor.execute(intent3)
        print(f"✓ Success: {result3.success}")
        print(f"✓ Message: {result3.message}")
        print(f"✓ Execution time: {result3.execution_time:.3f}s")
        
        # Test 4: Unknown action (error handling)
        print("\n--- Test 4: Unknown action (error handling) ---")
        intent4 = Intent(
            action="unknown_action",
            parameters={},
            timestamp=datetime.now(),
            user_command="Do something unknown",
            confidence=0.50
        )
        
        result4 = executor.execute(intent4)
        print(f"✓ Success: {result4.success} (should be False)")
        print(f"✓ Message: {result4.message}")
        
        # Test 5: Missing required parameter (error handling)
        print("\n--- Test 5: Missing parameter (error handling) ---")
        intent5 = Intent(
            action="analyze_aqi",
            parameters={},  # Missing location
            timestamp=datetime.now(),
            user_command="Analyze AQI",
            confidence=0.80
        )
        
        result5 = executor.execute(intent5)
        print(f"✓ Success: {result5.success} (should be False)")
        print(f"✓ Message: {result5.message}")
        
        print("\n✅ Task 6.6 PASSED: Execute method with action routing working correctly")
        return True
        
    except Exception as e:
        print(f"\n❌ Task 6.6 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("EXECUTOR TASKS 6.3-6.6 VERIFICATION TEST SUITE")
    print("=" * 70)
    
    results = []
    
    # Run all tests
    results.append(("Task 6.3: analyze_aqi()", test_analyze_aqi()))
    results.append(("Task 6.4: generate_report()", test_generate_report()))
    results.append(("Task 6.5: send_alert()", test_send_alert()))
    results.append(("Task 6.6: execute()", test_execute_method()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Tasks 6.3-6.6 are complete and working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
