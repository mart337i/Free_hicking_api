# util_routes.py
from fastapi import APIRouter, HTTPException
from database import gpx_enabled
import os

GPX_STORAGE_PATH = str(os.getenv("GPX_STORAGE_PATH"))
GPX_IMG_STORAGE_PATH = str(os.getenv("GPX_IMG_STORAGE_PATH"))


router = APIRouter()

seed_trails = [
    {
        "schema_version": 1, 
        "name": "Tommerup Stationsby Glamsbjerg_Assens", 
        "filename": "Tommerup_Stationsby_Glamsbjerg_Assens.gpx",
        "location": "Fyn", 
        "image_path": f"{GPX_IMG_STORAGE_PATH}/Tommerup_Stationsby_Glamsbjerg_Assens.jpg",
        "gpx_path": f"{GPX_STORAGE_PATH}/Tommerup_Stationsby_Glamsbjerg_Assens.gpx",
        "length": 10.5, 
        "estimatedTime": 3.5
    },
]

@router.post("/seed-trails/")
async def seed_trails_data():
    try:
        # Insert the seed data into the database
        result = gpx_enabled.insert_many(seed_trails)
        return {"message": f"Successfully inserted {len(result.inserted_ids)} trails."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to seed database: {e}")
    
@router.get("/files/")
async def list_files():
    # Check if the given directory exists
    if not os.path.exists(GPX_STORAGE_PATH):
        raise HTTPException(status_code=404, detail="Directory not found")

    # List all files in the directory
    try:
        files = [f for f in os.listdir(GPX_STORAGE_PATH) if os.path.isfile(os.path.join(GPX_STORAGE_PATH, f))]
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))