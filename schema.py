from typing import Optional
from pydantic import BaseModel

class Todo(BaseModel):
    title: str
    description : Optional[str] = None
    published : bool = False

    class Config:
        orm_mode = True
        
class UpdateTodo(BaseModel):
    title:  Optional[str] = None
    description : Optional[str] = None
    published :  Optional[bool]=None