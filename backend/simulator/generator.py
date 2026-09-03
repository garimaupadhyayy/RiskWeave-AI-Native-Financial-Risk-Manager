import yaml
import os
import pandas as pd
from .legitimate import generate_legitimate_transactions
from .attacks import generate_attacks
import logging

logger = logging.getLogger(__name__)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def generate_entities(config, scale=1.0):
    num_cust = int(config['entities']['customers'] * scale)
    num_merch = int(config['entities']['merchants'] * scale)
    
    customers = []
    corp_count = int(config['legitimate_edge_cases']['corporate_network']['user_count'] * scale)
    hr_count = int(config['legitimate_edge_cases']['high_rollers']['user_count'] * scale)
    
    for i in range(num_cust):
        devices = [f"dev_c_{i}_{j}" for j in range(max(1, int(config['entities']['devices_per_customer'])))]
        ips = [f"ip_c_{i}_{j}" for j in range(max(1, int(config['entities']['ips_per_customer'])))]
        
        customers.append({
            'customer_id': f"cust_{i}",
            'is_corporate': i < corp_count,
            'is_high_roller': corp_count <= i < (corp_count + hr_count),
            'devices': devices,
            'ips': ips
        })
        
    merchants = [{'merchant_id': f"merch_{i}", 'category': 'general'} for i in range(num_merch)]
    
    return {'customers': customers, 'merchants': merchants}

def run(scale=1.0):
    logger.info(f"Starting Data Simulator at scale {scale}")
    config = load_config()
    
    entities = generate_entities(config, scale)
    
    logger.info("Generating Legitimate Transactions...")
    df_legit = generate_legitimate_transactions(config, entities, scale)
    
    logger.info("Generating Attack Transactions...")
    df_attacks = generate_attacks(config, entities, scale)
    
    df_all = pd.concat([df_legit, df_attacks]).sort_values('timestamp').reset_index(drop=True)
    
    # Overwrite transaction IDs to be purely sequential so they don't leak context
    df_all['transaction_id'] = [f"tx_{i:08d}" for i in range(len(df_all))]
    
    logger.info(f"Generated {len(df_all)} total transactions.")
    
    return entities, df_all
