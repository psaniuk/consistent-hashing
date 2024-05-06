import hashlib

HASH_RING_MAX_VALUE = 2**128 - 1


def get_range_size(number_of_virtual_nodes: int) -> int:
    return HASH_RING_MAX_VALUE // number_of_virtual_nodes


def map_virtual_nodes_to_ranges(
    number_of_virtual_nodes: int, range_size: int
) -> list[tuple[int, int], int]:
    if number_of_virtual_nodes <= 0:
        raise ValueError("Number of virtual nodes should be greater than 0")

    if range_size <= 0:
        raise ValueError("Range size should be greater than 0")

    return [
        (i * range_size, (i + 1) * range_size) for i in range(number_of_virtual_nodes)
    ]


def get_hash(partition_key: any) -> int:
    md5_hex = hashlib.md5(str(partition_key).encode()).hexdigest()
    return int(md5_hex, 16)
