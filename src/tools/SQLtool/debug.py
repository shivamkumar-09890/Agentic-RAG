import pandas as pd
from sqlalchemy import create_engine
import os

class PrepareSQLFromTabularData:
    def __init__(self, files_dir):
        # Load config and initialize variables
        APPCFG = LoadConfig()
        self.files_directory = files_dir
        self.file_dir_list = os.listdir(files_dir)
        
        db_path = APPCFG.stored_csv_xlsx_sqldb_directory
        db_path = f"sqlite:///{db_path}"
        self.engine = create_engine(db_path)
        
        print("Number of files:", len(self.file_dir_list))

    def _prepare_db(self):
        for file in self.file_dir_list:
            full_file_path = os.path.join(self.files_directory, file)
            file_name, file_extension = os.path.splitext(file)
            
            if file_extension == ".csv":
                print(f"Processing CSV file: {file}")
                # Process the CSV file in chunks
                for chunk in pd.read_csv(full_file_path, chunksize=50000):  # Adjust chunk size if needed
                    chunk.to_sql(file_name, self.engine, index=False, if_exists='append')
                print(f"Completed processing of {file}")
            elif file_extension == ".xlsx":
                print(f"Processing XLSX file: {file}")
                df = pd.read_excel(full_file_path)
                df.to_sql(file_name, self.engine, index=False)
            else:
                print(f"Unsupported file type: {file_extension}")
                continue

        print("==============================")
        print("All supported files are saved into the SQL database.")

    def _validate_db(self):
        # Validate the tables created in SQL DB
        insp = inspect(self.engine)
        table_names = insp.get_table_names()
        print("==============================")
        print("Available table names in the created SQL DB:", table_names)
        print("==============================")

    def run_pipeline(self):
        # Run the full pipeline
        self._prepare_db()
        self._validate_db()
