#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

from django.db import connection

def test_database_connection():
    try:
        # Test basic connection
        cursor = connection.cursor()
        print("✅ Database connection successful")
        
        # Test query execution
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ Found {len(tables)} tables in database")
        
        # List table names
        table_names = [table[0] for table in tables]
        print("📋 Tables:", ", ".join(table_names))
        
        # Test Django's database connection
        from django.db import connections
        from django.core.management import execute_from_command_line
        connections['default'].ensure_connection()
        print("✅ Django database connection verified")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
