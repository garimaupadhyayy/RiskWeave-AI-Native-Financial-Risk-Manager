import argparse
import logging
import pandas as pd
import mysql.connector
import os
from simulator import generator
from app.core.config import settings
from scripts.init_db import init_db

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def insert_data(entities, df_tx):
    conn = mysql.connector.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE
    )
    cursor = conn.cursor()

    logger.info("Inserting Customers...")
    cust_data = [(c['customer_id'], c['is_high_roller'], c['is_corporate']) for c in entities['customers']]
    cursor.executemany("INSERT INTO customers (customer_id, is_high_roller, is_corporate) VALUES (%s, %s, %s)", cust_data)

    logger.info("Inserting Merchants...")
    merch_data = [(m['merchant_id'], m['category']) for m in entities['merchants']]
    cursor.executemany("INSERT INTO merchants (merchant_id, category) VALUES (%s, %s)", merch_data)

    # Extract unique IPs and Devices
    ips = set(df_tx['ip_id'].unique())
    devices = set(df_tx['device_id'].unique())
    
    logger.info("Inserting Devices & IPs...")
    cursor.executemany("INSERT INTO devices (device_id, device_type) VALUES (%s, 'unknown')", [(d,) for d in devices])
    cursor.executemany("INSERT INTO ips (ip_id, country) VALUES (%s, 'IN')", [(i,) for i in ips])

    logger.info("Inserting Transactions (No labels!)...")
    tx_data = df_tx[['transaction_id', 'customer_id', 'merchant_id', 'device_id', 'ip_id', 'amount', 'timestamp', 'status', 'payment_method', 'auth_status', 'is_refund']].values.tolist()
    cursor.executemany("""
        INSERT INTO transactions 
        (transaction_id, customer_id, merchant_id, device_id, ip_id, amount, timestamp, status, payment_method, auth_status, is_refund) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tx_data)

    logger.info("Generating and Inserting Entity Relationships...")
    # Customer -> Device
    c_d = df_tx[['customer_id', 'device_id']].drop_duplicates()
    rel_data = [(row['customer_id'], 'CUSTOMER', row['device_id'], 'DEVICE', 'USED_DEVICE') for _, row in c_d.iterrows()]
    
    # Customer -> IP
    c_i = df_tx[['customer_id', 'ip_id']].drop_duplicates()
    rel_data.extend([(row['customer_id'], 'CUSTOMER', row['ip_id'], 'IP', 'USED_IP') for _, row in c_i.iterrows()])
    
    cursor.executemany("""
        INSERT IGNORE INTO entity_relationships 
        (source_id, source_type, target_id, target_type, relationship_type) 
        VALUES (%s, %s, %s, %s, %s)
    """, rel_data)

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Database insertion complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--scale', type=float, default=1.0, help='Scale factor for dataset size')
    args = parser.parse_args()

    # 1. Init DB
    init_db()

    # 2. Generate Data
    entities, df_tx = generator.run(scale=args.scale)

    # 3. Save Ground Truth separately!
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    os.makedirs(data_dir, exist_ok=True)
    gt_path = os.path.join(data_dir, 'ground_truth.csv')
    df_tx.to_csv(gt_path, index=False)
    logger.info(f"Ground truth saved to {gt_path} with {len(df_tx)} rows.")

    # 4. Insert into DB (Without leakage fields!)
    insert_data(entities, df_tx)
