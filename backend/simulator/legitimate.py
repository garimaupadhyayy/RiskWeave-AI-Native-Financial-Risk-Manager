import pandas as pd
import numpy as np
from datetime import timedelta
import random

def generate_legitimate_transactions(config, entities, scale=1.0):
    """Generates the baseline legitimate transactions including edge cases."""
    start_date = pd.to_datetime(config['simulation']['start_date'])
    days = config['simulation']['days']
    target_tx = int(config['simulation']['total_transactions_target'] * scale * 0.97) # ~97% legitimate
    
    # Pre-calculate probabilities for merchants (power law to simulate popular merchants)
    merchant_probs = np.random.pareto(a=2, size=len(entities['merchants']))
    merchant_probs /= merchant_probs.sum()

    transactions = []
    
    # 1. Standard Legitimate
    standard_users = [c for c in entities['customers'] if not c.get('is_corporate') and not c.get('is_high_roller')]
    
    # 2. Corporate Network Edge Case
    corp_users = [c for c in entities['customers'] if c.get('is_corporate')]
    corp_ip = config['legitimate_edge_cases']['corporate_network']['shared_ip']
    
    # 3. High Rollers
    high_rollers = [c for c in entities['customers'] if c.get('is_high_roller')]
    hr_multiplier = config['legitimate_edge_cases']['high_rollers']['amount_multiplier']

    # Generate timestamps across the 30 days using a diurnal pattern
    # Simplified: generate random timestamps, but skew towards daytime
    time_offsets = np.random.uniform(0, days * 24 * 3600, target_tx)
    timestamps = [start_date + timedelta(seconds=int(ts)) for ts in time_offsets]
    timestamps.sort()

    for ts in timestamps:
        # 10% chance it's a corporate user, if during their active hours
        if corp_users and ts.hour in config['legitimate_edge_cases']['corporate_network']['active_hours'] and random.random() < 0.1:
            user = random.choice(corp_users)
            ip_id = corp_ip
            amt_mult = 1.0
        # 2% chance it's a high roller
        elif high_rollers and random.random() < 0.02:
            user = random.choice(high_rollers)
            ip_id = random.choice(user['ips'])
            amt_mult = hr_multiplier
        # Standard user
        else:
            user = random.choice(standard_users)
            ip_id = random.choice(user['ips'])
            amt_mult = 1.0

        # Log-normal transaction amounts
        base_amount = np.random.lognormal(mean=3.5, sigma=1.0) # ~ 30-100 base
        amount = max(1.0, round(base_amount * amt_mult, 2))
        
        merchant = np.random.choice(entities['merchants'], p=merchant_probs)
        device = random.choice(user['devices'])

        transactions.append({
            'transaction_id': f"tx_legit_{len(transactions)}",
            'customer_id': user['customer_id'],
            'merchant_id': merchant['merchant_id'],
            'device_id': device,
            'ip_id': ip_id,
            'amount': amount,
            'timestamp': ts,
            'status': 'SUCCESS',
            'payment_method': random.choice(['CARD', 'UPI', 'NETBANKING']),
            'auth_status': 'SUCCESS' if random.random() > 0.05 else 'FAILED',
            'is_refund': False,
            'is_fraud': 0, # Ground truth only
            'attack_ring_id': None,
            'topology': 'legitimate'
        })
        
    return pd.DataFrame(transactions)
