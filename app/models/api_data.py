from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

# Creating a base class for declarative class definitions
Base = declarative_base()

# Defining a model class for the 'api_data' table
class ApiDataModel(Base):
    # Defining the table name

    __tablename__ = "api_data"
    
    # Defining columns

    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Using default value of current UTC time for timestamp column
    timestamp = Column(DateTime, default=datetime.utcnow)
    value = Column(Integer)
    weekday = Column(String)
    days_till_christmas = Column(Integer)
    days_till_halloween = Column(Integer)
    