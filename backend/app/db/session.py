import mysql.connector
from app.core.config import settings

def get_db():
    conn = mysql.connector.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE,
        ssl_verify_cert=False,
        ssl_verify_identity=False
    )
    try:
        yield conn
    finally:
        conn.close()
