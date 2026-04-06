import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import urllib.parse

db_user = "postgres"
db_password = "Na01zi02m03@"
db_host = "localhost"
db_port = "5432"
db_name = "autointel"

try:
    # Connect to default postgres DB to create the new one
    conn = psycopg2.connect(
        dbname='postgres', 
        user=db_user, 
        host=db_host, 
        password=db_password, 
        port=db_port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute(f'CREATE DATABASE {db_name}')
        print(f"DATABASE_CREATED: {db_name}")
    else:
        print(f"DATABASE_ALREADY_EXISTS: {db_name}")
        
    cursor.close()
    conn.close()
    
    # Generate the encoded URL for .env
    # We need to quote the password because it contains special characters like '@'
    encoded_password = urllib.parse.quote_plus(db_password)
    database_url = f"postgres://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    print(f"URL_FOR_ENV: {database_url}")
    
except Exception as e:
    print(f"ERROR: {repr(e)}")
