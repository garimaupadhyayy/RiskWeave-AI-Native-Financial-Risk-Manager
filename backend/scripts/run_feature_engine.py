import argparse
import logging
import pandas as pd
import os
from features.engine import FeatureEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_feature_engine(input_csv, output_csv):
    logger.info(f"Loading data from {input_csv}...")
    df_tx = pd.read_csv(input_csv, parse_dates=['timestamp'])
    
    logger.info("Initializing Feature Engine...")
    engine = FeatureEngine(df_tx)
    
    logger.info("Generating Features (this may take a moment for large datasets)...")
    df_features = engine.generate_all_features()
    
    logger.info(f"Saving features to {output_csv}...")
    df_features.to_csv(output_csv, index=False)
    logger.info("Feature extraction complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='../data/ground_truth.csv')
    parser.add_argument('--output', type=str, default='../data/features.csv')
    args = parser.parse_args()
    
    input_path = os.path.join(os.path.dirname(__file__), args.input)
    output_path = os.path.join(os.path.dirname(__file__), args.output)
    
    run_feature_engine(input_path, output_path)
