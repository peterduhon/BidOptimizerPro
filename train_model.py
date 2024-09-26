import sys
import os
import pandas as pd
import sqlite3
import logging

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from modules.bid_simulation.machine_learning import train_bid_model

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Connect to SQLite Database
    try:
        conn = sqlite3.connect('bidoptimizerpro.db')
        logging.info("Connected to SQLite database 'bidoptimizerpro.db'.")
    except sqlite3.Error as e:
        logging.error(f"SQLite connection error: {e}")
        return
    
    # Fetch bid data
    try:
        df = pd.read_sql_query("SELECT * FROM bids", conn)
        logging.info(f"Fetched {len(df)} records from 'bids' table.")
    except Exception as e:
        logging.error(f"Error fetching data from SQLite: {e}")
        conn.close()
        return
    
    conn.close()
    
    if df.empty:
        logging.error("No data available to train the model. Please run simulations first.")
        return
    
    # Train the model
    try:
        train_bid_model(df)
        logging.info("Model training completed successfully.")
    except Exception as e:
        logging.error(f"Error during model training: {e}")

if __name__ == "__main__":
    main()
