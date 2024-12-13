import json
import os
import traceback
import shutil
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

# def transform_brackets(json_data):
#     # Convert JSON data to string for manipulation
#     json_str = json.dumps(json_data)
    
#     # Find positions of the first and last square brackets
#     first_square_bracket = json_str.find('[')
#     last_square_bracket = json_str.rfind(']')
    
#     # Create a new list to hold the transformed string
#     transformed_data = []
#     start = 0
    
#     # Loop through the string to replace brackets
#     while start < len(json_str):
#         if start == first_square_bracket:
#             # Convert the first square bracket to '('
#             transformed_data.append('(')
#             start += 1
#             first_square_bracket = -1  # Mark the first bracket as handled
#         elif start == last_square_bracket:
#             # Convert the last square bracket to ')'
#             transformed_data.append(')')
#             break  # End the loop as we've handled the last bracket
#         elif json_str[start] == '[':
#             # Convert intermediate square brackets to '('
#             transformed_data.append('(')
#             start += 1
#         elif json_str[start] == ']':
#             # Convert intermediate square brackets to ')'
#             transformed_data.append(')')
#             start += 1
#         else:
#             # Append each character to the transformed list
#             transformed_data.append(json_str[start])
#             start += 1

#     # Join the transformed string into a final string
#     transformed_str = ''.join(transformed_data)

#     # Replace every instance of "), (" with "),\n("
#     transformed_str = transformed_str.replace('), (', '),\n(')

#     # Remove the first and last characters
#     transformed_str = transformed_str[1:-1]

#     # Add '[' to the beginning and ']' to the end
#     transformed_str = f'[\n{transformed_str}\n]'

#     return transformed_str



# def scrape_articles(team_names):
#     articles = []
#     for team_name in team_names:
#         print(f"Scraping for team: {team_name}")  
#         try:
#             if team_name in nbaTeams or team_name in nflTeams:
#                 # Scrape articles from each source
#                 apnews_articles = get_apnews_article_details(get_apnews_articles(team_name))
#                 si_articles = extract_si_articles(get_si_article_links(team_name))
#                 espn_articles = get_espn_article_details(scrape_espn_articles(team_name))
                
#                 print(f"AP News articles: {len(apnews_articles)}")  
#                 print(f"SI articles: {len(si_articles)}")  
#                 print(f"ESPN articles: {len(espn_articles)}")  
                
#                 # Combine all articles as tuples (URL, content)
#                 articles.extend(apnews_articles)
#                 articles.extend(si_articles)
#                 articles.extend(espn_articles)
#         except Exception as e:
#             print(f"Error scraping articles for {team_name}: {str(e)}")
    
#     return articles


# @app.route('/scrape_articles', methods=['POST'])
# def scrape_articles_route():
#     try:
#         # Get the team names from the request
#         team_names = request.json.get('teamNames', [])
#         print(f"Received teams: {team_names}")  
        
#         # Validate input
#         if not team_names:
#             return jsonify({"error": "No teams provided"}), 400
        
#         # Scrape articles for the selected teams
#         articles = scrape_articles(team_names)
#         formatted_articles = [list(article) for article in articles]
        
#         print(f"Total articles scraped: {len(articles)}")  
        
#         # Transform the brackets in the formatted articles
#         transformed_articles_str = transform_brackets(formatted_articles)
        
#         # Determine the full file path
#         file_path = os.path.join(os.getcwd(), 'articles.json')
#         print(f"Attempting to write to: {file_path}")  
        
#         # Save the transformed articles to articles.json
#         with open(file_path, 'w', encoding='utf-8') as f:
#             f.write(formatted_articles)
        
#         return jsonify({
#             "message": "Articles fetched and saved successfully.", 
#             "article_count": len(articles),
#             "file_path": file_path
#         })
#     except Exception as e:
#         print(f"Error in scrape_articles_route: {str(e)}")  # Add detailed error logging
#         traceback.print_exc()  # Print full stack trace
#         return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)

def scrape_articles(team_names):
    articles = []
    for team_name in team_names:
        print(f"Scraping for team: {team_name}")
        try:
            if team_name in nbaTeams or team_name in nflTeams:
                # Scrape articles from each source
                apnews_articles = get_apnews_article_details(get_apnews_articles(team_name))
                si_articles = extract_si_articles(get_si_article_links(team_name))
                espn_articles = get_espn_article_details(scrape_espn_articles(team_name))
                
                print(f"AP News articles: {len(apnews_articles)}")
                print(f"SI articles: {len(si_articles)}")
                print(f"ESPN articles: {len(espn_articles)}")
                
                # Combine all articles as tuples (URL, content)
                articles.extend(apnews_articles)
                articles.extend(si_articles)
                articles.extend(espn_articles)
        except Exception as e:
            print(f"Error scraping articles for {team_name}: {str(e)}")
    return articles

def copy_articles_to_public():
    try:
        # Define the source and destination paths
        source = os.path.join(os.getcwd(), 'articles.json')  # Root directory
        destination = os.path.join(os.getcwd(), 'fanfocus', 'public', 'articles.json')  # Public folder

        # Ensure the destination folder exists
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        # Copy the file
        shutil.copy(source, destination)
        print(f"Copied {source} to {destination}")
    except Exception as e:
        print(f"Error copying articles.json: {str(e)}")


@app.route('/scrape_articles', methods=['POST'])
def scrape_articles_route():
    try:
        # Get the team names from the request
        team_names = request.json.get('teamNames', [])
        print(f"Received teams: {team_names}")
        
        # Validate input
        if not team_names:
            return jsonify({"error": "No teams provided"}), 400
        
        # Scrape articles for the selected teams
        articles = scrape_articles(team_names)
        
        # Transform articles into a JSON serializable format (e.g., list of lists)
        formatted_articles = [list(article) for article in articles]
        
        print(f"Total articles scraped: {len(articles)}")
        
        # Determine the full file path
        file_path = os.path.join(os.getcwd(), 'articles.json')
        print(f"Attempting to write to: {file_path}")
        
        # Save the articles to articles.json
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(formatted_articles, f, ensure_ascii=False, indent=4)
        
        copy_articles_to_public()
        
        return jsonify({
            "message": "Articles fetched and saved successfully.",
            "article_count": len(articles),
            "file_path": file_path
        })
    except Exception as e:
        print(f"Error in scrape_articles_route: {str(e)}")  # Add detailed error logging
        traceback.print_exc()  # Print full stack trace
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    copy_articles_to_public()
    app.run(debug=True)