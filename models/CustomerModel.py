from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    customer_id: int
    customer_name: str
    phone: str
    created_at: str
    updated_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": 1,
                "customer_name": "pipo",
                "phone": "0812345667"
            }
        }

