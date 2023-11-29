from pydantic import BaseModel, Field, Base64Str
from datetime import datetime
from typing import Optional, List, Dict

class Trail(BaseModel):
    schema_version : Optional[int] = 1
    name : Optional[str]
    filename : Optional[str]
    location : Optional[str]
    image_path : Optional[str]
    gpx_path : Optional[str]
    length : Optional[float]
    estimatedTime : Optional[float]


class TrailSchema(BaseModel):
    name : Optional[str]
    filename : Optional[str]
    location : Optional[str]
    image_path : Optional[str]
    gpx_path : Optional[str]
    
