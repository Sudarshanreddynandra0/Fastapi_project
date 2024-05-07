from fastapi import FastAPI, HTTPException,APIRouter
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI app
app = APIRouter()

# Connect to MongoDB database for student enrollments
enrollment_uri = "mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net/student_enrollment"
enrollment_client = MongoClient(enrollment_uri)
enrollment_db = enrollment_client.student_enrollment
enrollment_collection = enrollment_db.enrollments

# Connect to MongoDB database for assessments
assessment_uri = "mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net/assessments"
assessment_client = MongoClient(assessment_uri)
assessment_db = assessment_client.assessments
assessment_collection = assessment_db.assessments_data

# Model for Assessment
class Assessment(BaseModel):
    student_id: str
    student_name: str
    assessment: str

# API Endpoint to assign assessment
@app.post("/assign_assessment/", response_model=Assessment)
async def assign_assessment(assessment: Assessment):
    # Check if student exists in the student enrollment database and enrolled in the assessment's subject
    enrollment = enrollment_collection.find_one({"student_id": assessment.student_id, "name": assessment.student_name, "subject": assessment.assessment})
    if enrollment:
        # Student is enrolled, assign the assessment
        result = assessment_collection.insert_one(assessment.dict())
        return assessment
    else:
        # Student not found or not enrolled in the subject matching the assessment
        raise HTTPException(status_code=404, detail="Student not found or not enrolled in the subject matching the assessment")
