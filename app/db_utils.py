import mysql.connector
from mysql.connector.aio import connect


def create_connection_pool(
    id: int, db_config: dict, default_pool_size: int = 5
) -> mysql.connector.pooling.MySQLConnectionPool:
    return mysql.connector.pooling.MySQLConnectionPool(
        pool_name=f"pool_{id}", pool_size=default_pool_size, **db_config
    )
