from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from database import SessionLocal, engine
from models import DetectionResult, Base
from detector import PersonDetector

app = FastAPI()

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize YOLO detector
detector = PersonDetector("./checkpoint/best.pt")

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for API validation
class UploadResponse(BaseModel):
    num_people: int
    image_path: str

class DetectionResultOut(BaseModel):
    id: int
    timestamp: datetime
    num_people: int
    image_path: str

    class Config:
        from_attributes = True

class DetectionHistoryResponse(BaseModel):
    records: List[DetectionResultOut]
    total: int

@app.post("/upload/", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # Save uploaded image
    image_path = os.path.join("uploads", file.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    num_people, boxes = detector.detect(image_path)

    output_filename = f"vis_{file.filename}"
    output_path = f"outputs/{output_filename}"
    detector.visualize(image_path, boxes, output_path)

    detection = DetectionResult(num_people=num_people, image_path=output_path)
    db.add(detection)
    db.commit()
    db.refresh(detection)

    return {"num_people": num_people, "image_path": output_path}

@app.get("/history/", response_model=DetectionHistoryResponse)
async def get_history(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    search: Optional[str] = None
):
    query = db.query(DetectionResult)
    
    if search:
        query = query.filter(DetectionResult.image_path.contains(search))

    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time)
            query = query.filter(DetectionResult.timestamp >= start_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_time format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")
    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time)
            query = query.filter(DetectionResult.timestamp <= end_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_time format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")
    
    total = query.count()
    records = query.offset(skip).limit(limit).all()
    return {"records": records, "total": total}