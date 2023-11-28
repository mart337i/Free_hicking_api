#-------------------------------------------# - Core libs
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
#-------------------------------------------# - Ekstra libs
import logging
import gpxpy.gpx

#-------------------------------------------# - Database Integration and models



#-------------------------------------------# - Routes

from routes.util_route import router as util_router
from routes.trail_route import router as trail_router
from routes.trail_seeding_route import router as trail_seeding_route


import os

LOGGING_PATH = str(os.getenv("LOGGING_PATH"))


logging.basicConfig(filename=LOGGING_PATH,
                    filemode='a',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# _logger = logging.getLogger(__name__)

app = FastAPI()
add_pagination(app)

# This is not a problem in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(util_router, prefix="/utils", tags=["Utils"]) 
app.include_router(trail_router, prefix="/trail", tags=["Trail"]) 
app.include_router(trail_seeding_route, prefix="/trail_seeding", tags=["Trail Seeding"]) 



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



