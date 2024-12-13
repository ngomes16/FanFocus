import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def create_user():
    name = input("Enter name: ")
    key_terms = input("Enter key terms (comma-separated): ").split(',')
    favorite_team = input("Enter favorite team: ")
    url = f"{BASE_URL}/user"
    data = {
        "name": name,
        "key_terms": key_terms,
        "favorite_team": favorite_team
    }
    response = requests.post(url, json=data)
    print_response(response)
    return response.json().get("uuid")

def update_key_terms():
    uuid = input("Enter user UUID: ")
    key_terms = input("Enter key terms (comma-separated): ").split(',')
    url = f"{BASE_URL}/user/{uuid}/key-terms"
    data = {
        "key_terms": key_terms
    }
    response = requests.put(url, json=data)
    print_response(response)

def update_favorite_team():
    uuid = input("Enter user UUID: ")
    favorite_team = input("Enter favorite team: ")
    url = f"{BASE_URL}/user/{uuid}/favorite-team"
    data = {
        "favorite_team": favorite_team
    }
    response = requests.put(url, json=data)
    print_response(response)

def retrieve_articles():
    uuid = input("Enter user UUID: ")
    k = int(input("Enter number of articles to retrieve: "))
    url = f"{BASE_URL}/articles/{uuid}"
    params = {
        "k": k
    }
    response = requests.get(url, params=params)
    print_response(response)
    return response.json()

def record_feedback():
    uuid = input("Enter user UUID: ")
    article_id = input("Enter article ID: ")
    vote = input("Enter vote (upvote 1 /downvote 0): ")
    url = f"{BASE_URL}/article/{uuid}/{article_id}/feedback"
    data = {
        "vote": vote
    }
    response = requests.post(url, json=data)
    print_response(response)

def track_seen_article():
    uuid = input("Enter user UUID: ")
    article_id = input("Enter article ID: ")
    url = f"{BASE_URL}/article/{uuid}/{article_id}/seen"
    response = requests.post(url)
    print_response(response)

def reset_seen_articles():
    uuid = input("Enter user UUID: ")
    url = f"{BASE_URL}/user/{uuid}/reset-seen"
    response = requests.post(url)
    print_response(response)

def get_user():
    uuid = input("Enter user UUID: ")
    url = f"{BASE_URL}/user/{uuid}"
    response = requests.get(url)
    print_response(response)

if __name__ == '__main__':
    while True:
        print("\nMenu:")
        print("1. Create User Profile")
        print("2. Update Key Terms")
        print("4. Update Favorite Team")
        print("5. Retrieve Articles")
        print("6. Record Feedback")
        print("7. Track Seen Article")
        print("8. Reset Seen Articles")
        print("9. Get User by UUID")
        print("0. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            create_user()
        elif choice == '2':
            update_key_terms()
        elif choice == '4':
            update_favorite_team()
        elif choice == '5':
            retrieve_articles()
        elif choice == '6':
            record_feedback()
        elif choice == '7':
            track_seen_article()
        elif choice == '8':
            reset_seen_articles()
        elif choice == '9':
            get_user()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")
