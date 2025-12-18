
"""
visualize_results.py

Purpose:
Create clear, business-oriented charts for the NYC Airbnb analysis.
Designed for Data Analyst roles (clarity > complexity).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")

def load_data(path="comprehensive_data.csv"):
    """Load cleaned analytical dataset."""
    return pd.read_csv(path)

def plot_revpar_by_room(df):
    room_rev = (
        df.groupby("room_type")
          .agg(avg_revpar=("revpar", "mean"), listings=("id", "count"))
          .reset_index()
    )

    plt.figure(figsize=(8,5))
    ax = sns.barplot(data=room_rev, x="room_type", y="avg_revpar")

    for i, r in room_rev.iterrows():
        ax.text(i, r.avg_revpar + 2, f"${r.avg_revpar:.0f}", ha="center")

    plt.title("Revenue Efficiency by Room Type")
    plt.xlabel("")
    plt.ylabel("Avg RevPAR ($)")
    sns.despine()
    plt.show()

def main():
    df = load_data()
    plot_revpar_by_room(df)

if __name__ == "__main__":
    main()
