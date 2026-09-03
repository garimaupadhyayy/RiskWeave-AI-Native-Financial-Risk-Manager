import logging
import pandas as pd
import os
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def run_ablation(features_path):
    logger.info("==================================================")
    logger.info("  RISKWEAVE ABLATION STUDY: BASELINE VS 10-D DNA")
    logger.info("==================================================")
    
    df = pd.read_csv(features_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
    
    # --- Prepare Baseline Features ---
    df['hour_of_day'] = df['timestamp'].dt.hour
    df['is_refund_int'] = df['is_refund'].astype(int)
    
    le = LabelEncoder()
    df['payment_method_encoded'] = le.fit_transform(df['payment_method'])
    
    baseline_cols = ['amount', 'hour_of_day', 'is_refund_int', 'payment_method_encoded']
    
    # --- Prepare RiskWeave DNA Features ---
    dna_cols = [
        'dna_entity_reuse_1h', 'dna_entity_reuse_24h', 'dna_velocity_burst',
        'dna_amount_escalation', 'dna_auth_failure_rate', 'dna_graph_degree_proxy',
        'dna_merchant_concentration_1h', 'dna_temporal_density_5m',
        'dna_payment_diversity', 'dna_account_age_hours',
        'attack_momentum'
    ]
    
    # --- Temporal Splitting ---
    start_date = df['timestamp'].min()
    train_end = start_date + pd.Timedelta(days=20)
    test_start = start_date + pd.Timedelta(days=25)
    
    df_train = df[df['timestamp'] < train_end]
    df_test = df[df['timestamp'] >= test_start]
    
    logger.info(f"Train Set: {len(df_train)} records (Days 1-20)")
    logger.info(f"Test Set:  {len(df_test)} records (Days 26-30 - Unseen Topology)\n")
    
    num_neg = (df_train['is_fraud'] == 0).sum()
    num_pos = (df_train['is_fraud'] == 1).sum()
    scale_pos = num_neg / num_pos
    
    y_train = df_train['is_fraud']
    y_test = df_test['is_fraud']
    
    # --- Model A: Baseline ---
    logger.info("Training Model A: Naive ML (Isolated Features)...")
    model_baseline = xgb.XGBClassifier(
        max_depth=5, learning_rate=0.1, n_estimators=100, 
        scale_pos_weight=scale_pos, eval_metric='auc', random_state=42
    )
    model_baseline.fit(df_train[baseline_cols], y_train)
    
    # --- Model B: RiskWeave ---
    logger.info("Training Model B: RiskWeave (10-D Attack DNA)...")
    model_rw = xgb.XGBClassifier(
        max_depth=5, learning_rate=0.1, n_estimators=100, 
        scale_pos_weight=scale_pos, eval_metric='auc', random_state=42
    )
    model_rw.fit(df_train[dna_cols], y_train)
    
    # --- Evaluation ---
    logger.info("\nEvaluating on Unseen 'Rotating-Device Ring' Topology...")
    
    def evaluate(model, X):
        y_pred = model.predict(X)
        y_prob = model.predict_proba(X)[:, 1]
        
        return {
            'auc': roc_auc_score(y_test, y_prob),
            'prec': precision_score(y_test, y_pred, zero_division=0),
            'rec': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0)
        }
        
    res_base = evaluate(model_baseline, df_test[baseline_cols])
    res_rw = evaluate(model_rw, df_test[dna_cols])
    
    # --- Output Matrix ---
    logger.info("\n" + "="*60)
    logger.info(f"{'Metric':<15} | {'Model A (Naive ML)':<20} | {'Model B (RiskWeave)':<20}")
    logger.info("-" * 60)
    logger.info(f"{'ROC-AUC':<15} | {res_base['auc']*100:>18.2f}% | {res_rw['auc']*100:>18.2f}%")
    logger.info(f"{'Precision':<15} | {res_base['prec']*100:>18.2f}% | {res_rw['prec']*100:>18.2f}%")
    logger.info(f"{'Recall':<15} | {res_base['rec']*100:>18.2f}% | {res_rw['rec']*100:>18.2f}%")
    logger.info(f"{'F1-Score':<15} | {res_base['f1']*100:>18.2f}% | {res_rw['f1']*100:>18.2f}%")
    logger.info("=" * 60)
    
    if res_rw['rec'] > res_base['rec']:
        uplift = ((res_rw['rec'] - res_base['rec']) / (res_base['rec'] + 1e-9)) * 100
        logger.info(f"\n🚀 CONCLUSION: RiskWeave's 10-D DNA outperformed Naive ML by {uplift:.1f}% in Recall on zero-day topologies!")
    else:
        logger.info("\nCONCLUSION: Baseline performed adequately.")

if __name__ == "__main__":
    input_path = os.path.join(os.path.dirname(__file__), '../data/features.csv')
    run_ablation(input_path)
