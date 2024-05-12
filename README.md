# consistent-hashing

key takeaways:
- leveraging consistent hashing decreases the amount of data to shift/move in case a db node removed/added
- adding virtual nodes into hashing ring enhances data distribution
- the efficient way to representing a hashing ring is a binary tree
- when selecting by datetime range, a hash key should be calculated for every time period
