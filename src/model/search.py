#TODO: set requirements.txt
#!pip install faiss-cpu
#!pip install sentence_transformers

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Set up NLTK and other preprocessing tools
en_stop = set(stopwords.words('english'))
stemmer = WordNetLemmatizer()

def process_text(document):
    """
    Preprocesses a text document.

    Args:
        document (str): The input text document.

    Returns:
        str: Cleaned and preprocessed text.
    """
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    document = re.sub(r'\W', ' ', str(document))
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
    document = document.lower()
    tokens = document.split()
    lemma_txt = [stemmer.lemmatize(word) for word in tokens]
    lemma_no_stop_txt = [word for word in lemma_txt if word not in en_stop]
    clean_txt = ' '.join(lemma_no_stop_txt)
    return clean_txt

def build_faiss_index(embeddings):
    """
    Builds a Faiss index for given embeddings.

    Args:
        embeddings (np.ndarray): The document embeddings.

    Returns:
        faiss.IndexIDMap: A Faiss index.
    """
    d = embeddings.shape[1] #embeddings' dimension
    index =  faiss.IndexFlatL2(d) 
    index.add(encoded_data)
    
    # TODO: partition the index with voronoi cells 
    # URL: https://www.pinecone.io/learn/series/faiss/faiss-tutorial/#Partitioning-The-Index
    # m = 8  # number of centroid IDs in final compressed vectors
    # bits = 8 # number of bits in each centroid

    # nlist = 50 # number of partitions (Voronoi cells) we’d like our index to have
    # quantizer = faiss.IndexFlatL2(d)  # we keep the same L2 distance flat index
    # index = faiss.IndexIVFPQ(quantizer, d, nlist, m, bits)
    # index.train(encoded_data)
    # index.add(encoded_data)
    
    return index
    

def search(query, k, index, model):
    """
    Performs semantic search using the given query and index.

    Args:
        query (str): The query text.
        top_k (int): Number of top results to retrieve.
        index (faiss.IndexIDMap): Faiss index.
        model (SentenceTransformer): Sentence embedding model.

    Returns:
        list: List of tuples containing (document ID, similarity score).
    """
    query_vector = model.encode([query])
    distances, top_k_ids = index.search(query_vector, k) #top k vectors closest to query_vector

    results = []
    for i in range(len(top_k_ids[0])):
        results.append((top_k_ids[0][i], distances[0][i]))  # Capture similarity score

    return results # (document id, similarity)

def main():
    document_list = ["program 1: nudge", "program 2: audit"] # List of document contents
    
    # Preprocess the documents (based on sentence_transformers docs)
    clean_corpus = [process_text(sentence) for sentence in tqdm(document_list) if sentence.strip() != '']
    clean_corpus_lst = [d.split() for d in clean_corpus]
    
    # Load SentenceTransformer model
    model = SentenceTransformer('msmarco-distilbert-base-dot-prod-v3')

    # Encode documents
    encoded_data = model.encode(clean_corpus_lst)
    encoded_data = np.asarray(encoded_data.astype('float32'))

    # Build Faiss index
    index = build_faiss_index(encoded_data)
    #faiss.write_index(index, 'eval_report.index') # load the index in production

    # Perform search
    query = "poke"
    search(query, k=2, index=index, model=model)

if __name__ == "__main__":
    main()
