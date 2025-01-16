"""
Main entry point for the RAG application.
"""
# from config.constants import CONFIG_PATH, INPUT_DIR, OUTPUT_DIR

# def load_config() -> Dict[Any, Any]:
#     """Load configuration from YAML file."""
#     with open(CONFIG_PATH, 'r') as f:
#         return yaml.safe_load(f)


def index_pdfs():
    """Index all PDFs in the input directory"""
    input_dir = r"data\input"
    #calling resluts will give the output dict as below after classifying each pages on basis of text and scanned.
    # {  
    #   {
    #   "file1.pdf": {
    #       "text_pages": [0, 1, 2],
    #       "image_pages": [3, 4]
    #   },
    #   "file2.pdf": {
    #       "text_pages": [0, 1],
    #       "image_pages": [2, 3, 4]
    #   }
    # }
    results = process_folder(input_dir)

    # Get all PDF files
    pdf_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.pdf')]
    
    all_chunks = []
    all_metadata = []
    
    # Process each PDF
    for pdf_file in pdf_files:
        logger.info(f"Processing {pdf_file}...")
        #getting text pages for pdf file
        text_pages = results[pdf_file]["text_pages"]  # [0, 1, 2]
        #passed text pages to get chunks only for those
        chunks, metadata = load_and_process_pdf(pdf_file,text_pages)
        all_chunks.extend(chunks)
        all_metadata.extend(metadata)
    
    # Calculate embeddings for all chunks
    calculate_embedding(all_chunks, all_metadata)
    logger.info("PDF indexing completed")

def query_index(query):
    """Query the index with the given query"""
    # Load index and query
    index, documents, ids = load_index("data/output/faiss_index.index", "data/output/doc_map.json")
    results = query_embeddings(index, query, documents, ids)

    response = retrieve_information_citation(query, results)
    logger.info(f"Query: {query}")
    logger.info(f"Response: {response['content']}")
    logger.info(f"Citations: {response['citations']}")

def main():
    # Set up logging
    logger.info("Starting RAG application")
    
    # # Load configuration
    # config = load_config()
    # logger.info("Configuration loaded successfully")

    # Index PDFs
    index_pdfs()

    query = "What is discrete variable?"
    query_index(query)

if __name__ == '__main__':
    import yaml
    from pathlib import Path
    from typing import Dict, Any
    import time
    from dataprocessing import load_and_process_pdf
    from embedding import calculate_embedding, query_embeddings, load_index, save_index
    from findingtextpage import process_folder
    from llmcalling import retrieve_information
    from citation import retrieve_information_citation
    import os
    logger = setup_logger(__name__)
    main()
