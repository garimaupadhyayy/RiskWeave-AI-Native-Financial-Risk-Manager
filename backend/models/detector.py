import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler
import joblib
import json
import os
import logging

logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self, contamination=0.1, random_state=42):
        # We use a loose contamination during training, actual cutoff is done via validation calibration
        self.model = IsolationForest(n_estimators=150, contamination=contamination, random_state=random_state, n_jobs=-1)
        self.scaler = RobustScaler()
        self.threshold = None
        
        self.feature_cols = [
            'dna_entity_reuse_1h', 'dna_entity_reuse_24h', 'dna_velocity_burst',
            'dna_amount_escalation', 'dna_auth_failure_rate', 'dna_graph_degree_proxy',
            'dna_merchant_concentration_1h', 'dna_temporal_density_5m',
            'dna_payment_diversity', 'dna_account_age_hours'
        ]

    def fit(self, df_train):
        logger.info(f"Fitting RobustScaler on {len(df_train)} training records...")
        X_train = df_train[self.feature_cols].values
        X_scaled = self.scaler.fit_transform(X_train)
        
        logger.info("Fitting Isolation Forest...")
        self.model.fit(X_scaled)
        
    def calibrate(self, df_val, target_fpr=0.05):
        """
        Calibrates the threshold using the validation set to achieve the target False Positive Rate.
        Since we assume an unsupervised environment, we assume the majority of validation data is legitimate.
        We find the score where `target_fpr` % of transactions fall below it.
        """
        logger.info(f"Calibrating threshold on {len(df_val)} validation records for target FPR {target_fpr}...")
        X_val = df_val[self.feature_cols].values
        X_scaled = self.scaler.transform(X_val)
        
        # score_samples returns negative anomaly scores (lower = more anomalous)
        scores = self.model.score_samples(X_scaled)
        
        # We want the threshold where target_fpr% of data is BELOW the threshold
        # e.g. 5th percentile
        percentile = target_fpr * 100
        self.threshold = np.percentile(scores, percentile)
        
        logger.info(f"Calibrated Threshold: {self.threshold:.4f} (Score < Threshold is anomalous)")
        
        # Just to verify on the validation set itself
        anomalies = np.sum(scores < self.threshold)
        logger.info(f"Verification: {anomalies}/{len(scores)} ({anomalies/len(scores)*100:.2f}%) flagged as anomalous in validation.")
        return self.threshold

    def predict_scores(self, df):
        X = df[self.feature_cols].values
        X_scaled = self.scaler.transform(X)
        return self.model.score_samples(X_scaled)

    def is_anomalous(self, df):
        if self.threshold is None:
            raise ValueError("Model has not been calibrated with a threshold yet.")
        scores = self.predict_scores(df)
        return scores < self.threshold

    def save(self, directory):
        os.makedirs(directory, exist_ok=True)
        joblib.dump(self.model, os.path.join(directory, 'isolation_forest.joblib'))
        joblib.dump(self.scaler, os.path.join(directory, 'scaler.joblib'))
        with open(os.path.join(directory, 'threshold.json'), 'w') as f:
            json.dump({'threshold': self.threshold}, f)
        logger.info(f"Model artifacts saved to {directory}")

    @classmethod
    def load(cls, directory):
        instance = cls()
        instance.model = joblib.load(os.path.join(directory, 'isolation_forest.joblib'))
        instance.scaler = joblib.load(os.path.join(directory, 'scaler.joblib'))
        with open(os.path.join(directory, 'threshold.json'), 'r') as f:
            instance.threshold = json.load(f)['threshold']
        return instance
