from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db,engine
from schema import Todo
import model

model.BASE.metadata.create_all(bind=engine)


route = APIRouter()

@route.get("/getallpost")
def get_all_post(db: Session= Depends(get_db)):
    posts = db.query(model.Todo).all()
    if posts is None:
        return []
    return posts

@route.post("/post/create")
def create_post(todo:Todo,db: Session =Depends(get_db)):
    todoCont = model.Todo(**todo.model_dump())
    db.add(todoCont)
    db.commit()
    db.refresh(todoCont)
    return todoCont

@route.get("/published_post")
def get_published_post(db: Session= Depends(get_db)):
    published_todo = db.query(model.Todo).filter(model.Todo.published == True).all()
    return published_todo

@route.get("/draft_post")
def get_draft_post(db: Session= Depends(get_db)):
    published_todo = db.query(model.Todo).filter(model.Todo.published == False).all()
    return published_todo

@route.get("/getbyid/{post_id}")
def get_by_id(post_id:int,db:Session =Depends(get_db)):
    post = db.query(model.Todo).filter(model.Todo.id == post_id).first()
    return post

@route.delete("/delete/{post_id}")
def delete_post(post_id:int,db:Session = Depends(get_db)):
    post = db.query(model.Todo).filter(model.Todo.id == post_id).first()
    db.delete(post)
    db.commit()