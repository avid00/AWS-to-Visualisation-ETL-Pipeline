import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# this refreshes the csv used by tableau to connect to the database and imports the updated data into tableau
df = pd.read_sql("SELECT * FROM stroke_data_processed;", engine)
df.to_csv("stroke_data.csv", index=False)
print("CSV refreshed")
