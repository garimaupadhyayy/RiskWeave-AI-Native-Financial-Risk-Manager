import logging
from app.services.optimizer import CostOptimizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_tests():
    optimizer = CostOptimizer()
    
    test_cases = [
        {"name": "Low Risk, Low Amount", "p": 0.001, "v": 20.0},
        {"name": "Low Risk, High Amount", "p": 0.001, "v": 5000.0},
        {"name": "Medium Risk, Low Amount", "p": 0.15, "v": 15.0},
        {"name": "Medium Risk, High Amount", "p": 0.15, "v": 4000.0},
        {"name": "High Risk, Low Amount", "p": 0.95, "v": 25.0},
        {"name": "High Risk, High Amount", "p": 0.95, "v": 8000.0},
    ]
    
    logger.info("Running Financial Risk Optimizer Validation...")
    
    for case in test_cases:
        res = optimizer.evaluate(case["p"], case["v"])
        logger.info(f"--- {case['name']} ---")
        logger.info(f"Inputs: p={case['p']:.3f}, Amount=${case['v']:.2f}")
        logger.info(f"Optimal Action: {res['optimal_action']} (Expected Cost: ${res['min_expected_cost']:.2f})")
        logger.info(f"Breakdown: {res['cost_breakdown']}")
        print()

if __name__ == "__main__":
    run_tests()
