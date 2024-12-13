import os
import nltk

nltk_data_path = os.path.join(os.path.dirname(__file__), 'data', 'nltk_data')
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

#stop words for tokenizign text
nltk.download('stopwords', download_dir=nltk_data_path)
nltk.download('punkt', download_dir=nltk_data_path)