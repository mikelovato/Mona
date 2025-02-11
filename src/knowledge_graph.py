from neo4j import GraphDatabase
import os

class KnowledgeGraph:
    insertkey = []
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://neo4j:7687",
            auth=("neo4j", "password")
        )
    
    def querytwoprof(self, keyword1, keyword2):
        with self.driver.session() as session:
            result = session.run("MATCH path = (a:Prof {name: '"+keyword1.replace("'", "\"")+"'})-[*]->()<-[*]-(b:Prof {name:'"+keyword2.replace("'", "\"")+"'}) UNWIND nodes(path) AS node WITH DISTINCT node RETURN node")
            return result.data()
    
    def queryConcept(self, keyword):
        with self.driver.session() as session:
            result = session.run("MATCH path = (a:Prof {name: '"+keyword.replace("'", "\"")+"'})-[*]->(c:Concept) WITH DISTINCT c return c")
            return result.data()
        
    def __replace_space__(self, s):
        return s.replace("'", "\"")

    
    def insert(self, label, name, properties):
        # label = "Professor"
        # name = "Yao Lu"
        # properties = {"name":"Yao Lu", "birthday": "1983"}
        name = self.__replace_space__(name)
        if 'name' not in properties or self.check_node_exists(self.__replace_space__(properties['name'])):
            return
        propertiesList = []
        for i in properties:
            propertiesList.append(f"{i}: '{self.__replace_space__(properties[i])}'")
        propertiesStr = ", ".join(propertiesList)

        with self.driver.session() as session:
            try:
                session.run(f"CREATE ({name}:{label} {{{propertiesStr}}})")
            except Exception as e:
                print(e)
                pass

    def check_node_exists(self, name):
        with self.driver.session() as session:
            try:
                query = "OPTIONAL MATCH (n {name: '"+name+"'}) RETURN n"
                result = session.run(query).data()
                if len(result)>1 or 'None' not in str(result):
                    return 1
                return 0
            except Exception as e:
                print(e)
                return 0
            
    def clear_knowledge_graph(self):
        with self.driver.session() as session:
            try:
                query = "MATCH (n) DETACH DELETE (n)"
                session.run(query)
            except Exception as e:
                print(e)
    
    def insert_connection(self, name1, name2, relation="HAVE"):
        with self.driver.session() as session:
            try:
                session.run("MATCH (a {name: '"+ name1+"'}), (b {name: '"+name2+"'}) CREATE (a)-[r:"+relation+"]->(b)")
            except Exception as e:
                print(e)
                pass

if __name__ == "__main__":
    kg = KnowledgeGraph()
    nodes = kg.query("Graph")
    print(nodes)
    kg.insert({"name": "Graph"})