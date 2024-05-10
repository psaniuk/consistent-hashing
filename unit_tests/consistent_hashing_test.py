import app.consistent_hashing as ch


class TestConsistentHashing:
    def test_map_virtual_nodes_to_ranges(self):
        assert ch.map_virtual_nodes_to_ranges(3, 1) == [(0, 1), (1, 2), (2, 3)]
        assert ch.map_virtual_nodes_to_ranges(3, 10) == [(0, 10), (10, 20), (20, 30)]
        assert ch.map_virtual_nodes_to_ranges(3, 100) == [
            (0, 100),
            (100, 200),
            (200, 300),
        ]

    def test_get_hash(self):
        print(ch.get_hash("127.0.0.1:3306"))
        print(ch.get_hash("127.0.0.1:3307"))
        print(ch.get_hash("127.0.0.1:3308"))
        print(2**128 - 1)
        assert False
