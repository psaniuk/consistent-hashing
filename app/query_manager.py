from typing import Sequence
from app.data_access import *
from app.consistent_hashing import *
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
    if not virtual_nodes_index:
        raise ValueError("Virtual nodes index is not configured")

    if not range_to_db_config_mappings:
        raise ValueError("Range to connection pool ID mappings are not configured")

    partition_key_hash = get_hash(partition_key)
    node = search(virtual_nodes_index, partition_key_hash)
    if not node:
        raise ValueError("Node not found for the given partition key")

    if not node.value in range_to_db_config_mappings:
        raise ValueError(
            f"Connection pool ID not found for the given range: {node.value}"
        )

    db_config = range_to_db_config_mappings[node.value]
    return await execute_query(query, parameters, db_config)
