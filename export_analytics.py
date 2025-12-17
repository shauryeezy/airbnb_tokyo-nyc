import pandas as pd
from sqlalchemy import create_engine
import config

def export_valuation_model():
    """
    Exports clean listing data along with Sensitivity Analysis scenarios 
    to a CSV file for downstream reporting (Tableau/Power BI).
    """
    print("⏳ Starting Analytics Export...")
    
    try:
        engine = create_engine(config.DATABASE_URL)
        connection = engine.connect() # Verify connection
        connection.close()
    except Exception as e:
        print(f"❌ DB Connection Failed: {e}")
        return

    # Fetching the Sensitivity Analysis Data
    query = """
    SELECT 
        id, 
        city,
        neighbourhood, 
        price_clean as nightly_rate, 
        revenue_bear as annual_revenue_conservative,
        revenue_base as annual_revenue_realistic,
        revenue_bull as annual_revenue_optimistic
    FROM yield_analysis 
    """
    
    try:
        print("⏳ Extracting data from PostgreSQL using Pandas...")
        df = pd.read_sql(query, engine)
        
        output_file = "valuation_model_input.csv"
        df.to_csv(output_file, index=False)
        
        print(f"✅ Successfully exported {len(df)} records to '{output_file}'.")
        print("📊 This file is ready for Power BI/Tableau ingestion.")
        
    except Exception as e:
        print(f"❌ Export Failed: {e}")

if __name__ == "__main__":
    export_valuation_model()
