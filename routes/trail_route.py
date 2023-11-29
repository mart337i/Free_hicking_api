# util_routes.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi_pagination import Page, paginate
from typing import List
from models.trail import Trail, TrailSchema
from database import gpx_enabled
from pydantic import ValidationError
import logging
import os

GPX_STORAGE_PATH = str(os.getenv("GPX_STORAGE_PATH"))
GPX_IMG_STORAGE_PATH = str(os.getenv("GPX_IMG_STORAGE_PATH"))

_logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/gpx_test/")
async def gpx_test_file():
    return FileResponse("/home/mart337i/code/repo/gpx-api/static/Tommerup_Stationsby_Glamsbjerg_Assens.gpx", headers={"name" : "test"})

@router.get("/trails/", response_model=Page[Trail])
async def get_trails():
    # Fetch all trails from MongoDB
    trails_cursor = gpx_enabled.find()

    # Filter and validate data according to Trail model
    trails: List[Trail] = []
    for trail_data in trails_cursor:
        try:
            trail = Trail(**trail_data)
            trails.append(trail)
        except ValidationError as e:
            _logger.warning(f"{e}")
            continue

    # Apply pagination to the trails list
    return paginate(trails)

    
def upload_trail_to_db(trail: Trail):
    try:
        trail_id = gpx_enabled.insert_one(trail.model_dump()).inserted_id
        return trail_id
    except Exception as e:
        raise ValueError(f"Failed to upload trail: {e}")

@router.post("/upload/", response_model=Trail)
async def add_trail(trail: Trail):
    try:
        trail_id = upload_trail_to_db(trail)
        return trail
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/get-gpx/{filename}")
async def get_gpx_file(filename: str):
    # Check if the file extension is .gpx
    if not filename.endswith(".gpx"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .gpx files are allowed.")

    file_path = os.path.join(GPX_STORAGE_PATH, filename)

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(file_path)


@router.get("/get-img/{filename}")
async def get_img_file(filename: str):
    # Check if the file extension is .gpx
    if not filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only img files are allowed.")

    file_path = os.path.join(GPX_IMG_STORAGE_PATH, filename)

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(file_path)
