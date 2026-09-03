import logging
from app.services.agent import GeminiInvestigator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_gemini_agent():
    logger.info("Initializing Gemini Investigator...")
    agent = GeminiInvestigator()
    
    mock_payload = {
      "transaction_id": "tx_evil_99",
      "timestamp": "2026-09-09 12:05:00",
      "amount": 9500.0,
      "is_anomalous": True,
      "probability_fraud": 0.985,
      "action": "REVIEW",
      "expected_cost": 45.0,
      "cost_breakdown": {
        "ALLOW": 9357.5,
        "MONITOR": 9357.55,
        "STEP_UP": 475.1,
        "REVIEW": 45.0,
        "HOLD": 35.6
      },
      "graph": {
        "nodes": [
          {"id": "tx_evil_99", "label": "Transaction", "amount": 9500.0},
          {"id": "C_hacker", "label": "Customer"},
          {"id": "D_burner", "label": "Device"}
        ],
        "edges": [
          {"source": "tx_evil_99", "target": "C_hacker", "relation": "PERFORMED_BY"},
          {"source": "tx_evil_99", "target": "D_burner", "relation": "FROM_DEVICE"}
        ]
      }
    }
    
    logger.info("Generating summary...")
    summary = agent.generate_summary(mock_payload)
    
    print("\n--- GENERATED SUMMARY ---")
    print(summary)
    print("-------------------------\n")

if __name__ == "__main__":
    test_gemini_agent()
