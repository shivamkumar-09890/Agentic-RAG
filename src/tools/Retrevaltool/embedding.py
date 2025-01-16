from langchain_openai import OpenAIEmbeddings

import faiss
import numpy as np
import os
import json
import logging
import time
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key not found. Please set it in the .env file.")

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Save and load index functions
def save_index(index, documents, ids, index_file_path, doc_map_file_path):
    # Save the FAISS index
    faiss.write_index(index, index_file_path)
    logger.info(f"Index saved to {index_file_path}")

    # Save the document-to-ID mapping with metadata
    doc_map = {}
    for i in range(len(documents)):
        if isinstance(documents[i], dict):
            # If document is already a metadata dict
            doc_map[ids[i]] = documents[i]
        else:
            # If document is just text, create basic metadata
            doc_map[ids[i]] = {
                'text': documents[i],
                'file': 'unknown',
                'page': None
            }

    # Save the document map to a file (using JSON format)
    with open(doc_map_file_path, 'w') as doc_map_file:
        json.dump(doc_map, doc_map_file)
    logger.info(f"Document mapping saved to {doc_map_file_path}")

def load_index(index_file_path, doc_map_file_path):
    # Load the FAISS index
    index = faiss.read_index(index_file_path)
    logger.info(f"Index loaded from {index_file_path}")

    # Load the document-to-ID mapping
    with open(doc_map_file_path, 'r') as doc_map_file:
        doc_map = json.load(doc_map_file)
    logger.info(f"Document mapping loaded from {doc_map_file_path}")

    # Extract ids and documents from the mapping
    ids = list(doc_map.keys())
    documents = list(doc_map.values())

    return index, documents, ids

def calculate_embedding(chunks, metadata, BATCH_SIZE=20, persist_path="data/output/faiss_index.index", doc_map_path="data/output/doc_map.json"):
    start_time_1 = time.time()

    # Create a FAISS index (L2 distance)
    embedding_dim = len(embeddings.embed_documents(["test"])[0])
    index = faiss.IndexFlatL2(embedding_dim)
    documents = metadata  # Store metadata instead of just chunks
    ids = []

    # Check if an index exists and load it
    if os.path.exists(persist_path):
        logger.info("Loading existing FAISS index and document mapping...")
        index, documents, ids = load_index(persist_path, doc_map_path)
    else:
        logger.info("Creating new FAISS index and document mapping...")

    end_time_1 = time.time()
    logger.info(f"Time for setting up FAISS index: {end_time_1 - start_time_1:.2f} seconds")

    start_time = time.time()
    for i in range(0, len(chunks), BATCH_SIZE):
        batch_chunks = chunks[i:i + BATCH_SIZE]
        batch_metadata = metadata[i:i + BATCH_SIZE]
        
        # Generate unique IDs for each chunk
        batch_ids = [f"{meta['file']}_page{meta['page']}_{j}" for j, meta in enumerate(batch_metadata)]
        
        # Create embeddings for the text chunks
        batch_embeddings = embeddings.embed_documents(batch_chunks)
        batch_embeddings = np.array(batch_embeddings).astype('float32')
        
        # Add to index
        index.add(batch_embeddings)
        ids.extend(batch_ids)
    
    end_time = time.time()
    logger.info(f"Time for creating/updating FAISS index: {end_time - start_time:.2f} seconds")

    # Save the updated index and document mapping
    save_index(index, documents, ids, persist_path, doc_map_path)

def query_embeddings(index, query_text, documents, ids, top_k=3):
    """
    Query the FAISS index for the closest embeddings and return the top-k documents.
    """
    query_embedding = np.array([embeddings.embed_query(query_text)]).astype('float32')
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i in range(top_k):
        index_id = indices[0][i]
        if index_id < len(ids):
            doc_id = ids[index_id]
            document = documents[index_id]
            distance = distances[0][i]
            results.append((document['text'], doc_id, distance))
        else:
            results.append((None, None, None))

    return results

def print_query_results(results):
    """
    Print the results from the query_embeddings function in a readable format.
    
    Args:
        results: List of tuples where each tuple contains (document, id, distance).
    """
    if not results:
        print("No results found.")
        return

    print("Query Results:")
    print("=" * 40)
    for rank, (document, doc_id, distance) in enumerate(results, start=1):
        print(f"Rank {rank}:")
        print(f"Document: {document}")
        print(f"ID: {doc_id}")
        print(f"Distance: {distance:.4f}")
        print("-" * 40)
