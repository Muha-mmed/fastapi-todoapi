from sqlalchemy import Column,text,Integer,Boolean,TIMESTAMP,String
from database import BASE

class Todo(BASE):
    __tablename__ = 'todos'
    
    id= Column(Integer,primary_key=True,nullable=False)    
    title=Column(String, nullable=False)
    description = Column(String,nullable=True)
    published = Column(Boolean, server_default=text('False'))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))