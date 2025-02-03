from fastapi import APIRouter, Depends
from sqlalchemy.orm import session
from database import get_db,engine
from schema import Todo
import model

model.BASE.metadata.create_all(bind=engine)


route = APIRouter()

@route.post("/post/create")
def create_post(todo:Todo,db: session =Depends(get_db)):
    todoCont = model.Todo(**todo.model_dump())
    db.add(todoCont)
    db.commit()
    db.refresh(todoCont)
    return todoCont

@route.get("/post/get")
def get_post(db: session= Depends(get_db)):
    published_todo = db.query(model.Todo).filter(model.Todo.published == True).all()
    return published_todo