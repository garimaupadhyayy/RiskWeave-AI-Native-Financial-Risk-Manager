from fastapi import FastAPI
import mysql.connector
from mysql.connector import Error as MySQLError
import redis
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)

from app.api import graph, evaluate
app.include_router(graph.router, prefix="/api/v1/graph", tags=["Graph Intelligence"])
app.include_router(evaluate.router, prefix="/api/v1/evaluate", tags=["Policy Engine"])

@app.get("/api/v1/system/health")
def health_check():
    status = {
        "status": "ok",
        "mysql": "unknown",
        "redis": "unknown"
    }

    # Check MySQL
    try:
        conn = mysql.connector.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DATABASE,
            connect_timeout=2
        )
        if conn.is_connected():
            status["mysql"] = "connected"
            conn.close()
    except MySQLError as e:
        status["mysql"] = f"error: {str(e)}"
        status["status"] = "degraded"

    # Check Redis
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, socket_connect_timeout=2)
        if r.ping():
            status["redis"] = "connected"
    except redis.RedisError as e:
        status["redis"] = f"error: {str(e)}"
        status["status"] = "degraded"

    return status

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}
