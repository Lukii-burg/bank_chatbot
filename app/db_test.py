import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found. Check your .env file.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def main():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();")).fetchone()
        print("Connected to PostgreSQL Successfully!")
        print(result[0])

if __name__ == "__main__":
    main()