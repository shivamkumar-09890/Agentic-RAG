# import os
# import pandas as pd
# from load_config import LoadConfig
# import pandas as pd
# from sqlalchemy import create_engine, inspect

# class PrepareSQLFromTabularData:
#     def __init__(self, files_dir):
#         # Load config and initialize variables
#         APPCFG = LoadConfig()
#         self.files_directory = files_dir
#         self.file_dir_list = os.listdir(files_dir)
        
#         db_path = APPCFG.stored_csv_xlsx_directory
#         db_path = f"sqlite:///{db_path}"
#         self.engine = create_engine(db_path)
        
#         print("Number of files:", len(self.file_dir_list))

#     def _prepare_db(self):
#         for file in self.file_dir_list:
#             full_file_path = os.path.join(self.files_directory, file)
#             file_name, file_extension = os.path.splitext(file)
            
#             if file_extension == ".csv":
#                 print(f"Processing CSV file: {file}")
#                 # Process the CSV file in chunks
#                 df = pd.read_csv(full_file_path)
#                 print(f"Completed processing of {file}")
#             elif file_extension == ".xlsx":
#                 print(f"Processing XLSX file: {file}")
#                 df = pd.read_excel(full_file_path)
#                 df.to_sql(file_name, self.engine, index=False)
#             else:
#                 print(f"Unsupported file type: {file_extension}")
#                 continue
#             df.to_sql(file_name, self.engine, index=False)

#         print("==============================")
#         print("All supported files are saved into the SQL database.")

#     def _validate_db(self):
#         # Validate the tables created in SQL DB
#         insp = inspect(self.engine)
#         table_names = insp.get_table_names()
#         print("==============================")
#         print("Available table names in the created SQL DB:", table_names)
#         print("==============================")

#     def run_pipeline(self):
#         # Run the full pipeline
#         self._prepare_db()
#         self._validate_db()


# # Specify the directory containing CSV/XLSX files
# input_dir = "data/input"

# # Create an instance of the class
# sql_preparer = PrepareSQLFromTabularData(input_dir)

# # Run the pipeline
# sql_preparer.run_pipeline()

import os
import pandas as pd
from sqlalchemy import create_engine

# Load the Titanic dataset
df = pd.read_csv(r'data\input\Titanic-Dataset.csv')

# Define the folder and database file path
output_folder = 'data/output'
db_file = 'titanic.db'
db_path = os.path.join(output_folder, db_file)

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Create a connection to the SQLite database in the specified folder
engine = create_engine(f'sqlite:///{db_path}')

# Save the DataFrame to the SQL database as a table
# Table name: 'titanic'
df.to_sql('titanic', con=engine, if_exists='replace', index=False)

print(f"DataFrame has been saved to the SQL database at: {db_path}")

# Query the database to verify
with engine.connect() as connection:
    # Use a proper SQL string for execution
    result = connection.execute("SELECT * FROM titanic")

    # Print the fetched rows
    for row in result:
        print(row)
