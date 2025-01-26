import os
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.agent_toolkits import create_sql_agent
from load_config import LoadConfig

APPCFG = LoadConfig()


class ChatBot:
    """
    A ChatBot class to interact with SQL databases created from CSV/XLSX files.
    """

    @staticmethod
    def respond(chatbot: list, message: str, chat_type: str) -> tuple:
        """
        Respond to a message by querying a SQL database created from CSV/XLSX files.

        Args:
            chatbot (list): A list storing the chatbot's conversation history.
            message (str): The user's query.
            chat_type (str): Type of interaction (e.g., 'Q&A with stored CSV/XLSX SQL-DB').

        Returns:
            tuple: Updated chatbot conversation list and an optional response.
        """
        if chat_type == "Q&A with stored CSV/XLSX SQL-DB":
            if os.path.exists(APPCFG.stored_csv_xlsx_directory):
                # Connect to the stored SQL database
                engine = create_engine(
                    f"sqlite:///{APPCFG.stored_csv_xlsx_directory}")
                db = SQLDatabase(engine=engine)

                # Print available tables for debugging
                print(f"Available tables: {db.get_usable_table_names()}")

                # Create a SQL agent to process the query
                agent_executor = create_sql_agent(
                    APPCFG.langchain_llm, db=db, agent_type="openai-tools", verbose=True
                )

                # Process the user's query
                response = agent_executor.invoke({"input": message})
                chatbot.append((message, response["output"]))
                return "", chatbot
            else:
                chatbot.append(
                    (message, "SQL DB from the stored CSV/XLSX files does not exist. "
                              "Please first create the database."))
                return "", chatbot, None
        else:
            chatbot.append(
                (message, "Invalid chat type. Only 'Q&A with stored CSV/XLSX SQL-DB' is supported."))
            return "", chatbot, None


# Example usage
chatbot = []  # List to store chatbot conversation history
message = "What are the available tables in the database?"  # User's query
chat_type = "Q&A with stored CSV/XLSX SQL-DB"  # Specify interaction type

# Respond using the ChatBot class
response = ChatBot.respond(chatbot, message, chat_type)

# Print the response
print(response)
