from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Needed for raw SQL
# while True:
#     try:
#         conn = psycopg.connect(
#             host='localhost',
#             dbname='fastAPI',
#             user='postgres',
#             password='password123',
#             row_factory=dict_row
#         )
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as e:
#         print("Failed to connect to database")
#         print("Error: ", e)
#         time.sleep(2)