from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ingresos(BaseModel):
    id: Optional[int] = Field(default=None, title="Id of the ingreso")
    date: Optional[str] = Field(None, title="Date of the ingreso")
    description: Optional[str] = Field(None, title="Description of the ingreso")
    value: Optional[float] = Field(None, title="Value of the ingreso")
    category: Optional[str] = Field(None, title="Category of the ingreso")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "date": "2025-04-04",
                "description": "Example description",
                "value": 5000,
                "category": "Example category"
            }
        }
