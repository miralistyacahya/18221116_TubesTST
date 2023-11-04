from fastapi import APIRouter, HTTPException, status
from models.CustomerModel import Customer
from typing import List

customerRouter = APIRouter(
    tags=["Customer"]
)

customers = {}

@customerRouter.get("/customer", response_model=List[Customer])
async def getAllCustomer() -> List[Customer]:
    return customers

# @customerRouter.get("/customer/{id}", response_model=Customer)
# async def getCustomer(customer_id: int) -> Customer:

