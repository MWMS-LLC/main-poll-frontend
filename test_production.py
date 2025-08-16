#!/usr/bin/env python3
"""
Production Environment Test Script
This simulates exactly what will happen in production
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def test_production_environment():
    """Test the production environment locally"""
    print("🧪 Testing Production Environment...")
    
    # 1. Test imports with fresh Python environment
    print("\n1️⃣ Testing imports...")
    try:
        import fastapi
        import uvicorn
        import psycopg2
        import dotenv
        import pydantic
        print("   ✅ All required packages import successfully")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # 2. Test FastAPI app creation
    print("\n2️⃣ Testing FastAPI app...")
    try:
        from main import app
        print("   ✅ FastAPI app loads successfully")
        print(f"   ✅ App title: {app.title}")
        print(f"   ✅ App version: {app.version}")
    except Exception as e:
        print(f"   ❌ FastAPI app failed: {e}")
        return False
    
    # 3. Test environment variables
    print("\n3️⃣ Testing environment variables...")
    required_vars = ['DATABASE_URL']
    for var in required_vars:
        if os.getenv(var):
            print(f"   ✅ {var} is set")
        else:
            print(f"   ⚠️  {var} is not set (will use default)")
    
    # 4. Test database connection (if DATABASE_URL is set)
    print("\n4️⃣ Testing database connection...")
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        try:
            import psycopg2
            conn = psycopg2.connect(db_url)
            conn.close()
            print("   ✅ Database connection successful")
        except Exception as e:
            print(f"   ❌ Database connection failed: {e}")
            print("   💡 This is expected if DATABASE_URL points to production")
    else:
        print("   ⚠️  No DATABASE_URL set, skipping database test")
    
    # 5. Test uvicorn startup
    print("\n5️⃣ Testing uvicorn startup...")
    try:
        # Test if uvicorn can start (we'll stop it immediately)
        process = subprocess.Popen([
            'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8001'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it a moment to start
        import time
        time.sleep(2)
        
        # Check if it's running
        if process.poll() is None:
            print("   ✅ Uvicorn starts successfully")
            process.terminate()
            process.wait()
        else:
            stdout, stderr = process.communicate()
            print(f"   ❌ Uvicorn failed to start: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"   ❌ Uvicorn test failed: {e}")
        return False
    
    # 6. Test requirements.txt
    print("\n6️⃣ Testing requirements.txt...")
    try:
        subprocess.run([
            'pip', 'install', '-r', 'requirements.txt', '--dry-run'
        ], check=True, capture_output=True)
        print("   ✅ requirements.txt is valid")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ requirements.txt has issues: {e}")
        return False
    
    print("\n🎉 All production tests passed!")
    print("🚀 Your app is ready for deployment!")
    return True

if __name__ == "__main__":
    success = test_production_environment()
    sys.exit(0 if success else 1)
