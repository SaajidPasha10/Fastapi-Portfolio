from fastapi import APIRouter,Depends,status,HTTPException,Form
from fastapi.security import OAuth2PasswordRequestForm
import jwt 
from config import settings
from db.database import SESSION_MAKER,get_db
from sqlalchemy.orm import Session
from db.schemas.user_schema import UserSchema
from sqlalchemy import or_, and_
from apis.utils import hash_password,verify_hash
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2 = OAuth2PasswordBearer("/auth/login/")

@router.post("/register/")
async def register(uname : str = Form(...,min_length=3,max_length=20),password : str= Form(...,min_length=3,max_length=20),email : str = Form(...,min_length=3,max_length=20),db : Session = Depends(get_db)):
    try:
        # check if user already present in db
        existing_user = check_user_in_db(uname=uname,email=email,db=db)
        if  existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User Registered Already!") 
        else:
            # user not found in db we store user in db
            hashed_password = hash_password(password)
            user = UserSchema(email=email,username=uname,password=hashed_password)
            db.add(user)
            db.commit()
            return {"statusCode" : 204,"msg" : "User Registered Successfully!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

def check_user_in_db(uname:str,email:str,db,password:str = None):
    if password == None:
        existing_user = db.query(UserSchema).filter((uname == UserSchema.username) | (UserSchema.email == email)).first()
        if existing_user:
            return True
    else:
        existing_user = db.query(UserSchema).filter(or_(uname == UserSchema.username,UserSchema.email == email)).first()
        is_valid_password = verify_hash(password=password,hashed_password=existing_user.password)
        if existing_user and is_valid_password:
            return True
    return False

@router.post("/login/")
async def login(formData : OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
    try:
        uname_or_email = formData.username
        password = formData.password 

        # Authentication : verify credentials 
        token = authenticate_user(uname_or_email,password,db=db)
        response = {}
        response['statusCode'] = 200
        response['msg'] = "Login successful!"
        response['token'] = token
        response['token_type'] = "Bearer"
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

def authenticate_user(uname_or_email,password,db):
    existing_user = check_user_in_db(uname=uname_or_email,email=uname_or_email,password=password,db=db)
    if existing_user:
        return jwt.encode({"username":uname_or_email},settings.JWT_SECRET_KEY,algorithm='HS256')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials!")