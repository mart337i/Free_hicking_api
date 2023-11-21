#-------------------------------------------# - Core libs
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
#-------------------------------------------# - Ekstra libs
import logging
import base64
from datetime import datetime
import gpxpy
import gpxpy.gpx
from lxml import etree

#-------------------------------------------# - Database Integration and models
from database import db, gpx_enabed
from models.gpx import GPXSchema, FileInfo,GPXData, TrackInfo,Metadata
from typing import Optional, List, Dict

#-------------------------------------------# - STATIC
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEBUG : bool = os.getenv("DEBUGMODE")
GPX_XSD_PATH = os.getenv("GPX_XSD_PATH")


logging.basicConfig(filename='/home/mart337i/code/repo/gpx-api/log/app.log',
                    filemode='a',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

_logger = logging.getLogger(__name__)

app = FastAPI()
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

# Endpoint to upload a GPX file
@app.post("/upload", response_model=GPXSchema)
async def upload_gpx(file: UploadFile = File(...)):
    # Here, implement your logic to handle the file and create the GPXSchema object
    # For example:
    gpx_schema = GPXSchema(
        gpxData=GPXData(
            file=FileInfo(
                type=file.content_type,
                name=file.filename,
                size=len(await file.read()),
                content=""  # Add the base64 encoded content here
            ),
            trackInfo=TrackInfo(),
            metadata=Metadata(
                createdDate=datetime.now(),
                updatedDate=datetime.now()
            )
        )
    )
    # Save to database or perform additional processing
    return gpx_schema

# Endpoint to get all GPX data
@app.get("/gpx-data", response_model=List[GPXSchema])
async def get_all_gpx_data():
    # Implement your logic to retrieve all GPX data from the database
    return []

# Endpoint to get the latest GPX data
@app.get("/gpx-data/latest", response_model=GPXSchema)
async def get_latest_gpx_data():
    # Implement your logic to retrieve the latest GPX data from the database
    return GPXSchema()


async def validate_gpx_file(file: UploadFile):
    
    if not GPX_XSD_PATH and DEBUG == True:
        return True

    # Check MIME type
    if file.content_type != 'application/gpx+xml':
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Read file content
    contents = await file.read()

    # Sanitize and parse with gpxpy
    try:
        gpx = gpxpy.parse(contents.decode())
    except gpxpy.gpx.GPXXMLSyntaxException:
        raise HTTPException(status_code=400, detail="Invalid GPX file")

    # Validate against GPX schema
    with open(GPX_XSD_PATH, 'r') as schema_file:
        schema = etree.XMLSchema(etree.parse(schema_file))
        parser = etree.XMLParser(schema=schema, resolve_entities=False)
        try:
            etree.fromstring(contents, parser)
        except etree.XMLSyntaxError as e:
            raise HTTPException(status_code=400, detail=f"GPX schema validation error: {str(e)}")

    # Return true if validation passes
    return True
