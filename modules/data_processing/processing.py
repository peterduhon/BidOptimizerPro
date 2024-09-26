# BidOptimizerPro/modules/data_processing/processing.py

import pandas as pd

def process_bid_data(data):
    """
    Processes raw bid simulation data into a structured dictionary of DataFrames.

    Args:
        data (pd.DataFrame): Raw bid data.

    Returns:
        dict: Processed bid data with additional computed metrics.
    """
    # Calculate win rate per SSP
    win_rate_ssp = data.groupby('ssp_id')['is_won'].mean().reset_index(name='win_rate')
    
    # Ensure all SSPs are represented, even if they have no wins
    all_ssps = pd.DataFrame({'ssp_id': [f'ssp_{i}' for i in range(1, 6)]})
    win_rate_ssp = all_ssps.merge(win_rate_ssp, on='ssp_id', how='left').fillna(0)

    # Calculate average bid amount per advertiser
    avg_bid_adv = data.groupby('advertiser_id')['bid_amount'].mean().reset_index(name='avg_bid_amount')

    # Extract execution time distribution
    execution_time_distribution = data['execution_time']

    processed_data = {
        'win_rate_ssp': win_rate_ssp,
        'avg_bid_adv': avg_bid_adv,
        'execution_time_distribution': execution_time_distribution
    }

    return processed_data
