from app.sql_query_executor import configure


def main():
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


if __name__ == "__main__":
    main()
