from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime, timezone
import pandas as pd
import logging
import shutil
import uuid
import os

# -------------------------------------------------
# INITIALIZE APP (ONLY ONCE!)
# -------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# LOAD ENV + DB
# -------------------------------------------------
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

PROCESSED_FILE_DIR = ROOT_DIR / "processed_file"
PROCESSED_FILE_DIR.mkdir(exist_ok=True)

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

# -------------------------------------------------
# API ROUTER
# -------------------------------------------------
api = APIRouter(prefix="/api")

# MODELS
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str


# -------------------------------------------------
# BASIC ROUTES
# -------------------------------------------------
@api.get("/")
async def root():
    return {"message": "Hello World"}


# -------------------------------------------------
# UPLOAD ENDPOINT (Front-end Depends on JSON Response)
# -------------------------------------------------
@api.post("/upload")
async def upload_loan_file(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith((".xlsx", ".xls")):
            raise HTTPException(status_code=400, detail="Only Excel files allowed")

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        original_name = file.filename.rsplit(".", 1)[0]

        upload_path = PROCESSED_FILE_DIR / f"{original_name}_{timestamp}.xlsx"
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        df = pd.read_excel(upload_path)
        df.columns = df.columns.str.strip()

        df = df.dropna(how="all")

        df["Status"] = df.apply(
            lambda row: "Approved"
            if (
                str(row.get("Document Submitted", "")).lower() == "yes"
                and str(row.get("KYC Submitted", "")).lower() == "yes"
                and str(row.get("Business Proof Submitted", "")).lower() == "yes"
            )
            else "Rejected",
            axis=1,
        )

        output_file = f"{original_name}_{timestamp}_processed.csv"
        output_path = PROCESSED_FILE_DIR / output_file
        df.to_csv(output_path, index=False)

        # 👉 RETURN JSON (Expected by frontend)
        return {
            "status": "success",
            "filename": output_file
        }

    except Exception as e:
        logging.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# LIST PROCESSED FILES
# -------------------------------------------------
@api.get("/processed-files")
async def processed_files():
    files = []

    for file in PROCESSED_FILE_DIR.glob("*.csv"):
        df = pd.read_csv(file)

        approved = df[df["Status"] == "Approved"].shape[0]
        rejected = df[df["Status"] == "Rejected"].shape[0]

        files.append({
            "filename": file.name,
            "approved": approved,
            "rejected": rejected,
            "total": approved + rejected
        })

    return files



# -------------------------------------------------
# DOWNLOAD FILE
# -------------------------------------------------
@api.get("/download/{filename}")
async def download_file(filename: str):
    path = PROCESSED_FILE_DIR / filename

    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path, filename=filename)


# -------------------------------------------------
# REGISTER ROUTES
# -------------------------------------------------
app.include_router(api)

