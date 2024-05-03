from dataclasses import dataclass


@dataclass
class TreeNode:
    value: tuple
    left: "TreeNode|None"
    right: "TreeNode|None"


def build_virtual_nodes_index(
    virtual_nodes_number: int, range_size: int
) -> TreeNode | None:

    def build(virtual_nodes: list[int]) -> TreeNode | None:
        if not virtual_nodes:
            return None

        mid = len(virtual_nodes) // 2

        return TreeNode(
            value=virtual_nodes[mid] * range_size,
            left=build(virtual_nodes[:mid]),
            right=build(virtual_nodes[mid + 1 :]),
        )

    virtual_nodes = [i for i in range(1, virtual_nodes_number + 1)]
    return build(virtual_nodes)
