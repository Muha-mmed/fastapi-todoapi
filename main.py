from fastapi import FastAPI
from route import route
app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world!!!"}

app.include_router(route)