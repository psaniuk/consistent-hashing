import app.db_partitions_manager


class TestDbPartitionsManager:
    def test_configure(self):
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

        app.db_partitions_manager.configure(db_configs)
        assert app.db_partitions_manager.virtual_nodes_index is not None
        assert len(app.db_partitions_manager.range_to_db_config_mappings.keys()) == 1000
