from fastapi import FastAPI
from apis.auth import router as LoginRouter
from apis.users import router as UsersRouter
from db.database import Base,engine

app = FastAPI()
Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)

app.include_router(LoginRouter,prefix="/auth",tags=["Authentication"])
app.include_router(UsersRouter,prefix="/users",tags=["Users"])


