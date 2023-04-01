from fastapi import FastAPI , HTTPException, Depends
from app.router import post, users

app = FastAPI()

@app.get("/")
async def home():
    return {"Greet": "Welcome"}


# routers
app.include_router(post.app)
app.include_router(users.app)


