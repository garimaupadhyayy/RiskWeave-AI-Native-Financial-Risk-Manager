import mysql.connector
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    conn = mysql.connector.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
    )
    cursor = conn.cursor()

    # Create Database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DATABASE};")
    cursor.execute(f"USE {settings.MYSQL_DATABASE};")

    # Drop existing tables for fresh start during simulator run
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    tables = ['entity_relationships', 'transactions', 'ips', 'devices', 'merchants', 'customers']
    for t in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {t};")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # Customers
    cursor.execute("""
    CREATE TABLE customers (
        customer_id VARCHAR(50) PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_high_roller BOOLEAN DEFAULT FALSE,
        is_corporate BOOLEAN DEFAULT FALSE
    );
    """)

    # Merchants
    cursor.execute("""
    CREATE TABLE merchants (
        merchant_id VARCHAR(50) PRIMARY KEY,
        category VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Devices
    cursor.execute("""
    CREATE TABLE devices (
        device_id VARCHAR(50) PRIMARY KEY,
        device_type VARCHAR(50)
    );
    """)

    # IPs
    cursor.execute("""
    CREATE TABLE ips (
        ip_id VARCHAR(50) PRIMARY KEY,
        country VARCHAR(50)
    );
    """)

    # Transactions (No ground truth labels here to prevent leakage!)
    cursor.execute("""
    CREATE TABLE transactions (
        transaction_id VARCHAR(50) PRIMARY KEY,
        customer_id VARCHAR(50),
        merchant_id VARCHAR(50),
        device_id VARCHAR(50),
        ip_id VARCHAR(50),
        amount DECIMAL(15,2),
        timestamp DATETIME,
        status VARCHAR(20),
        payment_method VARCHAR(50),
        auth_status VARCHAR(20),
        is_refund BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id),
        FOREIGN KEY (device_id) REFERENCES devices(device_id),
        FOREIGN KEY (ip_id) REFERENCES ips(ip_id),
        INDEX idx_timestamp (timestamp),
        INDEX idx_customer (customer_id),
        INDEX idx_merchant (merchant_id)
    );
    """)

    # Entity Relationships (Explicit edges for graph traversal)
    cursor.execute("""
    CREATE TABLE entity_relationships (
        source_id VARCHAR(50),
        source_type VARCHAR(20),
        target_id VARCHAR(50),
        target_type VARCHAR(20),
        relationship_type VARCHAR(50),
        last_seen DATETIME,
        weight INT DEFAULT 1,
        PRIMARY KEY (source_id, target_id, relationship_type),
        INDEX idx_source (source_id, source_type),
        INDEX idx_target (target_id, target_type)
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    logger.info(f"Database {settings.MYSQL_DATABASE} initialized successfully with strict schema.")

if __name__ == "__main__":
    init_db()
