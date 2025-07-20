from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from db.database import get_db
from db.schemas.user_schema import UserSchema
from sqlalchemy import text
from apis.constants import DUMMY_USERS
from apis.utils import hash_password
from apis.auth import oauth2

router = APIRouter()


@router.delete("/delete_all_users/")
async def delete_all_users(db:Session = Depends(get_db),token = Depends(oauth2)):
    try:
        # BELOW CODE WILL NOT RESET THE AUTOINCREMENT TO 0
        db.query(UserSchema).delete()
        # db.commit()
        # db.execute(text("DELETE FROM USERS"))
        # db.execute(text("DELETE FROM sqlite_sequence WHERE name='users'"))
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@router.post("/bulk_insert")
async def bulk_insert(db:Session=Depends(get_db)):
    try:
        users = list(map(lambda user : UserSchema(email=user['email'],username=user['username'],password=hash_password(user['password'])),DUMMY_USERS))
        db.add_all(users)
        db.commit()
        return {"statusCode" : 201,"msg" : "Bulk insert done!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e)) 

@router.get("/all-users")
async def all_users(db : Session = Depends(get_db)):
    try:
        users = db.query(UserSchema).all()
        return users 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))