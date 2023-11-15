from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

def connect_to_database():
    # Create a database engine
    engine = create_engine('mysql+pymysql://root:1234@localhost:33061/db1', echo=False)

    try:
        # Connect to the database
        connection = engine.connect()

        print("Connected to the database successfully!")
        return connection
    except Exception as e:
        # Handle any connection errors
        print("An error occurred while connecting to the database:", str(e))
        return None

connect_to_database()
