# util_routes.py
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi import Depends, FastAPI, File, UploadFile, HTTPException, params
from fastapi.responses import HTMLResponse, StreamingResponse
from typing_extensions import Annotated
from typing import List
from sys import exception
import base64
import io

router = APIRouter()


@router.post("/encode_gpx")
async def encode_gpx(file: Annotated[bytes, File(...)]):
    try: 
        return base64.b64encode(file)
    except exception as e: 
        raise HTTPException(status_code=400, detail=f"Invalid GPX file {e}")


@router.post("/decode-file/")
async def decode_file(encoded_string: str):
    try:
        # Decode the base64 string
        decoded_content = base64.b64decode(encoded_string)
    except exception as e:
        # Handle invalid base64 strings
        raise HTTPException(status_code=400, detail=f"{e}")

    # Return the decoded file as a streaming response
    return StreamingResponse(io.BytesIO(decoded_content), media_type="application/octet-stream")

