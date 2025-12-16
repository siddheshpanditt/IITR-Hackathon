#!/usr/bin/env python3
"""
Test script to verify all features are working
"""

import requests
import json
import time

def test_application():
    """Test all application features"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Universal Website Monitor Features")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print("❌ Health check: FAILED")
    except:
        print("❌ Health check: FAILED (connection error)")
        return
    
    # Test 2: Login
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{base_url}/auth/login", json=login_data, timeout=5)
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("✅ Authentication: PASSED")
        else:
            print("❌ Authentication: FAILED")
            return
    except Exception as e:
        print(f"❌ Authentication: FAILED ({e})")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 3: System metrics
    try:
        response = requests.get(f"{base_url}/api/real-metrics", headers=headers, timeout=5)
        if response.status_code == 200:
            metrics = response.json()
            print(f"✅ Real metrics: PASSED (CPU: {metrics.get('cpu', 0)}%)")
        else:
            print("❌ Real metrics: FAILED")
    except Exception as e:
        print(f"❌ Real metrics: FAILED ({e})")
    
    # Test 4: Status endpoint
    try:
        response = requests.get(f"{base_url}/status", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Status endpoint: PASSED")
        else:
            print("❌ Status endpoint: FAILED")
    except Exception as e:
        print(f"❌ Status endpoint: FAILED ({e})")
    
    # Test 5: AI Prediction
    try:
        response = requests.get(f"{base_url}/ai/prediction", headers=headers, timeout=5)
        if response.status_code == 200:
            prediction = response.json()
            print(f"✅ AI Prediction: PASSED (Risk: {prediction.get('probability', 0)})")
        else:
            print("❌ AI Prediction: FAILED")
    except Exception as e:
        print(f"❌ AI Prediction: FAILED ({e})")
    
    # Test 6: Self-healing stats
    try:
        response = requests.get(f"{base_url}/ai/healing-stats", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Self-healing stats: PASSED")
        else:
            print("❌ Self-healing stats: FAILED")
    except Exception as e:
        print(f"❌ Self-healing stats: FAILED ({e})")
    
    # Test 7: Alert summary
    try:
        response = requests.get(f"{base_url}/ai/alert-summary", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Alert summary: PASSED")
        else:
            print("❌ Alert summary: FAILED")
    except Exception as e:
        print(f"❌ Alert summary: FAILED ({e})")
    
    # Test 8: Financial data
    try:
        response = requests.get(f"{base_url}/financial", headers=headers, timeout=5)
        if response.status_code == 200:
            financial = response.json()
            print(f"✅ Financial data: PASSED (Balance: ${financial.get('current_balance', 0)})")
        else:
            print("❌ Financial data: FAILED")
    except Exception as e:
        print(f"❌ Financial data: FAILED ({e})")
    
    # Test 9: URL monitoring
    try:
        response = requests.get(f"{base_url}/monitored-urls", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ URL monitoring: PASSED")
        else:
            print("❌ URL monitoring: FAILED")
    except Exception as e:
        print(f"❌ URL monitoring: FAILED ({e})")
    
    # Test 10: Fix deployment
    try:
        response = requests.post(f"{base_url}/fix", headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Self-healing trigger: PASSED")
        else:
            print("❌ Self-healing trigger: FAILED")
    except Exception as e:
        print(f"❌ Self-healing trigger: FAILED ({e})")
    
    print("=" * 50)
    print("🎉 Feature testing completed!")
    print("📱 Access the dashboard at: http://localhost:5000")

if __name__ == "__main__":
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    test_application()