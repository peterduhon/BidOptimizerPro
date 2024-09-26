# generate_synthetic_data.py

import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_records=1000):
    data = []
    advertisers = ['A', 'B', 'C', 'D', 'E']
    ssps = ['ssp_1', 'ssp_2', 'ssp_3', 'ssp_4', 'ssp_5']
    
    start_date = datetime.now() - timedelta(days=30)
    
    for _ in range(num_records):
        advertiser_id = random.choice(advertisers)
        ssp_id = random.choice(ssps)
        bid_amount = round(random.uniform(0.1, 10.0), 2)
        is_won = random.choice([True, False])
        execution_time = round(random.uniform(0.001, 0.1), 3)
        timestamp = start_date + timedelta(seconds=random.randint(0, 30*24*60*60))
        
        data.append({
            'advertiser_id': advertiser_id,
            'ssp_id': ssp_id,
            'bid_amount': bid_amount,
            'is_won': is_won,
            'execution_time': execution_time,
            'timestamp': timestamp
        })
    
    return pd.DataFrame(data)

def create_and_populate_database(df):
    conn = sqlite3.connect('bidoptimizerpro.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bids (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        advertiser_id TEXT,
        ssp_id TEXT,
        bid_amount REAL,
        is_won BOOLEAN,
        execution_time REAL,
        timestamp TEXT
    )
    ''')
    
    df.to_sql('bids', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    synthetic_data = generate_synthetic_data()
    create_and_populate_database(synthetic_data)
    print("Synthetic data generated and database populated.")