from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    customer_id: int
    name: str
    phone: str
    created_at: str
    updated_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": 1,
                "name": "pipo",
                "phone": "0812345667"
            }
        }

