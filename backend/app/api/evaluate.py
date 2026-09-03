from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import os

from app.db.session import get_db
from app.services.policy import PolicyEngine
from app.services.agent import GeminiInvestigator

router = APIRouter()
logger = logging.getLogger(__name__)

# Single instance of the PolicyEngine
models_dir = os.path.join(os.path.dirname(__file__), '../../models/artifacts')
policy_engine = None
investigator = None

def get_policy_engine():
    global policy_engine
    if policy_engine is None:
        policy_engine = PolicyEngine(models_dir)
    return policy_engine

def get_investigator():
    global investigator
    if investigator is None:
        investigator = GeminiInvestigator()
    return investigator

class TransactionRequest(BaseModel):
    transaction_id: str
    timestamp: str
    customer_id: str
    merchant_id: str
    amount: float
    device_id: str
    ip_id: str
    payment_method: str
    auth_status: str
    is_refund: bool

@router.post("")
def evaluate_transaction(tx: TransactionRequest, db=Depends(get_db)):
    """
    Evaluates a transaction through the RiskWeave pipeline.
    """
    try:
        cursor = db.cursor(dictionary=True)
        # Convert pydantic model to dict
        tx_dict = tx.dict()
        
        engine = get_policy_engine()
        result = engine.evaluate(tx_dict, db_cursor=cursor)
        
        # Trigger Gemini if action is REVIEW or HOLD
        if result['action'] in ['REVIEW', 'HOLD']:
            logger.info(f"Triggering Gemini Agent for {result['action']} decision...")
            agent = get_investigator()
            summary = agent.generate_summary(result)
            result['investigation_summary'] = summary
            
        return result
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        # In a real system we would fail open (ALLOW) but for hackathon we raise
        raise HTTPException(status_code=500, detail=str(e))
