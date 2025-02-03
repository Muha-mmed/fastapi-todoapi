from typing import Optional
from pydantic import BaseModel

class Todo(BaseModel):
    title: str
    description : Optional[str] = None
    published : bool = False
