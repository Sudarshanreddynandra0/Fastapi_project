from fastapi import FastAPI, HTTPException, APIRouter
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI app
app = APIRouter()

# Connect to MongoDB database for student profiles
profile_uri = "mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net/student_profile"
profile_client = MongoClient(profile_uri)
profile_db = profile_client.student_profile
profile_collection = profile_db.students

# Connect to MongoDB database for student enrollments
enrollment_uri = "mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net/student_enrollment"
enrollment_client = MongoClient(enrollment_uri)
enrollment_db = enrollment_client.student_enrollment
enrollment_collection = enrollment_db.enrollments

# Model for Enrollment
class Enrollment(BaseModel):
    student_id: str
    name: str
    subject: str

# API Endpoint to enroll in a subject
@app.post("/enroll/", response_model=Enrollment)
async def enroll_subject(enrollment: Enrollment):
    # Check if student exists in the student profile database
    student_profile = profile_collection.find_one({"student_id": enrollment.student_id, "name": enrollment.name})
    if student_profile:
        # Student exists, enroll in the subject
        result = enrollment_collection.insert_one(enrollment.dict())
        return enrollment
    else:
        # Student not found in the profile database
        raise HTTPException(status_code=404, detail="Student not found in profile database")

# API Endpoint to quit from a subject
@app.delete("/enroll/")
async def quit_subject(student_id: str, subject: str):
    # Check if student is enrolled in the subject
    enrollment = enrollment_collection.find_one({"student_id": student_id, "subject": subject})
    if enrollment:
        # Student is enrolled, remove enrollment
        enrollment_collection.delete_one({"student_id": student_id, "subject": subject})
        return {"message": "Student successfully quit from subject"}
    else:
        # Student not enrolled in the subject
        raise HTTPException(status_code=404, detail="Student not enrolled in this subject")

