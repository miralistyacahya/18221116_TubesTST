from fastapi import APIRouter, HTTPException, status, File, UploadFile, Request, Depends
from fastapi.responses import FileResponse, StreamingResponse
from models.OrderModel import Order
from models.userModel import User
from routes.auth.auth import get_current_user
from typing import List
from db import cursor, conn
import uuid
import os
import json
from google.cloud import storage
import io
from PIL import Image
from io import BytesIO

orderRouter = APIRouter(
    tags=["Order"]
)

order = {}

@orderRouter.get("/order")
async def getAllOrder(user : User = Depends(get_current_user)):
    # cursor = conn.cursor()
    query = "SELECT * FROM orders;"
    cursor.execute(query)
    order_records = cursor.fetchall()
    # cursor.close()

    # kalo error gaada data
    if not order_records:
        raise HTTPException(status_code=404, detail="Orders not found")

    return {
        "success": True,
        "message": "success",
        "code": 200,
        "response": order_records
    }   
    
@orderRouter.get("/order/{order_id}")
async def getOrder(order_id: int):
    # cursor = conn.cursor()
    query = "SELECT order_id, customer_id, cake_id, order_date, pickup_date, order_status, addr, cake_img, created_at, updated_at FROM orders WHERE order_id=%s;"
    cursor.execute(query, (order_id,))
    order_records = cursor.fetchone()
    # cursor.close() 

    if not order_records:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "success": True,
        "message": "success",
        "code": 200,
        "response": order_records
    }

@orderRouter.get("/order/{order_id}/design", response_class=FileResponse)
async def getDesign(order_id: int):
    # cursor = conn.cursor()
    query = "SELECT cake_img FROM orders WHERE order_id=%s;"
    cursor.execute(query, (order_id,))
    cake_design = cursor.fetchone()
    # cursor.close() 

    if cake_design:
       
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
        path = os.path.basename(cake_design[0])
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
            return StreamingResponse(io.BytesIO(im), media_type="image/jpeg", 
                                     headers={"Content-Disposition": "inline; filename=cake_design.jpeg"})
        
        except (IOError, Image.UnidentifiedImageError) as e:
            print(f"Error opening image: {e}")

@orderRouter.get("/order/recommendation")
async def getRecommendation():
    query = "With getMost as (SELECT cake_id, COUNT(*) as order_count FROM orders GROUP BY cake_id ORDER BY order_count desc LIMIT 1) select cake_id from getMost;"
    cursor.execute(query)
    order_counts = cursor.fetchone()

    if not order_counts:
        raise HTTPException(status_code=400, detail="Belum ada rekomendasi yang dapat diberikan")
    
    mostOrderedId = order_counts[0]

    query = "SELECT cake_name, cake_img FROM cakes join orders ON cakes.cake_id = orders.cake_id WHERE cakes.cake_id = %s ORDER BY order_date DESC LIMIT 1;"
    cursor.execute(query, (mostOrderedId,))
    mostOrderedInfo = cursor.fetchone()

    if not mostOrderedInfo:
        raise HTTPException(status_code=400, detail="Belum ada rekomendasi yang dapat diberikan")
    
    return {
        "cake_name": mostOrderedInfo[0],
        "cake_img": mostOrderedInfo[1]
    }
    
    # try:
    #     # GCS environment yang di set di env
    #     credentials_json = os.getenv("GCS_CREDENTIALS")
    #     # diubah (decode) menjadi JSON lagi
    #     decoded_json = json.loads(credentials_json)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error loading GCS credentials: {str(e)}")
        
    # # connect dengan bucket di GSC bismillah ga error
    # client = storage.Client.from_service_account_info(decoded_json)
    # GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
    # bucket = client.get_bucket(GCS_BUCKET_NAME)

    # # mengambil link image dari database, hanya butuh nama file aja
    # path = os.path.basename(mostOrderedInfo[1])
    # blob = bucket.blob(path)

    # # Cek blob
    # if not blob.exists():
    #     raise HTTPException(status_code=404, detail="Image not found")
    # try:
    #     # open image dari bucker
    #     img_bytes = blob.download_as_bytes()
    #     img = Image.open(BytesIO(img_bytes))
    #     img_byte_arr = BytesIO()
    #     img.save(img_byte_arr, format="JPEG")
    #     im = img_byte_arr.getvalue()
    #     # menampilkan image bisa plis T T
    #     return {
    #         "cake_name": mostOrderedInfo[0],
    #         "design reference": StreamingResponse(io.BytesIO(im), media_type="image/jpeg", headers={"Content-Disposition": "inline; filename=cake_design.jpeg"})
    #     }
        
    # except (IOError, Image.UnidentifiedImageError) as e:
    #     print(f"Error opening image: {e}")        



@orderRouter.post("/order")
async def createOrder(order: Order): 
    try:

        # cursor = conn.cursor()
        query = "INSERT INTO orders (customer_id, cake_id, order_date, pickup_date, order_status, addr) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (order.customer_id, order.cake_id, order.order_date, order.pickup_date, order.order_status, order.addr))
        conn.commit()
        order_id = cursor.lastrowid
        # cursor.close()

        return {
            "success": True,
            "message": "Order berhasil dibuat",
            "code": 200,
            "order_id": order_id
        }  
    except Exception as e:
        if "cake_id" in str(e):
            raise HTTPException(status_code=400, detail="Cake tidak tersedia pada bakery")
        if "customer_id" in str(e):
            raise HTTPException(status_code=400, detail="Customer tidak ditemukan")
        else:
            raise HTTPException(status_code=404, detail=f"Terjadi kesalahan: {str(e)}")



@orderRouter.patch("/order/{order_id}/image")
async def addImage(order_id: int, file: UploadFile = File(...)):
    try:
        # cursor = conn.cursor()
        query = "SELECT order_id FROM orders WHERE order_id=%s"
        cursor.execute(query, (order_id,))
        existing_order = cursor.fetchone()
    
        if not existing_order:
            # cursor.close()
            raise HTTPException(status_code=404, detail=f"Order dengan ID {order_id} tidak ditemukan")
        
        allowed_image_types = ["jpeg", "jpg", "png"]
        
        file_type = (file.filename.split("."))[1]

        if file_type not in allowed_image_types:
            raise HTTPException(status_code=400, detail="Format file tidak sesuai")
        
        file.filename = f"{uuid.uuid4()}.{file_type}"

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

        # set file path dan upload yuk bisa yuk
        file_path = file.filename
        blob = bucket.blob(file_path)
        blob.upload_from_file(file.file, content_type='image/jpeg')
        img_url = f'https://storage.googleapis.com/{GCS_BUCKET_NAME}/{file_path}'
        
        # cursor = conn.cursor()
        query = "UPDATE orders set cake_img = %s WHERE order_id = %s"
        cursor.execute(query, (img_url, order_id))
        conn.commit()
        # cursor.close()

        return {
            "success": True,
            "message": f"Design kue berhasil ditambahkan pada {img_url}",
            "code": 200
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Terjadi kesalahan: {str(e)}")



@orderRouter.delete("/order/{order_id}")
async def deleteOrder(order_id: int, user : User = Depends(get_current_user)):
    # cursor = conn.cursor()
    query = "SELECT order_id FROM orders WHERE order_id=%s"
    cursor.execute(query, (order_id,))
    existing_order = cursor.fetchone()
    
    if not existing_order:
        cursor.close()
        raise HTTPException(status_code=404, detail=f"Order dengan ID {order_id} tidak ditemukan")

    query = "DELETE FROM orders WHERE order_id=%s"
    cursor.execute(query, (order_id,))
    conn.commit()
    # cursor.close()

    return {
        "success": True,
        "message": f"order dengan id {order_id} berhasil dihapus",
        "code": 200
    }