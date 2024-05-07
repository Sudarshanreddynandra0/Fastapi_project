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

# API Endpoint for student to download teaching material
@app.get("/download_material/{student_id}/{material_topic}")
async def download_material(student_id: str, material_topic: str):
    material = materials_collection.find_one({"student_id": student_id, "material_topic": material_topic})
    if material:
        return {"material_content": material["material_content"]}
    else:
        raise HTTPException(status_code=404, detail="Material not found")
