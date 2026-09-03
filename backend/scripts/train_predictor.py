import argparse
import logging
import pandas as pd
import os
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
from models.predictor import FraudPredictor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_training(features_path, output_dir):
    logger.info(f"Loading features from {features_path}...")
    df = pd.read_csv(features_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
    
    # 1. Temporal Splitting
    start_date = df['timestamp'].min()
    
    # Train: Days 1-20
    train_end = start_date + pd.Timedelta(days=20)
    # Validate/Test: Days 26-30
    test_start = start_date + pd.Timedelta(days=25)
    
    df_train = df[df['timestamp'] < train_end]
    df_test = df[df['timestamp'] >= test_start]
    
    logger.info(f"Data Splits -> Train: {len(df_train)}, Test: {len(df_test)}")
    
    # 2. Handle Class Imbalance dynamically
    num_neg = (df_train['is_fraud'] == 0).sum()
    num_pos = (df_train['is_fraud'] == 1).sum()
    
    # If no fraud in train set (possible if scale is too small)
    if num_pos == 0:
        logger.error("No fraud found in training set! Increase dataset scale.")
        return
        
    scale_pos_weight = num_neg / num_pos
    logger.info(f"Calculated scale_pos_weight: {scale_pos_weight:.2f} ({num_neg} Legitimate / {num_pos} Fraud)")

    # 3. Initialize and Train
    predictor = FraudPredictor(scale_pos_weight=scale_pos_weight)
    predictor.fit(df_train)
    
    # 4. Save Artifacts
    predictor.save(output_dir)
    
    # 5. Evaluate on Test (Unseen Topology)
    logger.info(f"--- TEST SET PERFORMANCE (Days 26-30) ---")
    logger.info(f"Includes Unseen 'Rotating-Device Ring' Topology")
    
    y_true = df_test['is_fraud']
    if y_true.sum() == 0:
        logger.warning("No fraud in the test set to evaluate metrics on.")
    else:
        y_pred = predictor.predict(df_test)
        y_prob = predictor.predict_proba(df_test)
        
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_true, y_prob)
        
        logger.info(f"ROC-AUC:   {roc_auc*100:.2f}%")
        logger.info(f"Precision: {prec*100:.2f}%")
        logger.info(f"Recall:    {rec*100:.2f}%")
        logger.info(f"F1-Score:  {f1*100:.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='../data/features.csv')
    parser.add_argument('--output_dir', type=str, default='artifacts')
    args = parser.parse_args()
    
    input_path = os.path.join(os.path.dirname(__file__), args.input)
    out_dir = os.path.join(os.path.dirname(__file__), '../models', args.output_dir)
    
    run_training(input_path, out_dir)
