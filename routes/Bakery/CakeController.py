from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.responses import FileResponse, StreamingResponse
from models.CakeModel import Cake
from models.userModel import User
from routes.auth.auth import get_current_user
from typing import List
from db import cursor, conn
from google.cloud import storage
import os
import json
import io
from PIL import Image
from io import BytesIO

cakeRouter = APIRouter(
    tags=["Cake"]
)

cake = {}


@cakeRouter.get("/cake")
async def getAllCake():
    # cursor = conn.cursor()
    query = "SELECT * FROM cakes;"
    cursor.execute(query)
    cake_records = cursor.fetchall()
    # cursor.close()

    # kalo error gaada data
    if not cake_records:
        raise HTTPException(status_code=404, detail="Cakes not found")

    return {
        "success": True,
        "message": "success",
        "code": 200,
        "response": cake_records
    }

@cakeRouter.get("/cake/{cake_id}")
async def getCake(cake_id: int):
    # cursor = conn.cursor()
    query = "SELECT cake_id, cake_name, template_img, created_at, updated_at FROM cakes WHERE cake_id=%s;"
    cursor.execute(query, (cake_id,))
    cake_records = cursor.fetchone()
    # cursor.close() 

    if not cake_records:
        raise HTTPException(status_code=404, detail="Cake not found")

    return {
        "success": True,
        "message": "success",
        "code": 200,
        "response": cake_records
    } 

@cakeRouter.get("/cake/{cake_id}/template", response_class=FileResponse)
async def chooseCake(cake_id: int):
    # cursor = conn.cursor()
    query = "SELECT template_img FROM cakes WHERE cake_id=%s;"
    cursor.execute(query, (cake_id,))
    cake_template = cursor.fetchone()
    # cursor.close() 

    if cake_template:
       
        try:
            # GCS environment yang di set di env
            credentials_json = os.getenv("GCS_CREDENTIALS")
            # diubah (decode) menjadi JSON lagi
            decoded_json = json.loads(credentials_json)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading GCS credentials: {str(e)}")
        
        # connect dengan bucket di GSC bismillah ga error
        client = storage.Client.from_service_account_info(decoded_json)
        GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
        bucket = client.get_bucket(GCS_BUCKET_NAME)

        # mengambil link image dari database, hanya butuh nama file aja
        path = os.path.basename(cake_template[0])
        blob = bucket.blob(path)

        # Cek blob
        if not blob.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        try:
            # open image dari bucker
            img_bytes = blob.download_as_bytes()
            img = Image.open(BytesIO(img_bytes))
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format="JPEG")
            im = img_byte_arr.getvalue()
            # menampilkan image bisa plis T T
            return StreamingResponse(io.BytesIO(im), media_type="image/jpeg", headers={"Content-Disposition": "inline; filename=cake_image.jpeg"})
        
        except (IOError, Image.UnidentifiedImageError) as e:
            print(f"Error opening image: {e}")

@cakeRouter.get("/cake/id/{cake_name}")
async def getCakeIdByName(cake_name: str):
    # cursor = conn.cursor()
    query = "SELECT cake_id FROM cakes WHERE cake_name=%s;"
    cursor.execute(query, (cake_name,))
    cake_id = cursor.fetchone()
    # cursor.close() 

    if cake_id:
        return cake_id #int(cake_id[0])
    else:
        return None



@cakeRouter.post("/cake")
async def createNewCake(cake : Cake, user : User = Depends(get_current_user)):

    # cursor = conn.cursor()
    query = "INSERT INTO cakes (cake_name) VALUES (%s)"
    cursor.execute(query, (cake.cake_name,))
    conn.commit()
    cake_id = cursor.lastrowid
    # cursor.close()

    return {
        "success": True,
        "message": f"cake {cake.cake_name} berhasil dibuat",
        "code": 200,
        "cake_id": cake_id
    }



@cakeRouter.patch("/cake/{cake_id}")
async def editCake(cake_id: int, cake_name: str, user : User = Depends(get_current_user)):

    # cursor = conn.cursor()
    query = "SELECT cake_id FROM cakes WHERE cake_id=%s"
    cursor.execute(query, (cake_id,))
    existing_cake = cursor.fetchone()
    
    if not existing_cake:
        # cursor.close()
        raise HTTPException(status_code=404, detail=f"Cake dengan ID {cake_id} tidak ditemukan")
    
    if cake_name: # hanya mengubah nama
        query = "UPDATE cakes SET cake_name=%s WHERE cake_id=%s"
        cursor.execute(query, (cake_name, cake_id))


    conn.commit()
    # cursor.close()

    return {
        "success": True,
        "message": f"cake dengan id {cake_id} berhasil diubah",
        "code": 200
    }
    


@cakeRouter.delete("/cake/{cake_id}")
async def deleteCake(cake_id: int, user : User = Depends(get_current_user)):
    # cursor = conn.cursor()
    query = "SELECT cake_id FROM cakes WHERE cake_id=%s"
    cursor.execute(query, (cake_id,))
    existing_cake = cursor.fetchone()
    
    if not existing_cake:
        # cursor.close()
        raise HTTPException(status_code=404, detail=f"Cake dengan ID {cake_id} tidak ditemukan")

    query = "DELETE FROM cakes WHERE cake_id=%s"
    cursor.execute(query, (cake_id,))
    conn.commit()
    # cursor.close()

    return {
        "success": True,
        "message": f"cake dengan id {cake_id} berhasil dihapus",
        "code": 200
    }