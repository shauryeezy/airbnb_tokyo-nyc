import pandas as pd
from sqlalchemy import create_engine
import config

def export_comprehensive_data():
    """
    Exports a rich dataset including room types, ratings, and capacity 
    to support the expanded '10 Insights' dashboard.
    """
    print("⏳ Starting Extended Data Export...")
    
    try:
        engine = create_engine(config.DATABASE_URL)
        connection = engine.connect()
        connection.close()
    except Exception as e:
        print(f"❌ DB Connection Failed: {e}")
        return

    # Joining clean_listings (Profile) with yield_analysis (Financials)
    query = """
    SELECT 
        cl.id,
        cl.city,
        cl.neighbourhood,
        cl.room_type,
        cl.property_type,
        cl.accommodates,
        cl.rating,
        cl.reviews,
        ya.price_clean as nightly_rate,
        ya.revenue_base as annual_revenue
    FROM clean_listings cl
    JOIN yield_analysis ya ON cl.id = ya.id
    """
    
    try:
        print("⏳ Extracting comprehensive dataset...")
        df = pd.read_sql(query, engine)
        
        output_file = "comprehensive_data.csv"
        df.to_csv(output_file, index=False)
        
        print(f"✅ Successfully exported {len(df)} records to '{output_file}'.")
        print("📊 Ready for visualization engine.")
        
    except Exception as e:
        print(f"❌ Export Failed: {e}")

if __name__ == "__main__":
    export_comprehensive_data()
