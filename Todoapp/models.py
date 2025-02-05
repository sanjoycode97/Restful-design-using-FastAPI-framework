#creating the Models help understand to sqlalchemy what kind of database table going to use in our Database
#we need to import base  from database.py inorder to create the database model
#this is means we are creating the model for the database.py file

from database import Base
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()



class Todos(Base):
    __tablename__='todos'
    id = Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    complete=Column(Boolean,default=False)
