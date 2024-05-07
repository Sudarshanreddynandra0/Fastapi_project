from fastapi import FastAPI, HTTPException,APIRouter
from pymongo import MongoClient
from pydantic import BaseModel

# Initialize FastAPI app
app = APIRouter()

# Connect to MongoDB database for assessments
assessments_uri = "mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net/assessments"
assessments_client = MongoClient(assessments_uri)
assessments_db = assessments_client.assessments
assessments_collection = assessments_db.assessments_data

# Connect to MongoDB database for feedback
feedback_uri = "mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net/feedback"
feedback_client = MongoClient(feedback_uri)
feedback_db = feedback_client.feedback
feedback_collection = feedback_db.feedback_responses

# Model for Feedback
class Feedback(BaseModel):
    student_name: str
    assessment: str
    feedback: str

# API Endpoint for teacher to provide feedback
@app.post("/teacher/feedback/")
async def provide_feedback(feedback: Feedback):
    # Check if student name and assessment match in assessments database
    assessment_query = {
        "student_name": feedback.student_name,
        "assessment": feedback.assessment
    }
    assessment_data = assessments_collection.find_one(assessment_query)
    if not assessment_data:
        raise HTTPException(status_code=404, detail="No matching assessment found")
    
    # Save feedback in the feedbacks collection
    result = feedback_collection.insert_one(feedback.dict())
    return {"message": "Feedback provided and saved successfully"}
