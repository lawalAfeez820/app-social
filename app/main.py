from fastapi import FastAPI , HTTPException, Depends
from app.router import post, users, login
from app.models.posts import Posts
from app.models.users import User

Posts.update_forward_refs(User=User)
User.update_forward_refs(Posts=Posts)

app = FastAPI()

@app.get("/")
async def home():
    return {"Greet": "Welcome"}


# routers
app.include_router(post.app)
app.include_router(users.app)
app.include_router(login.app)



