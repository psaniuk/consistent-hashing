import app.consistent_hashing as ch
import uuid


class TestConsistentHashing:
    def test_map_virtual_nodes_to_ranges(self):
        assert ch.get_virtual_ranges(3, 1) == [1, 2, 3]
        assert ch.get_virtual_ranges(3, 10) == [10, 20, 30]
        assert ch.get_virtual_ranges(3, 100) == [100, 200, 300]
