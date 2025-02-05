#SQLALchemy - it is an ORM which is fas aPi will going to use inorder to intract with database

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Correct SQLite connection string
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create the engine with the correct 'check_same_thread' argument
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={'check_same_thread': False}  # Make sure the argument is correctly spelled
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
