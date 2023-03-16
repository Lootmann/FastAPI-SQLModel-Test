from fastapi import FastAPI

from api.routers.posts import router as post_router
from api.routers.users import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
