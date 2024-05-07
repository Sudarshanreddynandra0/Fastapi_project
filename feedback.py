from fastapi import FastAPI, HTTPException,APIRouter

from pymongo import MongoClient
from pydantic import BaseModel

# Initialize FastAPI app
app = APIRouter()

# Connect to MongoDB database for feedback
feedback_uri = "mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net/feedback"
feedback_client = MongoClient(feedback_uri)
feedback_db = feedback_client.feedback
feedback_collection = feedback_db.feedback_responses

# Model for Feedback
class FeedbackResponse(BaseModel):
    student_name: str
    assessment: str
    feedback: str

# API Endpoint for student to view feedback by name
@app.get("/student/feedback/")
async def view_feedback(student_name: str):
    # Find feedback responses matching student name
    feedbacks = list(feedback_collection.find({"student_name": student_name}))
    if not feedbacks:
        raise HTTPException(status_code=404, detail="No feedback found for the given student name")
    
    # Extract relevant details for the student
    student_feedback = []
    for feedback in feedbacks:
        student_feedback.append({
            "assessment": feedback["assessment"],
            "feedback": feedback["feedback"]
        })
    
    return {"student_name": student_name, "feedback": student_feedback}
