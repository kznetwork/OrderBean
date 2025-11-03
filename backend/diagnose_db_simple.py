"""
Database Connection Diagnostic Script (Simple Version)
"""
import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("\n" + "="*60)
print("Database Connection Diagnostic")
print("="*60)
print()

# 1. Check environment variables
print("[1/5] Checking environment variables...")
db_host = os.getenv('DB_HOST', 'NOT_SET')
db_port = os.getenv('DB_PORT', 'NOT_SET')
db_name = os.getenv('DB_NAME', 'NOT_SET')
db_user = os.getenv('DB_USER', 'NOT_SET')
db_password = os.getenv('DB_PASSWORD', 'NOT_SET')

print(f"   DB_HOST: {db_host}")
print(f"   DB_PORT: {db_port}")
print(f"   DB_NAME: {db_name}")
print(f"   DB_USER: {db_user}")
print(f"   DB_PASSWORD: {'*' * len(db_password) if db_password != 'NOT_SET' else 'NOT_SET'}")
print()

if 'NOT_SET' in [db_host, db_port, db_name, db_user, db_password]:
    print("ERROR: .env file is not configured properly!")
    print("   Please check your .env file.")
    sys.exit(1)

print("OK: Environment variables are set")
print()

# 2. Test PostgreSQL server connection
print("[2/5] Testing PostgreSQL server connection...")
try:
    import psycopg2
    
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database='postgres',
        user=db_user,
        password=db_password,
        connect_timeout=5
    )
    print("OK: PostgreSQL server is accessible!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version()")
    version = cursor.fetchone()[0]
    print(f"   Version: {version.split(',')[0]}")
    
    cursor.close()
    conn.close()
    print()
    
except psycopg2.OperationalError as e:
    print(f"ERROR: Cannot connect to PostgreSQL server!")
    print(f"   Error: {e}")
    print()
    print("Solutions:")
    print("  1. Check if PostgreSQL service is running")
    print("     Windows + R -> services.msc -> search 'postgresql'")
    print("  2. Check password in .env file")
    print("  3. Check port number (default: 5432)")
    print()
    sys.exit(1)

# 3. Check if database exists
print(f"[3/5] Checking if '{db_name}' database exists...")
try:
    import psycopg2
    
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database='postgres',
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (db_name,)
    )
    exists = cursor.fetchone()
    
    if exists:
        print(f"OK: '{db_name}' database exists.")
    else:
        print(f"ERROR: '{db_name}' database does not exist!")
        print()
        print("Solution:")
        print("  python create_database.py")
        print()
        cursor.close()
        conn.close()
        sys.exit(1)
    
    cursor.close()
    conn.close()
    print()
    
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

# 4. Test direct connection to database
print(f"[4/5] Testing direct connection to '{db_name}'...")
try:
    import psycopg2
    
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    print(f"OK: Connected to '{db_name}' successfully!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT current_database()")
    current_db = cursor.fetchone()[0]
    print(f"   Current database: {current_db}")
    
    # Check tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    
    if tables:
        print(f"   Tables found: {len(tables)}")
        print("   Table list:")
        for table in tables:
            print(f"      - {table[0]}")
    else:
        print("   WARNING: No tables found.")
        print("      Run: python init_database.py")
    
    cursor.close()
    conn.close()
    print()
    
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

# 5. Test asyncpg connection
print("[5/5] Testing asyncpg (async) connection...")
try:
    import asyncio
    import asyncpg
    
    async def test_asyncpg():
        try:
            conn = await asyncpg.connect(
                host=db_host,
                port=int(db_port),
                database=db_name,
                user=db_user,
                password=db_password,
                timeout=10
            )
            
            version = await conn.fetchval('SELECT version()')
            print(f"OK: asyncpg connection successful!")
            print(f"   {version.split(',')[0]}")
            
            await conn.close()
            return True
            
        except Exception as e:
            print(f"ERROR: asyncpg connection failed!")
            print(f"   Error: {e}")
            print()
            print("This is the driver used by FastAPI server.")
            print("If this fails, the API server will not work.")
            return False
    
    success = asyncio.run(test_asyncpg())
    print()
    
    if not success:
        sys.exit(1)
        
except ImportError as e:
    print(f"ERROR: Required package not installed")
    print(f"   {e}")
    print("   Run: pip install asyncpg")
    print()
    sys.exit(1)

# Final result
print("="*60)
print("SUCCESS: All diagnostics passed!")
print("="*60)
print()
print("Database connection is working properly.")
print("You can now start the FastAPI server:")
print("  uvicorn app.main:app --reload")
print()

