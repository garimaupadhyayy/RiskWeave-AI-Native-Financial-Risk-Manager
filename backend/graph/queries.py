import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

# The raw recursive CTE query. Uses standard SQL supported by MySQL and SQLite.
# We pass global time bounds to avoid dialect-specific interval math.
GRAPH_CTE_QUERY = """
WITH RECURSIVE graph_traversal AS (
    -- Anchor Member (Depth 0)
    SELECT 
        transaction_id, 
        customer_id, 
        device_id, 
        ip_id, 
        amount, 
        timestamp, 
        0 AS depth
    FROM transactions
    WHERE transaction_id = :seed_tx_id

    UNION

    -- Recursive Member (Depth 1 & 2)
    SELECT 
        t.transaction_id, 
        t.customer_id, 
        t.device_id, 
        t.ip_id, 
        t.amount, 
        t.timestamp,
        g.depth + 1 AS depth
    FROM transactions t
    INNER JOIN graph_traversal g 
        ON (
            t.device_id = g.device_id OR 
            t.ip_id = g.ip_id OR 
            t.customer_id = g.customer_id
        )
    WHERE g.depth < 2
      AND t.transaction_id != g.transaction_id
      AND t.timestamp >= :global_start_time
      AND t.timestamp <= :global_end_time
)
SELECT * FROM graph_traversal LIMIT 500;
"""

def build_graph_from_rows(rows):
    """
    Transforms tabular CTE rows into a D3-friendly Nodes & Edges dictionary.
    Nodes: Transactions, Customers, Devices, IPs
    Edges: Relationships between them
    """
    nodes = {}
    edges = []
    
    def add_node(node_id, label, properties):
        if node_id not in nodes:
            nodes[node_id] = {'id': node_id, 'label': label, **properties}
            
    for row in rows:
        # Depending on the DB driver, row could be a dict or tuple. Assuming dict/Object for now.
        tx_id = row['transaction_id']
        cust_id = row['customer_id']
        dev_id = row['device_id']
        ip = row['ip_id']
        
        # Add Transaction Node
        add_node(tx_id, 'Transaction', {
            'amount': row['amount'], 
            'timestamp': str(row['timestamp']),
            'depth': row['depth']
        })
        
        # Add Entity Nodes
        add_node(cust_id, 'Customer', {})
        add_node(dev_id, 'Device', {})
        add_node(ip, 'IP_Address', {})
        
        # Add Edges
        edges.append({'source': tx_id, 'target': cust_id, 'relation': 'PERFORMED_BY'})
        edges.append({'source': tx_id, 'target': dev_id, 'relation': 'FROM_DEVICE'})
        edges.append({'source': tx_id, 'target': ip, 'relation': 'FROM_IP'})

    # Deduplicate edges just in case
    unique_edges = []
    seen = set()
    for e in edges:
        sig = (e['source'], e['target'], e['relation'])
        if sig not in seen:
            seen.add(sig)
            unique_edges.append(e)

    return {
        'nodes': list(nodes.values()),
        'edges': unique_edges
    }
