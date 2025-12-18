import pandas as pd
from sqlalchemy import create_engine
import os
import config

def load_data():
    """
    Orchestrates the EL (Extract-Load) process.
    Reads raw CSVs in chunks and writes to PostgreSQL.
    """
    print("🚀 Starting Data Ingestion...")
    
    # Establish Connection
    try:
        engine = create_engine(config.DATABASE_URL)
        connection = engine.connect()
        print(f"✅ Connected to PostgreSQL database: {config.DB_NAME}")
        connection.close()
    except Exception as e:
        print(f"❌ Failed to connect to DB. Ensure PostgreSQL is running and credentials in config.py are correct.\nError: {e}")
        return

    # Ingestion Loop
    for filename, table_name in config.FILES.items():
        file_path = os.path.join(config.DATA_DIR, filename)
        
        if not os.path.exists(file_path):
            print(f"⚠️ Warning: {filename} not found. Skipping.")
            continue

        print(f"📥 Loading {filename} into '{table_name}'...")
        
        # Chunking Strategy for Memory Management
        chunksize = 100000
        count = 0
        
        try:
            for chunk in pd.read_csv(file_path, chunksize=chunksize, low_memory=False):
                # 'replace' for the first chunk, 'append' for subsequent chunks
                if_exists = 'replace' if count == 0 else 'append'
                
                chunk.to_sql(table_name, engine, if_exists=if_exists, index=False, method='multi')
                
                count += 1
                print(f"   Processed {count * chunksize} rows...", end='\r')
            
            print(f"\n✅ Finished loading {table_name} ({count} chunks).")
            
        except Exception as e:
            print(f"\n❌ Error loading {filename}: {e}")

    print("🏁 Ingestion Complete.")

if __name__ == "__main__":
    load_data()
