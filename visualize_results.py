import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_visuals():
    print("🎨 Generating Visualizations...")
    
    # Load Data
    try:
        df = pd.read_csv("valuation_model_input.csv")
    except FileNotFoundError:
        print("❌ valuation_model_input.csv not found. Run pipeline.py first.")
        return

    # Data Cleaning for Visualization
    # Convert Tokyo JPY to USD (Approx 1 JPY = 0.0067 USD or ~150 JPY/USD)
    conversion_rate = 0.0067
    tky_mask = df['city'] == 'Tokyo'
    
    cols_to_convert = ['nightly_rate', 'annual_revenue_conservative', 'annual_revenue_realistic', 'annual_revenue_optimistic']
    for col in cols_to_convert:
        df.loc[tky_mask, col] = df.loc[tky_mask, col] * conversion_rate


    # Set Style
    sns.set_theme(style="whitegrid")
    
    # 1. Revenue Scenario Comparison (Bar Chart)
    plt.figure(figsize=(10, 6))
    scenario_data = df[['annual_revenue_conservative', 'annual_revenue_realistic', 'annual_revenue_optimistic']].mean()
    scenario_data.index = ['Bear (40%)', 'Base (60%)', 'Bull (80%)']
    ax = sns.barplot(x=scenario_data.index, y=scenario_data.values, palette="viridis")
    plt.title("Expected Annual Revenue per Listing by Occupancy Scenario", fontsize=16)
    plt.ylabel("Annual Revenue ($)", fontsize=12)
    plt.xlabel("Occupancy Scenario", fontsize=12)
    plt.savefig("assets/revenue_scenarios.png")
    print("✅ Created assets/revenue_scenarios.png")
    plt.close()

    # 2. Top 10 Neighbourhoods by Yield (Base Case) - Top 5 from EACH City
    plt.figure(figsize=(12, 8))
    
    # Calculate means per neighbourhood
    nbhd_stats = df.groupby(['city', 'neighbourhood'])['annual_revenue_realistic'].mean().reset_index()
    
    # Get Top 5 for NYC and Top 5 for Tokyo
    nyc_top = nbhd_stats[nbhd_stats['city'] == 'NYC'].sort_values('annual_revenue_realistic', ascending=False).head(5)
    tokyo_top = nbhd_stats[nbhd_stats['city'] == 'Tokyo'].sort_values('annual_revenue_realistic', ascending=False).head(5)
    
    # Combine
    top_neighborhoods = pd.concat([nyc_top, tokyo_top]).sort_values('annual_revenue_realistic', ascending=False)
    
    # Plot with hue to distinguish cities
    sns.barplot(
        data=top_neighborhoods,
        x='annual_revenue_realistic',
        y='neighbourhood',
        hue='city',
        dodge=False,
        palette="magma"
    )
    
    plt.title("Top 5 Most Profitable Neighbourhoods: NYC vs Tokyo (Base Case)", fontsize=16)
    plt.xlabel("Average Annual Revenue ($)", fontsize=12)
    plt.ylabel("Neighbourhood", fontsize=12)
    plt.legend(title="City")
    plt.savefig("assets/top_neighbourhoods.png")
    print("✅ Created assets/top_neighbourhoods.png")
    plt.close()

    # 3. Price Distribution: NYC vs Tokyo
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=df[df['nightly_rate'] < 1000], x="city", y="nightly_rate", palette="muted") # Filter outliers for viz
    plt.title("Nightly Rate Distribution: NYC vs Tokyo (< $1000)", fontsize=16)
    plt.ylabel("Nightly Rate ($)")
    plt.savefig("assets/price_distribution.png")
    print("✅ Created assets/price_distribution.png")
    plt.close()
    
    print("✨ All visualizations generated successfully!")

if __name__ == "__main__":
    generate_visuals()
