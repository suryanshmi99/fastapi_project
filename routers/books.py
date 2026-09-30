from fastapi import APIRouter, Depends, HTTPException
import models
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from routers.auth import get_user_by_verifingTokens







router = APIRouter(prefix="/books_db",tags=["Books"])



class Books_Database(BaseModel):
    title:str
    author:str
    price:int





@router.post("/books_db")
def addingNewBook(books:Books_Database,db:Session=Depends(get_db), current_user: str = Depends(get_user_by_verifingTokens)):
    new_books=models.Books(title=books.title,author=books.author,price=books.price)
    db.add(new_books)
    db.commit()
    db.refresh(new_books)
    return new_books


@router.get("")
def geting_Books(db:Session=Depends(get_db),aunticateAuther:str=Depends(get_user_by_verifingTokens)):
    seeing_boks=db.query(models.Books).all()
    return seeing_boks




@router.get("/{books_id}")
def geting_BooksBy_ID(books_id:int,db:Session=Depends(get_db)):
    seeing_boks=db.query(models.Books).filter(models.Books.id==books_id).first()
    if not seeing_boks:
        raise HTTPException(status_code=404,detail="ye book ni hain ")
    return seeing_boks


@router.put("/{books_id}")
def updatingBooks(books:Books_Database,books_id:int,db:Session=Depends(get_db)):
    updating_books=db.query(models.Books).filter(models.Books.id==books_id).first()
    if not updating_books:
        raise HTTPException(status_code=404,detail="ye book ni hain cnt update")

    updating_books.title=books.title        #type:ignore
    updating_books.author=books.author      #type:ignore
    updating_books.price=books.price        #type:ignore

    db.commit()
    db.refresh(updating_books)
    return " the updated data is ",updating_books




    
@router.delete("/{books_id}",status_code=200)
def delete_books(books_id:int,db:Session=Depends(get_db)):
    deleteBooks=db.query(models.Books).filter(models.Books.id==books_id).first()
    if not deleteBooks:
        raise HTTPException(status_code=404,detail="ye book ni hain cnt delete")
    db.delete(deleteBooks)
    db.commit()
    return {f"message":"books ID {books_id} hogya delete"}