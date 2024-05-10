from datetime import datetime, timedelta
from typing import Sequence
from app.data_access import *
from app.consistent_hashing import *
from app.timestamp import datetime_to_hh_mm_ss
from app.virtual_nodes_index import *

virtual_nodes_index = None
range_to_db_config_mappings = {}


def configure(db_configs: list[dict], number_of_virtual_nodes: int = 1000):
    if not db_configs:
        raise ValueError("DB configs should not be empty")

    if number_of_virtual_nodes <= 0:
        raise ValueError("Number of virtual nodes should be greater than 0")

    global virtual_nodes_index
    virtual_nodes_index = build_virtual_nodes_index(
        number_of_virtual_nodes,
        get_range_size(number_of_virtual_nodes),
    )

    configs = db_configs * number_of_virtual_nodes

    ranges = map_virtual_nodes_to_ranges(
        number_of_virtual_nodes, get_range_size(number_of_virtual_nodes)
    )

    global range_to_db_config_mappings
    range_to_db_config_mappings = {
        key_range: db_node_config
        for key_range, db_node_config in list(zip(ranges, configs[: len(ranges)]))
    }


async def run_query(query: str, parameters: Sequence[any], partition_key: any) -> any:
    __validate_config()
    range = __search_range(partition_key)
    db_config = __map_to_db_config(range)
    return await execute_query(query, parameters, db_config)


async def insert(metric_name: str, value: float, timestamp: datetime) -> any:
    __validate_config()
    range = __search_range(__get_partition_key(timestamp))
    db_config = __map_to_db_config(range)
    query = "INSERT INTO metrics (name, value, timestamp) VALUES(%s, %s, %s);"
    return await execute_query(query, (metric_name, value, timestamp), db_config)


async def select(datetime_range: tuple[datetime, datetime]) -> any:
    __validate_config()

    start_at, end_at = datetime_range
    distinct_ranges = set()
    while start_at < end_at:
        range = __search_range(__get_partition_key(start_at))
        distinct_ranges.add(range)
        start_at += timedelta(seconds=1)

    host_to_config_mappings = {}
    for range in distinct_ranges:
        db_config = __map_to_db_config(range)
        config_key = str(db_config["host"]) + str(db_config["port"])
        if config_key not in host_to_config_mappings:
            host_to_config_mappings[config_key] = db_config

    query = "SELECT * FROM metrics WHERE timestamp >= %s AND timestamp <= %s;"
    result = []
    for config in list(host_to_config_mappings.values()):
        result.extend(await execute_query(query, datetime_range, config))
    return result


def __map_to_db_config(range: tuple[int, int]) -> dict:
    if range not in range_to_db_config_mappings:
        raise ValueError(f"DB config not found for the given range: {range}")

    return range_to_db_config_mappings[range]


def __search_range(partition_key: any) -> tuple[int, int]:
    partition_key_hash = get_hash(partition_key)
    node = search(virtual_nodes_index, partition_key_hash)
    if not node:
        raise ValueError("Node not found for the given partition key")

    return node.value


def __get_partition_key(timestamp: datetime) -> str:
    return datetime_to_hh_mm_ss(timestamp)


def __validate_config():
    if not virtual_nodes_index:
        raise ValueError("Virtual nodes index is not configured")

    if not range_to_db_config_mappings:
        raise ValueError("Range to db config mappings are not configured")
