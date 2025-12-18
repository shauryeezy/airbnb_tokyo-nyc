from sqlalchemy import create_engine, text
import config

def run_query(query_text, engine):
    """Executes a list of SQL statements separated by semicolons."""
    statements = [s.strip() for s in query_text.split(';') if s.strip()]
    with engine.begin() as conn:  # Transactional context
        for stmt in statements:
            print(f"Executing: {stmt[:50]}...")
            conn.execute(text(stmt))
    print("Query set executed.\n")

def transform():
    print("🚀 Starting SQL Transformations & Analytics...")
    
    try:
        engine = create_engine(config.DATABASE_URL)
    except Exception as e:
        print(f"❌ DB Connection Failed: {e}")
        return

    # 1. Cleaner: Create a unified 'clean_listings' table
    # Standardizing for NYC Market
    clean_sql = """
    DROP TABLE IF EXISTS clean_listings;
    
    CREATE TABLE clean_listings AS
    SELECT 
        'NYC' as city,
        id,
        name,
        neighbourhood_cleansed as neighbourhood,
        property_type,
        room_type,
        accommodates,
        CAST(NULLIF(regexp_replace(price, '[^0-9.]', '', 'g'), '') AS FLOAT) as price_clean,
        COALESCE(number_of_reviews, 0) as reviews,
        COALESCE(review_scores_rating, 0) as rating,
        COALESCE(reviews_per_month, 0) as reviews_per_month
    FROM raw_listings_nyc;
    """
    
    # 2. Yield Analysis (Sensitivity Modeling)
    # Replacing "Approximations" with Scenarios: Bear(40%), Base(60%), Bull(80%)
    yield_sql = """
    DROP TABLE IF EXISTS yield_analysis;
    
    CREATE TABLE yield_analysis AS
    SELECT 
        city,
        neighbourhood,
        id,
        price_clean,
        -- RevPAR = Price * Occupancy Rate
        (price_clean * 365 * 0.40) as revenue_bear,
        (price_clean * 365 * 0.60) as revenue_base,
        (price_clean * 365 * 0.80) as revenue_bull
    FROM clean_listings
    WHERE price_clean > 0;
    """
    
    # 3. Aggregation: Create 'neighbourhood_stats'
    stats_sql = """
    DROP TABLE IF EXISTS neighbourhood_stats;
    
    CREATE TABLE neighbourhood_stats AS
    SELECT 
        city,
        neighbourhood,
        COUNT(*) as total_listings,
        AVG(price_clean) as avg_price,
        AVG(revenue_base) as avg_annual_revenue, -- Using Base case for general reporting
        AVG(rating) as avg_rating
    FROM yield_analysis
    JOIN clean_listings USING(id, city, neighbourhood, price_clean)
    GROUP BY city, neighbourhood;
    """

    print("Step 1: Cleaning & Unifying Schemas...")
    run_query(clean_sql, engine)

    # 1.1 Outlier Detection (Statistical IQR Method)
    # Why? To ensure analysis is based on valid data distributions, not skewed by extremes
    print("Step 1.1: Detecting Statistical Outliers (IQR Method)...")
    outlier_sql = """
    ALTER TABLE clean_listings ADD COLUMN is_outlier BOOLEAN DEFAULT FALSE;

    WITH city_stats AS (
        SELECT 
            city,
            percentile_cont(0.25) WITHIN GROUP (ORDER BY price_clean) as p25,
            percentile_cont(0.75) WITHIN GROUP (ORDER BY price_clean) as p75
        FROM clean_listings
        WHERE price_clean > 0
        GROUP BY city
    )
    UPDATE clean_listings cl
    SET is_outlier = TRUE
    FROM city_stats cs
    WHERE cl.city = cs.city
    AND (
        cl.price_clean < (cs.p25 - 1.5 * (cs.p75 - cs.p25)) OR 
        cl.price_clean > (cs.p75 + 1.5 * (cs.p75 - cs.p25))
    );
    """
    run_query(outlier_sql, engine)
    
    print("Step 2: Conducting Yield Analysis (Sensitivity Modeling)...")
    # Updated to exclude outliers from financial projections
    yield_sql_updated = """
    DROP TABLE IF EXISTS yield_analysis;
    
    CREATE TABLE yield_analysis AS
    SELECT 
        city,
        neighbourhood,
        id,
        price_clean,
        (price_clean * 365 * 0.40) as revenue_bear,
        (price_clean * 365 * 0.60) as revenue_base,
        (price_clean * 365 * 0.80) as revenue_bull
    FROM clean_listings
    WHERE price_clean > 0 AND is_outlier = FALSE;
    """
    run_query(yield_sql_updated, engine)
    
    print("Step 3: Aggregating Neighborhood Statistics...")
    run_query(stats_sql, engine)
    
    print("✅ Transformations & Analytics Complete!")

if __name__ == "__main__":
    transform()
