from embedding import load_index, query_embeddings
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_openai import ChatOpenAI

# Define the system prompt
system_prompt = """
You are an AI assistant that helps find specific information within a given set of results. 
Your job is to examine the provided results and retrieve relevant information that answers the user's query. 
Be precise, extract only the necessary details, and provide clear and concise answers.
If the query cannot be answered with the given results, respond with 'The information is not available in the results.'
"""


chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    HumanMessagePromptTemplate.from_template(
        """
        User Query: {query}
        
        Search Results:
        {results}
        
        Your Answer:
        """
    )
])


llm = ChatOpenAI(
    model="gpt-3.5-turbo",  
    temperature=0.5
)

# Define the chain
chain = chat_prompt | llm

# Function to retrieve information
def retrieve_information(query, results):
    response = chain.invoke({
        "query": query,
        "results": results
    })
    return response

