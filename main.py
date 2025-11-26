from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Centralized prices
PARTS_DB = {
    "ex2": 520,
    "in2": 310,
    "rm2": 780,
    "tu2": 1120
}

class Part(BaseModel):
    id: str
    type: str
    name: str

class BuildRequest(BaseModel):
    parts: List[Part]

# 1. Return all part prices
@app.get("/parts")
def get_parts():
    return {
        "parts": [
            {"id": pid, "price": price}
            for pid, price in PARTS_DB.items()
        ]
    }

# 2. Price of single part
@app.get("/price/{part_id}")
def get_price(part_id: str):
    return {"price": PARTS_DB.get(part_id, 0)}

# 3. Calculate total + provide individual prices
@app.post("/calculate")
def calculate_price(data: BuildRequest):
    total = 0
    items = []

    for part in data.parts:
        price = PARTS_DB.get(part.id, 0)
        total += price

        items.append({
            "id": part.id,
            "name": part.name,
            "type": part.type,
            "price": price
        })

    return {
        "total_price": total,
        "items": items
    }