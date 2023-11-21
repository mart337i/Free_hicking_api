# GPX File Handling Service

## Overview
This project is a FastAPI application designed to upload, store, and retrieve GPX (GPS Exchange Format) files. It provides endpoints for uploading GPX files, retrieving all stored GPX data, and fetching the most recent GPX entry.

## Features
- **Upload GPX**: Allows users to upload GPX files, which are stored with metadata including track information and region data.
- **Retrieve GPX Data**: Endpoints to retrieve all GPX entries and the latest entry.

## Endpoints
- `POST /upload`: Upload a GPX file.
- `GET /gpx-data`: Get all GPX data entries.
- `GET /gpx-data/latest`: Get the latest GPX data entry.

## Models
Uses Pydantic models for data validation and serialization.

## Setup and Installation
_TODO: Instructions for setting up and running the project._

## Usage
_TODO: Examples on how to use the endpoints._

## Contributing
Contributions to the project are welcome. Please ensure to follow the project's contribution guidelines.

## License
_TODO: Specify the license under which the project is released._
