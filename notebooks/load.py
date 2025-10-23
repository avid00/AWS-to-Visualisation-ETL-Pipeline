import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import text

# load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

#  SQLAlchemy connection string 
connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)

# 1. load processed data from csv
df = pd.read_csv("notebooks/processed_strokedata.csv")

print(f"Loaded {len(df)} rows from processed_strokedata.csv")

# 2. write data to PostgreSQL table 
table_name = "stroke_data_processed"

df.to_sql(table_name, engine, if_exists="append", index=False)

print(f"Data written to table '{table_name}' successfully!")

# # 3. verify row count 
# with engine.connect() as conn:
#     result = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
#     count = result.scalar()
#     print(f"Total rows now in table: {count}")

