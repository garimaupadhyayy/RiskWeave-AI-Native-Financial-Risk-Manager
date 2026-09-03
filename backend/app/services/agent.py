import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GeminiInvestigator:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = None
        
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Gemini API Client initialized successfully.")
            except ImportError:
                logger.error("google-genai package not found. Running in offline/mock mode.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini Client: {e}")
        else:
            logger.warning("GEMINI_API_KEY not found in environment. Running in offline/mock mode.")

    def generate_summary(self, payload: Dict[str, Any]) -> str:
        """
        Takes the policy engine evaluation payload and returns a markdown summary.
        """
        system_instruction = (
            "You are an expert AI Risk Investigator for RiskWeave. You are analyzing a transaction "
            "that has already been flagged for REVIEW or HOLD by an XGBoost model and Cost Optimizer. "
            "Your job is NOT to make a decision, but to concisely explain the provided telemetry to a human analyst. "
            "Highlight extreme values in the features, interpret the Cost Breakdown mathematically, "
            "and describe the Graph topology if provided. Keep it under 4 paragraphs."
        )
        
        prompt = f"Please provide an investigation summary for this transaction payload:\n\n{json.dumps(payload, indent=2)}"
        
        if self.client:
            try:
                from google.genai import types
                
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2,
                    ),
                )
                return response.text
            except Exception as e:
                logger.error(f"Gemini API call failed: {e}")
                return self._mock_summary(payload)
        else:
            return self._mock_summary(payload)

    def _mock_summary(self, payload: Dict[str, Any]) -> str:
        tx_id = payload.get("transaction_id", "Unknown")
        action = payload.get("action", "UNKNOWN")
        p_fraud = payload.get("probability_fraud", 0)
        
        return (
            f"### MOCK INVESTIGATION REPORT (Offline Mode)\n"
            f"**Transaction:** `{tx_id}` | **Action Taken:** `{action}`\n\n"
            f"The XGBoost model assigned a **{p_fraud*100:.2f}%** probability of fraud based on the Attack DNA. "
            f"The Cost Optimizer mathematically selected **{action}** to minimize expected financial loss.\n\n"
            f"*(Note: Provide a valid `GEMINI_API_KEY` to enable live generative AI summaries!)*"
        )
