import os
from typing import List, Dict, Any
import logging
from dataprocessing import load_and_process_pdf
from embedding import calculate_embedding, query_embeddings, load_index
from llmcalling import retrieve_information
from citation import retrieve_information_citation

logger = logging.getLogger(__name__)

class RetrievalTool:
    def __init__(self, input_dir: str = r"data\input", index_path: str = "data/output/faiss_index.index", doc_map_path: str = "data/output/doc_map.json"):
        self.input_dir = input_dir
        self.index_path = index_path
        self.doc_map_path = doc_map_path

    def index_pdfs(self) -> None:
        """Index all PDFs in the input directory."""
        pdf_files = [os.path.join(self.input_dir, f) for f in os.listdir(self.input_dir) if f.endswith('.pdf')]
        
        all_chunks = []
        all_metadata = []
        
        for pdf_file in pdf_files:
            logger.info(f"Processing {pdf_file}...")
            chunks, metadata = load_and_process_pdf(pdf_file)
            all_chunks.extend(chunks)
            all_metadata.extend(metadata)
        
        # Calculate embeddings for all chunks
        calculate_embedding(all_chunks, all_metadata)
        logger.info("PDF indexing completed")

    def query_index(self, query: str) -> Dict[str, Any]:
        """Query the index with the given query."""
        index, documents, ids = load_index(self.index_path, self.doc_map_path)
        results = query_embeddings(index, query, documents, ids)

        response = retrieve_information_citation(query, results)
        return {
            "query": query,
            "response": response['content'],
            "citations": response['citations']
        }

    def execute(self, query: str) -> Dict[str, Any]:
        """
        Executes indexing and querying the index.
        
        :param query: The query to search for.
        :return: A dictionary containing query, response, and citations.
        """
        # Index PDFs before querying
        self.index_pdfs()
        
        # Query the index with the provided query
        return self.query_index(query)


# # Example usage as a tool in your agent
# if __name__ == "__main__":
#     # Initialize the retrieval tool
#     retrieval_tool = RetrievalTool()

#     # Query to search
#     query = "What is discrete variable?"

#     # Execute tool and get response
#     result = retrieval_tool.execute(query=query)
    
#     # Print the result
#     print("Query Result:")
#     print(result)
