from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db,engine
from schema import Todo,UpdateTodo
import model
from typing import List


model.BASE.metadata.create_all(bind=engine)


route = APIRouter()

@route.get("/getalltodos")
def get_all_todo(db: Session= Depends(get_db)):
    todos = db.query(model.Todo).all()
    if todos is None:
        return []
    return todos

@route.post("/todo/create")
def create_todo(todo:Todo,db: Session =Depends(get_db)):
    todoCont = model.Todo(**todo.model_dump())
    db.add(todoCont)
    db.commit()
    db.refresh(todoCont)
    return todoCont

@route.put("/todo/update/{post_id}", response_model=UpdateTodo)
def update_todo(new_post: UpdateTodo, post_id: int, db: Session = Depends(get_db)):
    todo = db.query(model.Todo).filter(model.Todo.id == post_id).first()
    if not todo:
        return {"error": "odo not found"}
    
    update_data = new_post.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo, key, value)
        
    db.commit()
    db.refresh(todo)
    return todo

@route.get("/published_todo")
def get_published_todos(db: Session= Depends(get_db)):
    published_todo = db.query(model.Todo).filter(model.Todo.published == True).all()
    return published_todo

@route.get("/draft_todo")
def get_draft_post(db: Session= Depends(get_db)):
    draft_todo = db.query(model.Todo).filter(model.Todo.published == False).all()
    return draft_todo

@route.get("/getbyid/{todo_id}")
def get_by_id(todo_id:int,db:Session =Depends(get_db)):
    todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    return todo


# Search endpoint
@route.get("/search", response_model=List[Todo])
def search_todo(name: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(model.Todo)
    
    if name:
        query = query.filter(model.Todo.title.like(f"%{name}%") | model.Todo.description.like(f"%{name}%"))
        todos = query.all()
        if not todos:
            return {"error": "No post found"}
        return todos
    return []


@route.delete("/delete/{todo_id}")
def delete_post(todo_id:int,db:Session = Depends(get_db)):
    todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()