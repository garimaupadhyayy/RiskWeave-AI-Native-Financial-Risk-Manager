import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CostOptimizer:
    """
    Calculates the Expected Financial Cost of various interventions
    and selects the action that minimizes overall loss.
    """
    
    def __init__(self, 
                 sms_cost: float = 0.10, 
                 manual_review_cost: float = 5.00,
                 mfa_dropoff_rate: float = 0.05,
                 review_dropoff_rate: float = 0.10,
                 insult_cost_factor: float = 0.25):
        self.sms_cost = sms_cost
        self.manual_review_cost = manual_review_cost
        self.mfa_dropoff_rate = mfa_dropoff_rate
        self.review_dropoff_rate = review_dropoff_rate
        self.insult_cost_factor = insult_cost_factor

    def evaluate(self, p_fraud: float, amount: float) -> Dict[str, Any]:
        """
        Evaluate costs for all actions given a probability of fraud and transaction amount.
        Returns the optimal action and a breakdown of all expected costs.
        """
        
        # 1. ALLOW
        # E[Cost] = p * amount + (1-p) * 0
        cost_allow = p_fraud * amount
        
        # 2. MONITOR
        # E[Cost] = p * amount + 0.05 (logging/alerting marginal cost)
        cost_monitor = (p_fraud * amount) + 0.05
        
        # 3. STEP_UP (MFA)
        # Cost if legit: friction drop-off + sms cost
        # Cost if fraud: 5% of fraudsters still bypass MFA + sms cost
        cost_stepup = (1 - p_fraud) * (self.mfa_dropoff_rate * amount + self.sms_cost) + \
                      p_fraud * (self.mfa_dropoff_rate * amount + self.sms_cost)
        # Simplifies to: mfa_dropoff_rate * amount + sms_cost
        
        # 4. REVIEW
        # Cost if legit: review delay causes 10% drop-off
        # Cost if fraud: 0 (agent catches it)
        # Base cost: $5.00 human time
        cost_review = self.manual_review_cost + (1 - p_fraud) * (self.review_dropoff_rate * amount)
        
        # 5. HOLD (Block)
        # Cost if legit: Insult cost (churn, margin loss)
        # Cost if fraud: 0
        cost_hold = (1 - p_fraud) * (self.insult_cost_factor * amount)
        
        costs = {
            "ALLOW": round(cost_allow, 4),
            "MONITOR": round(cost_monitor, 4),
            "STEP_UP": round(cost_stepup, 4),
            "REVIEW": round(cost_review, 4),
            "HOLD": round(cost_hold, 4)
        }
        
        optimal_action = min(costs, key=costs.get)
        
        return {
            "optimal_action": optimal_action,
            "min_expected_cost": costs[optimal_action],
            "cost_breakdown": costs,
            "inputs": {
                "p_fraud": p_fraud,
                "amount": amount
            }
        }
