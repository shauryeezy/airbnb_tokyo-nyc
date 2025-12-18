import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import traceback

def generate_visuals():
    print("🎨 Step 1: Loading Data...")
    df = pd.read_csv("comprehensive_data.csv")
    print("   Data Loaded. Shape:", df.shape)

    print("🎨 Step 2: Converting Currency...")
    tky_mask = df['city'] == 'Tokyo'
    conversion_rate = 0.0067
    for col in ['nightly_rate', 'annual_revenue']:
        if col in df.columns:
            df.loc[tky_mask, col] = df.loc[tky_mask, col] * conversion_rate
    print("   Currency Converted.")

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

    # 2. Top 5 Neighbourhoods (Split City)
    try:
        plt.figure(figsize=(12, 8))
        nbhd_stats = df.groupby(['city', 'neighbourhood'])['annual_revenue'].mean().reset_index()
        nyc_top = nbhd_stats[nbhd_stats['city'] == 'NYC'].sort_values('annual_revenue', ascending=False).head(5)
        tokyo_top = nbhd_stats[nbhd_stats['city'] == 'Tokyo'].sort_values('annual_revenue', ascending=False).head(5)
        top_neighborhoods = pd.concat([nyc_top, tokyo_top]).sort_values('annual_revenue', ascending=False)
        sns.barplot(data=top_neighborhoods, x='annual_revenue', y='neighbourhood', hue='city', dodge=False, palette="magma")
        plt.title("2. Top 5 Most Profitable Neighbourhoods: NYC vs Tokyo")
        plt.savefig("assets/2_top_neighbourhoods.png")
        plt.close()
        print("   Chart 2 OK.")
    except Exception:
        print("   Chart 2 Failed.")
        traceback.print_exc()

    # 3. Price Distribution
    try:
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=df[df['nightly_rate'] < 1000], x="city", y="nightly_rate", palette="muted")
        plt.title("3. Nightly Rate Distribution (<$1000)")
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
        sns.barplot(data=df, x='room_type', y='nightly_rate', hue='city', palette="coolwarm")
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
        sample = df[(df['nightly_rate'] < 1000) & (df['reviews'] < 500)].sample(min(5000, len(df)))
        sns.scatterplot(data=sample, x='nightly_rate', y='reviews', hue='city', alpha=0.5, size='rating')
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
        sns.histplot(data=df[df['rating'] > 0], x='rating', bins=20, hue='city', kde=True, palette="husl")
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
        sns.boxplot(data=df[df['accommodates'] <= 10], x='city', y='accommodates', palette="Set2")
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


if __name__ == "__main__":
    generate_visuals()
