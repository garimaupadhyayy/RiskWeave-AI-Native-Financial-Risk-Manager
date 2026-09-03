import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class FeatureEngine:
    def __init__(self, df_tx):
        self.df = df_tx.copy().sort_values('timestamp').reset_index(drop=True)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], format='mixed')
        
    def generate_all_features(self):
        logger.info("Computing DNA Dim 1: Entity Reuse (Device/IP 1h & 24h)")
        self._compute_entity_reuse()
        logger.info("Computing DNA Dim 2: Velocity Burst")
        self._compute_velocity_burst()
        logger.info("Computing DNA Dim 3: Amount Escalation")
        self._compute_amount_escalation()
        logger.info("Computing DNA Dim 4: Auth Failure Rate")
        self._compute_auth_failure_rate()
        logger.info("Computing DNA Dim 5: Graph Degree Proxy")
        self._compute_graph_degree()
        logger.info("Computing DNA Dim 6: Merchant Concentration")
        self._compute_merchant_concentration()
        logger.info("Computing DNA Dim 7: Temporal Density")
        self._compute_temporal_density()
        logger.info("Computing DNA Dim 8: Payment Diversity")
        self._compute_payment_diversity()
        logger.info("Computing DNA Dim 9: Account Age Concentration")
        self._compute_account_age()
        logger.info("Computing DNA Dim 10: Refund Coupling")
        self._compute_refund_coupling()
        logger.info("Computing Attack Momentum")
        self._compute_momentum()
        return self.df

    def _compute_entity_reuse(self):
        for window, suffix in [('1h', '1h'), ('24h', '24h')]:
            for col in ['device_id', 'ip_id']:
                temp = self.df[['transaction_id', col, 'timestamp']].sort_values([col, 'timestamp'])
                counts = temp.groupby(col).rolling(window, on='timestamp')['transaction_id'].count()
                metric_name = f"{col.split('_')[0]}_reuse_{suffix}"
                temp[metric_name] = counts.groupby(level=0).shift(1).fillna(0).values
                self.df = self.df.merge(temp[['transaction_id', metric_name]], on='transaction_id', how='left')
            
            self.df[f'dna_entity_reuse_{suffix}'] = self.df[f'device_reuse_{suffix}'] + self.df[f'ip_reuse_{suffix}']

    def _compute_velocity_burst(self):
        avg_hourly_24h = (self.df['dna_entity_reuse_24h'] / 24.0).clip(lower=1.0)
        self.df['dna_velocity_burst'] = self.df['dna_entity_reuse_1h'] / avg_hourly_24h

    def _compute_amount_escalation(self):
        temp = self.df[['transaction_id', 'customer_id', 'timestamp', 'amount']].sort_values(['customer_id', 'timestamp'])
        avg_amt = temp.groupby('customer_id').rolling('24h', on='timestamp')['amount'].mean()
        temp['user_avg_amount_24h'] = avg_amt.groupby(level=0).shift(1).fillna(self.df['amount'].mean()).values
        self.df = self.df.merge(temp[['transaction_id', 'user_avg_amount_24h']], on='transaction_id', how='left')
        self.df['dna_amount_escalation'] = self.df['amount'] / self.df['user_avg_amount_24h'].clip(lower=1.0)

    def _compute_auth_failure_rate(self):
        temp = self.df[['transaction_id', 'ip_id', 'timestamp', 'auth_status']].copy().sort_values(['ip_id', 'timestamp'])
        temp['is_auth_fail'] = (temp['auth_status'] == 'FAILED').astype(int)
        
        aggs = temp.groupby('ip_id').rolling('24h', on='timestamp')['is_auth_fail'].agg(['sum', 'count'])
        temp['past_fails'] = aggs['sum'].groupby(level=0).shift(1).fillna(0).values
        temp['past_count'] = aggs['count'].groupby(level=0).shift(1).fillna(0).values
        
        temp['dna_auth_failure_rate'] = np.where(temp['past_count'] > 0, temp['past_fails'] / temp['past_count'], 0)
        self.df = self.df.merge(temp[['transaction_id', 'dna_auth_failure_rate']], on='transaction_id', how='left')

    def _compute_graph_degree(self):
        temp = self.df[['transaction_id', 'device_id', 'customer_id', 'timestamp']].copy().sort_values(['device_id', 'timestamp'])
        temp['cust_changed'] = (temp['customer_id'] != temp.groupby('device_id')['customer_id'].shift(1)).astype(int)
        
        deg = temp.groupby('device_id').rolling('24h', on='timestamp')['cust_changed'].sum()
        temp['dna_graph_degree_proxy'] = deg.groupby(level=0).shift(1).fillna(0).values
        self.df = self.df.merge(temp[['transaction_id', 'dna_graph_degree_proxy']], on='transaction_id', how='left')

    def _compute_merchant_concentration(self):
        temp = self.df[['transaction_id', 'merchant_id', 'timestamp']].sort_values(['merchant_id', 'timestamp'])
        merch = temp.groupby('merchant_id').rolling('1h', on='timestamp')['transaction_id'].count()
        temp['dna_merchant_concentration_1h'] = merch.groupby(level=0).shift(1).fillna(0).values
        self.df = self.df.merge(temp[['transaction_id', 'dna_merchant_concentration_1h']], on='transaction_id', how='left')

    def _compute_temporal_density(self):
        temp = self.df[['transaction_id', 'timestamp']].sort_values('timestamp')
        sys = temp.rolling('5min', on='timestamp')['transaction_id'].count()
        temp['dna_temporal_density_5m'] = sys.shift(1).fillna(0).values
        self.df = self.df.merge(temp[['transaction_id', 'dna_temporal_density_5m']], on='transaction_id', how='left')

    def _compute_payment_diversity(self):
        temp = self.df[['transaction_id', 'customer_id', 'payment_method', 'timestamp']].copy().sort_values(['customer_id', 'timestamp'])
        temp['is_new_method'] = (~temp.duplicated(subset=['customer_id', 'payment_method'])).astype(int)
        temp['dna_payment_diversity'] = temp.groupby('customer_id')['is_new_method'].cumsum().shift(1).fillna(0).values
        self.df = self.df.merge(temp[['transaction_id', 'dna_payment_diversity']], on='transaction_id', how='left')

    def _compute_account_age(self):
        first_tx = self.df.groupby('customer_id')['timestamp'].transform('min')
        self.df['dna_account_age_hours'] = (self.df['timestamp'] - first_tx).dt.total_seconds() / 3600.0

    def _compute_refund_coupling(self):
        temp = self.df[['transaction_id', 'merchant_id', 'timestamp', 'is_refund']].copy().sort_values(['merchant_id', 'timestamp'])
        temp['is_refund_int'] = temp['is_refund'].astype(int)
        merch_ref = temp.groupby('merchant_id').rolling('24h', on='timestamp')['is_refund_int'].sum()
        temp['dna_refund_coupling'] = merch_ref.groupby(level=0).shift(1).fillna(0).values
        self.df = self.df.merge(temp[['transaction_id', 'dna_refund_coupling']], on='transaction_id', how='left')

    def _compute_momentum(self):
        # Normalize velocity and graph degree (using simple arbitrary max division for hackathon, or rank)
        # Normally this would be a robust scaler fitted on training data. 
        # We will use simple MinMax approximation over rolling 24h for demonstration
        
        v_max = self.df['dna_velocity_burst'].clip(upper=10).max() or 1
        g_max = self.df['dna_graph_degree_proxy'].clip(upper=10).max() or 1
        
        norm_v = self.df['dna_velocity_burst'].clip(upper=10) / v_max
        norm_g = self.df['dna_graph_degree_proxy'].clip(upper=10) / g_max
        
        # Momentum = w1*v + w2*g + (anomaly_score will be added in Phase 4)
        raw_momentum = 0.6 * norm_v + 0.4 * norm_g
        
        # EMA over time per device
        temp = pd.DataFrame({'device_id': self.df['device_id'], 'raw_momentum': raw_momentum})
        self.df['attack_momentum'] = temp.groupby('device_id')['raw_momentum'].transform(lambda x: x.ewm(span=5, adjust=False).mean())
