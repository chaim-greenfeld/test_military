from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Response
from pydantic import BaseModel, EmailStr, Field
import sqlite3
from datetime import datetime
import uvicorn
import csv
import io

app = FastAPI()

class Soldier:
    def __init__(self, personal_number,f_name, l_name, gender, city, residential_distance):
        self.personal_number = personal_number
        self.f_name = f_name
        self.l_name = l_name
        self.gender = gender
        self.city = city
        self.residential_distance = residential_distance
        self.placement_status = f"{False}, in waiting list"



class Room:
    
    def __init__(self):
        
        
        self.soldier = []
        self.is_full = False

    def add_mens(self,  militery_mens):
        self.soldier.append(militery_mens)
        militery_mens.placement_status = True
        
        if len(self.soldier) == 8:
            self.is_full = True

            return "There is no room."     
        return f"there is {len(self.soldier)} soldier in room"
    
class Home_mili:
    def __init__(self):
        self.rooms:list[Room]=[Room() for _ in range(10)]


drop_a = Home_mili()
drop_b = Home_mili()
class Base:
    drop = [drop_a, drop_b]











soldiers_sorti=[]
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
    result.sort(key = lambda x: int(x['מרחק מהבסיס']))

    for i in result:
        i['מספר אישי'] = Soldier(i['מספר אישי'], i['שם פרטי'], i['שם משפחה'], i['מין'], i['עיר מגורים'], i['מרחק מהבסיס'], )
        soldiers_sorti.append(i['מספר אישי'])
    result = soldiers_sorti.copy()
    for i in Base.drop:
        for j in i.rooms:
            while not j.is_full:
                j.add_mens(soldiers_sorti.pop())

    return {"Soldiers who were deployed":len(result) - len(soldiers_sorti), "Soldiers on the waiting list": len(soldiers_sorti)}, result







