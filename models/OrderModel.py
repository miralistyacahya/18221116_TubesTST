from pydantic import BaseModel
from typing import Optional
from models.CustomerModel import Customer
from models.KueModel import Kue

class Order(BaseModel):
    order_id: int
    customer_id: int #id customer dari kelas Customer
    katalog_id: int
    tanggal_order: str
    tanggal_pengambilan: str
    status: str
    alamat: Optional[str]
    design_kue: str

    class Config:
        schema_extra = {
            "example": {
                "customer_id": 1,
                "katalog_id": 1,
                "tanggal_order": "2023-03-12",
                "tanggal_pengambilan":"2023-03-21",
                "status": "Delivery",
                "alamat":"Jl. Dago Asri III No. 21",
                "design_kue":"0f4b49b8d1863d55.jpg",
            }
        }
