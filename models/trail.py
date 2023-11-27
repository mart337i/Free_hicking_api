from pydantic import BaseModel, Field, Base64Str
from datetime import datetime
from typing import Optional, List, Dict

class Trail(BaseModel):
    schema_version : Optional[int] = 1
    name : Optional[str]
    location : Optional[str]
    image : Optional[Base64Str]
    gpx : Optional[Base64Str]
    length : Optional[float]
    estimatedTime : Optional[float]
    
    
