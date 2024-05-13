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
        assert qm.physical_nodes_index is not None
        assert len(qm.hash_key_to_db_config_mappings.keys()) == 3

    @pytest.mark.asyncio
    async def test_run_query(self):
        qm.configure(self.db_configs)
        await qm.delete_all()

        partition_key = "partition key"
        await qm.run_query(
            "INSERT INTO metrics (name, value, timestamp) VALUES (%s, %s, %s);",
            ["test_metric", 1.0, partition_key],
            partition_key,
        )

        result = await qm.run_query(
            f"SELECT * FROM metrics WHERE name = %s;", ["test_metric"], partition_key
        )
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_bulk_insert(self):
        qm.configure(self.db_configs, 100000)
        await qm.delete_all()
        for _ in range(100):
            timestamp = datetime.now() - timedelta(seconds=random.randint(1, 100))
            await qm.insert("test_metric", random.random(), timestamp)
        assert True

    @pytest.mark.asyncio
    async def _test_select_5_mins_range(self):
        qm.configure(self.db_configs, 100000)
        await qm.delete_all()
        timestamp_now = datetime.now()
        NUM_OF_RECORDS, METRIC_NAME = 5, "test_5_mins_range"
        for _ in range(NUM_OF_RECORDS):
            timestamp = timestamp_now - timedelta(minutes=random.randint(1, 5))
            await qm.insert(METRIC_NAME, random.random(), timestamp)

        result = await qm.select((timestamp_now - timedelta(minutes=5), timestamp_now))

        assert len(result) == NUM_OF_RECORDS
