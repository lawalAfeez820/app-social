from fastapi import FastAPI , HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.router import post, users, login,comment, vote
from app.models.comments import CommentOut
from app.models.users import User, UserPost
from app.models.posts import Posts, PostOwner

CommentOut.update_forward_refs(PostOwner=PostOwner, UserPost= UserPost)


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"Greet": "Welcome!!!"}


# routers
app.include_router(post.app)
app.include_router(users.app)
app.include_router(login.app)
app.include_router(comment.app)
app.include_router(vote.app)



