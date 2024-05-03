"""
Configure virtual nodes by splitting the hash ring into 1000 virtual nodes.
Split 1000 virtual nodes into 3 physical nodes.
"""

from app.db_utils import create_connection_pool
from app.consistent_hashing import *
from app.virtual_nodes_index import *

connection_pools = {}
virtual_nodes_index = TreeNode | None
range_to_conn_pool_id_mappings = {}


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

    global connection_pools
    connection_pools = {
        index: create_connection_pool(index, config)
        for index, config in enumerate(db_configs)
    }

    conn_pool_ids = list(connection_pools.keys()) * number_of_virtual_nodes
    ranges = map_virtual_nodes_to_ranges(
        number_of_virtual_nodes, get_range_size(number_of_virtual_nodes)
    )
    global range_to_conn_pool_id_mappings
    range_to_conn_pool_id_mappings = {
        key_range: conn_pool_id
        for key_range, conn_pool_id in list(zip(ranges, conn_pool_ids[: len(ranges)]))
    }


def execute(query: str, partition_key: any) -> bool:
    pass
