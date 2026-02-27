"""
Quick diagnostic script to check if mood logging endpoint works
"""
import requests
import json

# Test 1: Check if backend is running
print("=" * 60)
print("TEST 1: Checking if backend is running...")
print("=" * 60)
try:
    response = requests.get("http://localhost:8000/docs")
    if response.status_code == 200:
        print("✅ Backend is running on http://localhost:8000")
    else:
        print(f"⚠️ Backend responded with status code: {response.status_code}")
except Exception as e:
    print(f"❌ Backend is NOT running. Error: {e}")
    print("\n📌 ACTION REQUIRED: Start the backend server first!")
    print("   Run: cd backend && python run.py")
    exit(1)

# Test 2: Try to access a protected endpoint (should fail without auth)
print("\n" + "=" * 60)
print("TEST 2: Testing mood endpoint without authentication...")
print("=" * 60)
try:
    response = requests.get("http://localhost:8000/api/mood/history")
    print(f"Status: {response.status_code}")
    if response.status_code == 403:
        print("✅ Endpoint exists and requires authentication (expected)")
    else:
        print(f"⚠️ Unexpected response: {response.text[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Check database tables
print("\n" + "=" * 60)
print("TEST 3: Checking if mood_entries table exists...")
print("=" * 60)
try:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from app.database import engine
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if "mood_entries" in tables:
        print("✅ mood_entries table exists")
        
        # Check columns
        columns = [col['name'] for col in inspector.get_columns('mood_entries')]
        print(f"   Columns: {', '.join(columns)}")
    else:
        print("❌ mood_entries table does NOT exist!")
        print(f"   Available tables: {', '.join(tables)}")
        print("\n📌 ACTION REQUIRED: Database tables not created properly")
        print("   The backend should create tables automatically on startup")
        print("   Try restarting the backend server")
except Exception as e:
    print(f"❌ Error checking database: {e}")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
print("\nIf all tests passed, the issue might be:")
print("1. Frontend token is invalid/expired - try logging out and back in")
print("2. CORS issue - check browser console for CORS errors")
print("3. Network issue - check browser Network tab")
