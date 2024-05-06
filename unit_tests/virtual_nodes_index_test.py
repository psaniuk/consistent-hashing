from app.virtual_nodes_index import *


class TestVirtualNodesIndex:
    def test_create(self):
        def traverse(node: TreeNode | None):
            if not node:
                return []
            return traverse(node.left) + [node.value] + traverse(node.right)

        traverse_result = traverse(build_virtual_nodes_index(5, 100))
        assert traverse_result == [
            (0, 100),
            (100, 200),
            (200, 300),
            (300, 400),
            (400, 500),
        ]

    def test_search(self):
        node = build_virtual_nodes_index(5, 100)
        assert search(node, 100).value == (100, 200)
        assert search(node, 200).value == (200, 300)
        assert search(node, 300).value == (300, 400)
        assert search(node, 400).value == (400, 500)
        assert search(node, 500) == None
        assert search(node, 600) == None
        assert search(node, 50).value == (0, 100)
        assert search(node, 150).value == (100, 200)
        assert search(node, 250).value == (200, 300)
        assert search(node, 350).value == (300, 400)
        assert search(node, 450).value == (400, 500)
        assert search(node, 550) == None
        assert search(node, 25).value == (0, 100)
        assert search(node, 175).value == (100, 200)
        assert search(node, 275).value == (200, 300)
        assert search(node, 375).value == (300, 400)
        assert search(node, 475).value == (400, 500)

        assert search(node, 0).value == (0, 100)
        assert search(node, 1000) == None
        assert search(node, 10000) == None
        assert search(node, -10000) == None
        assert search(node, 9999) == None
        assert search(node, -9999) == None
        assert search(node, 1).value == (0, 100)
        assert search(node, 99).value == (0, 100)
        assert search(node, 101).value == (100, 200)
        assert search(node, 199).value == (100, 200)
        assert search(node, 201).value == (200, 300)
        assert search(node, 299).value == (200, 300)
        assert search(node, 301).value == (300, 400)
        assert search(node, 399).value == (300, 400)
        assert search(node, 401).value == (400, 500)
        assert search(node, 499).value == (400, 500)
        assert search(node, 501) == None
        assert search(node, 599) == None
        assert search(node, 51).value == (0, 100)
