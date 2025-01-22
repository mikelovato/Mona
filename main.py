from src.scraper import get_article_list
from src.analyzer import CallGPT
import src.constants as constants
# from src.analyzer import analyze_keywords
from src.knowledge_graph import KnowledgeGraph
import time

professorMap = {
    "Tb1prqkAAAAJ": "Warut SUKSOMPONG",
    "t-sqBkIAAAAJ": "Yao Lu",
    "lkgd1BsAAAAJ": "Harold SOH"
}
kg = KnowledgeGraph()


def main():
    # wait for the neo4j to start
    time.sleep(8)
    
    print("Sync data from Google Scholar...")
    for professor in professorMap:
        print(f"Sync data for professor: {professor}")
        articles = get_article_list(constants.GoogleScholarURL + professor)
        kg.insert("Prof", 'n', {
            "name" :  professorMap[professor],
            "account": professorMap[professor]+ "@nus.edu.sg"
        })
   
        for article in articles:
            kg.insert("Paper", 'n', {
                'name': article['title'],
                'journal': article['journal'],
                'href': article['href'],
            })
            kg.insert_connection(professorMap[professor], article['title'], "YEAR {year:"+str(article['year'])+"}")
            print(f"Title: {article['title']}")
            keywords = CallGPT(constants.GetKeywordPrompt.format(article=article['title']))
            keywords = keywords.split("\n")
            
            for k in keywords:
                print(k[2:].strip())
                kg.insert("Concept", 'c', {'name': k[2:].strip()})
                kg.insert_connection(article['title'], k[2:].strip())

if __name__ == "__main__":
    main()