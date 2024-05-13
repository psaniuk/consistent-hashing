# consistent-hashing

## Description
This project provides a basic implementation of the consistent hashing algorithm. Consistent hashing is a fundamental technique used in distributed systems for assigning keys to nodes in a way that minimizes reassignment when nodes are added or removed from the system.

![consistent hash ring](diagram.png)
 
## Implementation details
- **Database Sharding**: The SQL database is sharded across three MySQL instances. Sharding distributes the data across multiple nodes, allowing for horizontal scalability and improved performance.
- **Hashing Algorithm**: The `md5` hashing algorithm is utilized to generate hash values for keys. `md5` produces a 128-bit hash value, which is suitable for mapping keys to physical database nodes.
- **Integer Mapping**: Each hash generated by `md5` is converted into a 128-bit integer, providing a consistent and uniform representation for mapping to physical DB nodes.
- **Hashing Ring Structure**: The hashing ring is constructed as a binary tree, where each node represents a range of keys. This structure facilitates efficient key lookup and node assignment.
- **Data Partitioning**: Data in the solution is partitioned based on a `timestamp`. 
- **Even Key Distribution**: To achieve even key distribution among available nodes, the algorithm leverages virtual nodes. Virtual nodes enable finer-grained distribution of keys across the hash ring, improving load balancing and system stability.

## How to run
The usage of the algorithm is demonstrated through integration tests. These tests provide examples of how to initialize the consistent hashing algorithm and execute `insert`, `select` queries:

- ```cd consistent_hashing```
- ```python3 -m venv env```
- ```source env/bin/activate```
- ```python3 -m pip install -r requirements.txt```
- ```docker compose up --build```, wait for DB to be created at every node, should be done after log message ` MySQL init process done. Ready for start up.`
- ```pytest integration_tests/*```
