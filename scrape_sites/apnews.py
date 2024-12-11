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

def get_apnews_article_details(article_links):
    articles = {}
    
    for link in article_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the title
        title_tag = soup.find('h1', class_='Page-headline')
        title = title_tag.get_text(strip=True) if title_tag else None
        
        # Extract the article content
        content_div = soup.find('div', class_='RichTextStoryBody RichTextBody')
        paragraphs = content_div.find_all('p') if content_div else []
        content = " ".join(paragraph.get_text(strip=True) for paragraph in paragraphs)
        
        if title and content:
            articles[title] = content

    return articles



team_name = "Chicago Bears"
article_links = get_apnews_articles(team_name)  
article_details = get_apnews_article_details(article_links)


for title, content in article_details.items():
    print(f"Title: {title}")
    print(f"Content: {content}\n")
