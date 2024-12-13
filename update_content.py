import json
import pickle
import os
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk

nltk_data_path = os.path.join(os.getcwd(), 'data', 'nltk_data')
corpora_path = os.path.join(nltk_data_path, 'corpora')
tokenizers_path = os.path.join(nltk_data_path, 'tokenizers')
os.makedirs(corpora_path, exist_ok=True)
os.makedirs(tokenizers_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)
nltk.data.path.append(corpora_path)
nltk.data.path.append(tokenizers_path)

def ensure_nltk_data():
    try:
        stop_words = stopwords.words('english')
    except LookupError:
        nltk.download('stopwords', download_dir=nltk_data_path)
    try:
        word_tokenize('This is a test.')
    except LookupError:
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

def update_content(new_articles, inverted_index_path='data/inverted_index.json', articles_path='data/articles.json', tfidf_data_path='data/tfidf_data.pkl'):
    os.makedirs(os.path.dirname(inverted_index_path), exist_ok=True)
    os.makedirs(os.path.dirname(articles_path), exist_ok=True)
    os.makedirs(os.path.dirname(tfidf_data_path), exist_ok=True)

    ensure_nltk_data()

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

    if os.path.exists(tfidf_data_path):
        with open(tfidf_data_path, 'rb') as f:
            tfidf_data = pickle.load(f)
            vectorizer = tfidf_data.get('vectorizer')
            tfidf_vectors = tfidf_data.get('tfidf_vectors', {})
    else:
        vectorizer = None
        tfidf_vectors = {}

    if vectorizer is None:
        vectorizer = TfidfVectorizer(stop_words='english')

    latest_id = max([int(id) for id in articles.keys()], default=-1)

    all_documents = [article['text'] for article in articles.values()]
    new_article_ids = []
    for i, (url, text) in enumerate(new_articles):
        new_id = str(latest_id + 1 + i)
        articles[new_id] = {'url': url, 'text': text}
        all_documents.append(text)
        new_article_ids.append(new_id)

    vectorizer.fit(all_documents)

    for article_id, article_content in articles.items():
        tfidf_vector = vectorizer.transform([article_content['text']])
        tfidf_vectors[article_id] = tfidf_vector

        #if article_id in new_article_ids:
        #    print(f"Article ID: {article_id}")
        #    print(f"TF-IDF Vector:\n{tfidf_vector.toarray()}\n")
        #    print(f"Matrix Size: {tfidf_vector.shape}\n")

    with open(articles_path, 'w') as f:
        json.dump(articles, f)

    inverted_index = update_inverted_index(inverted_index, articles)

    with open(inverted_index_path, 'w') as f:
        json.dump({k: list(v) for k, v in inverted_index.items()}, f)

    with open(tfidf_data_path, 'wb') as f:
        pickle.dump({'vectorizer': vectorizer, 'tfidf_vectors': tfidf_vectors}, f)

if __name__ == '__main__':
    new_articles = [
        ('http://example.org/test_article6', 'The Chicago Bears are a professional American football team based in Chicago. The Bears compete in the National Football League (NFL) as a member of the National Football Conference (NFC) North division. The Bears have won nine NFL Championships, eight prior to the AFL–NFL merger and one Super Bowl. They also hold the NFL records for the most enshrinees in the Pro Football Hall of Fame and the most retired jersey numbers. The Bears\' NFL championships and overall victories are second behind the Green Bay Packers, with whom they have a long-standing rivalry.')
    ]
    update_content(new_articles)
