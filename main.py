from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from routers import auth,students,books


Base.metadata.create_all(bind=engine)

app=FastAPI()


app.add_middleware(CORSMiddleware,
 allow_origins=["*"],
 allow_headers=["*"],
 allow_methods=["*"]
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(books.router)

@app.get("/")

def home():
    return{"message":"hello backend "}

# @app.put("/students")
# def update_student():
#     return {"message": "Student pura update hua"}

# @app.patch("/students")
# def partial_update_student():
#     return {"message": "Student ka kuch part update hua"}

# @app.get("/students/id/{books_id}")
# def book(books_id:int):
#     return{"message": f"ye lo book no {books_id} ka data"}

# @app.get("/students/title/{title}")
# def book_title(title:str):
#     return{"book_title":f"ye lo book {title} ka data"}



# @app.get("/courses/{course_id}")

# def course(course_id:int ,student_id:int, name:str,show_marks:bool=False):
# #we can use if-else to for condition and jaruart ka hisab sa
#     return{"student_detail:"f"student_id is {student_id} his name is {name} course_enroll no {course_id} "}


  
# class Student(BaseModel):
#     name: str
#     age: int
#     course: str
#     id:int


# @app.post("/students")
# def create_student(student: Student):      
#     # yaha student:Student student parameter _name hai or Student uska type jo base model hain isko object jase excess karege iske field ko
#     return {"message": f"Naya student add hua: {student.name}, age {student.age}, course {student.course} use ID {student.id}"}



# class Books(BaseModel):
#     title: str
#     price: int
#     author: str

# @app.post("/books")
# def create_books(books: Books):      
#     return {"message": f"Naya book add hua: {books.title}, price {books.price}, author  {books.author}"}



# class updates(BaseModel):
#     updated_name: str
#     age:int
   


# @app.put("/students/{student_id}/updates")
# def update_student(student_id:int,updates:updates):      
    
#     return {"message": f" student update hua: {updates.updated_name} is student_updated_ID {student_id} and age is {updates.age}"}




# @app.get("/students/{student_id}")
# def get_student(student_id: int):
#     students_db={100:{"name":"surya","age":32}}
#     if student_id not in students_db:
#         raise HTTPException(status_code=404, detail="Student nahi mila")
#     return students_db[student_id]

    

    



        


    






















# except Exception as e:
# # Yeh line sirf line number nikalegi
# line_no = sys.exc_info()[-1].tb_lineno
# # Ekdum short output
# print(f"Error aaya hai line {line_no} par: {e}")