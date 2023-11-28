# util_routes.py
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi_pagination import Page, Params, add_pagination, paginate
from typing import Optional, List, Dict
from database import db, gpx_enabed
from models.trail import Trail
from utils.gpx_utils import validate_gpx_file


router = APIRouter()

@router.get("/gpx_test/")
async def get_gpx_file():
    return FileResponse("/home/mart337i/code/repo/gpx-api/static/Tommerup_Stationsby_Glamsbjerg_Assens.gpx", headers={"name" : "test"})

@router.get("/trails/", response_model=Page[Trail])
async def get_trails(trail : Trail):
    trails = [Trail]
    return paginate(trails)
    

@router.post("/upload/", response_model=Trail)
async def add_trail(trail: Trail):
    pass