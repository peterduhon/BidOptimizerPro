# BidOptimizerPro/modules/visualization/plots.py

import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def plot_bid_results(processed_data):
    """
    Generate and display plots based on processed bid data.

    Args:
        processed_data (dict): Dictionary containing processed bid metrics.
    """
    try:
        # Example: Plot Win Rate by SSP
        plt.figure(figsize=(12, 6))
        win_rate_data = processed_data['win_rate_ssp']
        plt.bar(win_rate_data['ssp_id'], win_rate_data['win_rate'] * 100, color='skyblue')
        plt.xlabel('SSP ID')
        plt.ylabel('Win Rate (%)')
        plt.title('Win Rate by SSP')
        plt.ylim(0, 100)
        for i, v in enumerate(win_rate_data['win_rate']):
            plt.text(i, v * 100 + 1, f'{v*100:.1f}%', ha='center')
        plt.tight_layout()
        plt.show()
        logging.info("Win Rate by SSP plot displayed successfully.")

        # Example: Plot Average Bid Amount by Advertiser
        plt.figure(figsize=(8, 6))
        plt.bar(processed_data['avg_bid_adv']['advertiser_id'], processed_data['avg_bid_adv']['avg_bid_amount'], color='salmon')
        plt.xlabel('Advertiser ID')
        plt.ylabel('Average Bid Amount ($)')
        plt.title('Average Bid Amount by Advertiser')
        plt.tight_layout()
        plt.show()
        logging.info("Average Bid Amount by Advertiser plot displayed successfully.")

        # Example: Plot Execution Time Distribution
        plt.figure(figsize=(8, 6))
        plt.hist(processed_data['execution_time_distribution'], bins=20, color='green', edgecolor='black')
        plt.xlabel('Execution Time (seconds)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Execution Times')
        plt.tight_layout()
        plt.show()
        logging.info("Execution Time Distribution plot displayed successfully.")

    except Exception as e:
        logging.error(f"Error generating plots: {e}")
