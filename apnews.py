import requests
from bs4 import BeautifulSoup
import re

def get_apnews_articles(team_name):
    formatted_team_name = team_name.lower().replace(" ", "+")
    url = f"https://apnews.com/search?q={formatted_team_name}&s=0"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    results_container = soup.find('div', class_='SearchResultsModule-results')
    
    article_links = []
    
    if results_container:
        titles = results_container.find_all('div', class_='PagePromo-title', limit=10)
        for title in titles:
            link_tag = title.find('a', class_='Link')
            if link_tag and 'href' in link_tag.attrs:
                article_links.append(link_tag['href'])
    
    return article_links

team = "Chicago Bulls"
articles = get_apnews_articles(team)
print(articles)
