from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Response
from pydantic import BaseModel, EmailStr, Field
import sqlite3
from datetime import datetime
import uvicorn
import csv
import io

app = FastAPI()



def import_military_men_from_csv(csv_content: bytes) -> dict:
    csv_text = csv_content.decode('utf-8').splitlines()
    params=[]

    reader = csv.DictReader(csv_text)
    
    for row in reader:
        params.append(row)
            
    return params


@app.post("/assignWithCsv")
async def upload_car_owners_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")

    contents = await file.read()

    result = import_military_men_from_csv(contents)
    
    return result