import pandas as pd
from features.engine import FeatureEngine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_leakage():
    # Create a deterministic mock dataset
    data = [
        # tx 1: Time 0
        {'transaction_id': 'tx1', 'customer_id': 'c1', 'merchant_id': 'm1', 'device_id': 'd1', 'ip_id': 'ip1', 'amount': 100, 'timestamp': pd.to_datetime('2026-09-01 10:00:00'), 'status': 'SUCCESS', 'payment_method': 'CARD', 'auth_status': 'SUCCESS', 'is_refund': False, 'is_fraud': 0},
        
        # tx 2: Time 10 (Future leak candidate)
        {'transaction_id': 'tx2', 'customer_id': 'c2', 'merchant_id': 'm1', 'device_id': 'd1', 'ip_id': 'ip1', 'amount': 500, 'timestamp': pd.to_datetime('2026-09-01 10:10:00'), 'status': 'SUCCESS', 'payment_method': 'CARD', 'auth_status': 'FAILED', 'is_refund': False, 'is_fraud': 1},
    ]
    df = pd.DataFrame(data)
    
    engine = FeatureEngine(df)
    features = engine.generate_all_features()
    
    # Check TX1 (Time 0)
    tx1_features = features[features['transaction_id'] == 'tx1'].iloc[0]
    
    # If there is leakage, TX1 might show device_reuse_1h = 1 (because TX2 exists). 
    # But since it's point-in-time, at TX1, the historical reuse should be 0.
    assert tx1_features['dna_entity_reuse_1h'] == 0, f"Leakage detected in entity reuse: {tx1_features['dna_entity_reuse_1h']}"
    
    # TX1 should have 0 auth failures historically
    assert tx1_features['dna_auth_failure_rate'] == 0, "Leakage in auth failure rate"
    
    # Now check TX2 (Time 10)
    tx2_features = features[features['transaction_id'] == 'tx2'].iloc[0]
    
    # At TX2, the history includes TX1, so device reuse should be 1, and IP reuse should be 1. 
    # Therefore dna_entity_reuse_1h = 2.
    assert tx2_features['dna_entity_reuse_1h'] == 2, f"Historical state failed: {tx2_features['dna_entity_reuse_1h']}"
    
    logger.info("✅ Strict Point-in-Time leakage tests passed. No future data contaminated the past features.")

if __name__ == "__main__":
    test_leakage()
