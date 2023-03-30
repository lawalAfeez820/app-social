from fastapi import FastAPI , HTTPException, Depends
from app.router import post

app = FastAPI()

@app.get("/")
async def home():
    return {"Greet": "Welcome"}

app.include_router(post.app)


