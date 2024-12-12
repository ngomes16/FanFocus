from sports_illustrated import get_si_article_links, extract_si_articles
from espn import scrape_espn_articles, get_espn_article_details
from apnews import get_apnews_articles, get_apnews_article_details

def scrape_all_sites(team_name):
    all_articles = []

    print(f"Scraping Sports Illustrated for {team_name}...")
    si_links = get_si_article_links(team_name)
    all_articles.extend(extract_si_articles(si_links))

    print(f"Scraping ESPN for {team_name}...")
    espn_links = scrape_espn_articles(team_name)
    all_articles.extend(get_espn_article_details(espn_links))

    print(f"Scraping AP News for {team_name}...")
    ap_links = get_apnews_articles(team_name)
    ap_articles = get_apnews_article_details(ap_links)
    all_articles.extend(ap_articles.items())

    return all_articles

def scrape_articles_for_teams(team_names):
    all_team_articles = {}
    for team_name in team_names:
        print(f"\nStarting to scrape for {team_name}...\n")
        articles = scrape_all_sites(team_name)
        all_team_articles[team_name] = articles

    return all_team_articles

