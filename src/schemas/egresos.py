from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Egresos(BaseModel):
    id: Optional[int] = Field(default=None, title="Id of the egreso")
    date: Optional[str] = Field(None, title="Date of the egreso")
    description: Optional[str] = Field(None, title="Description of the egreso")
    value: Optional[float] = Field(None, title="Value of the egreso")
    category: Optional[str] = Field(None, title="Category of the egreso")

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