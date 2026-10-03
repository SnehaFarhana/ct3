from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
 
app = FastAPI()
 
# In-memory storage — no database needed
students = {}
next_id = 1
 
# Data model — defines what a student looks like
class Student(BaseModel):
    name: str
    id_number: str
    gpa: float
 
# Update model — all fields optional
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    gpa: Optional[float] = None
 
 
# ① GET — List all students
@app.get("/students")
def get_all_students():
    return students
 
 
# ② POST — Create a new student
@app.post("/students", status_code=201)
def create_student(student: Student):
    global next_id
    students[next_id] = student.dict()
    result = {"id": next_id, "student": student}
    next_id += 1
    return result
 
 
# ③ PUT — Update an existing student
@app.put("/students/{student_id}")
def update_student(student_id: int, update: StudentUpdate):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    data = students[student_id]
    if update.name:
        data["name"] = update.name
    if update.gpa is not None:
        data["gpa"] = update.gpa
    return data
 
 
# ④ DELETE — Remove a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": f"Student {student_id} deleted successfully"}