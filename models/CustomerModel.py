from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    customer_id: int
    name: str
    phone: str

    class Config:
        schema_extra = {
            "example": {
                "customer_id": 1,
                "name": "pipo",
                "phone": "0812345667"
            }
        }

