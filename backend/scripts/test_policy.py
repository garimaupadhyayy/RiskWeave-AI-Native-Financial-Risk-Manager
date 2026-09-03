import logging
from app.services.policy import PolicyEngine
import os
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_policy_test():
    models_dir = os.path.join(os.path.dirname(__file__), '../models/artifacts')
    engine = PolicyEngine(models_dir)
    
    # Mock a high-risk transaction (looks like a burst attack)
    tx_data = {
        "transaction_id": "tx_eval_1",
        "timestamp": "2026-09-09 12:00:00",
        "customer_id": "C_test",
        "merchant_id": "M_test",
        "amount": 2500.0,
        "device_id": "D_test",
        "ip_id": "IP_test",
        "payment_method": "CARD",
        "auth_status": "SUCCESS",
        "is_refund": False
    }
    
    logger.info("Evaluating transaction through Policy Engine...")
    result = engine.evaluate(tx_data, db_cursor=None) # Pass None to use mock CSV context
    
    logger.info("Policy Engine Output:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    run_policy_test()
