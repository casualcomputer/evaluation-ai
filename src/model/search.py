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
    index = faiss.IndexIDMap(faiss.IndexFlatIP(embeddings.shape[1]))
    index.add_with_ids(embeddings, np.array(range(0, embeddings.shape[0])))
    return index

def search(query, top_k, index, model):
    """
    Performs semantic search using the given query and index.

    Args:
        query (str): The query text.
        top_k (int): Number of top results to retrieve.
        index (faiss.IndexIDMap): Faiss index.
        model (SentenceTransformer): Sentence embedding model.

    Returns:
        list: List of top document IDs.
    """
    query_vector = model.encode([query]) #TODO: generalize to query vector (single query now)
    top_k = index.search(query_vector, top_k)
    top_k_ids = top_k[1].tolist()[0] #TODO: include scores; allow users to choose similarity scores
    top_k_ids = list(np.unique(top_k_ids))
    return top_k_ids

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
    faiss.write_index(index, 'eval_report.index')

    # Perform search
    query = "poke"
    top_k_ids = search(query, top_k=2, index=index, model=model)

    # Print search results
    print("Your top search results (most to least relevant):\n")
    for idx, x in enumerate(top_k_ids):
        print("result number:", idx + 1)
        print(document_list[x], "\n")

if __name__ == "__main__":
    main()
