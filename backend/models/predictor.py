import xgboost as xgb
import pandas as pd
import joblib
import os
import logging
import json

logger = logging.getLogger(__name__)

class FraudPredictor:
    def __init__(self, scale_pos_weight=1.0, max_depth=5, learning_rate=0.1, n_estimators=100):
        self.model = xgb.XGBClassifier(
            max_depth=max_depth,
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            scale_pos_weight=scale_pos_weight,
            objective='binary:logistic',
            eval_metric='auc',
            use_label_encoder=False,
            random_state=42,
            n_jobs=-1
        )
        
        self.feature_cols = [
            'dna_entity_reuse_1h', 'dna_entity_reuse_24h', 'dna_velocity_burst',
            'dna_amount_escalation', 'dna_auth_failure_rate', 'dna_graph_degree_proxy',
            'dna_merchant_concentration_1h', 'dna_temporal_density_5m',
            'dna_payment_diversity', 'dna_account_age_hours',
            'attack_momentum'
        ]

    def fit(self, df_train):
        logger.info(f"Training XGBoost Predictor on {len(df_train)} records...")
        X_train = df_train[self.feature_cols]
        y_train = df_train['is_fraud']
        
        self.model.fit(X_train, y_train)
        
    def predict_proba(self, df):
        X = df[self.feature_cols]
        # Return probability of class 1 (Fraud)
        return self.model.predict_proba(X)[:, 1]

    def predict(self, df, threshold=0.5):
        probs = self.predict_proba(df)
        return (probs >= threshold).astype(int)

    def save(self, directory):
        os.makedirs(directory, exist_ok=True)
        model_path = os.path.join(directory, 'xgboost_model.json')
        self.model.save_model(model_path)
        logger.info(f"Model saved to {model_path}")

    @classmethod
    def load(cls, directory):
        instance = cls()
        model_path = os.path.join(directory, 'xgboost_model.json')
        
        # XGBoost requires re-initializing the booster to load from json
        instance.model = xgb.XGBClassifier()
        instance.model.load_model(model_path)
        
        return instance
