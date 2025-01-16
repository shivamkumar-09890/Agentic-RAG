import os
import fitz  # PyMuPDF
import logging
from multiprocessing import Pool, cpu_count

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def categorize_pages_worker(args):
    """
    Worker function to categorize a range of pages in a PDF.
    
    Args:
        args (tuple): (file_path, page_range)
    
    Returns:
        text_pages (list): List of page numbers with extractable text.
        image_pages (list): List of page numbers with images but no extractable text.
    """
    file_path, page_range = args
    text_pages = []
    image_pages = []
    
    try:
        doc = fitz.open(file_path)
        for page_num in page_range:
            page = doc[page_num]
            text = page.get_text()[:100].strip()
            # images = page.get_images(full=True)

            if text:
                text_pages.append(page_num)
            else :
                image_pages.append(page_num)
        doc.close()
    except Exception as e:
        logging.error(f"Error processing pages {page_range} of {file_path}: {e}")
    
    return text_pages, image_pages

def categorize_pdf_pages(file_path, use_multiprocessing=True):
    """
    Categorize pages in a PDF into text-based and image-based pages.

    Args:
        file_path (str): Path to the PDF file.
        use_multiprocessing (bool): Use multiprocessing for large PDFs.
    
    Returns:
        text_pages (list): List of page numbers with extractable text.
        image_pages (list): List of page numbers with images but no extractable text.
    """
    try:
        doc = fitz.open(file_path)
        total_pages = len(doc)
        doc.close()
        
        if total_pages == 0:
            logging.warning(f"The PDF {file_path} is empty.")
            return [], []
        
        logging.info(f"Processing {total_pages} pages from {file_path}.")

        # Prepare page ranges for multiprocessing
        num_workers = cpu_count() if use_multiprocessing else 1
        pages_per_worker = max(1, total_pages // num_workers)
        page_ranges = [range(i, min(i + pages_per_worker, total_pages)) for i in range(0, total_pages, pages_per_worker)]

        text_pages, image_pages = [], []

        if use_multiprocessing:
            with Pool(processes=num_workers) as pool:
                results = pool.map(categorize_pages_worker, [(file_path, page_range) for page_range in page_ranges])
                for text, images in results:
                    text_pages.extend(text)
                    image_pages.extend(images)
        else:
            for page_range in page_ranges:
                text, images = categorize_pages_worker((file_path, page_range))
                text_pages.extend(text)
                image_pages.extend(images)

        logging.info(f"Completed {file_path}. Text-based pages: {len(text_pages)}, Image-based pages: {len(image_pages)}.")
        return text_pages, image_pages

    except Exception as e:
        logging.error(f"Error processing PDF {file_path}: {e}")
        return [], []

def process_folder(folder_path, use_multiprocessing=True):
    """
    Process all PDFs in a folder and categorize their pages.

    Args:
        folder_path (str): Path to the folder containing PDF files.
        use_multiprocessing (bool): Use multiprocessing for large PDFs.
    
    Returns:
        results (dict): A dictionary containing text-based and image-based pages for each PDF file.
    """
    results = {}
    try:
        # List all PDF files in the folder
        pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]

        if not pdf_files:
            logging.warning(f"No PDF files found in folder {folder_path}.")
            return results

        logging.info(f"Found {len(pdf_files)} PDF files in folder {folder_path}.")

        for pdf_file in pdf_files:
            logging.info(f"Processing {pdf_file}...")
            text_pages, image_pages = categorize_pdf_pages(pdf_file, use_multiprocessing)
            results[pdf_file] = {"text_pages": text_pages, "image_pages": image_pages}

        logging.info(f"Processing completed for folder {folder_path}.")
        return results

    except Exception as e:
        logging.error(f"Error processing folder {folder_path}: {e}")
        return results

# # Example usage
# if __name__ == "__main__":
#     folder_path = "pdf"  # Replace with the path to your folder containing PDFs
#     results = process_folder(folder_path)

#     for pdf_file, page_data in results.items():
#         print(f"File: {pdf_file}")
#         print("  Text-based pages:", page_data["text_pages"])
#         print("  Image-based pages:", page_data["image_pages"])
