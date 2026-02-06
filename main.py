from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory database
students_db = {}
next_id = 1

class Student(BaseModel):
    name: str
    age: int
    email: str
    roll_no: int
    Department: str

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str
    roll_no: int
    Department: str

@app.get("/")
def read_root():
    return {"Hello": "World", "Documentation": "/docs"}

@app.post("/students", response_model=StudentResponse)
def create_student_handler(student: Student):
    global next_id
    id = next_id
    new_student = StudentResponse(id=id, **student.dict())
    students_db[id] = new_student
    next_id += 1
    return new_student

@app.get("/students", response_model=List[StudentResponse])
def get_all_students():
    return list(students_db.values())

@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student_handler(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student_handler(student_id: int, student: Student):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    updated_student = StudentResponse(id=student_id, **student.dict())
    students_db[student_id] = updated_student
    return updated_student

@app.delete("/students/{student_id}")
def delete_student_handler(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=44, detail="Student not found")
    del students_db[student_id]
    return {"message": "Student deleted successfully"}