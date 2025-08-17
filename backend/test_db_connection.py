#!/usr/bin/env python3
"""
Simple database connection test script
This helps debug DATABASE_URL and connection issues
"""

import os
import sys
from urllib.parse import urlparse

def test_database_url_format():
    """Test if DATABASE_URL is properly formatted"""
    print("🔍 Testing DATABASE_URL format...")
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL environment variable is not set!")
        return False
    
    print(f"📝 Raw DATABASE_URL: {database_url}")
    
    # Check if it starts with postgresql://
    if not database_url.startswith("postgresql://"):
        print("❌ DATABASE_URL must start with 'postgresql://'")
        print("💡 Change from 'postgres://' to 'postgresql://'")
        return False
    
    try:
        parsed = urlparse(database_url)
        
        # Check required components
        if not parsed.hostname:
            print("❌ No hostname found in DATABASE_URL")
            return False
            
        if not parsed.path or parsed.path == "/":
            print("❌ No database name found in DATABASE_URL")
            return False
            
        print("✅ DATABASE_URL format is correct:")
        print(f"   - Protocol: {parsed.scheme}")
        print(f"   - Username: {parsed.username or 'postgres'}")
        print(f"   - Password: {'Yes' if parsed.password else 'No'}")
        print(f"   - Host: {parsed.hostname}")
        print(f"   - Port: {parsed.port or 5432}")
        print(f"   - Database: {parsed.path.lstrip('/')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to parse DATABASE_URL: {e}")
        return False

def test_database_connection():
    """Test actual database connection"""
    print("\n🔍 Testing database connection...")
    
    try:
        import pg8000
        
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ No DATABASE_URL to test")
            return False
        
        parsed = urlparse(database_url)
        
        # Extract connection parameters
        user = parsed.username or "postgres"
        password = parsed.password or ""
        host = parsed.hostname
        port = parsed.port or 5432
        database = parsed.path.lstrip("/")
        
        print(f"🔌 Attempting connection to {host}:{port}/{database}...")
        
        # Try to connect
        conn = pg8000.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        print("✅ Database connection successful!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"📊 PostgreSQL version: {version[0]}")
        
        # Test if our tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        print(f"📋 Available tables: {[table[0] for table in tables]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except ImportError:
        print("❌ pg8000 not installed. Install with: pip install pg8000")
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"💡 Error type: {type(e).__name__}")
        return False

def main():
    """Main test function"""
    print("🚀 Teen Poll Database Connection Test")
    print("=" * 50)
    
    # Test DATABASE_URL format
    format_ok = test_database_url_format()
    
    if format_ok:
        # Test actual connection
        connection_ok = test_database_connection()
    else:
        connection_ok = False
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   DATABASE_URL format: {'✅ PASS' if format_ok else '❌ FAIL'}")
    print(f"   Database connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    
    if format_ok and connection_ok:
        print("\n🎉 Database connection is working correctly!")
        return 0
    else:
        print("\n⚠️  Database connection has issues. Check the errors above.")
        
        if not format_ok:
            print("\n💡 Common DATABASE_URL issues:")
            print("   - Use 'postgresql://' not 'postgres://'")
            print("   - Include username, password, host, port, and database")
            print("   - Example: postgresql://user:pass@host:port/db")
        
        if format_ok and not connection_ok:
            print("\n💡 Common connection issues:")
            print("   - Database server is not running")
            print("   - Network/firewall blocking connection")
            print("   - Wrong credentials")
            print("   - Database doesn't exist")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
