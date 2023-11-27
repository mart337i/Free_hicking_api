#-------------------------------------------# - Core libs
from sys import exception
from xml.etree.ElementTree import XMLParser
from fastapi import Depends, FastAPI, File, UploadFile, HTTPException, params
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi_pagination import Page, Params, add_pagination, paginate
#-------------------------------------------# - Ekstra libs
import logging
import base64
import io
from datetime import datetime
from typing_extensions import Annotated
import gpxpy
import gpxpy.gpx
from lxml import etree
import tempfile
from pydantic import BaseModel, Field, Base64Str




#-------------------------------------------# - Database Integration and models
from typing import Optional, List, Dict
from database import db, gpx_enabed
from models.trail import Trail

#-------------------------------------------# - STATIC
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEBUG : bool = bool(os.getenv("DEBUGMODE"))
GPX_XSD_PATH = str(os.getenv("GPX_XSD_PATH"))


logging.basicConfig(filename='/home/mart337i/code/repo/gpx-api/log/app.log',
                    filemode='a',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

_logger = logging.getLogger(__name__)

app = FastAPI()
add_pagination(app)
app.mount("/static", StaticFiles(directory="/home/mart337i/code/repo/gpx-api/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def root():
    """
    Root get will return a basic website to serve the auto generated docs
    """
    return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Greenhouse API</title>
                <!-- Include Bootstrap CSS from CDN -->
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            </head>
            <body class="bg-light">
                <div class="container py-5">
                    <h1 class="display-4 text-center mb-3">Welcome to the Greenhouse Temperature and Humidity API</h1>
                    <p class="lead text-center mb-5">Use the links below to navigate to the API documentation:</p>
                    <div class="row">
                        <div class="col-md-6 text-center mb-3">
                            <a href="/docs" class="btn btn-primary btn-lg">Swagger UI Documentation</a>
                        </div>
                        <div class="col-md-6 text-center mb-3">
                            <a href="/redoc" class="btn btn-secondary btn-lg">ReDoc Documentation</a>
                        </div>
                    </div>
                </div>
                <!-- jQuery first, then Popper.js, then Bootstrap JS -->
                <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
            </body>
            </html>

    """

@app.get("/test", response_class=HTMLResponse)
async def main():
    # Load and return the HTML page
    with open("templates/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@app.get("/gpx_test/")
async def get_gpx_file():
    return FileResponse("/home/mart337i/code/repo/gpx-api/static/lillebaeltsstien.gpx")

@app.get("/trails/", response_model=Page[Trail])
async def get_trails(trail : Trail):
    trails = [Trail]
    return paginate(trails)
    

@app.post("/upload/", response_model=Trail)
async def add_trail(trail : Trail):
    if validate_gpx_file:
        return trail
    else: 
        raise HTTPException(status_code=400, detail="Invalid GPX file")


@app.post("/encode_gpx")
async def encode_gpx(file: Annotated[bytes, File(...)]):
    try: 
        return base64.b64encode(file)
    except exception as e: 
        raise HTTPException(status_code=400, detail=f"Invalid GPX file {e}")


@app.post("/decode-file/")
async def decode_file(encoded_string: str):
    try:
        # Decode the base64 string
        decoded_content = base64.b64decode(encoded_string)
    except exception as e:
        # Handle invalid base64 strings
        raise HTTPException(status_code=400, detail=f"{e}")

    # Return the decoded file as a streaming response
    return StreamingResponse(io.BytesIO(decoded_content), media_type="application/octet-stream")


@app.post("/validate_file")
async def validate_gpx_file(file: UploadFile):
    
    if not GPX_XSD_PATH and DEBUG == True:
        return True
    
    contents = await file.read()

    try:
        gpx = gpxpy.parse(contents.decode())
    except gpxpy.gpx.GPXXMLSyntaxException:
        raise HTTPException(status_code=400, detail="Invalid GPX file")

    with open(GPX_XSD_PATH, 'r') as schema_file:
        schema = etree.XMLSchema(etree.parse(schema_file,XMLParser))
        parser = etree.XMLParser(schema=schema, resolve_entities=False)
        try:
            etree.fromstring(contents, parser)
        except etree.XMLSyntaxError as e:
            raise HTTPException(status_code=400, detail=f"GPX schema validation error: {str(e)}")
    return True
