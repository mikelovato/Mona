import requests
from bs4 import BeautifulSoup

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# get article list for one user
def get_article_list(author_url):
    
    response = requests.get(author_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for row in soup.find_all('tr', class_='gsc_a_tr'):
        
        href = row.find('a', class_='gsc_a_at')['href']
        title = row.find('a', class_='gsc_a_at').text
        authors = row.find('div', class_='gs_gray').text
        journal = row.find_all('div', class_='gs_gray')[1].text
        year = row.find('span', class_='gsc_a_h gsc_a_hc gs_ibl').text
        cite = row.find('a', class_='gsc_a_ac gs_ibl').text
        articles.append({
            'title': title,
            'authors': authors,
            'journal': journal,
            'year': year,
            'href': href,
            'cite': cite,
        })

    return articles

# get article description for one article
def get_article_description(article_url):
    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    description_div = soup.find('div', class_='gsh_csp')
    if description_div:
        return description_div.text.strip()
    return "No description available"

def get_wikidata_keyword_id(keyword):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "search": keyword,  
        "language": "en",
        "format": "json",
        "limit": 1,
    }
    response = requests.get(url, params=params).json()
    
    if "search" in response:
        return response["search"][0]['id']
    else:
        return {}
    

def get_entity_properties(entity_id):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "ids": entity_id,
        "format": "json",
        "languages": "en"
    }
    response = requests.get(url, params=params).json()
    try:
        return response["entities"].get(entity_id, {}).get("claims", {})
    except Exception as e:
        print(e)
        return {}
    
def find_relationships(keyword1, keyword2):
    entity1 = get_wikidata_keyword_id(keyword1)
    entity2 = get_wikidata_keyword_id(keyword2)

    if not entity1 or not entity2:
        print("One or both entities not found.")
        return

    properties1 = get_entity_properties(entity1)
    print(properties1)
    properties2 = get_entity_properties(entity2)
    # print(properties2)

    for prop, values in properties1.items():
        for v in values:
            if "mainsnak" in v and "datavalue" in v["mainsnak"]:
                try: 
                    if v["mainsnak"]["datavalue"].get("value", {}).get("id") == entity2:
                        print(f"{keyword1} ({entity1}) → {prop} → {keyword2} ({entity2})")
                except Exception as e:
                    continue





if __name__ == "__main__":
    find_relationships("compute", "math")

    # author_url = "https://scholar.google.com/citations?user=q-MnrLcAAAAJ"
    # articles = get_article_list(author_url)
    # for article in articles:
    #     print(f"Title: {article['title']}")
    #     print(f"Authors: {article['authors']}")
    #     print(f"Journal: {article['journal']}")
    #     print(f"Year: {article['year']}")
    #     print(f"Cite: {article['cite']}")
    #     article_url = f"https://scholar.google.com{article['href']}"
    #     print(f"URL: {article_url}")
    #     description = get_article_description(article_url)
    #     print(f"Description: {description}")
    #     print()