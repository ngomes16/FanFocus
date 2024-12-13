import pickle
import json
import os 

tfidf_data_path = 'data/tfidf_data.pkl'

def inspect_tfidf_data(pickle_file_path):
    with open(pickle_file_path, 'rb') as f:
        tfidf_data = pickle.load(f)

    vectorizer = tfidf_data.get('vectorizer')
    tfidf_vectors = tfidf_data.get('tfidf_vectors')

    print("Vectorizer Type:", type(vectorizer))
    print("Vectorizer:", vectorizer)
    print("\nTF-IDF Vectors Type:", type(tfidf_vectors))
    
    if isinstance(tfidf_vectors, dict):
        for article_id, tfidf_vector in tfidf_vectors.items():
            print(f"Article ID: {article_id}, TF-IDF Vector Shape: {tfidf_vector.shape}")
    else:
        print("TF-IDF Vectors structure is not a dictionary.")

def reset_data_storage(reset_users=False):

    data_files = {
        'data/articles.json': {},
        'data/inverted_index.json': {},
        'data/tfidf_data.pkl': {'vectorizer': None, 'tfidf_vectors': {}},
        'data/users.json': {}
    }

    if not reset_users:
        data_files.pop('data/users.json')

    for file_path, default_content in data_files.items():
        with open(file_path, 'wb' if file_path.endswith('.pkl') else 'w') as f:
            if file_path.endswith('.pkl'):
                pickle.dump(default_content, f)
            else:
                json.dump(default_content, f, indent=4)
            print(f"{file_path} has been reset.")

def print_tfidf_data(pickle_file_path): 
    #loadp pikkl
    with open(pickle_file_path, 'rb') as f:
        tfidf_data = pickle.load(f) 

    vectorizer = tfidf_data.get('vectorizer') 
    tfidf_vectors = tfidf_data.get('tfidf_vectors') 
    print("Vectorizer Type:", type(vectorizer)) 
    print("Vectorizer:", vectorizer) 
    if isinstance(tfidf_vectors, dict): 
        for article_id, tfidf_vector in tfidf_vectors.items(): 
            print(f"Article ID: {article_id}") 
            print(f"TF-IDF Vector:\n{tfidf_vector.toarray() if hasattr(tfidf_vector, 'toarray') else tfidf_vector}\n") 
    else: 
        print("TF-IDF not a dictionary.")

if __name__ == "__main__":
    inspect_tfidf_data(tfidf_data_path)
    print_tfidf_data(tfidf_data_path)
    reset_input = input("Do you want to reset the users.json file as well? Yes = 1, No = 0, Exit = anythign else ")
    if reset_input == '1':
        reset_data_storage(reset_users=True)
    elif reset_input == '0':
        reset_data_storage()