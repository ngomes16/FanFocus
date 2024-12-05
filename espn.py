import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import HTTPError

team_data = {
    "Atlanta Hawks": "atl",
    "Boston Celtics": "bos",
    "Brooklyn Nets": "bkn",
    "Charlotte Hornets": "cha",
    "Chicago Bulls": "chi",
    "Cleveland Cavaliers": "cle",
    "Dallas Mavericks": "dal",
    "Denver Nuggets": "den",
    "Detroit Pistons": "det",
    "Golden State Warriors": "gs",
    "Houston Rockets": "hou",
    "Indiana Pacers": "ind",
    "LA Clippers": "lac",
    "Los Angeles Lakers": "lal",
    "Memphis Grizzlies": "mem",
    "Miami Heat": "mia",
    "Milwaukee Bucks": "mil",
    "Minnesota Timberwolves": "min",
    "New Orleans Pelicans": "no",
    "New York Knicks": "ny",
    "Oklahoma City Thunder": "okc",
    "Orlando Magic": "orl",
    "Philadelphia 76ers": "phi",
    "Phoenix Suns": "phx",
    "Portland Trail Blazers": "por",
    "Sacramento Kings": "sac",
    "San Antonio Spurs": "sa",
    "Toronto Raptors": "tor",
    "Utah Jazz": "utah",
    "Washington Wizards": "wsh",
}

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def get_espn_url(team_name):
    if team_name not in team_data:
        raise ValueError(f"Team '{team_name}' not found in team_data.")
    city_code = team_data[team_name]
    espn_team_name = team_name.lower().replace(" ", "-")
    return f"https://www.espn.com/nba/team/_/name/{city_code}/{espn_team_name}"


def scrape_espn_articles(team_name, max_retries=3):

    url = get_espn_url(team_name)
    
    # Headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            layout_column = soup.find("div", class_="layout__column layout__column--2")
            if not layout_column:
                print("Could not find the target layout column.")
                return []

            articles = layout_column.find_all("article", class_="contentItem")
            article_links = []
            
            for article in articles:
                # Find <a> tags within the article
                link_tag = article.find("a", class_="AnchorLink")
                if link_tag and link_tag.has_attr("href"):
                    # Build full URL
                    full_url = f"https://www.espn.com{link_tag['href']}"
                    article_links.append(full_url)

            return article_links

        except HTTPError as e:
            print(f"HTTP error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Wait before retrying
        time.sleep(2 ** attempt)  # Exponential backoff

    print(f"Failed to fetch articles for {team_name} after {max_retries} attempts.")
    return []

def get_espn_article_details(article_links):
    articles = {}

    for link in article_links:
        try:
            # Request the article page
            response = requests.get(link, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract the title from the header
            header = soup.find("header", class_="article-header")
            title_tag = header.find("h1") if header else None
            title = title_tag.get_text(strip=True) if title_tag else None

            # Extract the content from the article body
            body = soup.find("div", class_="article-body")
            paragraphs = body.find_all("p") if body else []
            content = " ".join(paragraph.get_text(strip=True) for paragraph in paragraphs)

            # Add the title and content to the dictionary if both exist
            if title and content:
                articles[title] = content

        except HTTPError as e:
            print(f"HTTP error while fetching article {link}: {e}")
        except Exception as e:
            print(f"An error occurred while processing article {link}: {e}")

    return articles


# Example usage
team_name = "Chicago Bulls"
article_links = scrape_espn_articles(team_name)  # Use the ESPN scraping function
article_details = get_espn_article_details(article_links)

# Output the results
for title, content in article_details.items():
    print(f"Title: {title}")
    print(f"Content: {content}\n")

