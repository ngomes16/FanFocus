import requests
from bs4 import BeautifulSoup
import re

def get_apnews_articles(team_name):
    # Format the team name to fit AP News search query
    formatted_team_name = team_name.lower().replace(" ", "+")
    url = f"https://apnews.com/search?q={formatted_team_name}&s=0"
    
    # Send a GET request to the AP News search results page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the main search results container
    results_container = soup.find('div', class_='SearchResultsModule-results')
    
    # Initialize an empty list to store the article links
    article_links = []
    
    # Get the first 10 article links within the results container
    if results_container:
        titles = results_container.find_all('div', class_='PagePromo-title', limit=10)
        for title in titles:
            link_tag = title.find('a', class_='Link')
            if link_tag and 'href' in link_tag.attrs:
                article_links.append(link_tag['href'])
    
    return article_links

# Example usage for Chicago Bulls
team = "Chicago Bulls"
articles = get_apnews_articles(team)
print(articles)
