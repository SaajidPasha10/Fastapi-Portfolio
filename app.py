from fastapi import FastAPI
from apis.auth import router as LoginRouter
from apis.users import router as UsersRouter
from apis.blog import router as BlogRouter
from db.database import Base,engine

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/media", StaticFiles(directory="media"), name="media")
templates = Jinja2Templates(directory="templates")


Base.metadata.create_all(bind=engine)

# Base.metadata.drop_all(bind=engine)

app.include_router(LoginRouter,prefix="/auth",tags=["Authentication"])
app.include_router(UsersRouter,prefix="/users",tags=["Users"])
app.include_router(BlogRouter,prefix="/blogs",tags=["Blogs"])


