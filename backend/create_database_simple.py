"""
PostgreSQL Database Creation Script (Simple Version)
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

def create_database():
    """Create orderbean_db database"""
    
    # Get settings from environment variables
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'orderbean_db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgresql')
    
    print("\n" + "="*60)
    print("PostgreSQL Database Creation")
    print("="*60)
    print()
    print("Database Settings:")
    print(f"   Host: {db_host}")
    print(f"   Port: {db_port}")
    print(f"   Database: {db_name}")
    print(f"   User: {db_user}")
    print()
    
    try:
        # Connect to postgres database (default)
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database='postgres',
            user=db_user,
            password=db_password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("   OK: Connected successfully!")
        print()
        
        # Check if database exists
        print(f"Checking if '{db_name}' database exists...")
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        exists = cursor.fetchone()
        
        if exists:
            print(f"   WARNING: '{db_name}' database already exists.")
            print()
            
            response = input("   Drop existing database and create new one? (y/N): ")
            if response.lower() == 'y':
                print(f"\nDropping '{db_name}' database...")
                # Terminate active connections
                cursor.execute(f"""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = '{db_name}'
                    AND pid <> pg_backend_pid()
                """)
                # Drop database
                cursor.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
                print("   OK: Dropped!")
                
                # Create new database
                print(f"\nCreating '{db_name}' database...")
                cursor.execute(f'CREATE DATABASE "{db_name}"')
                print("   OK: Created!")
            else:
                print("\n   Using existing database.")
        else:
            # Create database
            print(f"Creating '{db_name}' database...")
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print("   OK: Created!")
        
        cursor.close()
        conn.close()
        
        print()
        print("="*60)
        print("SUCCESS: Database is ready!")
        print("="*60)
        print()
        print("Next steps:")
        print("  1. Create tables: python init_database.py")
        print("  2. Test connection: python test_db_connection.py")
        print("  3. Start server: uvicorn app.main:app --reload")
        print()
        
        return True
        
    except psycopg2.OperationalError as e:
        print("\n" + "="*60)
        print("ERROR: PostgreSQL Connection Failed!")
        print("="*60)
        print(f"Error: {e}")
        print()
        print("Solutions:")
        print("  1. Check if PostgreSQL service is running")
        print("     - Windows: services.msc -> search 'postgresql'")
        print()
        print("  2. Check database settings in .env file")
        print(f"     DB_HOST={db_host}")
        print(f"     DB_PORT={db_port}")
        print(f"     DB_USER={db_user}")
        print(f"     DB_PASSWORD=******")
        print()
        print("  3. Verify PostgreSQL installation")
        print("     - Run pgAdmin")
        print("     - Or check: psql --version")
        print()
        
        return False
        
    except Exception as e:
        print("\n" + "="*60)
        print("ERROR: Unexpected error!")
        print("="*60)
        print(f"Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        
        return False


if __name__ == "__main__":
    success = create_database()
    exit(0 if success else 1)

