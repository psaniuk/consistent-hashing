from datetime import datetime, timedelta
import pytest
import app.query_manager as qm
import random


class TestDbPartitionsManager:
    @property
    def db_configs(self):
        ports = [3306, 3307, 3308]
        return [
            {
                "host": "127.0.0.1",
                "port": port,
                "user": "user",
                "password": "pwd",
                "database": "metrics_db",
            }
            for port in ports
        ]

    def test_configure(self):
        qm.configure(self.db_configs, 100000)
        assert qm.virtual_nodes_index is not None
        assert len(qm.range_to_db_config_mappings.keys()) == 100000

    @pytest.mark.asyncio
    async def test_run_query(self):
        qm.configure(self.db_configs)
        await qm.run_query(
            f"INSERT INTO metrics (name, value, timestamp) VALUES(%s, %s, %s);",
            ("test_metric", 100, datetime.now()),
            "test",
        )
        result = await qm.run_query(
            f"SELECT * FROM metrics WHERE name = %s;", ["test_metric"], "test"
        )
        assert len(result) >= 1

    @pytest.mark.asyncio
    async def test_bulk_insert(self):
        qm.configure(self.db_configs, 100000)
        for _ in range(10000):
            partition_key = str(
                datetime.now() - timedelta(seconds=random.randint(1, 10))
            ).split(".")[0]
            await qm.run_query(
                f"INSERT INTO metrics (name, value, timestamp) VALUES(%s, %s, %s);",
                ("test_metric", random.random(), datetime.now()),
                partition_key,
            )
        assert True
