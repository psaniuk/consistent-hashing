import asyncio
from datetime import datetime
from app.db_partitions_manager import *


async def main():
    ports = [3306, 3307, 3308]
    db_configs = [
        {
            "host": "127.0.0.1",
            "port": port,
            "user": "user",
            "password": "pwd",
            "database": "metrics_db",
        }
        for port in ports
    ]

    configure(db_configs)
    # partition_key = datetime.now()
    # print(":".join(str(partition_key).split(":")[:2]))

    # await execute(
    #     f"INSERT INTO metrics (name, value, timestamp) VALUES(%s, %s, %s);",
    #     ("metric1", 100, datetime.now()),
    #     partition_key,
    # )

    # print(
    #     await execute(
    #         f"SELECT * FROM metrics;",
    #         (),
    #         partition_key,
    #     )
    # )


if __name__ == "__main__":
    asyncio.run(main())
