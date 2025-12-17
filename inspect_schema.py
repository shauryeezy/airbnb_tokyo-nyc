from sqlalchemy import create_engine, text
import config

def inspect():
    engine = create_engine(config.DATABASE_URL)
    with engine.connect() as conn:
        # Get column details for raw_listings_nyc
        res = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'raw_listings_nyc'"))
        for row in res:
            if row[0] in ['id', 'price', 'number_of_reviews', 'review_scores_rating', 'reviews_per_month']:
                print(f"{row[0]}: {row[1]}")

if __name__ == "__main__":
    inspect()
