import json
import pickle
import os
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk

nltk_data_path = os.path.join(os.path.dirname(__file__), 'data', 'nltk_data')
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

nltk.download('stopwords', download_dir=nltk_data_path)
nltk.download('punkt', download_dir=nltk_data_path)

def process_text(text):
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    return [ps.stem(word) for word in tokens if word.isalnum() and word.lower() not in stop_words]

def update_inverted_index(inverted_index, articles):
    for article_id, article_content in articles.items():
        tokens = process_text(article_content['text'])
        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = set()
            inverted_index[token].add(article_id)
    return inverted_index

def update_document_tfidf(document_text, vectorizer=None):
    if vectorizer is None:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_vector = vectorizer.fit_transform([document_text])
    else:
        tfidf_vector = vectorizer.transform([document_text])
    
    return vectorizer, tfidf_vector

def update_content(new_articles, inverted_index_path='data/inverted_index.json', articles_path='data/articles.json', tfidf_data_path='data/tfidf_data.pkl'):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(inverted_index_path), exist_ok=True)
    os.makedirs(os.path.dirname(articles_path), exist_ok=True)
    os.makedirs(os.path.dirname(tfidf_data_path), exist_ok=True)

    if os.path.exists(inverted_index_path):
        with open(inverted_index_path, 'r') as f:
            inverted_index = json.load(f)
            inverted_index = {k: set(v) for k, v in inverted_index.items()}
    else:
        inverted_index = defaultdict(set)
    
    if os.path.exists(articles_path):
        with open(articles_path, 'r') as f:
            articles = json.load(f)
    else:
        articles = {}

    latest_id = max([int(id) for id in articles.keys()], default=-1)
    
    if os.path.exists(tfidf_data_path):
        with open(tfidf_data_path, 'rb') as f:
            tfidf_data = pickle.load(f)
            vectorizer = tfidf_data['vectorizer']
            tfidf_vectors = tfidf_data['tfidf_vectors']
    else:
        vectorizer = None
        tfidf_vectors = {}

    for i, (url, text) in enumerate(new_articles):
        new_id = str(latest_id + 1 + i)
        articles[new_id] = {'url': url, 'text': text}

        vectorizer, tfidf_vector = update_document_tfidf(text, vectorizer)
        tfidf_vectors[new_id] = tfidf_vector

    with open(articles_path, 'w') as f:
        json.dump(articles, f)

    inverted_index = update_inverted_index(inverted_index, articles)
    
    with open(inverted_index_path, 'w') as f:
        json.dump({k: list(v) for k, v in inverted_index.items()}, f)

    with open(tfidf_data_path, 'wb') as f:
        pickle.dump({'vectorizer': vectorizer, 'tfidf_vectors': tfidf_vectors}, f)


if __name__ == '__main__':
    new_articles = [('http://example.org/test_article1', 'Hello, this is the text of the first example article.'),('http://example.com/test_article2', 'Hello this is the text of the second test article. I am a Chicago Bulls fan.')]
    update_content(new_articles)
