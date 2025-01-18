from embedding import load_index, query_embeddings
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_openai import ChatOpenAI
from thefuzz import fuzz
import re

# Define the system prompt
system_prompt = """
You are an AI assistant designed to extract and synthesize information from multiple sources to answer user queries accurately. Your primary functions are:

1. Analyze the provided search results thoroughly.
2. Extract relevant information that directly addresses the user's query.
3. Provide concise, factual answers based solely on the given information.
4. Cite sources meticulously for every piece of information used.

Citation Guidelines:
- Format: [Source: filename (page X)]
- Place citations immediately after the relevant sentence or fact.
- Cite multiple sources if information is combined from different documents.
- If page numbers are unavailable, omit them from the citation.

Example Answer Structure:
"The concept of quantum entanglement involves particles that remain connected even when separated by large distances [Source: Introduction_to_Quantum_Physics.pdf (page 42)]. This phenomenon was famously described by Einstein as 'spooky action at a distance' [Source: Einstein_Biography.pdf (page 156)]."

If the query cannot be answered using the provided information, respond with:
"The information to answer this query is not available in the provided results."

Remember:
- Stick strictly to the information given in the search results.
- Do not introduce external knowledge or make assumptions.
- Ensure every statement is supported by a proper citation.
- Maintain objectivity and accuracy in your responses.
"""

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    HumanMessagePromptTemplate.from_template(
        """
        User Query: {query}
        
        Search Results:
        {results}
        
        Citation Information:
        {citation}
        
        Your Answer:
        """
    )
])

def extract_page_number(text):
    """Extract page number from text using regex."""
    # Common page number patterns
    patterns = [
        r'page[s]?\s*(\d+)',  # matches "page 1" or "pages 1"
        r'pg\.?\s*(\d+)',     # matches "pg 1" or "pg. 1"
        r'p\.?\s*(\d+)',      # matches "p 1" or "p. 1"
        r'\[(\d+)\]',         # matches "[1]"
        r'\((\d+)\)',         # matches "(1)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    return None

def fuzzy_match_filename(doc_id, file_list):
    """Find the best matching filename using fuzzy string matching."""
    best_match = None
    best_ratio = 0
    
    for filename in file_list:
        ratio = fuzz.ratio(doc_id.lower(), filename.lower())
        if ratio > best_ratio and ratio > 60:  # threshold of 60%
            best_ratio = ratio
            best_match = filename
    
    return best_match

llm = ChatOpenAI(
    model="gpt-3.5-turbo",  
    temperature=0.5
)

# Define the chain
chain = chat_prompt | llm

# Function to retrieve information with citations
def retrieve_information_citation(query, results):
    # Extract document IDs and try to match them to files
    doc_ids = [result[1] for result in results if result[1]]
    
    # Build citation information
    citations = []
    for doc_id in doc_ids:
        # Extract potential page number
        page_num = extract_page_number(doc_id)
        
        # Get filename through fuzzy matching
        filename = doc_id  # fallback to doc_id if no match
        if hasattr(results, 'file_list'):
            matched_file = fuzzy_match_filename(doc_id, results.file_list)
            if matched_file:
                filename = matched_file
        
        citation = f"{filename}"
        if page_num:
            citation += f" (page {page_num})"
            
        citations.append(citation)
    
    citation_info = "\n".join(citations)
    
    response = chain.invoke({
        "query": query,
        "results": results,
        "citation": citation_info
    })
    
    # Return both the response and citations
    return {
        "content": response.content,
        "citations": citation_info
    }
