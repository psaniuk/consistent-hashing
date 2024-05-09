from datetime import datetime, timedelta
import pytest
import app.query_manager as qm
import random
from app.timestamp import datetime_to_hh_mm_ss, now_str_hh_mm_ss


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

    async def insert_data(self, params, partition_key):
        await qm.run_query(
            f"INSERT INTO metrics (name, value, timestamp) VALUES(%s, %s, %s);",
            params,
            partition_key,
        )

    @pytest.mark.asyncio
    async def test_run_query(self):
        qm.configure(self.db_configs)
        await self.insert_data(("test_metric", 100, datetime.now()), now_str_hh_mm_ss())

        result = await qm.run_query(
            f"SELECT * FROM metrics WHERE name = %s;", ["test_metric"], "test"
        )
        assert len(result) >= 1

    @pytest.mark.asyncio
    # async def test_bulk_insert(self):
    async def bulk_insert(self):
        qm.configure(self.db_configs, 100000)
        for _ in range(10000):
            timestamp = datetime.now() - timedelta(seconds=random.randint(1, 10))
            await self.insert_data(
                ("test_metric", random.random(), timestamp),
                datetime_to_hh_mm_ss(timestamp),
            )
        assert True

    @pytest.mark.asyncio
    async def test_select_5_mins_range(self):
        qm.configure(self.db_configs, 100000)
        timestamp_now = datetime.now()
        NUM_OF_RECORDS, METRIC_NAME = 5, "test_5_mins_range"
        for _ in range(NUM_OF_RECORDS):
            timestamp = timestamp_now - timedelta(minutes=random.randint(1, 5))
            await self.insert_data(
                (METRIC_NAME, random.random(), timestamp),
                datetime_to_hh_mm_ss(timestamp),
            )

        result = await qm.run_select(
            (timestamp_now - timedelta(minutes=5), timestamp_now)
        )

        assert len(result) >= NUM_OF_RECORDS
