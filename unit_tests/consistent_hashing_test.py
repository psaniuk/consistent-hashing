from app.consistent_hashing import map_virtual_nodes_to_ranges


class TestConsistentHashing:
    def test_map_virtual_nodes_to_ranges(self):
        assert map_virtual_nodes_to_ranges(3, 1) == [(0, 1), (1, 2), (2, 3)]
        assert map_virtual_nodes_to_ranges(3, 10) == [(0, 10), (10, 20), (20, 30)]
        assert map_virtual_nodes_to_ranges(3, 100) == [(0, 100), (100, 200), (200, 300)]
