"""
Test script for read_pollution_data() method.

This script tests the data reading functionality to ensure it works correctly
with OpenClaw integration.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from executor import Executor


def test_read_pollution_data_success():
    """Test successful reading of pollution data."""
    print("Test 1: Reading existing pollution data file...")
    
    executor = Executor(data_dir="data", output_dir="output")
    
    try:
        data = executor.read_pollution_data("Delhi")
        print(f"✓ Successfully read data for {data['location']}")
        print(f"  - Timestamp: {data['timestamp']}")
        print(f"  - Number of readings: {len(data['data'])}")
        print(f"  - First reading AQI: {data['data'][0]['aqi']}")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False


def test_read_pollution_data_not_found():
    """Test handling of missing file."""
    print("\nTest 2: Handling missing pollution data file...")
    
    executor = Executor(data_dir="data", output_dir="output")
    
    try:
        data = executor.read_pollution_data("NonExistentCity")
        print(f"✗ Should have raised FileNotFoundError")
        return False
    except FileNotFoundError as e:
        print(f"✓ Correctly raised FileNotFoundError: {e}")
        return True
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_read_pollution_data_normalized():
    """Test location name normalization."""
    print("\nTest 3: Testing location name normalization...")
    
    executor = Executor(data_dir="data", output_dir="output")
    
    try:
        # Should work with different case
        data = executor.read_pollution_data("DELHI")
        print(f"✓ Successfully read data with uppercase location name")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False


def test_read_pollution_data_csv():
    """Test reading CSV format."""
    print("\nTest 4: Reading CSV format pollution data...")
    
    executor = Executor(data_dir="data", output_dir="output")
    
    try:
        data = executor.read_pollution_data("Mumbai")
        print(f"✓ Successfully read CSV data for {data['location']}")
        print(f"  - Format: {data.get('format', 'json')}")
        print(f"  - Number of readings: {len(data['data'])}")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Testing read_pollution_data() implementation")
    print("=" * 60)
    
    results = []
    results.append(test_read_pollution_data_success())
    results.append(test_read_pollution_data_not_found())
    results.append(test_read_pollution_data_normalized())
    results.append(test_read_pollution_data_csv())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    sys.exit(0 if all(results) else 1)
