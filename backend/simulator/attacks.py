import pandas as pd
import numpy as np
from datetime import timedelta
import random

def generate_attacks(config, entities, scale=1.0):
    start_date = pd.to_datetime(config['simulation']['start_date'])
    days = config['simulation']['days']
    
    attacks = []
    
    # We will pick a pool of victims for the attacks to use
    victims = entities['customers']
    
    # 1. Burst Attacks
    burst_cfg = config['attacks']['burst']
    for i in range(int(burst_cfg['events'] * scale)):
        ring_id = f"ring_burst_{i}"
        tx_count = random.randint(burst_cfg['tx_per_event'][0], burst_cfg['tx_per_event'][1])
        duration = random.randint(burst_cfg['duration_mins'][0], burst_cfg['duration_mins'][1])
        
        start_ts = start_date + timedelta(days=random.uniform(0, days - 1))
        
        attacker_ip = f"ip_atk_burst_{i}"
        merchant = random.choice(entities['merchants'])
        
        for j in range(tx_count):
            ts = start_ts + timedelta(minutes=random.uniform(0, duration))
            victim = random.choice(victims) # Account takeover scenario
            
            attacks.append({
                'transaction_id': f"tx_{ring_id}_{j}",
                'customer_id': victim['customer_id'],
                'merchant_id': merchant['merchant_id'],
                'device_id': f"dev_atk_burst_{i}", # Shared device
                'ip_id': attacker_ip, # Shared IP
                'amount': round(random.uniform(10, 50), 2), # Small testing amounts
                'timestamp': ts,
                'status': 'SUCCESS' if j < tx_count * 0.8 else 'FAILED',
                'payment_method': 'CARD',
                'auth_status': 'FAILED' if random.random() < 0.3 else 'SUCCESS',
                'is_refund': False,
                'is_fraud': 1,
                'attack_ring_id': ring_id,
                'topology': 'burst'
            })

    # 2. Rotating Device Ring (UNSEEN TOPOLOGY)
    rot_cfg = config['attacks']['rotating_device_ring']
    for i in range(int(rot_cfg['events'] * scale)):
        ring_id = f"ring_rot_{i}"
        start_day, end_day = rot_cfg['active_days']
        
        # Attack only happens in the specified window (days 26-30)
        attack_window_start = start_date + timedelta(days=start_day - 1)
        
        devices = [f"dev_rot_{i}_{d}" for d in range(rot_cfg['devices'])]
        accounts = [random.choice(victims) for _ in range(rot_cfg['accounts'])]
        merchant = random.choice(entities['merchants'])
        
        tx_count = random.randint(50, 150)
        
        for j in range(tx_count):
            ts = attack_window_start + timedelta(days=random.uniform(0, end_day - start_day))
            attacks.append({
                'transaction_id': f"tx_{ring_id}_{j}",
                'customer_id': random.choice(accounts)['customer_id'],
                'merchant_id': merchant['merchant_id'],
                'device_id': random.choice(devices), # Devices are rotated among many accounts
                'ip_id': f"ip_rot_{i}_{random.randint(1, 10)}", 
                'amount': round(random.uniform(100, 500), 2),
                'timestamp': ts,
                'status': 'SUCCESS',
                'payment_method': 'CARD',
                'auth_status': 'SUCCESS',
                'is_refund': False,
                'is_fraud': 1,
                'attack_ring_id': ring_id,
                'topology': 'rotating_device_ring'
            })
            
    # For hackathon brevity, only implementing 2 topologies in this script version,
    # Slow Bleed and Star Graph would follow similar explicit patterns.
    
    return pd.DataFrame(attacks)
