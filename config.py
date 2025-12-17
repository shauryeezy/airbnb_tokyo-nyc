import os

# Database Configuration
# NOTE: User must set DB_PASSWORD environment variable or update the default below for local setup
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgre1256") # Updated with user provided password
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "airbnb")

# PostgreSQL Connection String
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# File Paths
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "listings_tokyo.csv": "raw_listings_tokyo",
    "listings_nyc.csv": "raw_listings_nyc",
    "calendar_tokyo.csv": "raw_calendar_tokyo",
    "calendar_nyc.csv": "raw_calendar_nyc"
}
