# main.py

import sys
import os
import logging
import random
import sqlite3
from datetime import datetime

# Add the project directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from modules.bid_simulation.simulation import simulate_bids
from modules.bid_simulation.machine_learning import load_model, predict_bid_success
from modules.data_processing.processing import process_bid_data
from modules.visualization.plots import plot_bid_results

import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    advertisers = ['A', 'B', 'C', 'D', 'E']
    
    # Choose simulation mode
    mode = 'async'  # Options: 'async', 'thread', 'sequential'
    
    # Run simulations based on selected mode
    try:
        bids, exec_time = simulate_bids(advertisers, mode=mode)
    except ValueError as ve:
        logging.error(ve)
        return
    
    # Print execution time
    logging.info(f"{mode.capitalize()} execution time: {exec_time:.2f} seconds")
    print(f"{mode.capitalize()} execution time: {exec_time:.2f} seconds")
    
    # Convert bids to DataFrame
    data = pd.DataFrame(bids)
    
    # Add additional fields
    data['ssp_id'] = [f"ssp_{random.randint(1, 5)}" for _ in range(len(bids))]
    data['is_won'] = [random.random() < 0.3 for _ in range(len(bids))]  # Example win rate of 30%
    data['timestamp'] = pd.to_datetime(datetime.now())
    
    # Process Data
    processed_data = process_bid_data(data)
    
    # Save to SQLite Database
    conn = sqlite3.connect('bidoptimizerpro.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            advertiser_id TEXT,
            ssp_id TEXT,
            bid_amount REAL,
            is_won INTEGER,
            execution_time REAL,
            timestamp TEXT
        )
    ''')
    
    # Insert data into the database
    for _, row in data.iterrows():
        cursor.execute('''
            INSERT INTO bids (advertiser_id, ssp_id, bid_amount, is_won, execution_time, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row["advertiser_id"], 
            row["ssp_id"], 
            row["bid_amount"], 
            int(row["is_won"]),  # Convert boolean to integer
            row["execution_time"], 
            row["timestamp"].isoformat()  # Convert timestamp to string
        ))
    
    conn.commit()
    conn.close()
    
    # Load and use the ML model
    try:
        model = load_model()
        if model:
            data['predicted_won'] = data.apply(lambda row: predict_bid_success(model, row['bid_amount'], row['timestamp'].hour), axis=1)
            logging.info("Machine Learning model applied successfully.")
        else:
            data['predicted_won'] = None
    except Exception as e:
        logging.error(f"Error loading or applying ML model: {e}")
        data['predicted_won'] = None
    
    # Visualization
    plot_bid_results(processed_data)

if __name__ == "__main__":
    main()
