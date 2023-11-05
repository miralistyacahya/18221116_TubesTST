from fastapi import APIRouter, HTTPException, status
from models.CakeModel import Cake
from typing import List
from db import conn

cakeRouter = APIRouter(
    tags=["Cake"]
)

cake = {}


@cakeRouter.get("/cake")
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

    return {
        "success": True,
        "message": "success",
        "code": 200,
        "response": cakes
    }

@cakeRouter.get("/cake/{cake_id}")
async def getCake(cake_id: int):
    cursor = conn.cursor()
    query = "SELECT cake_id, cake_name, template_img, created_at, updated_at FROM cakes WHERE cake_id=%s;"
    cursor.execute(query, (cake_id,))
    cake_records = cursor.fetchone()
    cursor.close() 

    if not cake_records:
        raise HTTPException(status_code=404, detail="Cake not found")
    
    cake = Cake(
    cake_id=cake_records[0],
    cake_name=cake_records[1],
    template_img=cake_records[2],
    created_at=cake_records[3].isoformat(),
    updated_at=cake_records[4].isoformat()
    )

    return {
        "success": True,
        "message": "success",
        "code": 200,
        "response": cake
    } 

@cakeRouter.get("/cake/template/{cake_id}")
async def getCakeTemplate(cake_id: int):
    cursor = conn.cursor()
    query = "SELECT template_img FROM cakes WHERE cake_id=%s;"
    cursor.execute(query, (cake_id,))
    cake_template = cursor.fetchone()
    cursor.close() 

    if cake_template:
        return cake_template[0]
    else:
        raise HTTPException(status_code=404, detail="Cake not found") 

@cakeRouter.get("/cake/{cake_name}")
async def getCakeIdByName(cake_name: str):
    cursor = conn.cursor()
    query = "SELECT cake_id FROM cakes WHERE cake_name=%s;"
    cursor.execute(query, (cake_name,))
    cake_id = cursor.fetchone()
    cursor.close() 

    if cake_id:
        return cake_id[0]
    else:
        return None



@cakeRouter.post("/cake")
async def createNewCake(cake : Cake):

    # existing_cake = getCakeIdByName(cake.cake_name)

    # if existing_cake:
    #     raise HTTPException(status_code=400, detail=f"Cake {cake.cake_name} sudah tersedia")

    cursor = conn.cursor()
    query = "INSERT INTO cakes (cake_name) VALUES (%s)"
    cursor.execute(query, (cake.cake_name,))
    conn.commit()
    cursor.close()

    return {
        "success": True,
        "message": f"cake {cake.cake_name} berhasil dibuat",
        "code": 200
    }



@cakeRouter.put("/cake/{cake_id}")
async def editCake(cake_id: int, cake: Cake):
    cursor = conn.cursor()
    query = "SELECT cake_id FROM cakes WHERE cake_id=%s"
    cursor.execute(query, (cake_id,))
    existing_cake = cursor.fetchone()
    
    if not existing_cake:
        cursor.close()
        raise HTTPException(status_code=404, detail=f"Cake dengan ID {cake_id} tidak ditemukan")
    
    if cake.cake_name and cake.template_img:
        query = "UPDATE cakes SET cake_name=%s, template_img=%s WHERE cake_id=%s"
        cursor.execute(query, (cake.cake_name, cake.template_img, cake_id))
    elif cake.cake_name: # hanya mengubah nama
        query = "UPDATE cakes SET cake_name=%s WHERE cake_id=%s"
        cursor.execute(query, (cake.cake_name, cake_id))
    elif cake.template_img: # hanya mengubah template
        query = "UPDATE cakes SET template_img=%s WHERE cake_id=%s"
        cursor.execute(query, (cake.template_img, cake_id))

    conn.commit()
    cursor.close()

    return {
        "success": True,
        "message": f"cake dengan id {cake_id} berhasil diubah",
        "code": 200
    }
    


@cakeRouter.delete("/cake/{cake_id}")
async def deleteCake(cake_id: int):
    cursor = conn.cursor()
    query = "SELECT cake_id FROM cakes WHERE cake_id=%s"
    cursor.execute(query, (cake_id,))
    existing_cake = cursor.fetchone()
    
    if not existing_cake:
        cursor.close()
        raise HTTPException(status_code=404, detail=f"Cake dengan ID {cake_id} tidak ditemukan")

    query = "DELETE FROM cakes WHERE cake_id=%s"
    cursor.execute(query, (cake_id,))
    conn.commit()
    cursor.close()

    return {
        "success": True,
        "message": f"cake dengan id {cake_id} berhasil dihapus",
        "code": 200
    }