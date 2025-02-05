#now create the table using sqlalchemy
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Path, dependencies
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

import models
#from  database import engine
import database


app=FastAPI()

#create table so we have to import the database loacation and models (structure of the tables)
models.Base.metadata.create_all(bind=database.engine)

#create api enpoint that fetch data from the record

#when we access the database in each request and also close the database after response is delivered
def get_db():
    db=database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#endpoints for read all the record (Dependens(get_db) it will create the session for the db get the item from db and close the session once  it return the response)
#using dependency injection we are getting the get_db and run  it. thru SessionLocal we are able to contact the database to return all information back
#Annoted helps to creating the dependency injection
#DB dependency variable(we have created the dependency injection for API enpoint to open the database connection and close after returning the data)
db_dependency=Annotated[Session,Depends(get_db)]


#creating pydantic request which will contain body of the request of the todo's http post request 
class TodoRequest(BaseModel):  #in Fastapi application we dont have to worry about the request point of view we dont need mention the id as id is primary key so sQL alchemy will auto increament the id as we user dont know about the id its our responsibility to increamnet the id
    title : str = Field(min_length=3,max_length=100) #adding validation field for the request body
    description : str = Field(min_length=3,max_length=100)
    priority :int = Field(gt=0,lt=6)
    complete : bool
    

@app.get("/readall")
def read_all(db: db_dependency):
    return db.query(models.Todos).all()


#get particular item using item id or path parameter (adding path parameter validation also)
@app.get("/read_todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_data_by_id(db:db_dependency,todo_id: int=Path(gt=0)):
    model_db=db.query(models.Todos).filter(models.Todos.id==todo_id).first()
    if model_db is not None:
        return model_db
    raise HTTPException(status_code=404,detail='item is not found')

#create the post object and save to database and here we need pytdantic to create the and capture and validation the request body(so create pydantic model for post request body)

#creating post request
@app.post("/todo_create",status_code=status.HTTP_200_OK)
async def create_todo(db: db_dependency, todo_request: TodoRequest): #todorequest here is pydantic model (db_dependency is the connection making to the database)
    todo_post_model=models.Todos(**todo_request.model_dump()) #converting request to json after passing to Todos data base and then it will pass to the todo table 
    db.add(todo_post_model) #capturing the request and adding to the db
    db.commit() #saving to the table

#this is put request or update the resources 
@app.put("/todo_update/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_update_request: TodoRequest, todo_id: int=Path(gt=0)):


    todo_model_update=db.query(models.Todos).filter(models.Todos.id==todo_id).first()

    if todo_model_update is  None:
        raise HTTPException(status_code=404,detail="item not found")
    
    todo_model_update.title = todo_update_request.title
    todo_model_update.description = todo_update_request.description
    todo_model_update.priority = todo_update_request.priority
    todo_model_update.complete = todo_update_request.complete

    db.add(todo_model_update)
    db.commit()


#creating delete method 
@app.delete("/todo_delete/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_id(db: db_dependency, todo_id: int=Path(gt=0)):

    todo_model_delete=db.query(models.Todos).filter(models.Todos.id==todo_id).first()  #checking if the id is exist

    if todo_model_delete is None: #if not exist then raise http exception
        raise HTTPException(status_code=404,detail="item is not found")
    
    db.query(models.Todos).filter(models.Todos.id==todo_id).delete() #if exist  then just search or filter it and delete
    db.commit() # once delete transaction is completed then just commit to the db
        
    
    
