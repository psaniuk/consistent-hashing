from dataclasses import dataclass


@dataclass
class TreeNode:
    value: tuple[int, int]
    left: "TreeNode|None"
    right: "TreeNode|None"


def build_virtual_nodes_index(
    virtual_nodes_number: int, range_size: int
) -> TreeNode | None:

    def build(virtual_nodes: list[int]) -> TreeNode | None:
        if not virtual_nodes:
            return None

        mid = len(virtual_nodes) // 2
        lower_bound = virtual_nodes[mid] * range_size
        upper_bound = lower_bound + range_size

        return TreeNode(
            value=(lower_bound, upper_bound),
            left=build(virtual_nodes[:mid]),
            right=build(virtual_nodes[mid + 1 :]),
        )

    virtual_nodes = [i for i in range(virtual_nodes_number)]
    return build(virtual_nodes)


def search(root: TreeNode | None, key: int) -> TreeNode | None:
    def traverse(node):
        if not node:
            return None

        lower_bound, upper_bound = node.value
        if lower_bound <= key < upper_bound:
            return node

        return traverse(node.left) if key < lower_bound else traverse(node.right)

    return traverse(root)
