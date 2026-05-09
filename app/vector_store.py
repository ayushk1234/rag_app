import os
import chromadb
from fastembed import TextEmbedding

# Initialize embedding model
# jinaai/jina-embeddings-v2-small-en is a good model for embedding 
# because it is small and fast
embedding_model = TextEmbedding(
    model_name="jinaai/jina-embeddings-v2-small-en"
)

# Initialize ChromaDB client
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print("BASE_DIR: ",os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)

# gets an existing collection or create a new one if it doesn't exist
collection = client.get_or_create_collection(
    name="document_qa"
)

# creating embeddings for the chunks
def generate_embeddings(texts):

    embeddings = list(
        embedding_model.embed(texts)
    )

    return embeddings

#Store the embeddings and metadatas in ChromaDB
def store_chunks(chunks):

    texts = []
    metadatas = []
    ids = []

    for idx, chunk in enumerate(chunks):

        texts.append(chunk["text"])
        metadatas.append(chunk["metadata"])
        ids.append(
            f"{chunk['metadata']['source']}_{idx}"
        )

    embeddings = generate_embeddings(texts)

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Stored {len(texts)} chunks")

# Searches for  chunks based on the query
def search_chunks(query, top_k=4):

    query_embedding = generate_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results