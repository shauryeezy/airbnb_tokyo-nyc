-- 1. Cleaner: Create a unified 'clean_listings' table
-- Standardizing for NYC Market by casting price and handling nulls
DROP TABLE IF EXISTS clean_listings;

CREATE TABLE clean_listings AS
SELECT 
    'NYC' as city,
    id,
    name,
    neighbourhood_cleansed as neighbourhood,
    latitude,
    longitude,
    property_type,
    room_type,
    accommodates,
    CAST(NULLIF(regexp_replace(price, '[^0-9.]', '', 'g'), '') AS FLOAT) as price_clean,
    COALESCE(minimum_nights, 1) as minimum_nights,
    COALESCE(number_of_reviews, 0) as reviews,
    COALESCE(review_scores_rating, 0) as rating,
    COALESCE(reviews_per_month, 0) as reviews_per_month
FROM raw_listings_nyc;

-- 1.1 Outlier Detection (Statistical IQR Method)
-- Why? To ensure analysis is based on valid data distributions, not skewed by extremes
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
