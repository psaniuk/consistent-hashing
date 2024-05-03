from app.virtual_nodes_index import *


class TestVirtualNodesIndex:
    def test_create(self):
        def traverse(node: TreeNode | None):
            if not node:
                return []
            return traverse(node.left) + [node.value] + traverse(node.right)

        traverse_result = traverse(build_virtual_nodes_index(5, 100))
        assert traverse_result == [100, 200, 300, 400, 500]
