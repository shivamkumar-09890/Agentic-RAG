import os
from dotenv import load_dotenv
import yaml
from pyprojroot import here
import shutil
import sqlite3
import pandas as pd

# Load environment variables
load_dotenv()

class LoadConfig:
    def __init__(self) -> None:
        with open(here("src/tools/SQLtool/config.yaml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        self.load_directories(app_config)
        self.clean_sql_db_on_startup()

    def load_directories(self, app_config):
        """Load directory paths from the configuration."""
        self.stored_csv_xlsx_directory = here(app_config["directories"]["stored_csv_xlsx_directory"])
        self.sqldb_directory = here(app_config["directories"]["sqldb_directory"])
        self.uploaded_files_sqldb_directory = here(app_config["directories"]["uploaded_files_sqldb_directory"])

    def clean_sql_db_on_startup(self):
        """Remove the existing SQL database if it exists, ensuring a fresh start."""
        if os.path.exists(self.sqldb_directory):
            try:
                os.remove(self.sqldb_directory)
                print(f"Removed existing database at {self.sqldb_directory}")
            except OSError as e:
                print(f"Error removing database: {e}")

    def convert_to_sql(self, file_path: str, table_name: str):
        """
        Convert a CSV or Excel file into an SQL database.

        Parameters:
            file_path (str): Path to the input file (CSV or Excel).
            table_name (str): Name of the table to store in the SQL database.
        """
        try:
            # Determine file type
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

            # Save to SQL database
            with sqlite3.connect(self.sqldb_directory) as conn:
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                print(f"Table '{table_name}' successfully created in {self.sqldb_directory}")
        except Exception as e:
            print(f"Error converting file to SQL: {e}")
