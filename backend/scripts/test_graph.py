import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import logging
import json
from graph.queries import GRAPH_CTE_QUERY, build_graph_from_rows

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_recursive_cte():
    logger.info("Initializing in-memory SQLite database for graph test...")
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    
    # Create Table
    conn.execute("""
    CREATE TABLE transactions (
        transaction_id TEXT PRIMARY KEY,
        timestamp DATETIME,
        customer_id TEXT,
        merchant_id TEXT,
        amount REAL,
        device_id TEXT,
        ip_id TEXT,
        payment_method TEXT,
        auth_status TEXT,
        is_refund INTEGER
    )
    """)
    
    # Insert Mock Data: A Rotating-Device Ring
    # C1 uses D1, IP1
    # C2 uses D1, IP2
    # C3 uses D2, IP2
    
    base_time = datetime(2026, 9, 1, 12, 0, 0)
    
    data = [
        ('tx1', base_time, 'C1', 'M1', 100.0, 'D1', 'IP1', 'CARD', 'SUCCESS', 0),
        ('tx2', base_time + timedelta(minutes=5), 'C2', 'M1', 150.0, 'D1', 'IP2', 'CARD', 'SUCCESS', 0),
        ('tx3', base_time + timedelta(minutes=10), 'C3', 'M1', 200.0, 'D2', 'IP2', 'CARD', 'SUCCESS', 0),
        # Legitimate disconnected transaction
        ('tx4', base_time + timedelta(minutes=15), 'C99', 'M1', 50.0, 'D99', 'IP99', 'CARD', 'SUCCESS', 0),
    ]
    
    conn.executemany("""
    INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    
    # Test Query starting from tx1
    seed_tx_id = 'tx1'
    # Global bounds
    global_start = (base_time - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
    global_end = (base_time + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
    
    logger.info(f"Executing Graph CTE for seed={seed_tx_id}")
    
    # SQLite uses ? or named params. Python sqlite3 supports named params via dict
    params = {
        'seed_tx_id': seed_tx_id,
        'global_start_time': global_start,
        'global_end_time': global_end
    }
    
    cursor = conn.execute(GRAPH_CTE_QUERY, params)
    rows = cursor.fetchall()
    
    logger.info(f"CTE returned {len(rows)} rows.")
    for r in rows:
        logger.info(f"Depth {r['depth']}: {r['transaction_id']} (Cust: {r['customer_id']}, Dev: {r['device_id']}, IP: {r['ip_id']})")
        
    # Validations
    fetched_txs = [r['transaction_id'] for r in rows]
    assert 'tx1' in fetched_txs, "Seed not found"
    assert 'tx2' in fetched_txs, "Hop 1 failed"
    assert 'tx3' in fetched_txs, "Hop 2 failed"
    assert 'tx4' not in fetched_txs, "Leakage to disconnected graph!"
    
    logger.info("Graph traversal logic works perfectly!")
    
    # Test Graph Transform
    graph = build_graph_from_rows(rows)
    logger.info(f"Transformed Graph: {len(graph['nodes'])} Nodes, {len(graph['edges'])} Edges")
    
if __name__ == "__main__":
    test_recursive_cte()
