#!/usr/bin/env python3
# Test runner script for the School Feedback Platform

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def check_server_running(url="http://localhost:8000", timeout=30):
    """Check if the server is running"""
    print(f"Checking if server is running at {url}...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✅ Server is running!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)
    
    print("❌ Server is not responding")
    return False

def run_unit_tests():
    """Run unit tests (no server required)"""
    print("\n🧪 Running unit tests...")
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/test_sentiment.py", 
        "-v", 
        "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

def run_integration_tests():
    """Run integration tests (requires server)"""
    print("\n🌐 Running integration tests...")
    
    if not check_server_running():
        print("❌ Server not running. Starting with docker-compose...")
        
        # Try to start server
        start_cmd = ["docker-compose", "up", "-d"]
        start_result = subprocess.run(start_cmd, capture_output=True, text=True)
        
        if start_result.returncode != 0:
            print("❌ Failed to start server with docker-compose")
            print(start_result.stderr)
            return False
        
        # Wait for server to be ready
        print("⏳ Waiting for server to start...")
        time.sleep(15)
        
        if not check_server_running():
            print("❌ Server failed to start properly")
            return False
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/test_api.py", 
        "-v", 
        "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

def run_all_tests():
    """Run all tests"""
    print("\n🚀 Running all tests...")
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

def main():
    """Main test runner"""
    print("🎯 School Feedback Platform - Test Runner")
    print("=" * 50)
    
    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check if pytest is installed
    try:
        import pytest
        print(f"✅ pytest version: {pytest.__version__}")
    except ImportError:
        print("❌ pytest not installed. Run: pip install pytest")
        return 1
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    else:
        test_type = "all"
    
    success = True
    
    if test_type in ["unit", "u"]:
        success = run_unit_tests()
    elif test_type in ["integration", "int", "i"]:
        success = run_integration_tests()
    elif test_type in ["all", "a"]:
        print("Running unit tests first...")
        unit_success = run_unit_tests()
        
        print("\nRunning integration tests...")
        integration_success = run_integration_tests()
        
        success = unit_success and integration_success
    else:
        print(f"❌ Unknown test type: {test_type}")
        print("Usage: python scripts/run_tests.py [unit|integration|all]")
        return 1
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
