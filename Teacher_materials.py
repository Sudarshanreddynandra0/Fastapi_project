from fastapi import FastAPI, HTTPException,APIRouter
from pymongo import MongoClient
from pydantic import BaseModel

app = APIRouter()

# Connect to MongoDB database
mongo_uri = "mongodb+srv://19275469:siddu@comp7033.1xhdu5e.mongodb.net"
client = MongoClient(mongo_uri)
db = client["teaching_resource"]

# Collection for teaching materials
materials_collection = db["materials"]

# Model for teaching material
class Material(BaseModel):
    student_id: str
    material_topic: str
    material_content: str

# API Endpoint for teacher to upload teaching material
@app.post("/upload_material/")
async def upload_material(material: Material):
    materials_collection.insert_one(material.dict())
    return {"message": "Material uploaded successfully"}
