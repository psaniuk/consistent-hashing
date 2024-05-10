from dataclasses import dataclass


@dataclass
class TreeNode:
    value: int
    left: "TreeNode|None"
    right: "TreeNode|None"


def build(ranges: list[int]) -> TreeNode | None:
    ranges.sort()

    def build(virtual_nodes: list[int]) -> TreeNode | None:
        if not virtual_nodes:
            return None

        mid = len(virtual_nodes) // 2

        return TreeNode(
            value=virtual_nodes[mid],
            left=build(virtual_nodes[:mid]),
            right=build(virtual_nodes[mid + 1 :]),
        )

    return build(ranges)


def search(root: TreeNode | None, key: int) -> TreeNode | None:
    result = None

    def traverse(node):
        if not node:
            return None

        if key <= node.value:
            nonlocal result
            result = node

        return traverse(node.left) if key <= node.value else traverse(node.right)

    traverse(root)
    return result
