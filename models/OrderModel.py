from pydantic import BaseModel
from typing import Optional
from models.CustomerModel import Customer
from models.CakeModel import Cake

class Order(BaseModel):
    order_id: Optional[int] = None
    customer_id: int #id customer dari kelas Customer
    cake_id: int
    order_date: str
    pickup_date: str
    order_status: str
    addr: Optional[str]
    cake_img: Optional[str]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "customer_id": 1,
                "cake_id": 1,
                "order_date": "2023-03-12",
                "pickup_date":"2023-03-21",
                "order_status": "Delivery",
                "addr":"Jl. Dago Asri III No. 21",
                "cake_img":"0f4b49b8d1863d55.jpg"
            }
        }
