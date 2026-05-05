from neo4j import GraphDatabase 
URI = "bolt://localhost:7687"

AUTH = ("admin", "Plk161211.")
client = GraphDatabase.driver(URI, auth=AUTH)
session = client.session(database="plk")

#ret = session.run("match (n)-[r]->(m) return n,r,m limit 10")
 

#for item in ret.data():
        
#    print(item)

#session.run("CALL db.dropDB()")

#���ͼ��Ŀ���벻Ҫ���׳��ԣ����������ѡ�е�ͼ��Ŀ��ģ���Լ�����
session.run("CALL db.dropDB()")
#������ģ��
session.run("CALL db.createVertexLabel('person', 'id' , 'id' ,'INT32', false, 'name' ,'STRING', false)")
#������ģ��
session.run("CALL db.createEdgeLabel('is_friend','[[\"person\",\"person\"]]')")
#��������
session.run("CALL db.addIndex(\"person\", \"name\", false)")
#���������
session.run("create (n1:person {name:'jack',id:1}), (n2:person {name:'lucy',id:2})")
#���������
session.run("match (n1:person {id:1}), (n2:person {id:2}) create (n1)-[r:is_friend]->(n2)")
#��ѯ��ͱ�
res = session.run("match (n)-[r]->(m) return n,r,m")
#Parameterized Query
cypherQuery = "MATCH (n1:person {id:$id})-[r]-(n2:person {name:$name}) RETURN n1, r, n2"
result1 = session.run(cypherQuery, id=1, name="lucy")
for item in result1.data():
        
    print(item)

#ɾ��������
session.run("match (n1:person {id:1}) delete n1")
#ɾ��������
session.run("match (n1:person {id:1})-[r]-(n2:person{id:2}) delete r")
#ɾ����ģ��
session.run("CALL db.deleteLabel('edge', 'is_friend')")
#ɾ����ģ��
session.run("CALL db.deleteLabel('vertex', 'person')")

