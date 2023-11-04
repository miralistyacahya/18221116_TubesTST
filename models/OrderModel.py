from pydantic import BaseModel
from typing import Optional
from models.CustomerModel import Customer
from models.CakeModel import Cake

class Order(BaseModel):
    order_id: int
    customer_id: int #id customer dari kelas Customer
    cake_id: int
    order_date: str
    pickup_date: str
    status: str
    address: Optional[str]
    cake_img: str
    created_at: str
    updated_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": 1,
                "xake_id": 1,
                "order_date": "2023-03-12",
                "pickup_date":"2023-03-21",
                "status": "Delivery",
                "address":"Jl. Dago Asri III No. 21",
                "cake_img":"0f4b49b8d1863d55.jpg"
            }
        }
