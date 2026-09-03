import argparse
import logging
import pandas as pd
import os
from models.detector import AnomalyDetector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_training(features_path, output_dir, target_fpr):
    logger.info(f"Loading features from {features_path}...")
    df = pd.read_csv(features_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
    
    # 1. Temporal Splitting
    # Find the start date dynamically
    start_date = df['timestamp'].min()
    
    # Train: Days 1-20
    train_end = start_date + pd.Timedelta(days=20)
    # Val: Days 21-25
    val_end = start_date + pd.Timedelta(days=25)
    
    df_train = df[df['timestamp'] < train_end]
    df_val = df[(df['timestamp'] >= train_end) & (df['timestamp'] < val_end)]
    df_test = df[df['timestamp'] >= val_end]
    
    logger.info(f"Data Splits -> Train: {len(df_train)}, Val: {len(df_val)}, Test: {len(df_test)}")
    
    if len(df_train) == 0 or len(df_val) == 0:
        logger.error("Insufficient data for splitting. Adjust your dataset scale or dates.")
        return

    # 2. Initialize and Train
    detector = AnomalyDetector(random_state=42)
    detector.fit(df_train)
    
    # 3. Calibrate
    detector.calibrate(df_val, target_fpr=target_fpr)
    
    # 4. Save Artifacts
    detector.save(output_dir)
    
    # 5. Evaluate on Test (Unseen Topology)
    # Since we are unsupervised, we just report how many it flagged
    # Ground truth is used here ONLY for reporting, not for model logic
    if 'is_fraud' in df_test.columns:
        scores = detector.predict_scores(df_test)
        flagged = scores < detector.threshold
        
        true_fraud = df_test['is_fraud'] == 1
        
        tp = (flagged & true_fraud).sum()
        fp = (flagged & ~true_fraud).sum()
        fn = (~flagged & true_fraud).sum()
        
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        
        logger.info(f"--- TEST SET PERFORMANCE (Days 26-30) ---")
        logger.info(f"Includes Unseen 'Rotating-Device Ring' Topology")
        logger.info(f"Recall (Fraud Detected): {recall*100:.2f}%")
        logger.info(f"Precision: {precision*100:.2f}%")
        logger.info(f"Flagged {flagged.sum()} out of {len(df_test)} transactions.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='../data/features.csv')
    parser.add_argument('--output_dir', type=str, default='artifacts')
    parser.add_argument('--fpr', type=float, default=0.05, help="Target False Positive Rate for calibration")
    args = parser.parse_args()
    
    input_path = os.path.join(os.path.dirname(__file__), args.input)
    out_dir = os.path.join(os.path.dirname(__file__), '../models', args.output_dir)
    
    run_training(input_path, out_dir, args.fpr)
