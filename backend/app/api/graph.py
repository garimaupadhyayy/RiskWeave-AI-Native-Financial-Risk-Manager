from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from app.db.session import get_db
from graph.queries import GRAPH_CTE_QUERY, build_graph_from_rows

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{transaction_id}")
def get_transaction_graph(transaction_id: str, db=Depends(get_db)):
    """
    Retrieves the 2-hop entity graph for a given transaction.
    """
    try:
        # Fetch the transaction to get its timestamp for bounds
        # In a real setup, we'd use SQLAlchemy, but we can do a raw query
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT timestamp FROM transactions WHERE transaction_id = %s", (transaction_id,))
        tx = cursor.fetchone()
        
        if not tx:
            raise HTTPException(status_code=404, detail="Transaction not found")
            
        base_time = tx['timestamp']
        
        # We replace the named parameters with %s for MySQL connector
        mysql_query = GRAPH_CTE_QUERY.replace(':seed_tx_id', '%s')\
                                     .replace(':global_start_time', '%s')\
                                     .replace(':global_end_time', '%s')
                                     
        from datetime import timedelta
        start_time = base_time - timedelta(hours=24)
        end_time = base_time + timedelta(hours=24)
        
        cursor.execute(mysql_query, (transaction_id, start_time, end_time))
        rows = cursor.fetchall()
        
        graph_data = build_graph_from_rows(rows)
        return graph_data
        
    except Exception as e:
        logger.error(f"Graph traversal failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
