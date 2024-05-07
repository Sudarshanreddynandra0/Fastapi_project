from fastapi import FastAPI, HTTPException, Depends,APIRouter
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId

app = APIRouter()

# Connect to MongoDB
client = MongoClient("mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net")
db = client["login"]
collection = db["students"]

# MongoDB Model
class Student(BaseModel):
    id: str
    username: str
    password: str

# Dependency to get MongoDB collection
def get_collection():
    return collection

# Register route
@app.post("/register", response_model=Student)
async def register(student: Student, collection=Depends(get_collection)):
    existing_student = collection.find_one({"id": student.id})
    if existing_student:
        raise HTTPException(status_code=400, detail="User already registered")
    else:
        collection.insert_one(student.dict())
        return student

# Login route
@app.post("/login")
async def login(student: Student, collection=Depends(get_collection)):
    stored_student = collection.find_one({"id": student.id})
    if stored_student and stored_student["password"] == student.password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
