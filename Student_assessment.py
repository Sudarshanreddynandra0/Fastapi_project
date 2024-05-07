from fastapi import FastAPI, HTTPException,APIRouter
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI app
app = APIRouter()

# Connect to MongoDB database for assessments
assessment_uri = "mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net/assessments"
assessment_client = MongoClient(assessment_uri)
assessment_db = assessment_client.assessments
assessment_collection = assessment_db.assessments_data

# Connect to MongoDB database for assessment responses
response_uri = "mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net/assessments"
response_client = MongoClient(response_uri)
response_db = response_client.assessments
response_collection = response_db.assessment_responses

# Model for Assessment Response
class AssessmentResponse(BaseModel):
    student_id: str
    student_name: str
    assessment: str
    status: str

# API Endpoint to retrieve assessment details by student ID
@app.get("/assessment/{student_id}")
async def get_assessment_details(student_id: str):
    # Find assessment details by student ID
    assessment = assessment_collection.find_one({"student_id": student_id})
    if assessment:
        return {"assessment": assessment["assessment"]}
    else:
        raise HTTPException(status_code=404, detail="No assessment found for the student")

# API Endpoint to save assessment response
@app.post("/assessment/response/")
async def save_assessment_response(response: AssessmentResponse):
    # Save assessment response
    result = response_collection.insert_one(response.dict())
    return {"message": "Assessment response saved successfully"}
