from fastapi import APIRouter, HTTPException, status
from models.CakeModel import Cake
from typing import List
from database.db import conn

cakeRouter = APIRouter(
    tags=["Cake"]
)

cake = {}

@cakeRouter.get("/cake", response_model=List[Cake])
async def getAllCake() -> List[Cake]:
    cursor = conn.cursor()
    query = "SELECT * FROM cakes;"
    cursor.execute(query)
    cake_records = cursor.fetchall()
    cursor.close()

    # kalo error gaada data
    if not cake_records:
        raise HTTPException(status_code=404, detail="Cakes not found")

    # list Cake
    cakes = [Cake(
        cake_id=cake[0],
        cake_name=cake[1],
        template_img=cake[2],
        created_at=cake[3].isoformat(),
        updated_at=cake[4].isoformat()
    ) for cake in cake_records]

    return cakes