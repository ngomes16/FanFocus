import requests
from bs4 import BeautifulSoup

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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    articles = []

    for link in article_links:
        try:
            response = requests.get(link, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            content_div = soup.find('div', class_='RichTextStoryBody RichTextBody')
            paragraphs = content_div.find_all('p') if content_div else []
            content = " ".join(paragraph.get_text(strip=True) for paragraph in paragraphs)

            if content:
                articles.append((link, content))

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error while fetching article {link}: {e}")
        except Exception as e:
            print(f"An error occurred while processing article {link}: {e}")

    return articles

