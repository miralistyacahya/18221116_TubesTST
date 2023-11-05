from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    customer_id: Optional[int] = None
    customer_name: str
    phone: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": 1,
                "customer_name": "pipo",
                "phone": "0812345667"
            }
        }

