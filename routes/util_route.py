# util_routes.py
from fastapi import APIRouter, HTTPException
from fastapi import File, HTTPException
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated
import base64
import io

router = APIRouter()


@router.post("/encode_gpx")
async def encode_gpx(file: Annotated[bytes, File(...)]):
    try: 
        return base64.b64encode(file)
    except Exception as e: 
        raise HTTPException(status_code=400, detail=f"Invalid GPX file {e}")