from pydantic import BaseModel
from typing import Optional

class Kue(BaseModel):
    katalog_id: int
    nama_jenis: str
    template_kue: str

    class Config:
        schema_extra = {
            "example": {
                "katalog_id": 1,
                "nama_jenis": "Red Velvet Sponge Cake",
                "template_kue": "b5b7620a880375e1.jpg"
            }
        }