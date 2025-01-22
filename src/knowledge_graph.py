from neo4j import GraphDatabase
import os

class KnowledgeGraph:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://neo4j:7687",
            auth=("neo4j", "password")
        )
    
    def query(self, keyword):
        with self.driver.session() as session:
            result = session.run("MATCH (n) WHERE n.name=$keyword RETURN n", keyword=keyword)
            return [record["n"] for record in result]
    
    def __replace_space__(self, s):
        return s.replace(" ", "-")

    
    def insert(self, label, name, properties):
        # label = "Professor"
        # name = "Yao Lu"
        # properties = {"name":"Yao Lu", "birthday": "1983"}
        name = self.__replace_space__(name)
        propertiesList = []
        for i in properties:
            propertiesList.append(f"{i}: '{properties[i]}'")
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