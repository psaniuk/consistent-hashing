# consistent-hashing

## Description
The project is a basic implementation of horizontal data partitioning with consistent hashing. In the solution, SQL database is sharded across three MySQL nodes.

## Consistent hashing implementation

## key takeaways:
- leveraging consistent hashing decreases the amount of data to shift/move in case a db node removed/added
- adding virtual nodes into hashing ring enhances data distribution
- the efficient way to representing a hashing ring is a binary tree
- when selecting by datetime range, a hash key should be calculated for every time period
