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
        articles.append({
            'title': title,
            'authors': authors,
            'journal': journal,
            'year': year,
            'href': href,
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

if __name__ == "__main__":
    author_url = "https://scholar.google.com/citations?user=q-MnrLcAAAAJ"
    articles = get_article_list(author_url)
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Authors: {article['authors']}")
        print(f"Journal: {article['journal']}")
        print(f"Year: {article['year']}")
        article_url = f"https://scholar.google.com{article['href']}"
        print(f"URL: {article_url}")
        description = get_article_description(article_url)
        print(f"Description: {description}")
        print()