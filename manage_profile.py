from fastapi import FastAPI, HTTPException,APIRouter,Path
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI app
app = APIRouter()

# Connect to MongoDB database
uri = "mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net/student_profile"
client = MongoClient(uri)
db = client.student_profile
collection = db.students

# Model for Student Profile
class StudentProfile(BaseModel):
    student_id: str
    name: str

# API Endpoint to create student profile
@app.post("/student/", response_model=StudentProfile)
async def create_student_profile(student_profile: StudentProfile):
    result = collection.insert_one(student_profile.dict())
    return student_profile

# API Endpoint to retrieve student profile by student ID
@app.get("/student/{student_id}", response_model=StudentProfile)
async def get_student_profile(student_id: str = Path(..., description="The ID of the student to retrieve profile for")):
    student_profile = collection.find_one({"student_id": student_id})
    if student_profile:
        return student_profile
    else:
        raise HTTPException(status_code=404, detail="Student profile not found")

# API Endpoint to update student profile
@app.put("/student/{student_id}", response_model=StudentProfile)
async def update_student_profile(student_id: str, student_profile: StudentProfile):
    result = collection.update_one({"student_id": student_id}, {"$set": student_profile.dict()})
    if result.modified_count == 1:
        return student_profile
    else:
        raise HTTPException(status_code=404, detail="Student profile not found")

# API Endpoint to delete student profile
@app.delete("/student/{student_id}")
async def delete_student_profile(student_id: str):
    result = collection.delete_one({"student_id": student_id})
    if result.deleted_count == 1:
        return {"message": "Student profile deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Student profile not found")
