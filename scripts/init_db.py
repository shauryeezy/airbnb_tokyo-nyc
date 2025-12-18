import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import config

def init_db():
    """
    Connects to the default 'postgres' database to create the target 'airbnb' database.
    This is necessary because you cannot create a database while connected to it.
    """
    print("🚀 Initializing Database Environment...")
    
    # Connect to 'postgres' system database
    try:
        con = psycopg2.connect(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname='postgres'
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        
        # Check if DB exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{config.DB_NAME}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"🛠 Creating database '{config.DB_NAME}'...")
            cursor.execute(f"CREATE DATABASE {config.DB_NAME}")
            print(f"✅ Database '{config.DB_NAME}' created successfully.")
        else:
            print(f"ℹ️ Database '{config.DB_NAME}' already exists.")
            
        cursor.close()
        con.close()
        
    except Exception as e:
        print(f"❌ Database Initialization Failed: {e}")
        print("Suggestion: fast-check your DB_PASSWORD in config.py")

if __name__ == "__main__":
    init_db()
