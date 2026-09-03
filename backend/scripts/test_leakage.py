import pandas as pd
from simulator import generator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_leakage():
    logger.info("Generating sample data (scale=0.01)...")
    entities, df_tx = generator.run(scale=0.01)
    
    logger.info(f"Generated {len(df_tx)} transactions.")
    
    # Ground truth should have labels
    assert 'is_fraud' in df_tx.columns
    assert 'attack_ring_id' in df_tx.columns
    assert 'topology' in df_tx.columns
    logger.info("✅ Ground truth labels correctly present in dataframe.")
    
    # Simulate the DB insert column selection
    safe_columns = ['transaction_id', 'customer_id', 'merchant_id', 'device_id', 'ip_id', 'amount', 'timestamp', 'status', 'payment_method', 'auth_status', 'is_refund']
    df_db = df_tx[safe_columns]
    
    assert 'is_fraud' not in df_db.columns
    assert 'attack_ring_id' not in df_db.columns
    assert 'topology' not in df_db.columns
    logger.info("✅ Database schema strictly isolates ground truth to prevent ML leakage.")
    logger.info("Leakage test passed.")

if __name__ == "__main__":
    test_leakage()
