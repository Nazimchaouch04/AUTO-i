import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autointel.settings')
django.setup()

def test_db():
    try:
        with connection.cursor() as cursor:
            # First query that fails
            cursor.execute("SELECT 1")
            print("First query success")
            # Create a user to trigger signals
            from django.contrib.auth.models import User
            print("Creating test user...")
            u = User.objects.create_user(username='tester_db', email='db@test.com', password='pass')
            print(f"User created: {u}")
    except Exception as e:
        import traceback
        print("--- CAUGHT EXCEPTION ---")
        traceback.print_exc()
        print("--- END EXCEPTION ---")

if __name__ == "__main__":
    test_db()
