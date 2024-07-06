# Steps fpr the project:
# 1. download and load a LLM
# 2. download PostgreSQL and pgvectorstore; connect to the PostgreSQL database and write to it vector store
# 3. process and chunk documents, generate embeddings, and upload to the vector store
# 4. define a retriever and query engine; initialize an instance
# Credit/tutorial: https://docs.llamaindex.ai/en/stable/examples/low_level/oss_ingestion_retrieval/

from sqlalchemy import make_url
from llama_index.vector_stores.postgres import PGVectorStore
from pathlib import Path
from llama_index.readers.file import PyMuPDFReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TextNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.core.schema import NodeWithScore
from typing import Optional, Any, List
from llama_index.core import QueryBundle
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
import psycopg2
from llama_index.llms.llama_cpp import LlamaCPP

# from llama_cpp import Llama #this doesn't give me any error

# Initialize the LlamaCPP model
# model_url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf"

llm = LlamaCPP(
    # You can pass in the URL to a GGML model to download it automatically
    # model_url=model_url,
    # optionally, you can set the path to a pre-downloaded model instead of model_url
    model_path="llm_models/llama-2-13b-chat.Q4_0.gguf",
    temperature=0.1,
    max_new_tokens=256,
    # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
    context_window=6000,
    # kwargs to pass to __call__()
    generate_kwargs={},
    # kwargs to pass to __init__()
    # set to at least 1 to use GPU
    model_kwargs={"n_gpu_layers": 1},
    verbose=True,
)
# to fix the shutdown error (doesn't work): https://github.com/abetlen/llama-cpp-python/issues/891#issuecomment-1839701861

# Define database connection parameters
# If you don't have postgresql already, you need to install them (version 16): https://www.postgresql.org/download/
# you also need to intall the pgvector extension: https://github.com/pgvector/pgvector#windows

db_name = "vector_db"
host = "localhost"
password = "password"
port = "5432"
user = "postgres"

# Connect to the PostgreSQL server and manage connection properly
conn = psycopg2.connect(
    dbname="postgres",
    host=host,
    password=password,
    port=port,
    user=user,
)
conn.autocommit = True

with conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")
conn.close()

# Initialize the PGVectorStore with the specified parameters
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=host,
    password=password,
    port=port,
    user=user,
    table_name="llama2_paper",
    embed_dim=384,  # openai embedding dimension
)

from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data/clean/full").load_data()

## Load documents from a PDF file using PyMuPDFReader
# loader = PyMuPDFReader()
# documents = loader.load(file_path="./data/llama2.pdf")

# Use a Text Splitter to Split Documents
text_parser = SentenceSplitter(chunk_size=1024)

text_chunks = []
doc_idxs = []
for doc_idx, doc in enumerate(documents):
    cur_text_chunks = text_parser.split_text(doc.text)
    text_chunks.extend(cur_text_chunks)
    doc_idxs.extend([doc_idx] * len(cur_text_chunks))

# Manually Construct Nodes from Text Chunks
nodes = []
for idx, text_chunk in enumerate(text_chunks):
    node = TextNode(text=text_chunk)
    src_doc = documents[doc_idxs[idx]]
    node.metadata = src_doc.metadata
    nodes.append(node)

# Generate Embeddings for each Node
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

for node in nodes:
    node_embedding = embed_model.get_text_embedding(
        node.get_content(metadata_mode="all")
    )
    node.embedding = node_embedding
vector_store.add(nodes)

# # Construct vector store query
# query_str = "Can you tell me about the key concepts for safety finetuning"
# query_embedding = embed_model.get_query_embedding(query_str)

# vector_store_query = VectorStoreQuery(
#     query_embedding=query_embedding, similarity_top_k=2, mode="default"
# )

# # Execute query and parse result into a set of nodes
# query_result = vector_store.query(vector_store_query)
# print(query_result.nodes[0].get_content())

# nodes_with_scores = []
# for index, node in enumerate(query_result.nodes):
#     score: Optional[float] = None
#     if query_result.similarities is not None:
#         score = query_result.similarities[index]
#     nodes_with_scores.append(NodeWithScore(node=node, score=score))


# Define the VectorDBRetriever
class VectorDBRetriever(BaseRetriever):
    def __init__(
        self,
        vector_store: PGVectorStore,
        embed_model: Any,
        query_mode: str = "default",
        similarity_top_k: int = 2,
    ) -> None:
        self._vector_store = vector_store
        self._embed_model = embed_model
        self._query_mode = query_mode
        self._similarity_top_k = similarity_top_k
        super().__init__()

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        query_embedding = embed_model.get_query_embedding(query_bundle.query_str)
        vector_store_query = VectorStoreQuery(
            query_embedding=query_embedding,
            similarity_top_k=self._similarity_top_k,
            mode=self._query_mode,
        )
        query_result = vector_store.query(vector_store_query)

        nodes_with_scores = []
        for index, node in enumerate(query_result.nodes):
            score: Optional[float] = None
            if query_result.similarities is not None:
                score = query_result.similarities[index]
            nodes_with_scores.append(NodeWithScore(node=node, score=score))

        return nodes_with_scores


# Initialize and use the retriever
retriever = VectorDBRetriever(
    vector_store, embed_model, query_mode="hybrid", similarity_top_k=3
)  # can make query mode hybrid

# Plug this into our RetrieverQueryEngine to synthesize a response
query_engine = RetrieverQueryEngine.from_args(retriever, llm=llm)
query_str = "What are some program evaluations related to the underground economy?"

response = query_engine.query(query_str)
print(str(response))
print(response.source_nodes[0].get_content())
