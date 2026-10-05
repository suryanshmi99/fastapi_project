from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
import models
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


router = APIRouter(prefix="/auth",tags=["Auth"])

pwd_pass=CryptContext(schemes=["bcrypt"],deprecated="auto")

load_dotenv()
SECRET_KEY =os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

class user_data(BaseModel):
    userName:str
    password:str




@router.post("/register")

def user_credintials(user:user_data,db:Session=Depends(get_db)):
    Hash_Pass=pwd_pass.hash(user.password)
    new_user_credintial=models.User(user_name=user.userName,Hashed_password=Hash_Pass)
    db.add(new_user_credintial)
    db.commit()
    # db.refresh(new_user_credintial)
    return {"message":f" data created your user name is {user.userName}"}

def create_tokens(data:dict):
    data_toencode=data.copy()        #creatig data copy to use in future 
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)     #yaha ham current time main 30 min add kar rahe isee 30 min expire time milega 
    data_toencode["exp"]=expire     # yha pa ham jo time nikale expire main usko exp yani expire wale kaam main fix karna matlab token 
    # apne aap khatam hoayega iss particular 
    # time ka aab jo value exp main hote hain utne time period ka baad khatam ho jata hain token
    if not SECRET_KEY:
        raise ValueError("check .env filefor SECRET_KEY")

    token=jwt.encode(data_toencode,SECRET_KEY,algorithm=ALGORITHM)

           #Yahi asli "banane" wali line hai — jwt.encode() teen cheezein leta hai:

            # Data (jo dictionary mein daala — username + expiry)----> data_toencode
            # Secret Key (chaabi jisse lock karega)
            # Algorithm (kaunse formula se)
    return token



@router.post("/login")
def login(user: user_data, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_name == user.userName).first()
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="username not found"
        )

    if not pwd_pass.verify(user.password, db_user.Hashed_password):
        raise HTTPException(
            status_code=401,
            detail="wrong password"
        )

    token = create_tokens({"sub": db_user.user_name})
    return {"access_token": token, "token_type": "bearer"}



extrating_token=OAuth2PasswordBearer(tokenUrl="login")   #Ye FastAPI ka ek built-in tool hai jiska kaam hai
                                                           #— "Client ki request se token nikaalna


def get_user_by_verifingTokens(token:str=Depends(extrating_token)):
    try:
        if not SECRET_KEY:
            raise ValueError("check .env file for SECRET_KEY")
        decoded_token=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])    

# yaha client na jo token beja wo decode yani
# break kar rahe 3 parts main 
# decoded token main hi sab check hota hain
# jase token sahi to hain na exp time oor 
# jo token hain uske secret key or algo ka use karka
# purna token sa match hota hain ki sahi hain 
# aese security check hote hain
# decoded token ko payload bhi bol sakte hain 
# oor usme exp time username ye sab hota hain


        username=decoded_token.get("sub")   # yaha pa sub sa uername nikal rahe login main "sub" main username beja thaa 
        if not username:
            raise HTTPException(status_code=401,detail="Token valid hai par usme username nahi mila.")

        return username

    except JWTError: # agar starting main hi token galt nikala ya expire to yaha kaa game hoga suru
        raise HTTPException(status_code=401,detail="expire hogya ya invalid hain token ya fake")