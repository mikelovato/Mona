from neo4j import GraphDatabase
import os

class KnowledgeGraph:
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
        propertiesList = []
        for i in properties:
            propertiesList.append(f"{i}: '{self.__replace_space__(properties[i])}'")
        propertiesStr = ", ".join(propertiesList)

        with self.driver.session() as session:
            session.run(f"CREATE ({name}:{label} {{{propertiesStr}}})")
    
    def insert_connection(self, name1, name2, relation="HAVE"):
        with self.driver.session() as session:
            session.run("MATCH (a {name: '"+ name1+"'}), (b {name: '"+name2+"'}) CREATE (a)-[r:"+relation+"]->(b)")

if __name__ == "__main__":
    kg = KnowledgeGraph()
    nodes = kg.query("Graph")
    print(nodes)
    kg.insert({"name": "Graph"})