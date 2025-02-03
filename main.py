from src.scraper import get_article_list
from src.analyzer import CallGPT
import src.constants as constants
# from src.analyzer import analyze_keywords
from src.knowledge_graph import KnowledgeGraph
import time
from flask import Flask, request, jsonify

professorMap = {
    "Tb1prqkAAAAJ": "Warut SUKSOMPONG",
    "t-sqBkIAAAAJ": "Yao Lu",
    "lkgd1BsAAAAJ": "Harold SOH",
    "tuLa1AsAAAAJ": "Jin Song Dong",
}
kg = KnowledgeGraph()

def init_knowledge_graph():
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

def get_professor_relation_graph(professor1, professor2):
    search_results = kg.querytwoprof(professor1, professor2)
    common_concept_list = []
    for i in search_results:
        if len(i['node']) == 1 and i['node']['name'] not in common_concept_list and i['node']['name'] != "":
            common_concept_list.append(i['node']['name'])
    return common_concept_list

def get_professor_strength(professor1):
    search_results = kg.queryConcept(professor1)
    concept_list = []
    for i in search_results:
        if i['c']['name'] not in concept_list:
            concept_list.append(i['c']['name'])
    return concept_list[:10]
  
    
def main():
    # wait for the neo4j to start
    time.sleep(8)

    init_knowledge_graph()
    app = Flask(__name__)

    @app.route('/analyze', methods=['POST'])
    def analyze():
        data = request.json
        keyword1 = data.get('keyword1', "")
        keyword2 = data.get('keyword2', "")
        
        if not keyword1 or not keyword2:
            return jsonify({"error": "Both keywords are required"}), 400
        
    
        return jsonify({"r":','.join(get_professor_relation_graph(keyword1, keyword2))})
    
    @app.route('/gpt', methods=['POST'])
    def gpt():
        data = request.json
        prompt = data.get('prompt', "")
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        prof_list = []
        for prof in professorMap:
            if professorMap[prof] in prompt:
                prof_list.append(professorMap[prof])
        
        if len(prof_list) == 2:
            prof1_strength = ','.join(get_professor_strength(prof_list[0]))
            prof2_strength = ','.join(get_professor_strength(prof_list[1]))
            prompt = prompt + "," +prof_list[1] +"'s research stregth is in" + prof2_strength +", "+prof_list[0] +"'s research stregth is in" + prof1_strength + "their common interest is" + ','.join(get_professor_relation_graph(prof_list[0], prof_list[1]))
        elif len(prof_list) == 1:
            prof1_strength = ','.join(get_professor_strength(prof_list[0]))
            prompt = prompt + "," +prof_list[0] +"'s research stregth is in" + prof1_strength
        
        return jsonify({"response": CallGPT(prompt)})
    
    @app.route('/init', methods=['POST'])
    def search():
        init_knowledge_graph()
        return jsonify({"status": "success"})
    app.run(debug=False, host='0.0.0.0', port=8000)



if __name__ == "__main__":
    main()