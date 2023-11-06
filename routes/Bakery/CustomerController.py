from fastapi import APIRouter, HTTPException, status, Request
from models.CustomerModel import Customer
from typing import List
from db import conn

customerRouter = APIRouter(
    tags=["Customer"]
)

customer = {}


@customerRouter.get("/customer")
async def getAllCustomer() -> List[Customer]:
    cursor = conn.cursor()
    query = "SELECT * FROM customers;"
    cursor.execute(query)
    customer_records = cursor.fetchall()
    cursor.close()

    # kalo error gaada data
    if not customer_records:
        raise HTTPException(status_code=404, detail="Customers not found")

    # list Customer
    customers = [Customer(
        customer_id=customer[0],
        customer_name=customer[1],
        phone=customer[2],
        created_at=customer[3].isoformat(),
        updated_at=customer[4].isoformat()
    ) for customer in customer_records]

    return {
        "success": True,
        "message": "success",
        "code": 200,
        "response": customers
    }
        
@customerRouter.get("/customer/{customer_id}")
async def getCustomer(customer_id: int):
    cursor = conn.cursor()
    query = "SELECT customer_id, customer_name, phone, created_at, updated_at FROM customers WHERE customer_id=%s;"
    cursor.execute(query, (customer_id,))
    customer_records = cursor.fetchone()
    cursor.close() 

    if not customer_records:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer = Customer(
    customer_id=customer_records[0],
    customer_name=customer_records[1],
    phone=customer_records[2],
    created_at=customer_records[3].isoformat(),
    updated_at=customer_records[4].isoformat()
    )

    return {
        "success": True,
        "message": "success",
        "code": 200,
        "response": customer
    }

@customerRouter.get("/customer/phone/{phone}")
async def getCustomerIdByPhone(phone: str):
    cursor = conn.cursor()
    query = "SELECT customer_id FROM customers WHERE phone=%s;"
    cursor.execute(query, (phone,))
    customer_id = cursor.fetchone()
    cursor.close() 
    if customer_id:
        return (customer_id[0])
    else:
        return None



@customerRouter.post("/customer")
async def createNewCustomer(customer : Customer):
    
    # existing_customer = getCustomerIdByPhone(customer.phone)

    # if existing_customer is not None:
    #     raise HTTPException(status_code=400, detail=f"Customer dengan no. telpon {customer.phone} sudah tersedia")
    
    cursor = conn.cursor()
    query = "INSERT INTO customers (customer_name, phone) VALUES (%s, %s)"
    cursor.execute(query, (customer.customer_name, customer.phone))
    conn.commit()
    customer_id = cursor.lastrowid
    cursor.close()

    return {
        "success": True,
        "message": f"customer dengan nama {customer.customer_name} berhasil dibuat",
        "code": 200,
        "customer_id": customer_id
    }



@customerRouter.put("/customer/{customer_id}")
async def editCustomer(customer_id: int, request: Request):
    data = await request.json()
    phone = data.get("phone")
    customer_name = data.get("customer_name")

    cursor = conn.cursor()
    query = "SELECT customer_id FROM customers WHERE customer_id=%s"
    cursor.execute(query, (customer_id,))
    existing_customer = cursor.fetchone()
    
    if not existing_customer:
        cursor.close()
        raise HTTPException(status_code=404, detail=f"Customer dengan ID {customer_id} tidak ditemukan")
    
    if customer_name and phone:
        query = "UPDATE customers SET customer_name=%s, phone=%s WHERE customer_id=%s"
        cursor.execute(query, (customer_name, phone, customer_id))
    elif customer_name: # Mengubah hanya customer_name
        query = "UPDATE customers SET customer_name=%s WHERE customer_id=%s"
        cursor.execute(query, (customer_name, customer_id))
    elif phone:  # Mengubah hanya phone
        query = "UPDATE customers SET phone=%s WHERE customer_id=%s"
        cursor.execute(query, (phone, customer_id))

    conn.commit()
    cursor.close()

    return {
        "success": True,
        "message": f"Customer dengan ID {customer_id} berhasil diubah",
        "code": 200
    }



@customerRouter.delete("/customer/{customer_id}")
async def deleteCustomer(customer_id: int):
    cursor = conn.cursor()
    query = "SELECT customer_id FROM customers WHERE customer_id=%s"
    cursor.execute(query, (customer_id,))
    existing_customer = cursor.fetchone()
    
    if not existing_customer:
        cursor.close()
        raise HTTPException(status_code=404, detail=f"Customer dengan ID {customer_id} tidak ditemukan")

    query = "DELETE FROM customers WHERE customer_id=%s"
    cursor.execute(query, (customer_id,))
    conn.commit()
    cursor.close()

    return {
        "success": True,
        "message": f"customer dengan id {customer_id} berhasil dihapus",
        "code": 200
    }