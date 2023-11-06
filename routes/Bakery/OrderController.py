from fastapi import APIRouter, HTTPException, status, File, UploadFile, Request
from models.OrderModel import Order
from typing import List
from db import cursor, conn
import uuid
import shutil
# from imghdr import what
# from pydrive2.auth import GoogleAuth
# from pydrive2.drive import GoogleDrive
# from PIL import Image


orderRouter = APIRouter(
    tags=["Order"]
)

order = {}

@orderRouter.get("/order")
async def getAllOrder():
    # cursor = conn.cursor()
    query = "SELECT * FROM orders;"
    cursor.execute(query)
    order_records = cursor.fetchall()
    # cursor.close()

    # kalo error gaada data
    if not order_records:
        raise HTTPException(status_code=404, detail="Orders not found")

    # list Customer
    # orders = [Order(
    #     order_id=order[0],
    #     customer_id=order[1],
    #     cake_id=order[2],
    #     order_date=order[3].isoformat(),
    #     pickup_date=order[4].isoformat(),
    #     order_status=order[5],
    #     addr=order[6],
    #     cake_img=order[7],
    #     created_at=order[8].isoformat(),
    #     updated_at=order[9].isoformat()
    # ) for order in order_records]

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
    
    # order = Order(
    #     order_id=order_records[0],
    #     customer_id=order_records[1],
    #     cake_id=order_records[2],
    #     order_date=order_records[3].isoformat(),
    #     pickup_date=order_records[4].isoformat(),
    #     order_status=order_records[5],
    #     addr=order_records[6],
    #     cake_img=order_records[7],
    #     created_at=order_records[8].isoformat(),
    #     updated_at=order_records[9].isoformat()
    # )

    return {
        "success": True,
        "message": "success",
        "code": 200,
        "response": order_records
    }



@orderRouter.post("/order")
async def createOrder(customer_id: int, cake_id: int, order_date: str, pickup_date: str, order_status: str, addr: str):
    try:

        # cursor = conn.cursor()
        query = "INSERT INTO orders (customer_id, cake_id, order_date, pickup_date, order_status, addr) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (customer_id, cake_id, order_date, pickup_date, order_status, addr))
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





@orderRouter.put("/order/{order_id}/image")
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

        # UPLOAD_DIR = os.getenv("UPLOAD_DIR")
        # img_link = f"{UPLOAD_DIR}{file.filename}"
        # try:
        #     contents = await file.read()
        #     with open(img_link, "wb+") as f:
        #         f.write(contents)
            
            
        # except Exception:
        #     return{"message: Error uploading"}
        # finally:
        #     file.file.close()
            
                # shutil.copyfileobj(cake_img.file, buffer)
                # print(cake_img.file.read)
        # if url is None:
        #     # img_link = None
        #     raise HTTPException(status_code=400, detail="Cake image tidak berhasil disimpan")
        
        # cursor = conn.cursor()
        query = "UPDATE orders set cake_img = %s WHERE order_id = %s"
        cursor.execute(query, (file.filename, order_id))
        conn.commit()
        # cursor.close()

        return {
            "success": True,
            "message": f"Design kue berhasil ditambahkan pada {file.filename}",
            "code": 200
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Terjadi kesalahan: {str(e)}")


@orderRouter.delete("/order/{order_id}")
async def deleteOrder(order_id: int):
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