from fastapi import APIRouter, Depends, HTTPException
import models
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from routers.auth import get_user_by_verifingTokens


router = APIRouter(prefix="/students",tags=["Students"])




class Student_request(BaseModel):
    name:str
    age:int
    course:str



@router.post("")
def crete_student(student:Student_request,db: Session=Depends(get_db)):
    new_Student=models.Student(name=student.name ,age=student.age,course=student.course)
    db.add(new_Student)
    db.commit()
    db.refresh(new_Student)
    return new_Student






# db.query(TABLE).filter(CONDITION).order_by(...).limit(...)


# Simple trick: Jo bhi SQL tu likhta tha, usi ko top-to-bottom SQLAlchemy methods mein todh de — 
# SELECT → db.query(), WHERE → .filter(),
# ORDER BY → .order_by(), aur end mein .all() ya .first() 
# laga do.

# Subquery — SQL vs SQLAlchemy

# SQL:

# sql
# SELECT * FROM students WHERE age > (SELECT AVG(age) FROM students);

# SQLAlchemy:

# python
# avg_age = db.query(func.avg(models.Student.age)).scalar_subquery()
# db.query(models.Student).filter(models.Student.age > avg_age).all()












@router.get("")
def get_all_students(db: Session = Depends(get_db),current_user:str=Depends(get_user_by_verifingTokens)):
    students = db.query(models.Student).all()
    return students

@router.get("/{student_id}")
def get_all_students_byPara(student_id:int,db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(models.Student.id==student_id).first()
    if not students:
        raise HTTPException(status_code=400,detail='student mila ni is ID pa ')
    return students





@router.put("/{student_id}")
def update_students(student:Student_request,student_id:int,db:Session=Depends(get_db)):
    exiting_student=db.query(models.Student).filter(models.Student.id==student_id).first()
    if not exiting_student:
        raise HTTPException (status_code=404,detail='student ni hain ye to update ni hoga')
    exiting_student.name=student.name   # type: ignore
    exiting_student.age=student.age       # type: ignore
    exiting_student.course=student.course   # type: ignore

    db.commit()
    db.refresh(exiting_student)
    return exiting_student

    





@router.delete("/{student_id}",status_code=200)
def delte_students_byPara(student_id:int,db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(models.Student.id==student_id).first()
    if not students:
        raise HTTPException(status_code=400,detail='student mila ni is ID pa ')
    db.delete(students)
    db.commit()
    return {"message":f"ID {student_id} delete ho gaya hain table sa"}