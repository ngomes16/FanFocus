import requests
from bs4 import BeautifulSoup

def get_si_article_links(team_name):

    formatted_team_name = team_name.lower().replace(" ", "-")
    url = f"https://www.si.com/nba/team/{formatted_team_name}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")


        article_links = []

        #first container
        scroll_container = soup.find("div", class_="scrollContainer_1qtcybv")
        if scroll_container:
            scroll_items = scroll_container.find_all("div", class_="scrollItem_6fqm4p")
            for item in scroll_items:
                link_tag = item.find("a", class_="wrapper_1aaowaj", href=True)
                if link_tag:
                    article_links.append(link_tag["href"])

        # second
        padding_container = soup.find("div", class_="padding_73yipz-o_O-wrapper_1tpwrvm")
        if padding_container:
            articles = padding_container.find_all("article", class_="style_amey2v-o_O-wrapper_1wgo221")
            for article in articles:
                link_tag = article.find("a", class_="wrapper_1v5zw07", href=True)
                if link_tag:
                    article_links.append(link_tag["href"])

        return article_links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the Sports Illustrated page for {team_name}: {e}")
        return []


def extract_si_articles(link_list):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    articles_dict = {}

    for link in link_list:
        try:
            
            response = requests.get(link, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            
            title_tag = soup.find("h1", class_="tagStyle_ppbddh-o_O-title_mscmg3-o_O-sidesPadding_1kaga1a")
            if not title_tag:
                print(f"Could not find title for {link}")
                continue
            title = title_tag.get_text(strip=True)

            # Extract all <p> text with the specified class
            paragraphs = soup.find_all(
                "p",
                class_="tagStyle_16dbupz-o_O-style_mxvz7o-o_O-style_12bse5w-o_O-style_6s3kpz"
            )
            content = " ".join(p.get_text(strip=True) for p in paragraphs)

            if not content:
                print(f"No content found for {link}")
                continue

            
            articles_dict[title] = content

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {link}: {e}")

    return articles_dict

bulls_links = get_si_article_links("Boston Celtics")
articles=(extract_si_articles(bulls_links))

for title, content in articles.items():
    print(f"Title: {title}")
    print(f"Content: {content[:200]}...")  # Print the first 200 characters for brevity
    print()