import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import traceback

import numpy as np

def generate_visuals():
    print("🎨 Step 1: Loading Data...")
    df = pd.read_csv("comprehensive_data.csv")
    print("   Data Loaded. Shape:", df.shape)

    # Global Theme
    sns.set_theme(style="white", context="talk") # Clean white background
    
    # 🥇 1. Neighborhood Strategy (Scatter: Volume vs Efficiency)
    try:
        # Aggregation
        nbhd_stats = df.groupby('neighbourhood').agg({
            'annual_revenue': 'sum',
            'id': 'count'
        }).reset_index()
        nbhd_stats['revenue_per_listing'] = nbhd_stats['annual_revenue'] / nbhd_stats['id']
        
        # Filter sparse neighborhoods
        nbhd_stats = nbhd_stats[nbhd_stats['id'] > 50] # Reasonable sample size
        
        plt.figure(figsize=(10, 8))
        
        # Plot
        p = sns.scatterplot(
            data=nbhd_stats, 
            x='annual_revenue', 
            y='revenue_per_listing', 
            size='id', 
            sizes=(50, 500), 
            alpha=0.7, 
            hue='revenue_per_listing', 
            palette='viridis',
            legend=False
        )
        
        # Annotate Top Performers
        top_efficiency = nbhd_stats.sort_values('revenue_per_listing', ascending=False).head(5)
        top_volume = nbhd_stats.sort_values('annual_revenue', ascending=False).head(5)
        to_annotate = pd.concat([top_efficiency, top_volume]).drop_duplicates()
        
        for line in range(0, to_annotate.shape[0]):
             p.text(
                 to_annotate.annual_revenue.iloc[line], 
                 to_annotate.revenue_per_listing.iloc[line]+1000, 
                 to_annotate.neighbourhood.iloc[line], 
                 horizontalalignment='center', 
                 size='small', 
                 color='black', 
                 weight='semibold'
             )

        plt.title("1. Market Matrix: Identifying 'Cash Cows'", fontweight='bold')
        plt.xlabel("Total Market Revenue (Volume)", fontweight='bold')
        plt.ylabel("Avg Revenue Per Listing (Efficiency)", fontweight='bold')
        
        # Add Quadrant Text
        plt.axhline(nbhd_stats['revenue_per_listing'].median(), color='gray', linestyle='--', alpha=0.3)
        plt.axvline(nbhd_stats['annual_revenue'].median(), color='gray', linestyle='--', alpha=0.3)
        
        plt.text(nbhd_stats['annual_revenue'].max(), nbhd_stats['revenue_per_listing'].max(), "High Eff / High Vol\n(Cash Cows)", ha='right', va='top', color='green', fontweight='bold')
        plt.text(0, 0, "Low Eff / Low Vol\n(Avoid)", ha='left', va='bottom', color='red', padding=10)
        
        # Format Axis
        current_values = plt.gca().get_xticks()
        plt.gca().set_xticklabels(['${:,.0f}M'.format(x/1000000) for x in current_values])
        
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.tight_layout()
        plt.savefig("assets/1_top_revenue_hoods.png")
        plt.close()
        print("   Chart 1 OK.")
    except Exception:
        print("   Chart 1 Failed.")
        traceback.print_exc()

    # 🥈 2. Room Efficiency (Clean Bar Chart)
    try:
        plt.figure(figsize=(10, 6))
        
        # Filter
        clean_df = df[df['room_type'] != 'Hotel room']
        
        # Aggregation with N count
        efficiency = clean_df.groupby('room_type').agg({
            'revpar': 'mean',
            'id': 'count'
        }).reset_index()
        
        # Plot
        ax = sns.barplot(data=efficiency, x='room_type', y='revpar', palette="Blues_d")
        
        # Annotate
        for i, row in efficiency.iterrows():
            ax.text(i, row['revpar'] + 2, f"${row['revpar']:.0f}\n(n={row['id']})", 
                    ha='center', va='bottom', fontweight='bold', fontsize=12)
            
        plt.title("2. Asset Efficiency: RevPAR Comparison", fontweight='bold')
        
        # Remove Y-Axis (Data-Ink Ratio)
        plt.ylabel("")
        plt.yticks([]) 
        plt.xlabel("")
        sns.despine(left=True) # Remove left spine
        
        plt.figtext(0.5, 0.05, "Insight: Entire Homes generate highest yield per unit.", ha="center", style='italic')
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        plt.savefig("assets/2_room_efficiency.png")
        plt.close()
        print("   Chart 2 OK.")
    except Exception:
        print("   Chart 2 Failed.")
        traceback.print_exc()

    # 🥉 3. Price vs Occupancy (Low Alpha)
    try:
        plt.figure(figsize=(10, 8))
        
        # Filter outliers for clean Viz
        viz_df = df[(df['nightly_rate'] < 500) & (df['occupancy_rate'] > 0)].copy()
        p90_revpar = viz_df['revpar'].quantile(0.90)
        viz_df['is_top_performer'] = viz_df['revpar'] > p90_revpar
        
        # Plot (Fade non-performers to create heat map effect)
        sns.scatterplot(
            data=viz_df[~viz_df['is_top_performer']], 
            x='nightly_rate', 
            y='occupancy_rate', 
            color='#95a5a6', 
            alpha=0.1, # Critical fix
            s=40, 
            label='Standard Listings'
        )
        
        sns.scatterplot(
            data=viz_df[viz_df['is_top_performer']], 
            x='nightly_rate', 
            y='occupancy_rate', 
            color='#2ecc71', 
            alpha=0.8, 
            s=60, 
            label='Top 10% Yield'
        )
        
        # Annotate Optimal Zone
        opt_price = viz_df[viz_df['is_top_performer']]['nightly_rate'].median()
        plt.axvline(opt_price, color='#27ae60', linestyle='--', alpha=0.5)
        
        props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='#2ecc71')
        plt.text(opt_price + 20, 0.9, f"Optimal Band:\n~${opt_price-30:.0f} - ${opt_price+30:.0f}", 
                 bbox=props, fontsize=11, color='#27ae60', fontweight='bold')

        plt.title("3. Pricing Strategy: Efficiency Frontier", fontweight='bold')
        plt.xlabel("Nightly Price ($)")
        plt.ylabel("Est. Occupancy Rate")
        sns.despine()
        
        plt.legend(loc='upper right', frameon=True)
        plt.tight_layout()
        plt.savefig("assets/3_price_vs_occupancy.png")
        plt.close()
        print("   Chart 3 OK.")
    except Exception:
        print("   Chart 3 Failed.")
        traceback.print_exc()

    # 🏅 4. Illustrative Revenue Scenarios
    try:
        plt.figure(figsize=(10, 6))
        
        p25 = df['annual_revenue'].quantile(0.25)
        p50 = df['annual_revenue'].median()
        p75 = df['annual_revenue'].quantile(0.75)
        
        scenarios = pd.DataFrame({
            'Scenario': ['Conservative (P25)', 'Base (Median)', 'Aggressive (P75)'],
            'Revenue': [p25, p50, p75]
        })
        
        colors = ["#7f8c8d", "#2980b9", "#27ae60"]
        
        ax = sns.barplot(data=scenarios, x='Scenario', y='Revenue', palette=colors)
        
        for i, v in enumerate(scenarios['Revenue']):
            ax.text(i, v + 500, f"${v:,.0f}", ha='center', va='bottom', fontweight='bold', fontsize=14)

        plt.title("4. Investment Benchmarks: Illustrative Revenue Scenarios", fontweight='bold')
        plt.ylabel("")
        plt.yticks([])
        plt.xlabel("")
        sns.despine(left=True)
        
        plt.figtext(0.5, 0.02, "Note: Based on actual historical performance percentiles (P25/P50/P75) of the NYC dataset.", 
                    ha="center", fontsize=10, style='italic', color='gray')
        
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        plt.savefig("assets/4_revenue_scenarios.png")
        plt.close()
        print("   Chart 4 OK.")
    except Exception:
        print("   Chart 4 Failed.")
        traceback.print_exc()



    # 🏅 6. Pricing Strategy Table (Clean Design)
    try:
        stats = df['nightly_rate'].describe(percentiles=[0.25, 0.5, 0.75, 0.90])
        
        table_data = [
            ["Budget Strategy (P25)", f"${stats['25%']:.0f}"],
            ["Market Median",      f"${stats['50%']:.0f}"],
            ["Premium Tier (P75)",  f"${stats['75%']:.0f}"],
            ["Luxury Tier (P90)",   f"${stats['90%']:.0f}"]
        ]
        
        fig, ax = plt.subplots(figsize=(8, 3)) # Wider
        ax.axis('tight')
        ax.axis('off')
        
        the_table = ax.table(
            cellText=table_data, 
            colLabels=["Pricing Tier", "Target Price"], 
            loc='center', 
            cellLoc='left' # Align text left
        )
        
        # Polish Table Styling
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(13)
        the_table.scale(1, 2)
        
        # Remove cell borders
        for key, cell in the_table.get_celld().items():
            cell.set_linewidth(0) # No border
            if key[0] == 0: # Header
                cell.set_text_props(weight='bold')
                cell.set_linewidth(0)
                cell.set_facecolor('#ecf0f1') # Light gray header
            else:
                 cell.set_facecolor('white')
                 # Add thin bottom border
                 if key[1] == 0 or key[1] == 1:
                     cell.set_edgecolor('#bdc3c7')
                     cell.set_linewidth(0.5)
                     cell.set_linestyle('-')
                     cell.set_height(0.15)
        
        # Numbers right aligned
        for row in range(1, 5):
            the_table[(row, 1)].set_text_props(ha='right')
        
        plt.title("6. Pricing Strategy Guide", y=1.1, fontweight='bold')
        
        plt.savefig("assets/6_pricing_table.png", bbox_inches='tight', dpi=300)
        plt.close()
        print("   Chart 6 OK.")
    except Exception:
        print("   Chart 6 Failed.")
        traceback.print_exc()

if __name__ == "__main__":
    generate_visuals()
