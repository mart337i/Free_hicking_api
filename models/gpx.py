from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict

class FileInfo(BaseModel):
    type: str
    name: str
    size: int
    content: str

class TrackInfo(BaseModel):
    length: float = 0.0
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    startPoint: Dict[str, float] = {}
    endPoint: Dict[str, float] = {}
    bounds: Dict[str, float] = {}
    region: Optional[str] = None

class Metadata(BaseModel):
    createdDate: datetime
    updatedDate: datetime
    owner: Optional[str] = None
    tags: List[str] = []
    description: Optional[str] = None

class GPXData(BaseModel):
    file: FileInfo
    trackInfo: TrackInfo
    metadata: Metadata

class GPXSchema(BaseModel):
    schemaVersion: int = 1
    gpxData: GPXData