from app.binary_tree import *


class TestVirtualNodesIndex:
    def test_create(self):
        def traverse(node: TreeNode | None):
            if not node:
                return []
            return traverse(node.left) + [node.value] + traverse(node.right)

        traverse_result = traverse(build([100, 300, 200, 500, 400]))
        assert traverse_result == [100, 200, 300, 400, 500]

    def test_search(self):
        node = build([100, 200, 300, 400, 500])

        assert search(node, 100).value == 100
        assert search(node, 200).value == 200
        assert search(node, 300).value == 300
        assert search(node, 400).value == 400
        assert search(node, 500).value == 500
        assert search(node, 600) is None
        assert search(node, 50).value == 100
        assert search(node, 150).value == 200

        assert search(node, 250).value == 300
        assert search(node, 350).value == 400
        assert search(node, 450).value == 500
        assert search(node, 550) is None
        assert search(node, 25).value == 100
        assert search(node, 175).value == 200
        assert search(node, 275).value == 300
        assert search(node, 375).value == 400
        assert search(node, 475).value == 500

        assert search(node, 0).value == 100
        assert search(node, 1000) is None
        assert search(node, 10000) is None
        assert search(node, -10000).value == 100
        assert search(node, 9999) is None
        assert search(node, -9999).value == 100
        assert search(node, 1).value == 100
        assert search(node, 99).value == 100
        assert search(node, 101).value == 200
        assert search(node, 199).value == 200
        assert search(node, 201).value == 300
        assert search(node, 299).value == 300
        assert search(node, 301).value == 400
        assert search(node, 399).value == 400
        assert search(node, 401).value == 500
        assert search(node, 499).value == 500
        assert search(node, 501) is None
        assert search(node, 599) is None
        assert search(node, 51).value == 100
