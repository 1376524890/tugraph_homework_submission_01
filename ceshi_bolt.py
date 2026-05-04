# coding=gbk

from neo4j import GraphDatabase 
URI = "bolt://47.114.101.25:7687"

AUTH = ("admin", "!Z7DhWJC44YzwsST7")
client = GraphDatabase.driver(URI, auth=AUTH)
session = client.session(database="wmn")

#ret = session.run("match (n)-[r]->(m) return n,r,m limit 10")
 

#for item in ret.data():
        
#    print(item)

#session.run("CALL db.dropDB()")

#清空图项目，请不要轻易尝试，它会清空你选中的图项目的模型以及数据
session.run("CALL db.dropDB()")
#创建点模型
session.run("CALL db.createVertexLabel('person', 'id' , 'id' ,'INT32', false, 'name' ,'STRING', false)")
#创建边模型
session.run("CALL db.createEdgeLabel('is_friend','[[\"person\",\"person\"]]')")
#创建索引
session.run("CALL db.addIndex(\"person\", \"name\", false)")
#插入点数据
session.run("create (n1:person {name:'jack',id:1}), (n2:person {name:'lucy',id:2})")
#插入边数据
session.run("match (n1:person {id:1}), (n2:person {id:2}) create (n1)-[r:is_friend]->(n2)")
#查询点和边
res = session.run("match (n)-[r]->(m) return n,r,m")
#Parameterized Query
cypherQuery = "MATCH (n1:person {id:$id})-[r]-(n2:person {name:$name}) RETURN n1, r, n2"
result1 = session.run(cypherQuery, id=1, name="lucy")
for item in result1.data():
        
    print(item)

#删除点数据
session.run("match (n1:person {id:1}) delete n1")
#删除边数据
session.run("match (n1:person {id:1})-[r]-(n2:person{id:2}) delete r")
#删除边模型
session.run("CALL db.deleteLabel('edge', 'is_friend')")
#删除点模型
session.run("CALL db.deleteLabel('vertex', 'person')")

