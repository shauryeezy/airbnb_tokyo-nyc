import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
import config
import os

def analyze():
    print("==================================================")
    print("🤖 MACHINE LEARNING ANALYSIS (Price Drivers)")
    print("==================================================")
    
    # 1. Connect & Load Data
    print("   Connecting to Database...")
    try:
        engine = create_engine(config.DATABASE_URL)
        # We use the filtered dataset (no outliers) for a robust model
        query = """
        SELECT 
            price_clean as price,
            room_type,
            accommodates,
            reviews,
            rating
        FROM clean_listings 
        WHERE is_outlier = FALSE AND price_clean > 0
        """
        df = pd.read_sql(query, engine)
        print(f"   Loaded {len(df)} statistically valid listings.")
    except Exception as e:
        print(f"❌ DB Connection Failed: {e}")
        return

    if df.empty:
        print("❌ No data found. Run pipeline first.")
        return

    # 2. Preprocessing
    # Selecting predictors
    features = ['room_type', 'accommodates', 'reviews', 'rating']
    target = 'price'
    
    X = df[features]
    y = df[target]
    
    # One-Hot Encoding for Categorical Variables (Room Type)
    # drop_first=True avoids multicollinearity (dummy variable trap)
    X_encoded = pd.get_dummies(X, drop_first=True)
    
    # 3. Model Training
    print("   Training Linear Regression Model...")
    model = LinearRegression()
    model.fit(X_encoded, y)
    r_squared = model.score(X_encoded, y)
    print(f"   Model R² Score: {r_squared:.3f}")
    
    # 4. Feature Importance Extraction
    coefs = pd.DataFrame({
        'Feature': X_encoded.columns,
        'Impact ($)': model.coef_
    }).sort_values(by='Impact ($)', ascending=False)
    
    # Feature Name Cleaning
    name_map = {
        'room_type_Private room': 'Private Room',
        'room_type_Shared room': 'Shared Room',
        'room_type_Hotel room': 'Hotel Status',
        'accommodates': 'Capacity (Guests)',
        'reviews': 'Review Volume',
        'rating': 'Guest Rating'
    }
    coefs['Feature'] = coefs['Feature'].map(name_map).fillna(coefs['Feature'])
    
    print("\n   [Feature Impact Analysis]")
    print(coefs)
    
    # 5. Visualization
    print("   Generating Visualization...")
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")
    
    # Color logic: Green for Price Increases, Red for Price Decreases
    colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in coefs['Impact ($)']]
    
    plot = sns.barplot(data=coefs, x='Impact ($)', y='Feature', palette=colors)
    
    plt.title(f"11. Directional Price Signals (Linear Model, R²={r_squared:.2f})", fontsize=16, fontweight='bold')
    plt.xlabel("Est. Price Impact ($)", fontsize=12)
    plt.ylabel("Listing Benefit ($)", fontsize=12)
    
    # Add subtitle regarding model limitations
    plt.figtext(0.5, 0.01, "Note: Explanatory model only. Coefficients represent average marginal effect, not predictive guarantee.", 
                ha="center", fontsize=10, style='italic', color='gray')
    
    plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    
    # Save
    os.makedirs("assets", exist_ok=True)
    output_path = "assets/11_feature_importance.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"✅ Analysis Complete. Chart saved to: {output_path}")

if __name__ == "__main__":
    analyze()
