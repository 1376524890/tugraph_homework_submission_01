from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("admin", "Plk161211.")
client = GraphDatabase.driver(URI, auth=AUTH)
session = client.session(database="plk")

# 删除节点
session.run("match (n1:person {id:1}) delete n1")

# 删除边
session.run("match (n1:person {id:1})-[r]-(n2:person{id:2}) delete r")

# 删除边模型
session.run("CALL db.deleteLabel('edge', 'is_friend')")

# 删除顶点模型
session.run("CALL db.deleteLabel('vertex', 'person')")

session.close()
client.close()
