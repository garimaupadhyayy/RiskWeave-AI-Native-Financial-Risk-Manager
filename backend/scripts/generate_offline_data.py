import argparse
import logging
import pandas as pd
import os
from simulator import generator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--scale', type=float, default=1.0)
    args = parser.parse_args()

    # Generate Data
    entities, df_tx = generator.run(scale=args.scale)

    # Save Ground Truth
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    os.makedirs(data_dir, exist_ok=True)
    gt_path = os.path.join(data_dir, 'ground_truth.csv')
    df_tx.to_csv(gt_path, index=False)
    logger.info(f"Ground truth saved to {gt_path} with {len(df_tx)} rows.")
