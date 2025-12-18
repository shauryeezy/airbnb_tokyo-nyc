import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import traceback

def generate_visuals():
    print("🎨 Step 1: Loading Data...")
    df = pd.read_csv("comprehensive_data.csv")
    print("   Data Loaded. Shape:", df.shape)

    print("🎨 Step 3: Setting Theme...")
    sns.set_theme(style="whitegrid")
    
    print("🎨 Step 4: Plotting Chart 1 to 10...")
    
    # 1. Revenue Scenarios
    try:
        if 'annual_revenue_conservative' not in df.columns:
            df['annual_revenue_conservative'] = df['annual_revenue'] * 0.66
            df['annual_revenue_optimistic'] = df['annual_revenue'] * 1.33
            
        plt.figure(figsize=(10, 6))
        scenario_data = df[['annual_revenue_conservative', 'annual_revenue', 'annual_revenue_optimistic']].mean()
        scenario_data.index = ['Bear (40%)', 'Base (60%)', 'Bull (80%)']
        sns.barplot(x=scenario_data.index, y=scenario_data.values, palette="viridis")
        plt.title("1. Annual Revenue Scenarios (Global Avg)")
        plt.savefig("assets/1_revenue_scenarios.png")
        plt.close()
        print("   Chart 1 OK.")
    except Exception:
        print("   Chart 1 Failed.")
        traceback.print_exc()

    # 2. Top 10 Neighbourhoods (NYC)
    try:
        plt.figure(figsize=(12, 8))
        nbhd_stats = df.groupby('neighbourhood')['annual_revenue'].mean().reset_index()
        top_neighborhoods = nbhd_stats.sort_values('annual_revenue', ascending=False).head(10)
        sns.barplot(data=top_neighborhoods, x='annual_revenue', y='neighbourhood', palette="magma")
        plt.title("2. Top 10 Most Profitable NYC Neighbourhoods")
        plt.xlabel("Avg Annual Revenue ($)")
        plt.savefig("assets/2_top_neighbourhoods.png")
        plt.close()
        print("   Chart 2 OK.")
        print("   Chart 2 OK.")
    except Exception:
        print("   Chart 2 Failed.")
        traceback.print_exc()

    # 3. Price Distribution
    try:
        plt.figure(figsize=(10, 6))
        # Data is already statistically filtered via IQR in transformation layer
        sns.violinplot(data=df, y="nightly_rate", palette="muted")
        plt.title("3. Nightly Rate Distribution (Statistically Cleaned)")
        plt.ylabel("Nightly Rate ($)")
        plt.savefig("assets/3_price_distribution.png")
        plt.close()
        print("   Chart 3 OK.")
    except Exception:
        print("   Chart 3 Failed.")
        traceback.print_exc()

    # 4. Room Types (Already done)

    # 5. Avg Price by Room Type
    try:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='room_type', y='nightly_rate', palette="coolwarm")
        plt.title("5. Cost of Living: Avg Nightly Rate by Room Type")
        plt.ylabel("Avg Price ($)")
        plt.savefig("assets/5_price_by_room.png")
        plt.close()
        print("   Chart 5 OK.")
    except Exception:
        print("   Chart 5 Failed.")
        traceback.print_exc()

    # 6. Review Volume vs Price
    try:
        plt.figure(figsize=(10, 6))
        sample = df[df['reviews'] < 500].sample(min(5000, len(df)))
        sns.scatterplot(data=sample, x='nightly_rate', y='reviews', alpha=0.5, size='rating')
        plt.title("6. Value Seeking: Do Cheaper Listings Get More Reviews?")
        plt.savefig("assets/6_price_vs_reviews.png")
        plt.close()
        print("   Chart 6 OK.")
    except Exception:
        print("   Chart 6 Failed.")
        traceback.print_exc()

    # 7. Rating Traffic Light
    try:
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df[df['rating'] > 0], x='rating', bins=20, kde=True, palette="husl")
        plt.title("7. Quality Control: Guest Rating Distribution")
        plt.xlabel("Rating (0-5)")
        plt.savefig("assets/7_rating_dist.png")
        plt.close()
        print("   Chart 7 OK.")
    except Exception:
        print("   Chart 7 Failed.")
        traceback.print_exc()

    # 8. Accommodation Capacity
    try:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df[df['accommodates'] <= 10], y='accommodates', palette="Set2")
        plt.title("8. Group Size Capacity: Person Count per Listing")
        plt.savefig("assets/8_accommodates.png")
        plt.close()
        print("   Chart 8 OK.")
    except Exception:
        print("   Chart 8 Failed.")
        traceback.print_exc()

    # 9. Revenue Share by Property Type
    try:
        plt.figure(figsize=(10, 8))
        rev_share = df.groupby('property_type')['annual_revenue'].sum().sort_values(ascending=False).head(10)
        sns.barplot(y=rev_share.index, x=rev_share.values, palette="Blues_d")
        plt.title("9. Market Drivers: Total Revenue by Property Type (Top 10)")
        plt.xlabel("Total Market Revenue ($)")
        plt.savefig("assets/9_revenue_share.png")
        plt.close()
        print("   Chart 9 OK.")
    except Exception:
        print("   Chart 9 Failed.")
        traceback.print_exc()

    # 10. Top 10 Most Reviewed Neighbourhoods
    try:
        plt.figure(figsize=(12, 6))
        pop_hoods = df.groupby('neighbourhood')['reviews'].sum().sort_values(ascending=False).head(10)
        sns.barplot(x=pop_hoods.index, y=pop_hoods.values, palette="summer")
        plt.xticks(rotation=45)
        plt.title("10. Tourist Hotspots: Neighborhoods with Most Reviews")
        plt.ylabel("Total Reviews")
        plt.savefig("assets/10_popular_neighbourhoods.png")
        plt.close()
        print("   Chart 10 OK.")
    except Exception:
        print("   Chart 10 Failed.")
        traceback.print_exc()

    # 12. Correlation Heatmap (New)
    try:
        plt.figure(figsize=(10, 8))
        corr_cols = ['nightly_rate', 'reviews', 'rating', 'accommodates', 'annual_revenue']
        # Filter for numeric columns just in case
        valid_cols = [c for c in corr_cols if c in df.columns]
        corr = df[valid_cols].corr()
        
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("12. Market Dynamics: Correlation Matrix (Price vs Performance)")
        plt.tight_layout()
        plt.savefig("assets/12_correlation_matrix.png")
        plt.close()
        print("   Chart 12 OK.")
    except Exception:
        print("   Chart 12 Failed.")
        traceback.print_exc()


    # 13. RevPAR Analysis (High Yield Scatter)
    try:
        plt.figure(figsize=(10, 6))
        # Filter noise: RevPAR < 300 to show the dense cluster
        sns.scatterplot(data=df[df['revpar'] < 300], x='nightly_rate', y='revpar', hue='room_type', alpha=0.6, palette="deep")
        plt.title("13. Cash Cows: Price vs RevPAR (Revenue Per Available Night)")
        plt.xlabel("Nightly Price ($)")
        plt.ylabel("RevPAR ($)")
        plt.plot([0, 300], [0, 300], ls="--", c=".3") # Diagonal line
        plt.savefig("assets/13_revpar_scatter.png")
        plt.close()
        print("   Chart 13 OK.")
    except Exception:
        print("   Chart 13 Failed.")
        traceback.print_exc()

    # 15. Seasonality Analysis
    try:
        season_df = pd.read_csv("seasonal_trends.csv")
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=season_df, x='month_year', y='avg_price', marker="o", color="crimson")
        plt.xticks(rotation=45)
        plt.title("15. Seasonality: 12-Month Price Forecast")
        plt.ylabel("Avg Listing Price ($)")
        plt.grid(True)
        plt.savefig("assets/15_seasonality_trend.png")
        plt.close()
        print("   Chart 15 OK.")
    except Exception:
        print("   Chart 15 Failed.")
        traceback.print_exc()

    # 16. Geospatial Map (Static Scatter)
    try:
        plt.figure(figsize=(10, 10))
        # Scatterplot of Lat/Lon, colored by Price (log scale for visibility)
        # Filter extremely expensive ones for better color contrast
        map_df = df[df['nightly_rate'] < 500] 
        sns.scatterplot(data=map_df, x='longitude', y='latitude', hue='nightly_rate', palette="viridis", size='revpar', sizes=(10, 200), alpha=0.6)
        plt.title("16. Investment Map: High RevPAR Zones")
        plt.axis('equal') # Keep map aspect ratio
        plt.savefig("assets/16_geospatial_map.png")
        plt.close()
        print("   Chart 16 OK.")
    except Exception:
        print("   Chart 16 Failed.")
        traceback.print_exc()
        
if __name__ == "__main__":
    generate_visuals()
