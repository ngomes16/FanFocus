# NBA Teams and ESPN City Codes
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
    "Washington Wizards": "wsh"
}

# Generate URLs for each team
team_urls = {}

for team, code in team_data.items():
    # Format for AP News
    ap_team_name = team.lower().replace(" ", "+")
    ap_url = f"https://apnews.com/search?q={ap_team_name}&s=0"

    # Format for Yahoo Sports
    city = team.split()[0].lower()  # Get the city name
    if team == "Los Angeles Lakers":
        yahoo_url = "https://sports.yahoo.com/nba/teams/la-lakers/"
    elif team == "LA Clippers":
        yahoo_url = "https://sports.yahoo.com/nba/teams/la-clippers/"
    else:
        city_formatted = city.replace(" ", "-")  # Handle multi-word cities
        yahoo_url = f"https://sports.yahoo.com/nba/teams/{city_formatted}/"

    # Format for NBC Sports
    nbc_team_name = team.lower().replace(" ", "-")
    nbc_url = f"https://www.nbcsports.com/nba/{nbc_team_name}"

    # Format for ESPN
    espn_team_name = team.lower().replace(" ", "-")
    espn_url = f"https://www.espn.com/nba/team/_/name/{code}/{espn_team_name}"

    # Store URLs in the dictionary
    team_urls[team] = {
        "AP News": ap_url,
        "Yahoo Sports": yahoo_url,
        "NBC Sports": nbc_url,
        "ESPN": espn_url
    }

# # Example: Print URLs for the Chicago Bulls
# print("Chicago Bulls URLs:")
# for source, url in team_urls["Chicago Bulls"].items():
#     print(f"{source}: {url}")
