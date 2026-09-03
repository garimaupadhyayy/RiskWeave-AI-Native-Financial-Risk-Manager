import logging
import pandas as pd
import os
from typing import Dict, Any

from models.detector import AnomalyDetector
from models.predictor import FraudPredictor
from app.services.optimizer import CostOptimizer
from features.engine import FeatureEngine
from graph.queries import GRAPH_CTE_QUERY, build_graph_from_rows
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PolicyEngine:
    def __init__(self, models_dir: str):
        logger.info(f"Loading AI Models from {models_dir}...")
        self.detector = AnomalyDetector.load(models_dir)
        self.predictor = FraudPredictor.load(models_dir)
        self.optimizer = CostOptimizer()
        
        # Local mock context for when DB is unavailable (hackathon fallback)
        self.mock_data_path = os.path.join(models_dir, '../data/ground_truth.csv')
        self.mock_df = None

    def _fetch_context(self, db_cursor, tx_data: dict) -> pd.DataFrame:
        """
        Fetches the last 24h of transactions for the involved entities to compute rolling features.
        """
        try:
            query = """
            SELECT * FROM transactions 
            WHERE timestamp >= %s
              AND (customer_id = %s OR device_id = %s OR ip_id = %s OR merchant_id = %s)
            """
            tx_time = pd.to_datetime(tx_data['timestamp'])
            start_time = tx_time - timedelta(hours=24)
            
            db_cursor.execute(query, (
                start_time.strftime('%Y-%m-%d %H:%M:%S'),
                tx_data['customer_id'],
                tx_data['device_id'],
                tx_data['ip_id'],
                tx_data['merchant_id']
            ))
            rows = db_cursor.fetchall()
            df = pd.DataFrame(rows)
            return df
        except Exception as e:
            logger.warning(f"Database context fetch failed, falling back to mock CSV: {e}")
            return self._fetch_mock_context(tx_data)

    def _fetch_mock_context(self, tx_data: dict) -> pd.DataFrame:
        if self.mock_df is None:
            if not os.path.exists(self.mock_data_path):
                return pd.DataFrame() # No context available
            self.mock_df = pd.read_csv(self.mock_data_path)
            self.mock_df['timestamp'] = pd.to_datetime(self.mock_df['timestamp'], format='mixed')
            
        tx_time = pd.to_datetime(tx_data['timestamp'])
        start_time = tx_time - timedelta(hours=24)
        
        mask = (self.mock_df['timestamp'] >= start_time) & (self.mock_df['timestamp'] < tx_time) & (
            (self.mock_df['customer_id'] == tx_data['customer_id']) |
            (self.mock_df['device_id'] == tx_data['device_id']) |
            (self.mock_df['ip_id'] == tx_data['ip_id']) |
            (self.mock_df['merchant_id'] == tx_data['merchant_id'])
        )
        return self.mock_df[mask].copy()

    def _fetch_graph(self, db_cursor, tx_id: str, base_time: datetime):
        try:
            mysql_query = GRAPH_CTE_QUERY.replace(':seed_tx_id', '%s')\
                                         .replace(':global_start_time', '%s')\
                                         .replace(':global_end_time', '%s')
                                         
            start_time = base_time - timedelta(hours=24)
            end_time = base_time + timedelta(hours=24)
            
            db_cursor.execute(mysql_query, (tx_id, start_time, end_time))
            rows = db_cursor.fetchall()
            return build_graph_from_rows(rows)
        except Exception as e:
            logger.warning(f"Graph CTE failed (likely no DB): {e}")
            return {"nodes": [], "edges": []}

    def evaluate(self, tx_data: dict, db_cursor=None) -> Dict[str, Any]:
        """
        Orchestrates the full risk evaluation pipeline.
        """
        tx_id = tx_data['transaction_id']
        amount = float(tx_data['amount'])
        
        # 1. Fetch Context & Extract Features
        df_context = self._fetch_context(db_cursor, tx_data)
        
        # Append incoming transaction
        df_incoming = pd.DataFrame([tx_data])
        df_incoming['timestamp'] = pd.to_datetime(df_incoming['timestamp'], format='mixed')
        
        if len(df_context) > 0:
            df_combined = pd.concat([df_context, df_incoming], ignore_index=True)
        else:
            df_combined = df_incoming
            
        # Run Feature Engine
        engine = FeatureEngine(df_combined)
        df_features = engine.generate_all_features()
        
        # Extract features for the incoming transaction
        incoming_features = df_features[df_features['transaction_id'] == tx_id].iloc[0:1]
        
        # 2. Detection (Anomaly / Zero-Day)
        is_anomalous = bool(self.detector.is_anomalous(incoming_features)[0])
        
        # 3. Graph Intelligence (Triggered conditionally)
        graph_data = None
        if is_anomalous and db_cursor:
            graph_data = self._fetch_graph(db_cursor, tx_id, pd.to_datetime(tx_data['timestamp']))
            
        # 4. Prediction (Supervised Fraud Probability)
        p_fraud = float(self.predictor.predict_proba(incoming_features)[0])
        
        # 5. Financial Risk Optimization
        opt_result = self.optimizer.evaluate(p_fraud, amount)
        
        return {
            "transaction_id": tx_id,
            "timestamp": tx_data['timestamp'],
            "amount": amount,
            "is_anomalous": is_anomalous,
            "probability_fraud": round(p_fraud, 4),
            "action": opt_result['optimal_action'],
            "expected_cost": opt_result['min_expected_cost'],
            "cost_breakdown": opt_result['cost_breakdown'],
            "graph": graph_data
        }
