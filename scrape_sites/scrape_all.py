import json
from flask import Flask, request, jsonify
from sports_illustrated import get_si_article_links, extract_si_articles
from espn import scrape_espn_articles, get_espn_article_details
from apnews import get_apnews_articles, get_apnews_article_details

app = Flask(__name__)

nbaTeams = [
    "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", 
    "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", 
    "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", 
    "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", 
    "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", 
    "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", 
    "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", 
    "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", 
    "Utah Jazz", "Washington Wizards"
]

nflTeams = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills", 
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns", 
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers", 
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", 
    "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers", 
    "Los Angeles Rams", "Miami Dolphins", "Minnesota Vikings", 
    "New England Patriots", "New Orleans Saints", "New York Giants", 
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", 
    "San Francisco 49ers", "Seattle Seahawks", "Tampa Bay Buccaneers", 
    "Tennessee Titans", "Washington Commanders"
]

import json
import os
import traceback
from flask import Flask, request, jsonify
from sports_illustrated import get_si_article_links, extract_si_articles
from espn import scrape_espn_articles, get_espn_article_details
from apnews import get_apnews_articles, get_apnews_article_details

app = Flask(__name__)


def scrape_articles(team_names):
    articles = []
    for team_name in team_names:
        print(f"Scraping for team: {team_name}")  # Debug print
        try:
            if team_name in nbaTeams or team_name in nflTeams:
                # Scrape articles from each source
                apnews_articles = get_apnews_article_details(get_apnews_articles(team_name))
                si_articles = extract_si_articles(get_si_article_links(team_name))
                espn_articles = get_espn_article_details(scrape_espn_articles(team_name))
                
                print(f"AP News articles: {len(apnews_articles)}")  # Debug print
                print(f"SI articles: {len(si_articles)}")  # Debug print
                print(f"ESPN articles: {len(espn_articles)}")  # Debug print
                
                # Combine all articles as tuples (URL, content)
                articles.extend(apnews_articles)
                articles.extend(si_articles)
                articles.extend(espn_articles)
        except Exception as e:
            print(f"Error scraping articles for {team_name}: {str(e)}")
    
    return articles


@app.route('/scrape_articles', methods=['POST'])
def scrape_articles_route():
    try:
        # Get the team names from the request
        team_names = request.json.get('teamNames', [])
        print(f"Received teams: {team_names}")  # Add print statement
        
        # Validate input
        if not team_names:
            return jsonify({"error": "No teams provided"}), 400
        
        # Scrape articles for the selected teams
        articles = scrape_articles(team_names)
        
        print(f"Total articles scraped: {len(articles)}")  # Add print statement
        
        # Determine the full file path
        file_path = os.path.join(os.getcwd(), 'articles.json')
        print(f"Attempting to write to: {file_path}")  # Debug print
        
        # Save articles to articles.json
        with open(file_path, 'w', encoding='utf-8') as f:
            # Write the articles as a list of tuples (URL, content)
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            "message": "Articles fetched and saved successfully.", 
            "article_count": len(articles),
            "file_path": file_path
        })
    except Exception as e:
        print(f"Error in scrape_articles_route: {str(e)}")  # Add detailed error logging
        import traceback
        traceback.print_exc()  # Print full stack trace
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)