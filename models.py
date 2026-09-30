from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    course = Column(String)


class Books(Base):
    __tablename__="books"
    id =Column(Integer,primary_key=True,index=True)
    title=Column(String)
    author=Column(String)
    price=Column(Integer)       



class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    user_name=Column(String,unique=True)
    Hashed_password=Column(String)





    