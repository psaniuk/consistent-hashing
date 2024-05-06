from datetime import datetime
import pytest
import app.query_manager as qm


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
        qm.configure(self.db_configs)
        assert qm.virtual_nodes_index is not None
        assert len(qm.range_to_db_config_mappings.keys()) == 1000

    @pytest.mark.asyncio
    async def test_run_query(self):
        qm.configure(self.db_configs)
        await qm.run_query(
            f"INSERT INTO metrics (name, value, timestamp) VALUES(%s, %s, %s);",
            ("test_metric", 100, datetime.now()),
            "test",
        )
        result = await qm.run_query(
            "SELECT * FROM metrics WHERE name = 'test_metric';", (), "test"
        )
        assert len(result) >= 1
