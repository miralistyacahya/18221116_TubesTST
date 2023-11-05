from pydantic import BaseModel
from typing import Optional

class Cake(BaseModel):
    cake_id: Optional[int] = None
    cake_name: str
    template_img: Optional[str]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "cake_id": 1,
                "cake_name": "Red Velvet Sponge Cake",
                "template_img": "b5b7620a880375e1.jpg"
            }
        }