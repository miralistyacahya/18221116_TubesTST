from pydantic import BaseModel
from typing import Optional

class Cake(BaseModel):
    cake_id: int
    cake_name: str
    template_img: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "cake_id": 1,
                "cake_name": "Red Velvet Sponge Cake",
                "template_img": "b5b7620a880375e1.jpg"
            }
        }