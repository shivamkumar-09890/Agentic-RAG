import fitz  # PyMuPDF
import time
from multiprocessing import Pool, cpu_count
from langchain.text_splitter import CharacterTextSplitter
import os

text_splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=100)

def process_pages(args):
    file_path, text_page = args
    chunks = []
    chunk_metadata = []
    try:
        doc = fitz.open(file_path)
        filename = os.path.basename(file_path)
        for page_num in text_page:
            page = doc.load_page(page_num)
            text = page.get_text()
            if text.strip():
                page_chunks = text_splitter.split_text(text)
                chunks.extend(page_chunks)
                # Add metadata for each chunk from this page
                chunk_metadata.extend([{
                    'file': filename,
                    'page': page_num + 1,  # 1-based page numbering
                    'text': chunk
                } for chunk in page_chunks])
        doc.close()
    except Exception as e:
        print(f"Error processing pages {text_page} in {file_path}: {e}")
    return chunks, chunk_metadata

def load_and_process_pdf(file_path, num_workers=None):
    doc = fitz.open(file_path)
    total_pages = len(doc)
    doc.close()

    #using all available CPUs if num_worker is not specified
    if num_workers is None:
        num_workers = cpu_count()

    # Divide the text_page into chunks for parallel processing
    pages_per_worker = total_pages // num_workers if total_pages >= num_workers else 1
    page_ranges = [
        range(i, min(i + pages_per_worker, total_pages))  # Create ranges for each worker
        for i in range(0, total_pages, pages_per_worker)
    ]


    all_chunks = []
    all_metadata = []
    with Pool(processes=num_workers) as pool:
        # Map the processing to each chunk of text_page
        results = pool.map(process_pages, [(file_path, list(page_range)) for page_range in page_ranges])
        for chunks, metadata in results:
            all_chunks.extend(chunks)
            all_metadata.extend(metadata)

    return all_chunks, all_metadata
