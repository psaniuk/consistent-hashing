from datetime import datetime, timedelta
from typing import Sequence
from app.data_access import *
import app.consistent_hashing as consistent_hashing
from app.timestamp import datetime_to_hh_mm_ss
import app.binary_tree as binary_tree
import uuid

virtual_nodes_index, physical_nodes_index = None, None
hash_key_to_db_config_mappings = {}


def configure(db_configs: list[dict], number_of_virtual_nodes: int = 1000):
    if not db_configs:
        raise ValueError("DB configs should not be empty")

    if number_of_virtual_nodes <= 0:
        raise ValueError("Number of virtual nodes should be greater than 0")

    range_size = consistent_hashing.get_range_size(number_of_virtual_nodes)
    ranges = consistent_hashing.get_virtual_ranges(number_of_virtual_nodes, range_size)

    global virtual_nodes_index
    virtual_nodes_index = binary_tree.build(ranges)

    mappings = list(
        map(
            lambda config: (
                consistent_hashing.get_hash_key(uuid.uuid4()),
                config,
            ),
            db_configs,
        )
    )

    global physical_nodes_index
    physical_nodes_index = binary_tree.build([mapping[0] for mapping in mappings])

    global hash_key_to_db_config_mappings
    hash_key_to_db_config_mappings = {mapping[0]: mapping[1] for mapping in mappings}


async def run_query(query: str, parameters: Sequence[any], partition_key: any) -> any:
    __validate_config()
    virtual_node = __search_virtual_node(partition_key)
    db_config = __map_to_db_config(virtual_node)
    return await execute_query(query, parameters, db_config)


async def insert(metric_name: str, value: float, timestamp: datetime) -> any:
    __validate_config()
    node_hash_key = __search_virtual_node(__get_partition_key(timestamp))
    db_config = __map_to_db_config(node_hash_key)
    query = "INSERT INTO metrics (name, value, timestamp) VALUES(%s, %s, %s);"
    return await execute_query(query, (metric_name, value, timestamp), db_config)


async def select(datetime_range: tuple[datetime, datetime]) -> any:
    __validate_config()

    start_at, end_at = datetime_range
    distinct_ranges = set()
    while start_at < end_at:
        range = __search_virtual_node(__get_partition_key(start_at))
        distinct_ranges.add(range)
        start_at += timedelta(seconds=1)

    host_to_config_mappings = {}
    for range in distinct_ranges:
        db_config = __map_to_db_config(range)
        config_key = __get_db_config_key(db_config)
        if config_key not in host_to_config_mappings:
            host_to_config_mappings[config_key] = db_config

    query = "SELECT * FROM metrics WHERE timestamp >= %s AND timestamp <= %s;"
    result = []
    for config in list(host_to_config_mappings.values()):
        result.extend(await execute_query(query, datetime_range, config))
    return result


async def delete_all():
    __validate_config()
    for config in hash_key_to_db_config_mappings.values():
        query = "DELETE FROM metrics;"
        await execute_query(query, (), config)


def __map_to_db_config(virtual_node_hash_key: int) -> dict:
    physical_node = binary_tree.search(physical_nodes_index, virtual_node_hash_key)
    if not physical_node:
        # if the physical node is not found in the binary tree (the value > the max range)
        # then map the given value to the closest clockwise node
        physical_node = binary_tree.search(physical_nodes_index, 0)

    return hash_key_to_db_config_mappings[physical_node.value]


def __search_virtual_node(partition_key: any) -> int:
    virtual_node_hash_key = consistent_hashing.get_hash_key(partition_key)
    node = binary_tree.search(virtual_nodes_index, virtual_node_hash_key)
    if not node:
        raise ValueError("Virtual node not found for the given partition key")

    return node.value


def __get_partition_key(timestamp: datetime) -> str:
    return datetime_to_hh_mm_ss(timestamp)


def __validate_config():
    if not virtual_nodes_index:
        raise ValueError("Virtual nodes index is not configured")

    if not physical_nodes_index:
        raise ValueError("Physical nodes index is not configured")

    if not hash_key_to_db_config_mappings:
        raise ValueError("Range to db config mappings are not configured")


def __get_db_config_key(config: dict) -> str:
    return config["host"] + str(config["port"])
