import requests
from bs4 import BeautifulSoup

nba_data = {
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
    "Washington Wizards": "wsh"
}

nfl_data = {
    "Arizona Cardinals": "ari",
    "Atlanta Falcons": "atl",
    "Baltimore Ravens": "bal",
    "Buffalo Bills": "buf",
    "Carolina Panthers": "car",
    "Chicago Bears": "chi",
    "Cincinnati Bengals": "cin",
    "Cleveland Browns": "cle",
    "Dallas Cowboys": "dal",
    "Denver Broncos": "den",
    "Detroit Lions": "det",
    "Green Bay Packers": "gb",
    "Houston Texans": "hou",
    "Indianapolis Colts": "ind",
    "Jacksonville Jaguars": "jax",
    "Kansas City Chiefs": "kc",
    "Las Vegas Raiders": "lv",
    "Los Angeles Chargers": "lac",
    "Los Angeles Rams": "lar",
    "Miami Dolphins": "mia",
    "Minnesota Vikings": "min",
    "New England Patriots": "ne",
    "New Orleans Saints": "no",
    "New York Giants": "nyg",
    "New York Jets": "nyj",
    "Philadelphia Eagles": "phi",
    "Pittsburgh Steelers": "pit",
    "San Francisco 49ers": "sf",
    "Seattle Seahawks": "sea",
    "Tampa Bay Buccaneers": "tb",
    "Tennessee Titans": "ten",
    "Washington Commanders": "wsh"
}

def get_si_article_links(team_name):
    if team_name in nba_data:
        league = "nba"
    elif team_name in nfl_data:
        league = "nfl"
    else:
        raise ValueError(f"Team '{team_name}' not found in NBA or NFL data.")

    formatted_team_name = team_name.lower().replace(" ", "-")
    url = f"https://www.si.com/{league}/team/{formatted_team_name}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")

        article_links = []

        # First container
        scroll_container = soup.find("div", class_="scrollContainer_1qtcybv")
        if scroll_container:
            scroll_items = scroll_container.find_all("div", class_="scrollItem_6fqm4p")
            for item in scroll_items:
                link_tag = item.find("a", href=True)
                if link_tag:
                    article_links.append(link_tag["href"])

        # Second container
        padding_container = soup.find("div", class_="padding_73yipz-o_O-wrapper_1tpwrvm")
        if padding_container:
            articles = padding_container.find_all("article", class_="style_amey2v-o_O-wrapper_1wgo221")
            for article in articles:
                link_tag = article.find("a", href=True)
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

    articles = []

    for link in link_list:
        try:
            response = requests.get(link, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract all <p> text with the specified class
            paragraphs = soup.find_all(
                "p",
                class_="tagStyle_16dbupz-o_O-style_mxvz7o-o_O-style_12bse5w-o_O-style_6s3kpz"
            )
            content = " ".join(p.get_text(strip=True) for p in paragraphs)

            if not content:
                print(f"No content found for {link}")
                continue

            # Append the (url, content) tuple
            articles.append((link, content))

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {link}: {e}")

    return articles
