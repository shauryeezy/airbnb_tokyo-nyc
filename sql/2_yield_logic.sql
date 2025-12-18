-- 2. Yield Analysis (Sensitivity Modeling)
-- Purpose: Calculate RevPAR and projected revenue based on occupancy assumptions.
DROP TABLE IF EXISTS yield_analysis;

CREATE TABLE yield_analysis AS
SELECT 
    city,
    neighbourhood,
    id,
    price_clean,
    -- Occupancy Rate Estimation (Heuristic: 50% review rate, min stay)
    -- Formula: (Reviews/Month / 0.5) * Min_Nights / 30
    -- We cap it at 0.70 (70%) to be conservative and realistic
    LEAST(
        (reviews_per_month / 0.5) * minimum_nights / 30.0, 
        0.70
    ) as occupancy_rate,
    
    -- RevPAR = Price * Occupancy
    (price_clean * LEAST((reviews_per_month / 0.5) * minimum_nights / 30.0, 0.70)) as revpar,

    -- Sensitivity Scenarios (Bear/Base/Bull)
    (price_clean * 365 * 0.40) as revenue_bear,
    (price_clean * 365 * 0.60) as revenue_base,
    (price_clean * 365 * 0.80) as revenue_bull
FROM clean_listings
WHERE price_clean > 0 AND is_outlier = FALSE;

-- 2.1 Seasonality Analysis
-- Analyzing average price trends by month
DROP TABLE IF EXISTS seasonality_stats;
CREATE TABLE seasonality_stats AS
SELECT
    TO_CHAR(date::DATE, 'YYYY-MM') as month_year,
    AVG(CAST(NULLIF(regexp_replace(price::TEXT, '[^0-9.]', '', 'g'), '') AS FLOAT)) as avg_price
FROM raw_calendar_nyc
WHERE available = 't'
GROUP BY 1
ORDER BY 1;
