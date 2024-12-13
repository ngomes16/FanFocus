from flask import Flask, request, jsonify
import json
import pickle
import os
from uuid import uuid4
from update_content import update_content, process_text
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

USER_DATA_PATH = 'data/users.json'
ARTICLES_PATH = 'data/articles.json'
INVERTED_INDEX_PATH = 'data/inverted_index.json'
TFIDF_DATA_PATH = 'data/tfidf_data.pkl'

def check_data_jsons():
    os.makedirs('data', exist_ok=True)
    if not os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, 'w') as f:
            json.dump({}, f)
    if not os.path.exists(ARTICLES_PATH):
        with open(ARTICLES_PATH, 'w') as f:
            json.dump({}, f)
    if not os.path.exists(INVERTED_INDEX_PATH):
        with open(INVERTED_INDEX_PATH, 'w') as f:
            json.dump({}, f)

def load_user_data():
    if os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_user_data(users):
    with open(USER_DATA_PATH, 'w') as f:
        json.dump(users, f, indent=4)

def adjust_tfidf_based_on_feedback(article_id, feedback):
    with open(TFIDF_DATA_PATH, 'rb') as f:
        tfidf_data = pickle.load(f)
        vectorizer = tfidf_data['vectorizer']
        tfidf_vectors = tfidf_data['tfidf_vectors']

    if feedback == '1':
        multiplier = 1.05
    else:
        multiplier = 0.95
    
    target_vector = tfidf_vectors[article_id]

    similarities = {other_article_id: cosine_similarity(target_vector,other_vector).flatten()[0] for other_article_id,other_vector in tfidf_vectors.items() if other_article_id != article_id}

    for other_article,similarity in similarities.items():
        print(f"ARTICLE ID: {other_article}    SIMILIARITY: {similarity}")
        if similarity >= 0.15:
            tfidf_vectors[other_article] = tfidf_vectors[other_article].multiply(multiplier)
    print("DEOS IT GET HERE 2")
    tfidf_vectors[article_id] = tfidf_vectors[article_id].multiply(multiplier)

    print("DOES IT GET HERE 3")
    with open(TFIDF_DATA_PATH, 'wb') as f:
        pickle.dump({'vectorizer': vectorizer, 'tfidf_vectors': tfidf_vectors}, f)

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user_uuid = str(uuid4())
    users = load_user_data()
    users[user_uuid] = {
        'name': data.get('name'),
        'key_terms': data.get('key_terms', []),
        'favorite_team': data.get('favorite_team', ''),
        'seen_articles': [],
        'upvote_downvote_history': {}
    }
    save_user_data(users)
    return jsonify({'message': 'User profile created successfully', 'uuid': user_uuid}), 201

@app.route('/user/<uuid>/key-terms', methods=['PUT'])
def update_key_terms(uuid):
    data = request.json
    users = load_user_data()
    if uuid in users:
        users[uuid]['key_terms'] = data.get('key_terms', [])
        save_user_data(users)
        return jsonify({'message': 'Key terms updated successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<uuid>/favorite-team', methods=['PUT'])
def update_favorite_team(uuid):
    data = request.json
    users = load_user_data()
    if uuid in users:
        users[uuid]['favorite_team'] = data.get('favorite_team', '')
        save_user_data(users)
        return jsonify({'message': 'Favorite team updated successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/articles/<uuid>', methods=['GET'])
def retrieve_articles(uuid):
    k = request.args.get('k', default=5, type=int) #num articles to get back, we can set this to be whateer in data
    print("DOES IT GET HERE?")
    users = load_user_data()
    if uuid not in users:
        return jsonify({'message': 'User not found'}), 404
    
    user = users[uuid]
    key_terms = user['key_terms'] + [user['favorite_team']]
    
    if os.path.exists(TFIDF_DATA_PATH):
        with open(TFIDF_DATA_PATH, 'rb') as f:
            tfidf_data = pickle.load(f)
            vectorizer = tfidf_data['vectorizer']
            tfidf_vectors = tfidf_data['tfidf_vectors']
    
    query_vec = vectorizer.transform([' '.join(key_terms)])
    similarities = {article_id: cosine_similarity(query_vec, tfidf_vector).flatten()[0]
                    for article_id, tfidf_vector in tfidf_vectors.items() 
                    if article_id not in user['seen_articles']}
    print(similarities)
    if not similarities:
        return jsonify({'message': 'No more relevant articles available'}), 200
    
    sorted_articles = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
    top_articles = [article_id for article_id, _ in sorted_articles[:k]]
    
    with open(ARTICLES_PATH, 'r') as f:
        articles = json.load(f)
    
    result = []
    for article_id in top_articles:
        article = articles[article_id]
        result.append({
            'id': article_id,
            'url': article['url'],
            'title': article.get('title', 'No Title'),
            'excerpt': article.get('text', '')[:200]
        })
    
    return jsonify(result), 200

@app.route('/article/<uuid>/<article_id>/feedback', methods=['POST'])
def record_feedback(uuid, article_id):
    data = request.json
    users = load_user_data()
    feedback = data.get('vote')
    if uuid in users:
        users[uuid]['upvote_downvote_history'][article_id] = feedback
        print("IT GETS HERE 1")
        adjust_tfidf_based_on_feedback(article_id,feedback)
        save_user_data(users)
        return jsonify({'message': 'Feedback recorded successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/article/<uuid>/<article_id>/seen', methods=['POST'])
def track_seen_article(uuid, article_id):
    users = load_user_data()
    if uuid in users:
        if article_id not in users[uuid]['seen_articles']:
            users[uuid]['seen_articles'].append(article_id)
            save_user_data(users)
        return jsonify({'message': 'Article marked as seen'}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<uuid>/reset-seen', methods=['POST'])
def reset_seen_articles(uuid):
    users = load_user_data()
    if uuid in users:
        users[uuid]['seen_articles'] = []
        save_user_data(users)
        return jsonify({'message': 'Seen articles reset successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<uuid>', methods=['GET'])
def get_user(uuid):
    users = load_user_data()
    if uuid in users:
        user = users[uuid]
        return jsonify({
            'uuid': uuid,
            'name': user['name'],
            'key_terms': user['key_terms'],
            'favorite_team': user['favorite_team']
        }), 200
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    check_data_jsons()
    app.run(debug=True)
