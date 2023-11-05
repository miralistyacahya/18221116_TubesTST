from fastapi import APIRouter, HTTPException, status
from models.OrderModel import Order
from typing import List
from db import conn

orderRouter = APIRouter(
    tags=["Order"]
)

order = {}

@orderRouter.get("/order")
async def getAllOrder() -> List[Order]:
    cursor = conn.cursor()
    query = "SELECT * FROM orders;"
    cursor.execute(query)
    order_records = cursor.fetchall()
    cursor.close()

    # kalo error gaada data
    if not order_records:
        raise HTTPException(status_code=404, detail="Orders not found")

    # list Customer
    orders = [Order(
        order_id=order[0],
        customer_id=order[1],
        cake_id=order[2],
        order_date=order[3].isoformat(),
        pickup_date=order[4].isoformat(),
        order_status=order[5],
        addr=order[6],
        cake_img=order[7],
        created_at=order[8].isoformat(),
        updated_at=order[9].isoformat()
    ) for order in order_records]

    return {
        "success": True,
        "message": "success",
        "code": 200,
        "response": orders
    }   
    

@orderRouter.get("/order/{order_id}")
async def getOrder(order_id: int):
    cursor = conn.cursor()
    query = "SELECT order_id, customer_id, cake_id, order_date, pickup_date, order_status, addr, cake_img, created_at, updated_at FROM orders WHERE order_id=%s;"
    cursor.execute(query, (order_id,))
    order_records = cursor.fetchone()
    cursor.close() 

    if not order_records:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = Order(
        order_id=order_records[0],
        customer_id=order_records[1],
        cake_id=order_records[2],
        order_date=order_records[3].isoformat(),
        pickup_date=order_records[4].isoformat(),
        order_status=order_records[5],
        addr=order_records[6],
        cake_img=order_records[7],
        created_at=order_records[8].isoformat(),
        updated_at=order_records[9].isoformat()
    )

    return {
        "success": True,
        "message": "success",
        "code": 200,
        "response": order
    }


@orderRouter.delete("/order/{order_id}")
async def deleteOrder(order_id: int):
    cursor = conn.cursor()
    query = "SELECT order_id FROM orders WHERE order_id=%s"
    cursor.execute(query, (order_id,))
    existing_order = cursor.fetchone()
    
    if not existing_order:
        cursor.close()
        raise HTTPException(status_code=404, detail=f"Order dengan ID {order_id} tidak ditemukan")

    query = "DELETE FROM orders WHERE order_id=%s"
    cursor.execute(query, (order_id,))
    conn.commit()
    cursor.close()

    return {
        "success": True,
        "message": f"order dengan id {order_id} berhasil dihapus",
        "code": 200
    }