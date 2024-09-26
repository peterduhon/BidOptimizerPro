# BidOptimizerPro/modules/visualization/plots.py

import matplotlib.pyplot as plt
import pandas as pd

def plot_bid_results(data):
    """
    Generates visualizations based on processed bid data.

    Args:
        data (pd.DataFrame): Processed bid data.

    Returns:
        None
    """
    # Win Rate by SSP
    win_rate_ssp = data.groupby('ssp_id')['is_won'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(win_rate_ssp['ssp_id'], win_rate_ssp['is_won'], color='skyblue')
    plt.xlabel('SSP ID')
    plt.ylabel('Win Rate')
    plt.title('Win Rate by SSP')
    plt.ylim(0, 1)
    plt.show()

    # Average Bid Amount by Advertiser
    avg_bid_adv = data.groupby('advertiser_id')['bid_amount'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(avg_bid_adv['advertiser_id'], avg_bid_adv['bid_amount'], color='salmon')
    plt.xlabel('Advertiser ID')
    plt.ylabel('Average Bid Amount ($)')
    plt.title('Average Bid Amount by Advertiser')
    plt.show()

    # Execution Time Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(data['execution_time'], bins=20, color='green', edgecolor='black')
    plt.xlabel('Execution Time (seconds)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Execution Times')
    plt.show()
